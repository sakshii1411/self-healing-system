import time
import random
import logging
import json
import os
import asyncio
import httpx

from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from .metrics import (
    REQUEST_COUNT, REQUEST_LATENCY, ERROR_COUNT,
    DOWNSTREAM_CALLS, DOWNSTREAM_LATENCY,
    CPU_USAGE, MEMORY_USAGE
)

# Ensure logs directory exists
os.makedirs('/app/logs', exist_ok=True)

# JSON Logger
class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "service": "order-service",
            "message": record.getMessage(),
        })

logger = logging.getLogger("order-service")
logger.setLevel(logging.INFO)

if not logger.handlers:
    console = logging.StreamHandler()
    console.setFormatter(JsonFormatter(datefmt='%Y-%m-%d %H:%M:%S'))

    file_h = logging.FileHandler('/app/logs/order-service.log')
    file_h.setFormatter(JsonFormatter(datefmt='%Y-%m-%d %H:%M:%S'))

    logger.addHandler(console)
    logger.addHandler(file_h)

app = FastAPI(title="Order Service")

USER_SERVICE_URL = "http://user-service:8000"

# Middleware for metrics
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    try:
        response = await call_next(request)
        status = response.status_code if hasattr(response, 'status_code') else 200
    except Exception as e:
        status = 500
        ERROR_COUNT.labels(type=type(e).__name__).inc()
        logger.error(f"Request failed: {str(e)}")

        return JSONResponse(
            content={"detail": "Internal server error"},
            status_code=500
        )
    finally:
        duration = time.time() - start
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=status
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)

        # Dummy system metrics (for demo)
        CPU_USAGE.set(random.uniform(20, 85))
        MEMORY_USAGE.set(random.uniform(200_000_000, 900_000_000))

    return response


@app.get("/")
async def root():
    logger.info("Root endpoint called")
    return {"status": "healthy", "service": "order-service"}


@app.get("/orders")
async def get_orders():
    logger.info("Fetching orders - calling user-service")

    # Non-blocking sleep
    await asyncio.sleep(random.uniform(0.05, 0.6))

    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            start_ds = time.time()
            resp = await client.get(f"{USER_SERVICE_URL}/users")
            DOWNSTREAM_LATENCY.labels(
                target_service="user-service"
            ).observe(time.time() - start_ds)

        if resp.status_code == 200:
            DOWNSTREAM_CALLS.labels(
                target_service="user-service",
                status="success"
            ).inc()

            logger.info("Successfully called user-service")

            return {
                "orders": ["order1", "order2"],
                "users": resp.json().get("users", [])
            }
        else:
            DOWNSTREAM_CALLS.labels(
                target_service="user-service",
                status="error"
            ).inc()

            raise HTTPException(
                status_code=502,
                detail=f"Downstream status {resp.status_code}"
            )

    except Exception as e:
        DOWNSTREAM_CALLS.labels(
            target_service="user-service",
            status="error"
        ).inc()

        logger.error(f"Downstream call failed: {str(e)}")

        raise HTTPException(
            status_code=502,
            detail="User service unavailable"
        )


@app.get("/health")
async def health():
    logger.info("Health check")
    return {"status": "ok"}


@app.api_route("/metrics", methods=["GET", "HEAD"])
async def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    logger.info("🚀 Starting Order Service")
