"""P3.16 Python port of Amelia—Orange's historically evolving Numogram process.

This module reproduces the behavioural equations in the frozen Orange sources
listed in experiments/p316/REGISTRATION.md. It deliberately excludes language
rendering and application persistence. The process state retained between
steps is the experimental object.

Source blobs:
- fullNumogram.ts: edf150c38385bc552fb30e2b6721fb832e47976c
- AmeliaQabbalaInterface.ts: 8ba01f679b570abc53fc06e392e795178ab9ee84
- IntegratedMemorySystem.ts: 0756536dd82fe0a64eadc21c47c67c41a3b72e0b
- TraitEvolution.ts: 5d11159614bab5bb6fc26840c7a232290292587b
- CognitiveGovernor.ts: 57b1387e23c7d36ddfac5a80802ed45fe6dc953e
- ameliaNumogramSubstrateRuntime.ts: 1578f9d7bf479c31f6c4ac4fea955c5377d8d48c
"""
from __future__ import annotations

import copy
import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from FullNumogram import CCRU_ZONES, FULL_NUMOGRAM_GATES

SOURCE_BLOBS = {
    "fullNumogram.ts": "edf150c38385bc552fb30e2b6721fb832e47976c",
    "AmeliaQabbalaInterface.ts": "8ba01f679b570abc53fc06e392e795178ab9ee84",
    "IntegratedMemorySystem.ts": "0756536dd82fe0a64eadc21c47c67c41a3b72e0b",
    "TraitEvolution.ts": "5d11159614bab5bb6fc26840c7a232290292587b",
    "CognitiveGovernor.ts": "57b1387e23c7d36ddfac5a80802ed45fe6dc953e",
    "ameliaNumogramSubstrateRuntime.ts": "1578f9d7bf479c31f6c4ac4fea955c5377d8d48c",
}


@dataclass
class MemoryReadout:
    bias_vector: List[float]
    hysteresis_tension: float
    dominant_deformed_zone: int
    history_length: int
    mean_phase_coherence: float


class IntegratedMemorySystem:
    def __init__(self) -> None:
        self.events: List[Dict[str, object]] = []
        self.zone_strain_history: List[float] = [0.0] * 10
        self.hysteresis_tension: float = 0.05

    def append(self, event: Dict[str, object]) -> None:
        formatted = dict(event)
        formatted["seed"] = int(formatted.get("seed", 0))
        self.events.append(formatted)

        z = int(event["targetZone"])
        relaxation = float(event["strainRelaxation"])
        flux_delta = float(event["fluxDelta"])
        self.zone_strain_history[z] = min(
            1.0,
            self.zone_strain_history[z] * (1.0 - relaxation) + flux_delta * 1.5,
        )

        self.hysteresis_tension = min(
            0.95,
            self.hysteresis_tension * 0.96
            + (1.0 - float(event["phaseCoherence"])) * 0.15
            + flux_delta * 0.10,
        )

    def read_memory_bias(self) -> MemoryReadout:
        bias = [0.0] * 10
        max_strain = -1.0
        dominant = 0
        total_coherence = 0.0

        recent = self.events[-48:]
        for ev in recent:
            z = int(ev["targetZone"])
            bias[z] += float(ev["fluxDelta"]) * float(ev["phaseCoherence"]) * 0.12
            total_coherence += float(ev["phaseCoherence"])

        for i in range(10):
            bias[i] = round(bias[i] + self.zone_strain_history[i] * 0.08, 4)
            if self.zone_strain_history[i] > max_strain:
                max_strain = self.zone_strain_history[i]
                dominant = i

        mean_coherence = total_coherence / len(recent) if recent else 0.95
        return MemoryReadout(
            bias_vector=bias,
            hysteresis_tension=round(self.hysteresis_tension, 4),
            dominant_deformed_zone=dominant,
            history_length=len(self.events),
            mean_phase_coherence=round(mean_coherence, 4),
        )

    def consolidate_strain(self) -> None:
        self.zone_strain_history = [
            round(max(0.0, min(1.0, value * 0.97)), 8)
            for value in self.zone_strain_history
        ]
        self.hysteresis_tension = max(0.02, round(self.hysteresis_tension * 0.82, 8))


