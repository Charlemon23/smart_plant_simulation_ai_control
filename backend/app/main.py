from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from app.core.config import settings
from app.api.v1.routes import router as api_router
from app.services.simulator import simulator_loop, TelemetryEvent
import asyncio
import json

app = FastAPI(
    title="Smart Plant API",
    default_response_class=ORJSONResponse
)

# === CORS setup (Codespaces & local safe) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === REST API routes ===
app.include_router(api_router, prefix="/api/v1")

# === WebSocket telemetry endpoint ===
subscribers = set()

@app.websocket("/ws/telemetry")
async def ws_telemetry(ws: WebSocket):
    await ws.accept()
    subscribers.add(ws)
    try:
        queue = asyncio.Queue()

        async def enqueue_events():
            async for evt in simulator_loop():
                await queue.put(evt)

        forwarder = asyncio.create_task(enqueue_events())
        try:
            while True:
                evt: TelemetryEvent = await queue.get()
                await ws.send_text(json.dumps(evt.model_dump()))
        finally:
            forwarder.cancel()
    except Exception:
        pass
    finally:
        subscribers.discard(ws)
        await ws.close()


# === Health Check (for CI / Dev) ===
@app.get("/health")
def health():
    return {"status": "ok", "backend_url": settings.BACKEND_URL}
