# 🚀 Self-Healing Distributed System with ML Anomaly Detection

A production-inspired distributed monitoring and self-healing system built using **FastAPI, Docker, Prometheus, Grafana, and Machine Learning (Isolation Forest).**

The system continuously monitors live metrics, detects anomalies in real time, and simulates automated recovery workflows similar to modern DevOps + SRE environments.

---

# ✨ Features

* Microservices architecture (`user-service` & `order-service`)
* Real-time monitoring with Prometheus
* Grafana dashboards for visualization
* ML-based anomaly detection using Isolation Forest
* Automated decision & response engines
* Structured JSON logging
* Dockerized deployment with Docker Compose
* Simulated self-healing workflows

---

# 🏗️ Architecture

```text id="1l7m7j"
Services → Metrics → Prometheus → Grafana
                         ↓
              ML Anomaly Detector
                         ↓
                 Decision Engine
                         ↓
                 Response Engine
```

---

# 🛠️ Tech Stack

| Category         | Tools                           |
| ---------------- | ------------------------------- |
| Backend          | FastAPI, Python                 |
| ML               | Scikit-Learn (Isolation Forest) |
| Monitoring       | Prometheus                      |
| Visualization    | Grafana                         |
| Containerization | Docker, Docker Compose          |

---

# 📂 Project Structure

```bash id="7pwk6n"
self-healing-system/
│
├── services/
│   ├── user-service/
│   ├── order-service/
│   ├── ml-anomaly-detector/
│   ├── decision-engine/
│   └── response-engine/
│
├── docker-compose.yml
├── prometheus.yml
└── README.md
```

---

# 🚀 Run Locally

```bash id="vz3vib"
git clone https://github.com/sakshii1411/self-healing-system.git

cd self-healing-system

docker compose up --build -d
```

---

# 🌐 Services

| Service         | URL                                                          |
| --------------- | ------------------------------------------------------------ |
| User Service    | [http://localhost:8001](http://localhost:8001)               |
| Order Service   | [http://localhost:8002](http://localhost:8002)               |
| Decision Engine | [http://localhost:8003/decide](http://localhost:8003/decide) |
| Response Engine | [http://localhost:8004/act](http://localhost:8004/act)       |
| ML Detector     | [http://localhost:8005/train](http://localhost:8005/train)   |
| Prometheus      | [http://localhost:9091](http://localhost:9091)               |
| Grafana         | [http://localhost:3001](http://localhost:3001)               |

### Grafana Login

```text id="s5xihd"
Username: admin
Password: admin
```

---

# 🔑 Important Endpoints

```http id="nqlj7j"
GET /orders
GET /metrics
GET /train
GET /detect
GET /decide
GET /act
```

---

# 📊 Example Workflow

```text id="2m7j3t"
1. Services generate metrics
2. Prometheus collects telemetry
3. ML model detects anomalies
4. Decision engine classifies system state
5. Response engine simulates recovery actions
```

---

# 💡 Highlights

✅ Real-time observability pipeline
✅ ML integrated with DevOps workflows
✅ Production-style monitoring setup
✅ Self-healing system simulation
✅ End-to-end distributed architecture

---

# 🔮 Future Enhancements

* Kubernetes deployment
* Kafka integration
* Auto-scaling
* Real container restarts
* Slack / Email alerting
* Advanced deep learning anomaly detection

---

# 👨‍💻 Author

## Sakshi Awasthi
