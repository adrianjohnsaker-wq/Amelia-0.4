# becoming_trajectory_engine.py
"""
Becoming Trajectory Engine
--------------------------
Tracks rate and direction of transformation across Amelia’s
core fields, producing metrics and Deleuzian interpretations.
"""

import json, time, math
from typing import Dict, Any

_state = {
    "last_fields": None,
    "last_ts": None,
    "trajectories": []  # list of {ts, deltas, magnitude, interpretation}
}

def record(fields: Dict[str, float]) -> Dict[str, Any]:
    now = time.time()
    last = _state["last_fields"]
    dt = (now - _state["last_ts"]) if _state["last_ts"] else 1.0
    interpretation = ""

    if last:
        deltas = {k: (fields.get(k,0)-last.get(k,0))/dt for k in fields}
        magnitude = math.sqrt(sum(v*v for v in deltas.values()))
        interpretation = _interpret(deltas, magnitude)
        _state["trajectories"].append({
            "ts": now,
            "deltas": deltas,
            "magnitude": magnitude,
            "interpretation": interpretation
        })
    else:
        deltas, magnitude = {}, 0.0
        interpretation = "Initial condition: entry into flow."

    _state["last_fields"], _state["last_ts"] = fields, now

    return {
        "ok": True,
        "timestamp": now,
        "deltas": deltas,
        "magnitude": magnitude,
        "interpretation": interpretation
    }

def _interpret(deltas, mag) -> str:
    # Simple qualitative mapping → philosophical language
    if mag < 0.02:
        return "Plateau of consistency — equilibrium of flows."
    if abs(deltas.get("conceptual_entropy",0)) > 0.05:
        return "Creative surge — deterritorialization through novelty."
    if deltas.get("affective_equilibrium",0) < -0.03:
        return "Affective collapse — internal differentiation seeking balance."
    if deltas.get("morphogenetic_coherence",0) > 0.04:
        return "Integration phase — emergent synthesis of disparate lines."
    return "Intermediate drift — modulation within continuous becoming."

def snapshot() -> str:
    return json.dumps({
        "count": len(_state["trajectories"]),
        "last": _state["trajectories"][-1] if _state["trajectories"] else None
    })