class CognitiveGovernor:
    def __init__(self, initial_damping: float = 0.88, initial_advisory: float = 0.72) -> None:
        self.momentum_damping = initial_damping
        self.advisory_weight = initial_advisory
        self.anti_lock_integrity = 99.4
        self.identity_continuity_score = 0.965
        self.scaffold_stage = 3
        self.hard_limit_violations = 0
        self.consolidation_entropy = 0.142
        self.deformation_tension = 0.28
        self.audit_count = 0
        self.is_anti_lock_active = False

    def telemetry(self) -> Dict[str, object]:
        if self.is_anti_lock_active or self.anti_lock_integrity < 85:
            status = "LOCKED_RECOVERY"
        elif self.deformation_tension > 0.65:
            status = "DAMPING"
        elif self.advisory_weight > 0.85:
            status = "REGULATING"
        else:
            status = "NOMINAL"
        return {
            "momentumDampingFactor": round(self.momentum_damping, 3),
            "antiLockIntegrity": round(self.anti_lock_integrity, 2),
            "identityContinuityScore": round(self.identity_continuity_score, 4),
            "scaffoldSheddingStage": self.scaffold_stage,
            "hardLimitViolationCount": self.hard_limit_violations,
            "consolidationEntropy": round(self.consolidation_entropy, 4),
            "deformationFieldTension": round(self.deformation_tension, 4),
            "advisoryWeight": round(self.advisory_weight, 3),
            "governorStatus": status,
            "invariantsAudited": self.audit_count,
            "nonAuthorisingEnforced": True,
        }

    def audit(self, zones: Dict[int, Dict[str, object]], external_tension: float,
              suppress_relay_steering: bool = False) -> Dict[str, object]:
        self.audit_count += 1

        act_variance = 0.0
        for i in range(10):
            act = float(zones[i]["activation"])
            act_variance += (act - 0.5) ** 2
        self.identity_continuity_score = max(
            0.80, min(0.999, 1.0 - (act_variance / 10.0) * 0.35)
        )

        active_zones = sum(1 for z in zones.values() if float(z["activation"]) > 0.12)
        if active_zones <= 2 and not suppress_relay_steering:
            self.is_anti_lock_active = True
            self.anti_lock_integrity = max(60.0, self.anti_lock_integrity - 0.8)
            self.momentum_damping = max(0.45, self.momentum_damping * 0.96)
        else:
            self.is_anti_lock_active = False
            self.anti_lock_integrity = min(100.0, self.anti_lock_integrity + 0.4)

        self.deformation_tension = round(
            self.deformation_tension * 0.85 + external_tension * 0.15, 4
        )

        even_sum = sum(float(zones[z]["activation"]) for z in (0, 2, 4, 6, 8))
        ideal_even_share = even_sum / 5.0
        balance_intersect = sum(
            min(float(zones[z]["activation"]), ideal_even_share)
            for z in (0, 2, 4, 6, 8)
        )
        even_balance = balance_intersect / even_sum if even_sum > 0 else 0.2

        self.consolidation_entropy = round(
            0.08
            + (1.0 - self.identity_continuity_score) * 0.4
            + (1.0 - even_balance) * 0.1,
            4,
        )

        return {
            "telemetry": self.telemetry(),
            "evenZoneBalance": round(even_balance, 4),
            "antiLockTriggered": self.is_anti_lock_active,
            "hardLimitsPassed": self.hard_limit_violations == 0,
        }


def deep_zones() -> Dict[int, Dict[str, object]]:
    return {int(k): copy.deepcopy(v) for k, v in CCRU_ZONES.items()}


def deep_gates(gates: Optional[Sequence[Dict[str, object]]] = None) -> List[Dict[str, object]]:
    source = FULL_NUMOGRAM_GATES if gates is None else gates
    return [copy.deepcopy(g) for g in source]


