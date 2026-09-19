"""
P3.5A -- dependency-free Chaquopy build-viability probe.

Purpose: prove that Chaquopy itself compiles and runs through the current
native P0-P3.3 GitHub Actions -> APK -> device pipeline, with zero
dependencies (no numpy, no torch, no Numogram) before adding any of those
as variables. If this doesn't build and round-trip, nothing past it will
either, and the failure is isolated to Chaquopy/toolchain integration
rather than anything in the Numogram code itself.
"""

import json


def ping(request_json: str) -> str:
    try:
        request = json.loads(request_json)
        return json.dumps(
            {
                "status": "success",
                "probe": "P3.5A-chaquopy-probe-v1",
                "received": request,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    except Exception as exc:
        return json.dumps(
            {
                "status": "error",
                "error_type": type(exc).__name__,
                "message": str(exc),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
