"""P3.26 bounded Numogram graph-field mechanics.

This module is an experiment-side wrapper. It leaves the frozen P3.16 runtime
unchanged and applies a temporary, bounded flux adjustment only around one
ordinary process.step(None) transition.
"""
from __future__ import annotations

import hashlib
import math
from typing import Dict, List, Optional, Sequence, Tuple

FieldMode = str
MODES = {
    "canonical_live",
    "canonical_fixed",
    "degree_rewired",
    "relation_shuffled",
    "no_field",
    "pfm_feedback_muted",
}
FIELD_LAYERS = 3
LAYER_DECAY = 0.5
LOG_FLUX_BUDGET = 0.05


def _normalize(values: Sequence[float], allow_zero: bool = False) -> List[float]:
    if len(values) != 10:
        raise ValueError("P3.26 fields must contain ten zone values")
    centered = [float(v) for v in values]
    mean = sum(centered) / len(centered)
    centered = [v - mean for v in centered]
    norm = math.sqrt(sum(v * v for v in centered))
    if norm <= 1e-12:
        if allow_zero:
            return [0.0] * 10
        raise ValueError("P3.26 input field has zero centered magnitude")
    return [v / norm for v in centered]


def packet_from_randomness(randomness_hex: str, packet_index: int) -> List[float]:
    """Map independent source bytes to an unlabelled, reproducible zone field."""
    if packet_index < 0:
        raise ValueError("packet_index must be nonnegative")
    source = bytes.fromhex(randomness_hex)
    if not source:
        raise ValueError("randomness must not be empty")
    seed = hashlib.sha256(
        b"P3.26-FIELD-v1\0" + source + int(packet_index).to_bytes(8, "big")
    ).digest()
    values: List[float] = []
    counter = 0
    while len(values) < 10:
        block = hashlib.sha256(seed + counter.to_bytes(4, "big")).digest()
        for offset in range(0, len(block), 8):
            word = int.from_bytes(block[offset:offset + 8], "big")
            values.append((word / float(2**64)) * 2.0 - 1.0)
            if len(values) == 10:
                break
        counter += 1
    return _normalize(values)


def _state_edge_weight(
    gate: Dict[str, object],
    zones: Optional[Dict[int, Dict[str, object]]],
    memory_bias: Optional[Sequence[float]],
    deformation: Optional[Sequence[float]],
    state_conditioned: bool,
) -> float:
    source, target = int(gate["source"]), int(gate["target"])
    weight = (
        float(gate["flux"])
        * float(gate["permeability"])
        * (1.0 - float(gate["resistance"]))
    )
    if state_conditioned and zones is not None:
        state_delta = float(zones[target]["activation"]) - float(zones[source]["activation"])
        memory_delta = 0.0
        if memory_bias is not None:
            memory_delta = float(memory_bias[target]) - float(memory_bias[source])
        deformation_delta = 0.0
        if deformation is not None:
            deformation_delta = float(deformation[target]) - float(deformation[source])
        factor = 1.0 + 0.25 * state_delta + 0.10 * memory_delta + 0.05 * deformation_delta
        weight *= max(0.75, min(1.25, factor))
    return max(1e-12, weight)


def propagate_field(
    packet: Sequence[float],
    gates: Sequence[Dict[str, object]],
    zones: Optional[Dict[int, Dict[str, object]]] = None,
    memory_bias: Optional[Sequence[float]] = None,
    deformation: Optional[Sequence[float]] = None,
    state_conditioned: bool = True,
) -> List[float]:
    """Push a centered field over a directed graph for three bounded layers."""
    if not gates:
        raise ValueError("graph field requires at least one gate")
    current = _normalize(packet)
    accumulated = list(current)
    decay = LAYER_DECAY

    for _ in range(FIELD_LAYERS):
        numerators = [0.0] * 10
        denominators = [0.0] * 10
        for gate in gates:
            if not bool(gate["isOpen"]):
                continue
            source, target = int(gate["source"]), int(gate["target"])
            weight = _state_edge_weight(
                gate, zones, memory_bias, deformation, state_conditioned
            )
            numerators[target] += current[source] * weight
            denominators[target] += weight
        pushed = [
            numerators[z] / denominators[z] if denominators[z] else current[z]
            for z in range(10)
        ]
        pushed = _normalize(pushed, allow_zero=True)
        accumulated = [a + decay * b for a, b in zip(accumulated, pushed)]
        current = pushed
        decay *= LAYER_DECAY

    return _normalize(accumulated)