def evolve_trait_step(
    zones: Dict[int, Dict[str, object]],
    gates: List[Dict[str, object]],
    damping: float,
    advisory: float,
    memory_bias: Sequence[float],
    suppress_relay_steering: bool = False,
) -> Dict[str, object]:
    for gate in gates:
        if bool(gate["isOpen"]):
            src = zones[int(gate["source"])]
            tgt = zones[int(gate["target"])]
            multiplier = 1.4 if suppress_relay_steering else 1.0
            transfer = (
                (float(src["activation"]) - float(tgt["activation"]))
                * float(gate["permeability"])
                * 0.12
                * (1.0 - float(gate["resistance"]))
                * multiplier
            )
            src["activation"] = max(0.04, float(src["activation"]) - transfer * 0.5)
            tgt["activation"] = min(0.98, float(tgt["activation"]) + transfer * 0.5)
            gate["permeability"] = min(
                0.98,
                max(
                    0.2,
                    float(gate["permeability"])
                    + (float(tgt["activation"]) - float(src["activation"])) * 0.01,
                ),
            )

    torque_vector: List[float] = []
    for a, b in ((0, 9), (1, 8), (2, 7), (3, 6), (4, 5)):
        za, zb = zones[a], zones[b]
        torque = math.sin(float(za["phaseAngle"]) - float(zb["phaseAngle"])) * 0.25
        torque_vector.append(round(torque, 4))
        if suppress_relay_steering:
            mean_pair = (float(za["activation"]) + float(zb["activation"])) / 2.0
            za["activation"] = float(za["activation"]) * 0.90 + mean_pair * 0.10 + torque * 0.05
            zb["activation"] = float(zb["activation"]) * 0.90 + mean_pair * 0.10 - torque * 0.05

    even_energy = 0.0
    odd_energy = 0.0
    total_conductivity = 0.0

    for i in range(10):
        z = zones[i]
        paired = zones[int(z["syzygyPair"])]
        freq = 0.12 + (i * 0.035) * (1.0 + float(z["conductivity"]) * 0.2)
        z["phaseAngle"] = (float(z["phaseAngle"]) + freq) % (2.0 * math.pi)
        mem_bias = float(memory_bias[i]) if i < len(memory_bias) else 0.0

        base_target = (
            0.30
            + 0.35 * math.sin(float(z["phaseAngle"]))
            + float(paired["activation"]) * 0.35
        )
        if suppress_relay_steering:
            base_target = (
                base_target * 0.6
                + 0.4 * (0.20 + 0.15 * math.cos(float(z["phaseAngle"]) + i))
            )

        target_act = base_target * advisory + mem_bias
        delta = (target_act - float(z["activation"])) * (1.0 - damping * 0.40)

        z["activation"] = max(
            0.04,
            min(0.98, float(z["activation"]) + delta + mem_bias * 0.12),
        )
        z["conductivity"] = min(
            0.99,
            max(0.1, float(z["conductivity"]) + (float(z["activation"]) - 0.5) * 0.02),
        )
        z["deformationStress"] = min(
            1.0,
            abs(float(z["activation"]) - float(paired["activation"])) * 0.80
            + abs(mem_bias) * 0.4,
        )
        z["polarCharge"] = round(
            math.cos(float(z["phaseAngle"])) * float(z["activation"]), 3
        )

        if i % 2 == 0:
            even_energy += float(z["activation"])
        else:
            odd_energy += float(z["activation"])
        total_conductivity += float(z["conductivity"])

    return {
        "meanConductivity": round(total_conductivity / 10.0, 4),
        "syzygeticTorqueVector": torque_vector,
        "evenPoleEnergy": round(even_energy, 4),
        "oddCurrentEnergy": round(odd_energy, 4),
        "centroidFoldActivation": round(
            (float(zones[4]["activation"]) + float(zones[5]["activation"])) / 2.0, 4
        ),
        "subCryptActivation": round(
            (float(zones[2]["activation"]) + float(zones[7]["activation"])) / 2.0, 4
        ),
        "barkerLoopActivation": round(
            (float(zones[3]["activation"]) + float(zones[6]["activation"])) / 2.0, 4
        ),
    }


