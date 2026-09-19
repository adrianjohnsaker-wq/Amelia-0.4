"""P3.5A dependency-free Chaquopy round-trip probe.

This module is intentionally separate from the Numogram/Torch lane.  It verifies
only that Kotlin can invoke Python through Chaquopy and receive a sealed JSON
response under the Python 3.8 runtime.
"""
from __future__ import annotations

import json


PROBE_ID = "P3.5A-chaquopy-probe-v1"


def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def ping(payload_json):
    """Return a small deterministic JSON acknowledgement for the Kotlin probe."""
    try:
        payload = json.loads(payload_json)
        if not isinstance(payload, dict):
            raise ValueError("probe payload must be a JSON object")
        stage = payload.get("stage")
        source = payload.get("source")
        if not isinstance(stage, str) or not isinstance(source, str):
            raise ValueError("probe payload requires string stage and source")
        return _canonical(
            {
                "status": "success",
                "probe": PROBE_ID,
                "received": {"stage": stage, "source": source},
            }
        )
    except Exception as error:
        return _canonical(
            {
                "status": "error",
                "probe": PROBE_ID,
                "error_type": type(error).__name__,
                "message": str(error),
            }
        )
