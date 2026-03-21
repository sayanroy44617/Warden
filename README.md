
# 🛡️ Warden
> A System that guards your containers

Warden is a personal AI-powered monitoring and self-healing system for Docker containers. It continuously watches your containers, detects anomalies using AI, and notifies you with a suggested fix — which only executes with **your approval**.

---

## System Design Of Warden
![Warden](assets/img.png)

---

## ✨ What it does

- 📊 **Monitors** container CPU, memory, and restart counts via Prometheus + cAdvisor
- 📝 **Collects** container logs via Promtail + Loki
- 🤖 **Analyzes** anomalies using Claude AI — root cause + fix suggestion
- 📧 **Notifies** you via email with an Approve / Reject button
- 🔧 **Fixes** the issue automatically — but only when you say so
- 📈 **Visualizes** everything in a Grafana dashboard

---

## 🏗️ Architecture

```
Docker Containers (demo-app)
        │
        ├── cAdvisor ──── metrics ──▶ Prometheus
        │
        └── Promtail ──── logs ────▶ Loki
                                        │
                                        ▼
                              Warden Engine (FastAPI)
                                        │
                              polls every 30s (Prometheus)
                              fetches logs on anomaly (Loki)
                                        │
                                        ▼
                                   Claude AI
                              (root cause + fix plan)
                                        │
                                        ▼
                                  📧 Email Alert
                              [Approve Fix] [Reject]
                                        │
                              ┌─────────┴─────────┐
                              ▼                   ▼
                         Execute Fix         Log & Skip
                         (Docker SDK)        (PostgreSQL)
                              │
                              ▼
                       Verify Health
                       Send follow-up
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Monitoring | Prometheus + cAdvisor |
| Logs | Loki + Promtail |
| Visualization | Grafana |
| AI Analysis | Claude API (Anthropic) |
| Core Engine | Python + FastAPI + asyncio |
| Approval State | Redis |
| Incident Storage | PostgreSQL |
| Container Control | Docker Python SDK |
| Notifications | SMTP Email (Gmail) |

---

## 🚀 Getting Started

### Prerequisites
- Docker + Docker Compose
- Python 3.11+
- Anthropic API key
- Gmail account (for notifications)

### Setup

```bash
# Clone the repo
git clone https://github.com/sayanroy44617/Warden.git
cd Warden

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Start the stack
docker-compose up -d
```

### Access

| Service | URL |
|---|---|
| Grafana Dashboard | http://localhost:3000 |
| Prometheus | http://localhost:9090 |
| Warden API | http://localhost:8000 |
| Loki | http://localhost:3100 |

---

## ⚙️ Environment Variables

```env
# AI
ANTHROPIC_API_KEY=your_key_here

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
ALERT_EMAIL=your_email@gmail.com

# PostgreSQL (Warden)
POSTGRES_USER=warden
POSTGRES_PASSWORD=warden
POSTGRES_DB=warden

# PostgreSQL (Demo App)
POSTGRES_USER_DEMO=demo
POSTGRES_PASSWORD_DEMO=demo
POSTGRES_DB_DEMO=demo

# Prometheus
PROMETHEUS_URL=http://prometheus:9090

# Loki
LOKI_URL=http://loki:3100
```

---

## 🧪 Testing

Trigger a failure on the demo container:

```bash
# CPU spike
docker-compose stop demo-app
# Change MODE=cpu_spike in docker-compose.yml
docker-compose up -d demo-app

# Memory leak
# Change MODE=memory_leak in docker-compose.yml
docker-compose up -d demo-app

# Crash loop
# Change MODE=crash in docker-compose.yml
docker-compose up -d demo-app
```

Warden will detect the anomaly, analyze it with Claude, and send you an email within 30 seconds.

---

## 📁 Project Structure

```
Warden/
├── docker-compose.yml
├── warden.Dockerfile
├── requirements.txt
├── .env.example
├── config/
│   ├── prometheus.yml
│   ├── loki-config.yml
│   ├── promtail-config.yml
│   └── grafana-provisioning/
├── demo-app/
│   ├── app.py
│   └── Dockerfile
└── src/
    ├── main.py
    ├── monitor.py
    ├── ai_engine.py
    ├── notifier.py
    ├── fix_executor.py
    ├── approval_server.py
    └── models/
        ├── incident.py
        ├── fix_plan.py
        └── fix_result.py
```

---

## 🚧 Project Status

Work in progress — being built in pair programming sessions.

- [x] Project architecture + system design
- [x] Docker Compose stack
- [x] Demo app with failure modes
- [x] Prometheus + Loki + Grafana setup
- [x] Pydantic models (Incident, FixPlan, FixResult)
- [x] Monitor engine (Prometheus polling)
- [x] AI engine (Gemini integration)
- [x] Email notifier
- [x] Approval server (FastAPI)
- [ ] Fix executor (Docker SDK)
- [ ] End-to-end testing

---

## 🔮 Future Plans
- [ ] Agentic AI — autonomous multi-step remediation
- [ ] Multiple container monitoring
- [ ] Kubernetes support
---

## 📄 License

MIT License — personal project, feel free to fork and build on it.