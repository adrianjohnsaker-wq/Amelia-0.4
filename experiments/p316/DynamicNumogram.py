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
