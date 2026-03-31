import time
import random
import logging
import json
from fastapi import FastAPI, Request, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .metrics import (
    REQUEST_COUNT, REQUEST_LATENCY, ERROR_COUNT,
    CPU_USAGE, MEMORY_USAGE
)

# Structured JSON Logging with file output
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "service": "user-service",
            "message": record.getMessage(),
        }
        if hasattr(record, 'exc_info') and record.exc_info:
            log_record["exception"] = str(record.exc_info[1])
        return json.dumps(log_record)

logger = logging.getLogger("user-service")
logger.setLevel(logging.INFO)

# Remove default handlers
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(JsonFormatter(datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(console_handler)

# File handler (for centralized logging)
file_handler = logging.FileHandler('/app/logs/user-service.log')
file_handler.setFormatter(JsonFormatter(datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(file_handler)

logging.getLogger("uvicorn.error").setLevel(logging.CRITICAL)
logging.getLogger("uvicorn.access").setLevel(logging.INFO)

app = FastAPI(title="User Service - Data Generation Engine")

@app.middleware("http")
async def add_metrics_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        status = response.status_code if hasattr(response, "status_code") else 200
    except Exception as e:
        status = 500
        ERROR_COUNT.labels(type=type(e).__name__).inc()
        logger.error(f"Request failed: {str(e)}")
        return {"detail": "Internal server error"}, 500
    finally:
        duration = time.time() - start_time
        REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, status=status).inc()
        REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(duration)
        CPU_USAGE.set(random.uniform(12, 95))
        MEMORY_USAGE.set(random.uniform(120_000_000, 1_200_000_000))
    return response

@app.get("/")
async def root():
    logger.info("Root endpoint called - healthy request")
    if random.random() < 0.20:
        delay = random.uniform(0.7, 3.0)
        logger.warning(f"Simulated slow response: {delay:.2f}s delay")
        time.sleep(delay)
    return {"status": "healthy", "service": "user-service"}

@app.get("/users")
async def get_users():
    logger.info("Fetching users")
    if random.random() < 0.14:
        logger.error("Database connection failed - simulated outage")
        raise Exception("Simulated database connection error")
    if random.random() < 0.28:
        time.sleep(random.uniform(0.35, 1.5))
    else:
        time.sleep(random.uniform(0.05, 0.45))
    return {"users": ["alice", "bob", "charlie"], "count": 3}

@app.get("/health")
async def health_check():
    logger.info("Health check called")
    return {"status": "ok"}

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    logger.info("🚀 Starting User Service - Data Generation Engine")
