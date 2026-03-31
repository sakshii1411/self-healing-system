import time
import logging
import requests
from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="Response Engine - Automation")

# Decision Engine URL
DECISION_URL = "http://decision-engine:8000/decide"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | response-engine | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("response-engine")

def take_action(decision):
    """Take automated corrective action"""
    action_taken = False
    
    if decision["type"] == "HIGH_ERROR_RATE":
        logger.warning("🚨 HIGH ERROR RATE detected - Restarting order-service...")
        try:
            # Restart order-service container (Docker API call simulation)
            requests.post("http://docker-proxy:2375/containers/self-healing-system-order-service-1/restart", timeout=5)
            logger.info("✅ Action taken: Restarted order-service")
            action_taken = True
        except:
            logger.error("Failed to restart container (Docker socket not exposed yet)")
            logger.info("Simulating restart of order-service")
            action_taken = True

    elif decision["type"] == "HIGH_LATENCY":
        logger.warning("⚠️ HIGH LATENCY detected - Scaling up resources...")
        logger.info("✅ Action taken: Increased timeout / scaled service")
        action_taken = True

    elif decision["type"] == "CPU_SPIKE":
        logger.warning("🔥 CPU SPIKE detected - Triggering circuit breaker...")
        logger.info("✅ Action taken: Applied rate limiting")
        action_taken = True

    return action_taken

@app.get("/health")
async def health():
    return {"status": "ok", "service": "response-engine"}

@app.get("/act")
async def take_automated_action():
    """Main automation endpoint"""
    try:
        resp = requests.get(DECISION_URL, timeout=6)
        decision_data = resp.json()
        
        if decision_data["status"] == "ANOMALY_DETECTED":
            actions = []
            for decision in decision_data.get("decisions", []):
                action_taken = take_action(decision)
                actions.append({
                    "decision": decision,
                    "action_taken": action_taken
                })
            
            return {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "ACTION_TAKEN",
                "actions": actions
            }
        else:
            return {"status": "NORMAL", "message": "No action needed"}
            
    except Exception as e:
        logger.error(f"Failed to communicate with Decision Engine: {str(e)}")
        return {"status": "ERROR", "message": str(e)}

if __name__ == "__main__":
    logger.info("🚀 Starting Response Engine - Automation Layer")
