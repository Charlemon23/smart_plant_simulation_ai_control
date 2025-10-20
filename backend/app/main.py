from fastapi import FastAPI, WebSocket, Depends
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

# In-memory subscription set for demo purposes. Replace with Redis pub/sub in scale-out.
subscribers = set()

@app.websocket("/ws/telemetry")
async def ws_telemetry(ws: WebSocket):
    await ws.accept()
    subscribers.add(ws)
    try:
        # Broadcast simulator stream to this client
        # Each connection gets its own task to forward shared telemetry events.
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
