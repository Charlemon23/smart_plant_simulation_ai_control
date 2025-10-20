import asyncio
import time
from pydantic import BaseModel
from typing import AsyncIterator

# Simple deterministic plant dynamics stub
# Replace with Tennessee Eastman dynamics or FMU via PyFMI for fidelity.

class TelemetryEvent(BaseModel):
    ts: float
    temperature: float
    pressure: float
    flow: float
    composition: float
    temperature_sp: float
    pressure_sp: float
    reflux_ratio: float
    feed_rate: float

_state = {
    "temperature": 370.0,
    "pressure": 3.0,
    "flow": 100.0,
    "composition": 0.85,
}
_actuators = {
    "temperature_sp": 375.0,
    "pressure_sp": 3.2,
    "reflux_ratio": 1.5,
    "feed_rate": 100.0,
}

def plant_config():
    return {"state": _state, "actuators": _actuators}

def set_actuators(**kwargs):
    for k,v in kwargs.items():
        if k in _actuators:
            _actuators[k] = float(v)

def _step(dt: float = 0.5):
    # First-order approach to setpoints with simple cross-coupling
    k_t, k_p, k_f, k_c = 0.08, 0.05, 0.03, 0.02
    _state["temperature"] += k_t * (_actuators["temperature_sp"] - _state["temperature"]) * dt
    _state["pressure"]    += k_p * (_actuators["pressure_sp"] - _state["pressure"]) * dt
    _state["flow"]        += k_f * (_actuators["feed_rate"] - _state["flow"]) * dt
    # composition mildly depends on reflux and temperature
    _state["composition"] += k_c * ((1.8 - _actuators["reflux_ratio"]) + (380 - _state["temperature"])*0.002) * dt
    # clamp reasonable bounds
    _state["composition"] = max(0.0, min(1.0, _state["composition"]))

async def simulator_loop(period: float = 0.5) -> AsyncIterator[TelemetryEvent]:
    while True:
        _step(dt=period)
        evt = TelemetryEvent(
            ts=time.time(),
            temperature=_state["temperature"],
            pressure=_state["pressure"],
            flow=_state["flow"],
            composition=_state["composition"],
            temperature_sp=_actuators["temperature_sp"],
            pressure_sp=_actuators["pressure_sp"],
            reflux_ratio=_actuators["reflux_ratio"],
            feed_rate=_actuators["feed_rate"],
        )
        yield evt
        await asyncio.sleep(period)
