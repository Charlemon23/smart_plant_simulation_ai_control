# Smart Plant Simulation & AI Control — Production Starter

A production-grade starter for a virtual chemical plant with AI-driven control,
built with **FastAPI (Python)** + **React (TypeScript)**, ready for **Docker Compose** and **Kubernetes**.

## Stack
- Backend: FastAPI, uvicorn, SQLAlchemy, Pydantic, WebSocket, Celery (optional)
- Frontend: React (Vite, TS), Recharts, Zustand
- Data: PostgreSQL (TimescaleDB compatible), Redis (pub/sub, cache)
- Messaging: WebSocket (live telemetry). Optional Kafka hooks included.
- Reverse proxy: NGINX
- Containerization: Docker, docker-compose; Kubernetes manifests under `k8s/`.

## Local Development (Docker Compose)
```bash
cp .env.example .env
docker compose up --build
# Frontend: http://localhost:8080
# Backend:  http://localhost:8000/docs
```

## Kubernetes (kind or your cluster)
```bash
# Update image names/tags in k8s/*.yaml as needed
kubectl apply -f k8s/
```

## Services
- `backend/`: FastAPI app exposing REST & WebSocket for telemetry/control.
- `frontend/`: React dashboard with live plots and controls.
- `nginx/`: Reverse proxy serving frontend and routing API/WebSocket.
- `db/`: Postgres with TimescaleDB-compatible settings (vanilla Postgres image used as default).
- `redis/`: Cache and pub/sub for live telemetry.
- `scripts/`: helper scripts.
- `k8s/`: Kubernetes manifests (Deployment, Service, Ingress).

## Simulator & Controller
- `backend/app/services/simulator.py`: deterministic, configurable chemical process simulator stub (reactor + distillation loop).
- `backend/app/services/controller.py`: AI control hooks with an abstract interface for forecasting and RL control (plug in your models).
- `backend/app/services/anomaly.py`: basic anomaly detection stubs for cyber-resilience.

## Notes
This is a scaffold. Replace stubs with your Tennessee Eastman implementation or FMU via PyFMI if desired.
Keep the interface contracts stable to avoid frontend or API changes.
