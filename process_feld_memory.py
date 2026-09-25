"""P3.11 session-local Process Field Memory module for Amelia.

The module is deliberately deterministic and dependency-light. It retains a
10 x 10 bounded field for the lifetime of the Python process and exposes one
entry point, ``amelia_event(payload_json)``. It performs no file, environment,
network, native, or Android access.

P3.11 is an integration assay, not the final ProcessFieldMemory implementation.
Its purpose is to make history-conditioned contribution observable downstream
of an already-committed Numogram transition.
"""

import hashlib
import json

ZONE_COUNT = 10
DECAY = 0.96
ORIGIN_TRACE = 0.06
DESTINATION_TRACE = 0.18
PATH_TRACE = 0.24
SYZYGY_TRACE = 0.04


def _blank_tensor():
    return [[0.0 for _ in range(ZONE_COUNT)] for _ in range(ZONE_COUNT)]


_STATE = {
    "invocation": 0,
    "tensor": _blank_tensor(),
    "transition_counts": {},
    "last_transition": None,
}


def _clamp(value):
    return max(0.0, min(1.0, float(value)))


def _zone(value):
    zone = int(value)
    if zone < 0 or zone >= ZONE_COUNT:
        raise ValueError("zone must be in [0, 9]")
    return zone


def _profile(tensor):
    profile = []
    for zone in range(ZONE_COUNT):
        row_mean = sum(tensor[zone]) / ZONE_COUNT
        col_mean = sum(tensor[row][zone] for row in range(ZONE_COUNT)) / ZONE_COUNT
        profile.append(round((row_mean + col_mean) / 2.0, 6))
    return profile


def _state_digest(invocation, tensor, counts, last_transition):
    payload = {
        "invocation": invocation,
        "tensor": [[round(cell, 8) for cell in row] for row in tensor],
        "transition_counts": dict(sorted(counts.items())),
        "last_transition": last_transition,
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _interpretive_contribution(
    invocation,
    origin,
    destination,
    previous_profile,
    current_profile,
    prior_path_count,
    dominant_zone,
):
    if invocation == 1:
        return (
            "ProcessFieldMemory registers this as the first retained process event "
            "of the current session. The present transition therefore establishes "
            "a history that later events can inherit rather than inheriting an "
            "already-developed field."
        )

    inherited_destination = previous_profile[destination]
    if prior_path_count > 0:
        return (
            f"The Z{origin}→Z{destination} path has already occurred "
            f"{prior_path_count} time(s) in retained process history. The present "
            f"event therefore recurs through a previously deformed field; the "
            f"strongest retained zone after this update is Z{dominant_zone}."
        )

    if inherited_destination >= 0.03:
        return (
            f"The present transition enters Z{destination}, which already carried "
            f"retained field activation ({inherited_destination:.3f}) before this "
            f"event. Its current meaning is therefore conditioned by prior process "
            f"rather than by the transition alone."
        )

    return (
        f"The transition extends retained process into Z{destination} while "
        f"preserving deformation accumulated by earlier events. The strongest "
        f"current field concentration is Z{dominant_zone} "
        f"({current_profile[dominant_zone]:.3f})."
    )


def amelia_event(payload_json):
    payload = json.loads(payload_json)
    if not isinstance(payload, dict):
        raise ValueError("P3.11 payload must be a JSON object")

    transition = payload.get("transition") or {}
    plan = payload.get("event_plan") or {}

    origin = _zone(transition.get("from"))
    destination = _zone(transition.get("to"))
    event_type = str(plan.get("event_type") or "UNSPECIFIED")

    previous_tensor = [row[:] for row in _STATE["tensor"]]
    previous_profile = _profile(previous_tensor)

    updated = []
    for row in previous_tensor:
        updated.append([_clamp(cell * DECAY) for cell in row])

    for index in range(ZONE_COUNT):
        updated[origin][index] = _clamp(updated[origin][index] + ORIGIN_TRACE)
        updated[index][destination] = _clamp(updated[index][destination] + DESTINATION_TRACE)

    updated[origin][destination] = _clamp(
        updated[origin][destination] + PATH_TRACE
    )

    if origin + destination == 9:
        for index in range(ZONE_COUNT):
            updated[index][9 - index] = _clamp(
                updated[index][9 - index] + SYZYGY_TRACE
            )

    path_key = f"{origin}>{destination}"
    prior_path_count = int(_STATE["transition_counts"].get(path_key, 0))
    next_counts = dict(_STATE["transition_counts"])
    next_counts[path_key] = prior_path_count + 1

    invocation = int(_STATE["invocation"]) + 1
    current_profile = _profile(updated)
    dominant_zone = max(range(ZONE_COUNT), key=lambda z: current_profile[z])

    last_transition = {
        "from": origin,
        "to": destination,
        "event_type": event_type,
    }
    digest = _state_digest(invocation, updated, next_counts, last_transition)
    relay_marker = f"PFM-{invocation:03d}-{digest[:12]}"

    contribution = _interpretive_contribution(
        invocation=invocation,
        origin=origin,
        destination=destination,
        previous_profile=previous_profile,
        current_profile=current_profile,
        prior_path_count=prior_path_count,
        dominant_zone=dominant_zone,
    )

    _STATE["invocation"] = invocation
    _STATE["tensor"] = updated
    _STATE["transition_counts"] = next_counts
    _STATE["last_transition"] = last_transition

    result = {
        "schema": "amelia-p3.11-process-field-memory-v1",
        "status": "contribution_ready",
        "module": "ProcessFieldMemory",
        "history_depth": invocation,
        "transition": last_transition,
        "prior_same_path_count": prior_path_count,
        "previous_zone_profile": previous_profile,
        "current_zone_profile": current_profile,
        "dominant_zone": dominant_zone,
        "state_digest": digest,
        "relay_marker": relay_marker,
        "interpretive_contribution": contribution,
        "persistence_scope": "python_process_session",
    }
    return json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
