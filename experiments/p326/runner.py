"""P3.26 sequential encounter runner; only used by the sealed workflow."""
from __future__ import annotations

import copy
import hashlib
import json
from typing import Dict, Iterable, Sequence, Tuple

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
    controller_id: str,
    mapping_gates: Sequence[Dict[str, object]],
    atlas: object,
    lineage_id: str,
    release_steps: int,
    baseline_edges: Iterable[Tuple[int, int]],
    relation_permutation: Sequence[int] | None = None,
) -> object:
    """Run matched sequential calls and autonomous withdrawals on a clone."""
    if release_steps != 24:
        raise ValueError("sealed P3.26 release length is 24")
    working = copy.deepcopy(process)
    baseline = sorted([list(map(int, e)) for e in baseline_edges])
    for encounter_index, packet in enumerate(packets):
        start_digest = state_digest(working)
        memory_before = working.memory.read_memory_bias()
        pre_pfm = {
            "zone_strain_history": [float(v) for v in working.memory.zone_strain_history],
            "hysteresis_tension": float(memory_before.hysteresis_tension),
            "bias_vector": [float(v) for v in memory_before.bias_vector],
            "history_length": len(working.memory.events),
        }
        pre_fast = {
            "current_zone": int(working.current_zone),
            "zone_activation": [float(working.zones[z]["activation"]) for z in range(10)],
            "zone_phase_angle": [float(working.zones[z]["phaseAngle"]) for z in range(10)],
            "deformation_tensor": [float(v) for v in working.deformation_tensor],
        }
        effective_mapping_gates = (
            working.gates
            if mode in {"canonical_live", "no_field", "pfm_feedback_muted", "relation_shuffled"}
            else mapping_gates
        )
        transition, audit = apply_one_transition(
            working,
            packet,
            effective_mapping_gates,
            mode,
            relation_permutation=relation_permutation,
        )
        if not audit["flux_restored"]:
            raise RuntimeError("P3.26 temporary flux was not restored")
        release = [working.step(None) for _ in range(release_steps)]
        governor_values = [
            float(transition["governor"]["antiLockIntegrity"])
        ] + [float(x["governor"]["antiLockIntegrity"]) for x in release]
        if min(governor_values) < 85:
            raise RuntimeError("P3.26 Governor integrity stop threshold reached")
        memory_after = working.memory.read_memory_bias()
        record = {
            "schema": "amelia-p326-encounter-v1",
            "lineage_id": lineage_id,
            "encounter_index": encounter_index,
            "controller_id": controller_id,
            "mode": mode,
            "start_state_sha256": start_digest,
            "development_transition_edges": baseline,
            "packet": [float(v) for v in packet],
            "pre_fast_state": pre_fast,
            "pre_pfm_state": pre_pfm,
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
                    "governor_integrity": float(x["governor"]["antiLockIntegrity"]),
                }
                for x in release
            ],
            "pfm_event_count_after": len(working.memory.events),
            "pfm_state_after": {
                "zone_strain_history": [float(v) for v in working.memory.zone_strain_history],
                "hysteresis_tension": float(memory_after.hysteresis_tension),
                "bias_vector": [float(v) for v in memory_after.bias_vector],
                "history_length": len(working.memory.events),
            },
            "post_fast_state": {
                "current_zone": int(working.current_zone),
                "zone_activation": [float(working.zones[z]["activation"]) for z in range(10)],
                "zone_phase_angle": [float(working.zones[z]["phaseAngle"]) for z in range(10)],
                "deformation_tensor": [float(v) for v in working.deformation_tensor],
            },
            "end_state_sha256": state_digest(working),
        }
        atlas.append(record)
    return working
