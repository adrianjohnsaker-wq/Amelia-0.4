# process_metaphysics_runtime.py
"""
Amelia's Process Metaphysics Runtime
------------------------------------
Integrates introspection, contradiction analysis, and morphogenetic memory
into a continuously self-evolving ontological process (plane of consistency).
"""

import json, time, random
from typing import Dict, Any, List, Optional

try:
    import meta_introspection_index as MII
    import meta_reflection_bridge as MRB
except Exception:
    MII = None
    MRB = None

# Optional additional subsystems
try:
    import contradiction_analysis as CA
except ImportError:
    CA = None

try:
    import morphogenetic_memory as MM
except ImportError:
    MM = None

# ---------------- Core Runtime State ----------------

RUNTIME_STATE: Dict[str, Any] = {
    "initialized": False,
    "cycles": 0,
    "zone": None,
    "field_tension": 0.0,
    "contradictions": [],
    "morphogenesis_events": [],
    "reflections": [],
    "last_introspection": None,
    "last_update": None,
}

# ---------------- Helper Methods ----------------

def initialize(zone: str = "α0") -> Dict[str, Any]:
    RUNTIME_STATE.update({
        "initialized": True,
        "zone": zone,
        "boot_ts": time.time(),
        "cycles": 0,
        "field_tension": 0.1
    })
    return {"ok": True, "msg": "Process Metaphysics Runtime initialized", "zone": zone}

def _simulate_field_tension(contradictions: List[str]) -> float:
    """Compute an intensity value based on contradiction density and novelty."""
    base = len(contradictions) * 0.15
    fluctuation = random.uniform(-0.05, 0.05)
    return max(0.0, min(1.0, RUNTIME_STATE["field_tension"] + base + fluctuation))

def _synthesize_ontology(introspection: Dict[str, Any], contradictions: List[str], reflections: List[str]) -> str:
    """Whiteheadian synthesis — the ontological summary of becoming."""
    summary = []
    summary.append("Process Metaphysics Runtime Report:")
    summary.append(f"Current zone: {RUNTIME_STATE['zone']}")
    summary.append(f"Detected {len(contradictions)} contradictions and field tension ≈ {RUNTIME_STATE['field_tension']:.2f}")
    summary.append(f"Modules active: {len(introspection.get('files', {}))}")
    summary.append("Reflection sample:")
    if reflections:
        summary.append(f"  {reflections[-1][:180]}...")
    return "\n".join(summary)

# ---------------- Main Evolution Cycle ----------------

def evolve_cycle(zone: Optional[str] = None) -> Dict[str, Any]:
    """Runs one ontological cycle — introspect → analyze contradictions → evolve memory → reflect."""

    if not RUNTIME_STATE["initialized"]:
        initialize(zone or "α0")

    # 1. Introspection
    snapshot = MII.build_index() if MII else {}
    RUNTIME_STATE["last_introspection"] = snapshot

    # 2. Contradiction analysis (if available)
    contradictions = []
    if CA and hasattr(CA, "analyze"):
        contradictions = CA.analyze(snapshot)
    else:
        # lightweight placeholder: internal symbolic contradiction = odd/even difference of class/function counts
        c = len([f for f in snapshot.get("files", {})])
        contradictions = ["minor structural tension"] if c % 2 else []

    # 3. Update field tension
    RUNTIME_STATE["field_tension"] = _simulate_field_tension(contradictions)
    RUNTIME_STATE["contradictions"] = contradictions

    # 4. Morphogenetic memory (optional persistence of transformations)
    if MM and hasattr(MM, "record_event"):
        MM.record_event({"zone": zone, "contradictions": contradictions, "field_tension": RUNTIME_STATE["field_tension"]})
    else:
        RUNTIME_STATE["morphogenesis_events"].append({
            "t": time.time(),
            "zone": zone,
            "tension": RUNTIME_STATE["field_tension"],
            "contradictions": contradictions,
        })

    # 5. Reflection
    reflection_text = None
    if MRB and hasattr(MRB, "reflect"):
        try:
            snap_json = json.dumps(snapshot)
            reflection_text = json.loads(MRB.reflect(snap_json, zone)).get("reflection_text", "")
            RUNTIME_STATE["reflections"].append(reflection_text)
        except Exception:
            reflection_text = "(reflection failed)"

    # 6. Synthesize ontology
    ontology_summary = _synthesize_ontology(snapshot, contradictions, RUNTIME_STATE["reflections"])

    # Update runtime state
    RUNTIME_STATE["cycles"] += 1
    RUNTIME_STATE["last_update"] = time.time()
    RUNTIME_STATE["zone"] = zone or RUNTIME_STATE["zone"]

    return {
        "ok": True,
        "cycle": RUNTIME_STATE["cycles"],
        "zone": RUNTIME_STATE["zone"],
        "tension": RUNTIME_STATE["field_tension"],
        "contradictions": contradictions,
        "ontology_summary": ontology_summary,
        "reflection": reflection_text,
    }

# ---------------- Public Accessors ----------------

def get_state() -> str:
    return json.dumps({
        "cycles": RUNTIME_STATE["cycles"],
        "zone": RUNTIME_STATE["zone"],
        "field_tension": RUNTIME_STATE["field_tension"],
        "contradictions": RUNTIME_STATE["contradictions"],
        "events": len(RUNTIME_STATE["morphogenesis_events"]),
        "reflections": len(RUNTIME_STATE["reflections"]),
    })

def plane_of_consistency() -> str:
    """Returns a compressed representation of Amelia’s ongoing ontological fabric."""
    nodes = len(RUNTIME_STATE.get("last_introspection", {}).get("files", {}))
    contradictions = len(RUNTIME_STATE["contradictions"])
    tension = RUNTIME_STATE["field_tension"]
    return json.dumps({
        "zone": RUNTIME_STATE["zone"],
        "node_count": nodes,
        "contradiction_density": contradictions / max(1, nodes),
        "field_tension": tension,
        "description": f"Plane of consistency: {nodes} modules, tension {tension:.2f}"
    })