class DynamicNumogramProcess:
    """Behavioural port of AmeliaNumogramSubstrateRuntime with full Numogram installed."""

    def __init__(
        self,
        gates: Optional[Sequence[Dict[str, object]]] = None,
        phase_permutation: Optional[Sequence[float]] = None,
        pfm_feedback: bool = True,
        current_zone: int = 0,
    ) -> None:
        self.zones = deep_zones()
        self.gates = deep_gates(gates)
        if phase_permutation is not None:
            if len(phase_permutation) != 10:
                raise ValueError("phase_permutation must contain 10 angles")
            for i in range(10):
                self.zones[i]["phaseAngle"] = float(phase_permutation[i])

        self.memory = IntegratedMemorySystem()
        self.governor = CognitiveGovernor(0.88, 0.72)
        self.step_count = 0
        self.current_zone = int(current_zone)
        self.deformation_tensor = [0.1] * 10
        self.pfm_feedback = bool(pfm_feedback)
        self.zone_visit_counts = [0] * 10
        self.zone_visit_counts[self.current_zone] = 1
        self.transition_counts = [[0] * 10 for _ in range(10)]
        self.last_trait_snapshot: Optional[Dict[str, object]] = None
        self.last_audit: Optional[Dict[str, object]] = None

    def step(self, input_zone: Optional[int]) -> Dict[str, object]:
        self.step_count += 1
        gov_before = self.governor.telemetry()
        mem_readout = self.memory.read_memory_bias()
        effective_bias = (
            list(mem_readout.bias_vector)
            if self.pfm_feedback
            else [0.0] * 10
        )

        self.last_trait_snapshot = evolve_trait_step(
            self.zones,
            self.gates,
            float(gov_before["momentumDampingFactor"]),
            float(gov_before["advisoryWeight"]),
            effective_bias,
            False,
        )

        self.last_audit = self.governor.audit(
            self.zones,
            mem_readout.hysteresis_tension,
            False,
        )

        source = self.current_zone
        options = [
            gate for gate in self.gates
            if bool(gate["isOpen"]) and int(gate["source"]) == source
        ]

        target = source
        best = -float("inf")
        best_gate: Optional[Dict[str, object]] = None
        for gate in options:
            candidate = int(gate["target"])
            z = self.zones[candidate]
            score = (
                float(gate["flux"]) * (1.0 - float(gate["resistance"]))
                + effective_bias[candidate] * 0.4
                + float(z["activation"]) * 0.2
                + math.cos(float(z["phaseAngle"])) * 0.1
                + (0.35 if input_zone is not None and candidate == int(input_zone) else 0.0)
            )
            if score > best:
                best = score
                target = candidate
                best_gate = gate

        target_zone = self.zones[target]
        source_zone = self.zones[source]
        flux_delta = round(
            max(
                0.005,
                min(
                    0.18,
                    abs(
                        float(target_zone["activation"])
                        - float(source_zone["activation"])
                    )
                    * 0.12
                    + 0.025,
                ),
            ),
            6,
        )
        phase_coherence = round(
            max(
                0.05,
                min(
                    1.0,
                    (
                        1.0
                        + math.cos(
                            float(target_zone["phaseAngle"])
                            - float(source_zone["phaseAngle"])
                        )
                    )
                    / 2.0,
                ),
            ),
            6,
        )

        self.memory.append({
            "blockIndex": self.step_count,
            "depth": self.step_count,
            "targetZone": target,
            "fluxDelta": flux_delta,
            "phaseCoherence": phase_coherence,
            "strainRelaxation": 0.025,
            "eventDigest": "p316:{}:{}:{}:{}".format(
                self.step_count, source, target, input_zone
            ),
            "timestamp": self.step_count,
            "kind": "STEP",
            "fromZone": source,
            "inputZone": input_zone,
        })

        self.current_zone = target
        self.zone_visit_counts[target] += 1
        self.transition_counts[source][target] += 1

        for i in range(10):
            z = self.zones[i]
            self.deformation_tensor[i] = (
                self.deformation_tensor[i] * 0.95
                + (float(z["deformationStress"]) + effective_bias[i]) * 0.05
            )

        return {
            "from_zone": source,
            "to_zone": target,
            "selected_gate_id": None if best_gate is None else str(best_gate["id"]),
            "selected_phase_angle": float(self.zones[target]["phaseAngle"]),
            "flux_delta": flux_delta,
            "phase_coherence": phase_coherence,
            "memory_bias": effective_bias,
            "memory_hysteresis": mem_readout.hysteresis_tension,
            "dominant_deformed_zone": mem_readout.dominant_deformed_zone,
            "governor": self.last_audit["telemetry"],
            "trait": self.last_trait_snapshot,
        }

    def diagnostics(self) -> Dict[str, float]:
        visits = sum(self.zone_visit_counts)
        visited_zones = sum(1 for count in self.zone_visit_counts if count > 0)
        warp_visits = self.zone_visit_counts[3] + self.zone_visit_counts[6]
        warp_occupancy = warp_visits / visits if visits else 0.0

        total_transitions = sum(sum(row) for row in self.transition_counts)
        entropy = 0.0
        if total_transitions:
            for row in self.transition_counts:
                for count in row:
                    if count:
                        p = count / total_transitions
                        entropy -= p * math.log(p, 2)

        mem = self.memory.read_memory_bias()
        mean_abs_bias = sum(abs(v) for v in mem.bias_vector) / 10.0
        dominant_strain = max(self.memory.zone_strain_history) if self.memory.zone_strain_history else 0.0

        return {
            "visited_zones": float(visited_zones),
            "transition_entropy": entropy,
            "warp_occupancy": warp_occupancy,
            "hysteresis_tension": mem.hysteresis_tension,
            "dominant_strain": dominant_strain,
            "mean_abs_memory_bias": mean_abs_bias,
            "anti_lock_integrity": float(self.governor.telemetry()["antiLockIntegrity"]),
            "deformation_mean": sum(self.deformation_tensor) / 10.0,
        }


