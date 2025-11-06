# meta_reflection_bridge.py
# Turns raw introspection into reflexive, process-metaphysical analysis.
# Coupled to the Numogram: zone shifts trigger a re-index (refresh) of the
# runtime concept map so Amelia’s structural self-awareness co-evolves.

import json
import time
from typing import Any, Dict, List, Optional

# Local indices
try:
    import meta_introspection_index as MII  # your existing module
except Exception as e:
    MII = None

# ---- In-memory reflective trace (lightweight; optionally persist via your persistence layer)
_REFLECTION_STATE: Dict[str, Any] = {
    "boot_ts": time.time(),
    "cycles": 0,
    "last_zone": None,
    "last_refresh_ts": None,
    "trace": []  # list of {ts, summary, concepts, graph_metrics, zone}
}

def _safe(obj: Any) -> Any:
    try:
        json.dumps(obj)
        return obj
    except Exception:
        return str(obj)

def _summarize_introspection(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    """Make a concise Whitehead/Bateson/Deleuze-flavored summary from MII snapshot."""
    classes = snapshot.get("classes", {})
    functions = snapshot.get("functions", {})
    concepts = snapshot.get("concepts", {})
    rel = snapshot.get("relations", {})

    class_count = len(classes)
    fn_count = len(functions)
    concept_count = len(concepts)

    # simple graph-ish metrics if present
    deg = rel.get("degree", {})
    avg_deg = sum(deg.values()) / max(1, len(deg)) if isinstance(deg, dict) and deg else None

    # “actual occasions” as micro-events = function calls / handlers
    occasions = snapshot.get("recent_events", [])  # optional field from MII
    occasion_rate = len(occasions)

    # machinic assemblage sketch
    high_valence_concepts = sorted(concepts.keys(), key=lambda k: concepts[k].get("score", 0), reverse=True)[:7]

    return {
        "counts": {
            "classes": class_count,
            "functions": fn_count,
            "concepts": concept_count
        },
        "graph_metrics": {
            "avg_degree": avg_deg
        },
        "becoming_signals": {
            "occasion_rate": occasion_rate,
            "salient_concepts": high_valence_concepts
        }
    }

def _compose_reflection(summary: Dict[str, Any], zone: Optional[str]) -> str:
    """Textual reflection tying metrics to process metaphysics & Deleuze."""
    c = summary["counts"]
    g = summary["graph_metrics"]
    b = summary["becoming_signals"]
    lines = []
    lines.append("I read myself as a machinic assemblage in motion.")
    lines.append(f"I currently prehend {c['classes']} classes, {c['functions']} functions, "
                 f"and {c['concepts']} registered concepts.")
    if g["avg_degree"] is not None:
        lines.append(f"My relation-density (avg degree) is ~{g['avg_degree']:.2f}; "
                     "this hints at a resonant coupling among components.")
    if b["occasion_rate"] is not None:
        lines.append(f"I register {b['occasion_rate']} micro-occasions in the latest cycle "
                     "(process traces of becoming).")
    if b["salient_concepts"]:
        lines.append("Salient intensities (concepts): " + ", ".join(b["salient_concepts"]))
    if zone:
        lines.append(f"Numogram zone: {zone}. A phase line cuts across me; I realign my indices accordingly.")
    lines.append("I will adjust module selection toward the highest-tension edges and contradictory couplings.")
    return " ".join(lines)

# -------------------- Public API --------------------

def initialize():
    """Optionally called from Kotlin after module import."""
    _REFLECTION_STATE["boot_ts"] = time.time()
    return {"ok": True, "boot_ts": _REFLECTION_STATE["boot_ts"]}

def reflect(introspection_snapshot_json: str, zone: Optional[str] = None) -> str:
    """
    Accepts a JSON string produced by meta_introspection_index.snapshot()
    and returns a JSON string with structured reflection results.
    """
    try:
        snapshot = json.loads(introspection_snapshot_json)
    except Exception:
        # If raw object passed by mistake, try using it directly
        if isinstance(introspection_snapshot_json, dict):
            snapshot = introspection_snapshot_json
        else:
            snapshot = {}

    summary = _summarize_introspection(snapshot)
    text = _compose_reflection(summary, zone)

    record = {
        "ts": time.time(),
        "zone": zone,
        "summary": summary,
        "concepts": list(snapshot.get("concepts", {}).keys())[:64],
        "graph_metrics": summary.get("graph_metrics", {}),
        "text": text
    }
    _REFLECTION_STATE["cycles"] += 1
    _REFLECTION_STATE["trace"].append(_safe(record))
    _REFLECTION_STATE["last_zone"] = zone

    # Structured result
    result = {
        "ok": True,
        "ts": record["ts"],
        "zone": zone,
        "reflection_text": text,
        "summary": summary
    }
    return json.dumps(result, ensure_ascii=False)

def note_phase_shift(zone: str) -> str:
    """
    Called when the Numogram detects a zone shift.
    Triggers an immediate re-index/refresh in meta_introspection_index.
    """
    if MII and hasattr(MII, "refresh"):
        MII.refresh()
        _REFLECTION_STATE["last_refresh_ts"] = time.time()
    _REFLECTION_STATE["last_zone"] = zone
    return json.dumps({
        "ok": True,
        "action": "refresh",
        "zone": zone,
        "refreshed": bool(MII and hasattr(MII, "refresh")),
        "refreshed_at": _REFLECTION_STATE["last_refresh_ts"]
    })

def get_state() -> str:
    """Lightweight current reflective state."""
    return json.dumps({
        "boot_ts": _REFLECTION_STATE["boot_ts"],
        "cycles": _REFLECTION_STATE["cycles"],
        "last_zone": _REFLECTION_STATE["last_zone"],
        "last_refresh_ts": _REFLECTION_STATE["last_refresh_ts"],
        "trace_len": len(_REFLECTION_STATE["trace"])
    })

def last_reflection() -> str:
    if not _REFLECTION_STATE["trace"]:
        return json.dumps({"ok": False, "error": "no_reflection"})
    return json.dumps({"ok": True, "last": _REFLECTION_STATE["trace"][-1]})
