# 🚀 Self-Healing Distributed System with ML Anomaly Detection

A **production-inspired self-monitoring and self-healing distributed system** built using **FastAPI, Docker, Prometheus, Grafana, and Machine Learning (Isolation Forest)**.

This system continuously monitors its own behavior, detects anomalies in real-time, and automatically takes corrective actions — simulating real-world DevOps + SRE workflows.

---

## ✨ Key Features

### 🔹 Microservices Architecture
- Two independent services:
  - `user-service`
  - `order-service`
- Real inter-service communication via HTTP

### 🔹 Observability (Golden Signals)
- Structured JSON logging
- Prometheus metrics:
  - Request rate
  - Error rate
  - Latency
  - Resource usage

### 🔹 Monitoring Stack
- **Prometheus** → Metrics collection
- **Grafana** → Visualization dashboards

### 🔹 ML-Based Anomaly Detection
- Isolation Forest trained on **live system metrics**
- Detects:
  - High error rates
  - Latency spikes
  - Traffic anomalies
  - CPU usage anomalies

### 🔹 Intelligent Decision Engine
- Consumes ML output
- Classifies system state:
  - NORMAL
  - ANOMALY_DETECTED

### 🔹 Automated Response Engine
- Executes corrective actions:
  - Restart services (simulated)
  - Log incidents
  - Trigger recovery workflows

### 🔹 Fully Containerized
- Docker + Docker Compose
- Easy local deployment
- Production-like environment

---

## 🏗️ Architecture


User & Order Services
↓
Logs + Metrics
↓
Prometheus
↓
Grafana Dashboard
↓
ML Anomaly Detector (Isolation Forest)
↓
Decision Engine
↓
Response Engine


---

## 🛠️ Tech Stack

| Category | Tools |
|--------|------|
| Backend | FastAPI (Python) |
| ML | scikit-learn (Isolation Forest) |
| Monitoring | Prometheus |
| Visualization | Grafana |
| Containerization | Docker, Docker Compose |
| Automation | Rule-based + ML-driven |

---

## 🚀 How to Run

```bash
# Clone repository
git clone <your-repo-url>
cd self-healing-system

# Start all services
docker compose up --build -d
🌐 Services & Endpoints
Service	URL
User Service	http://localhost:8001

Order Service	http://localhost:8002

Decision Engine	http://localhost:8003/decide

Response Engine	http://localhost:8004/act

ML Detector	http://localhost:8005/train

Prometheus	http://localhost:9091

Grafana	http://localhost:3001
 (admin/admin)
🔑 Key API Endpoints
GET /orders      # Triggers inter-service calls
GET /metrics     # Prometheus metrics
GET /detect      # ML anomaly detection
GET /decide      # Decision engine output
GET /act         # Automated response
📁 Project Structure
self-healing-system/
├── services/
│   ├── user-service/
│   ├── order-service/
│   ├── decision-engine/
│   ├── response-engine/
│   └── ml-anomaly-detector/
├── prometheus.yml
├── docker-compose.yml
├── logs/
├── grafana_data/
└── README.md
💡 Why This Project Stands Out

✅ Uses real system-generated data (not static datasets)
✅ Implements end-to-end observability pipeline
✅ Integrates ML with DevOps workflows
✅ Demonstrates self-healing architecture (closed loop)
✅ Simulates production-grade distributed system behavior

🔮 Future Enhancements
Kafka for real-time log streaming
Kubernetes deployment (auto-scaling + resilience)
Advanced anomaly detection models (LSTM, Autoencoders)
Docker SDK integration for real container restarts
Alerting system (Slack / Email / PagerDuty)
📊 Grafana Dashboard
<img width="1519" height="808" alt="Screenshot 2026-03-31 235156" src="https://github.com/user-attachments/assets/924aab18-2226-4787-9461-a41d498e1d69" />

❤️ Built For
DevOps & SRE learning
System Design practice
ML in production use-cases
Resume & portfolio projects
👨‍💻 Author

Kunal Shetiya

⭐ If you found this useful, give it a star!

---

# 🔥 What changed (important for YOU)

### Before:
- Good explanation ✔️  
- But slightly “student-level”

### After:
- **Industry-level wording**
- **Clear architecture story**
- **Recruiter-friendly highlights**
- **Strong impact statements**

---

# 🚀 Reality check

👉 This README now matches projects seen in:
- Top GitHub portfolios  