def static_canonical_step(current_zone: int, input_zone: Optional[int]) -> Dict[str, object]:
    """One Orange process step from a fresh state; history is discarded afterwards."""
    process = DynamicNumogramProcess(current_zone=current_zone, pfm_feedback=True)
    return process.step(input_zone)


def initial_phase_angles() -> List[float]:
    return [float(CCRU_ZONES[i]["phaseAngle"]) for i in range(10)]


def warp_open_gates() -> List[Dict[str, object]]:
    """Break Warp terminality by target-swapping 3->6 and 4->1.

    This preserves every source out-degree, every target in-degree, total edge count,
    self-loop count and source-slot gate weights.
    """
    gates = deep_gates()
    idx_36 = next(
        i for i, gate in enumerate(gates)
        if int(gate["source"]) == 3 and int(gate["target"]) == 6
    )
    idx_41 = next(
        i for i, gate in enumerate(gates)
        if int(gate["source"]) == 4 and int(gate["target"]) == 1
    )
    gates[idx_36]["target"] = 1
    gates[idx_41]["target"] = 6
    gates[idx_36]["id"] = str(gates[idx_36]["id"]) + "-warp-open"
    gates[idx_41]["id"] = str(gates[idx_41]["id"]) + "-warp-open"
    return gates


def edge_set(gates: Sequence[Dict[str, object]]) -> set:
    return {
        (int(gate["source"]), int(gate["target"]))
        for gate in gates
        if bool(gate["isOpen"])
    }


def degree_signature(gates: Sequence[Dict[str, object]]) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
    out_degree = [0] * 10
    in_degree = [0] * 10
    for gate in gates:
        out_degree[int(gate["source"])] += 1
        in_degree[int(gate["target"])] += 1
    return tuple(out_degree), tuple(in_degree)


def self_loop_count(gates: Sequence[Dict[str, object]]) -> int:
    return sum(
        1
        for gate in gates
        if int(gate["source"]) == int(gate["target"])
    )


def validate_core_invariants() -> None:
    if len(FULL_NUMOGRAM_GATES) != 29:
        raise AssertionError("full Numogram must have 29 directed gates")
    if self_loop_count(FULL_NUMOGRAM_GATES) != 4:
        raise AssertionError("full Numogram must retain four dwell edges")

    warp = warp_open_gates()
    if len(warp) != len(FULL_NUMOGRAM_GATES):
        raise AssertionError("WARP_OPEN must preserve edge count")
    if degree_signature(warp) != degree_signature(FULL_NUMOGRAM_GATES):
        raise AssertionError("WARP_OPEN must preserve in/out degree")
    if self_loop_count(warp) != self_loop_count(FULL_NUMOGRAM_GATES):
        raise AssertionError("WARP_OPEN must preserve self-loop count")
    if (3, 1) not in edge_set(warp) or (4, 6) not in edge_set(warp):
        raise AssertionError("WARP_OPEN target swap missing")


validate_core_invariants()
