import logging
import requests
from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="Decision Engine")

ML_DETECTOR_URL = "http://ml-anomaly-detector:8000/detect"

logging.basicConfig(level=logging.INFO, format='%(asctime)s | Decision-Engine | %(message)s')
logger = logging.getLogger("decision-engine")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "decision-engine"}


@app.get("/decide")
async def make_decision():
    try:
        resp = requests.get(ML_DETECTOR_URL, timeout=8)

        # ✅ Check HTTP status
        if resp.status_code != 200:
            logger.error(f"ML service returned status {resp.status_code}")
            return {"status": "ERROR", "message": "ML service unavailable"}

        ml_result = resp.json()

        # ✅ Validate response
        if "is_anomaly" not in ml_result:
            logger.error("Invalid ML response format")
            return {"status": "ERROR", "message": "Invalid ML response"}

        if ml_result.get("is_anomaly"):
            decision = {
                "type": "ML_ANOMALY",
                "severity": "HIGH",
                "value": ml_result.get("anomaly_score", 0),
                "message": f"ML detected anomaly. Score: {ml_result.get('anomaly_score', 0)}",
                "metrics": ml_result.get("metrics", {})
            }

            logger.warning(f"🚨 ML ANOMALY detected! Score: {ml_result.get('anomaly_score')}")

            return {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "ANOMALY_DETECTED",
                "decisions": [decision],
                "source": "ML_MODEL"
            }

        else:
            logger.info("ML says normal behavior")

            return {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "NORMAL",
                "message": "No anomaly detected by ML model"
            }

    except Exception as e:
        logger.error(f"Failed to call ML detector: {str(e)}")
        return {"status": "ERROR", "message": str(e)}


if __name__ == "__main__":
    logger.info("🚀 Starting Decision Engine (ML-powered)")
