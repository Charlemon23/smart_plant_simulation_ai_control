from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from app.core.config import settings
from app.api.v1.routes import router as api_router
from app.services.simulator import simulator_loop, TelemetryEvent
import asyncio
import json

# ==============================================================
# Smart Plant API — Main Application Entry
# ==============================================================

app = FastAPI(
    title="Smart Plant API",
    description="Autonomous Process Control and Cyber Resilience Framework",
    version="1.0.0",
    default_response_class=ORJSONResponse,
)

# ==============================================================
# Global CORS Middleware
# Allows all Codespaces URLs, localhost, and internal API calls.
# ==============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # from config.py
    allow_origin_regex=r"https:\/\/.*\.app\.github\.dev",  # any Codespaces subdomain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================
# Include REST API routes
# ==============================================================

app.include_router(api_router, prefix="/api/v1")

# ==============================================================
# WebSocket — Live Telemetry Stream
# ==============================================================

@app.websocket("/ws/telemetry")
async def ws_telemetry(ws: WebSocket):
    """Real-time telemetry data feed for the Smart Plant dashboard."""
    await ws.accept()
    try:
        async for evt in simulator_loop():
            payload = json.dumps(evt.model_dump())
            await ws.send_text(payload)
    except Exception as e:
        print(f"WebSocket connection closed: {e}")
    finally:
        await ws.close()

# ==============================================================
# Health Check Endpoint
# ==============================================================

@app.get("/api/v1/health")
def health():
    """Simple health check for backend connectivity."""
    return {
        "status": "ok",
        "backend_url": settings.BACKEND_URL,
        "cors_allowed": settings.CORS_ORIGINS,
    }

# ==============================================================
# Root Endpoint — Friendly Info Page
# ==============================================================

@app.get("/")
def root():
    """Provide helpful links when visiting the root URL."""
    return {
        "message": "Smart Plant API running successfully",
        "docs": f"{settings.BACKEND_URL}/docs",
        "health": f"{settings.BACKEND_URL}/api/v1/health",
        "websocket": f"wss://{settings.BACKEND_URL.split('https://')[-1]}/ws/telemetry",
    }

# ==============================================================
# Startup / Shutdown Hooks (Optional Future Enhancements)
# ==============================================================

@app.on_event("startup")
async def startup_event():
    print("🚀 Smart Plant backend starting up...")
    print(f"Backend URL: {settings.BACKEND_URL}")
    print(f"CORS Origins: {settings.CORS_ORIGINS}")

@app.on_event("shutdown")
async def shutdown_event():
    print("🧩 Smart Plant backend shutting down...")
