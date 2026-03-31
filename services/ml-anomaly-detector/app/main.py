import time
import logging
import requests
import pandas as pd
import numpy as np
from fastapi import FastAPI
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
from datetime import datetime
from pathlib import Path

app = FastAPI(title="ML Anomaly Detector")

PROMETHEUS_URL = "http://prometheus:9090/api/v1/query"

logging.basicConfig(level=logging.INFO, format='%(asctime)s | ML-Anomaly | %(message)s')
logger = logging.getLogger("ml-anomaly")

model = None
scaler = None
model_path = Path("/app/model.joblib")
scaler_path = Path("/app/scaler.joblib")


def safe_query(query: str, default=0.0):
    """Safely query Prometheus"""
    try:
        resp = requests.get(PROMETHEUS_URL, params={"query": query}, timeout=5)
        if resp.status_code != 200:
            return default
        data = resp.json()
        if data.get("status") == "success" and data["data"].get("result"):
            return float(data["data"]["result"][0]["value"][1])
        return default
    except Exception:
        return default


def fetch_metrics():
    return {
        "error_rate": safe_query('100 * (sum(rate(user_service_errors_total[5m])) or 0) / (sum(rate(user_service_requests_total[5m])) or 1)'),
        "avg_latency": safe_query('rate(user_service_request_latency_seconds_sum[5m]) / (rate(user_service_request_latency_seconds_count[5m]) or 1)'),
        "request_rate": safe_query('sum(rate(user_service_requests_total[5m]))'),
        "cpu_usage": safe_query('user_service_cpu_usage_percent')
    }


@app.get("/health")
async def health():
    return {"status": "ok", "service": "ml-anomaly-detector"}


@app.get("/train")
async def train_model():
    global model, scaler
    logger.info("Training Isolation Forest...")

    data_points = []
    for _ in range(80):
        data_points.append(list(fetch_metrics().values()))
        time.sleep(0.2)  # ✅ allow variation in metrics

    df = pd.DataFrame(
        data_points,
        columns=["error_rate", "avg_latency", "request_rate", "cpu_usage"]
    )

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df.fillna(0))

    model = IsolationForest(
        contamination=0.1,
        random_state=42,
        n_estimators=150
    )
    model.fit(X_scaled)

    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)

    logger.info(f"✅ Model trained on {len(df)} samples")
    return {"status": "trained", "samples_used": len(df)}


@app.get("/detect")
async def detect_anomaly():
    global model, scaler

    # Safe model loading
    if model is None or scaler is None:
        if model_path.exists() and scaler_path.exists():
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            logger.info("Loaded saved model")
        else:
            return {"status": "error", "message": "Model not trained. Call /train first"}

    metrics = fetch_metrics()
    features = np.array([list(metrics.values())])

    try:
        X_scaled = scaler.transform(features)
        prediction = model.predict(X_scaled)[0]
        score = model.decision_function(X_scaled)[0]

        is_anomaly = prediction == -1

        result = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "is_anomaly": bool(is_anomaly),
            "anomaly_score": round(float(score), 4),
            "metrics": metrics
        }

        if is_anomaly:
            logger.warning(f"🚨 ML ANOMALY DETECTED! Score: {score:.4f} | Metrics: {metrics}")
        else:
            logger.info(f"Normal behavior. Score: {score:.4f}")

        return result

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    logger.info("🚀 Starting ML Anomaly Detector")