def shuffled_packet(packet: Sequence[float], permutation: Sequence[int]) -> List[float]:
    if sorted(int(v) for v in permutation) != list(range(10)):
        raise ValueError("permutation must contain each zone index exactly once")
    return _normalize([float(packet[int(permutation[i])]) for i in range(10)])


def edge_log_deltas(
    field: Sequence[float],
    candidate_gates: Sequence[Dict[str, object]],
    budget: float = LOG_FLUX_BUDGET,
) -> List[float]:
    """Return an equal-L2-budget signed gradient for candidate directed exits."""
    if budget < 0:
        raise ValueError("budget must be nonnegative")
    gradients = [
        float(field[int(g["target"])]) - float(field[int(g["source"])])
        for g in candidate_gates
    ]
    norm = math.sqrt(sum(v * v for v in gradients))
    if norm <= 1e-12 or budget == 0:
        return [0.0] * len(gradients)
    return [budget * value / norm for value in gradients]


def apply_one_transition(
    process: object,
    packet: Sequence[float],
    mapping_gates: Sequence[Dict[str, object]],
    mode: FieldMode,
    relation_permutation: Optional[Sequence[int]] = None,
    fixed_memory_bias: Optional[Sequence[float]] = None,
) -> Tuple[Dict[str, object], Dict[str, object]]:
    """Apply one graph-field call, restore gate flux, and return transition audit."""
    if mode not in MODES:
        raise ValueError("unknown P3.26 field mode: " + str(mode))
    mem = process.memory.read_memory_bias()
    memory_bias = list(mem.bias_vector)
    if mode == "pfm_feedback_muted":
        process.pfm_feedback = False
    field_packet = _normalize(packet)
    state_conditioned = mode in {"canonical_live", "degree_rewired", "no_field", "pfm_feedback_muted"}
    if mode == "canonical_fixed":
        field_packet = _normalize(packet)
        memory_bias = list(fixed_memory_bias or [0.0] * 10)
        zones = None
        deformation = None
        state_conditioned = False
    else:
        zones = process.zones
        deformation = process.deformation_tensor

    if mode == "relation_shuffled":
        if relation_permutation is None:
            raise ValueError("relation_shuffled requires a sealed permutation")
        field_packet = shuffled_packet(field_packet, relation_permutation)
        state_conditioned = False
        zones = None
        deformation = None

    field = propagate_field(
        field_packet,
        mapping_gates,
        zones=zones,
        memory_bias=memory_bias,
        deformation=deformation,
        state_conditioned=state_conditioned,
    )
    deltas = edge_log_deltas(field, process.gates)
    apply_field = mode != "no_field"
    original_flux = [float(g["flux"]) for g in process.gates]
    before = {
        "current_zone": int(process.current_zone),
        "step_count": int(process.step_count),
        "memory_events": len(process.memory.events),
        "field_sha256": hashlib.sha256(
            ",".join("{:.17g}".format(v) for v in field).encode("ascii")
        ).hexdigest(),
        "requested_log_flux_l2": math.sqrt(sum(v * v for v in deltas)),
        "applied": apply_field,
    }
    try:
        if apply_field:
            for gate, base_flux, delta in zip(process.gates, original_flux, deltas):
                gate["flux"] = base_flux * math.exp(delta)
        transition = process.step(None)
    finally:
        for gate, base_flux in zip(process.gates, original_flux):
            gate["flux"] = base_flux
    after = {
        "current_zone": int(process.current_zone),
        "step_count": int(process.step_count),
        "memory_events": len(process.memory.events),
        "memory_hysteresis": float(process.memory.read_memory_bias().hysteresis_tension),
        "pfm_feedback": bool(process.pfm_feedback),
        "deformation_tensor": [float(v) for v in process.deformation_tensor],
    }
    audit = {
        "mode": mode,
        "before": before,
        "after": after,
        "transition": transition,
        "field": field,
        "edge_log_deltas": deltas,
        "flux_restored": all(
            float(g["flux"]) == base_flux
            for g, base_flux in zip(process.gates, original_flux)
        ),
    }
    return transition, audit
