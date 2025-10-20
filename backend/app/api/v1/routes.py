from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.controller import controller
from app.services.simulator import plant_config, set_actuators

router = APIRouter()

class SetpointRequest(BaseModel):
    temperature_sp: float | None = None
    pressure_sp: float | None = None
    reflux_ratio: float | None = None
    feed_rate: float | None = None

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/config")
def get_config():
    return plant_config()

@router.post("/setpoints")
def update_setpoints(req: SetpointRequest):
    changes = {k:v for k,v in req.model_dump().items() if v is not None}
    if not changes:
        raise HTTPException(status_code=400, detail="No setpoints provided")
    set_actuators(**changes)
    return {"updated": changes}

@router.post("/control/tick")
def control_tick():
    # one-step control (useful for synchronous validation)
    action = controller.decide_action()
    set_actuators(**action)
    return {"action": action}
