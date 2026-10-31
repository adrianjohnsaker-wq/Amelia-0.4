"""P3.26 encounter runner primitives; execution awaits a sealed registration."""
from __future__ import annotations

import copy
import hashlib
import json
from typing import Dict, Iterable, List, Sequence

from graph_field import apply_one_transition


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def state_digest(process: object) -> str:
    state = {
        "current_zone": int(process.current_zone),
        "step_count": int(process.step_count),
        "zones": process.zones,
        "gates": process.gates,
        "deformation_tensor": process.deformation_tensor,
        "memory_events": process.memory.events,
        "zone_strain_history": process.memory.zone_strain_history,
        "hysteresis_tension": process.memory.hysteresis_tension,
        "governor": process.governor.telemetry(),
    }
    return hashlib.sha256(canonical_json(state).encode("utf-8")).hexdigest()


def run_encounters(
    process: object,
    packets: Sequence[Sequence[float]],
    mode: str,
    mapping_gates: Sequence[Dict[str, object]],
    atlas: object,
    lineage_id: str,
    release_steps: int,
    relation_permutation: Sequence[int] | None = None,
) -> object:
    """Run ordered temporary calls with equal autonomous withdrawal intervals."""
    if release_steps < 1:
        raise ValueError("release_steps must be positive")
    working = copy.deepcopy(process)
    for encounter_index, packet in enumerate(packets):
        start_digest = state_digest(working)
        transition, audit = apply_one_transition(
            working,
            packet,
            mapping_gates,
            mode,
            relation_permutation=relation_permutation,
        )
        release = [working.step(None) for _ in range(release_steps)]
        record = {
            "schema": "amelia-p326-encounter-v1",
            "lineage_id": lineage_id,
            "encounter_index": encounter_index,
            "mode": mode,
            "start_state_sha256": start_digest,
            "packet": [float(v) for v in packet],
            "graph_field": audit,
            "withdrawal_steps": release_steps,
            "withdrawal_path": [int(x["to_zone"]) for x in release],
            "withdrawal_transitions": [
                {
                    "from_zone": int(x["from_zone"]),
                    "to_zone": int(x["to_zone"]),
                    "selected_gate_id": x["selected_gate_id"],
                    "memory_hysteresis": float(x["memory_hysteresis"]),
                    "memory_bias": [float(v) for v in x["memory_bias"]],
                }
                for x in release
            ],
            "pfm_event_count_after": len(working.memory.events),
            "pfm_state_after": {
                "zone_strain_history": [float(v) for v in working.memory.zone_strain_history],
                "hysteresis_tension": float(working.memory.hysteresis_tension),
                "history_length": len(working.memory.events),
            },
            "end_state_sha256": state_digest(working),
        }
        atlas.append(record)
    return working
