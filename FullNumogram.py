"""Faithful Python port of Amelia—Orange src/core/fullNumogram.ts.

Source:
  repository: adrianjohnsaker-wq/Amelia---Orange
  path: src/core/fullNumogram.ts
  source blob: edf150c38385bc552fb30e2b6721fb832e47976c

The Orange implementation preserves its original 11 Numogram gates exactly and
adds every missing CCRU syzygy, current and digital-cumulation gate at the mean
flux, permeability and resistance of those base gates. The resulting directed
graph contains 29 gates.

This module preserves that construction for Amelia 0.4. It is intentionally
dependency-free so topology experiments can use the same graph without Torch,
language rendering, PFM, or application state.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Dict, List, Tuple

ZONE_COUNT = 10
ZONES: Tuple[int, ...] = tuple(range(10))
TIME_CIRCUIT: Tuple[int, ...] = (1, 2, 4, 5, 7, 8)
WARP: Tuple[int, ...] = (3, 6)
PLEX: Tuple[int, ...] = (0, 9)
OUTER: Tuple[int, ...] = (0, 3, 6, 9)

ORANGE_SOURCE_REPOSITORY = "adrianjohnsaker-wq/Amelia---Orange"
ORANGE_SOURCE_PATH = "src/core/fullNumogram.ts"
ORANGE_SOURCE_BLOB_SHA = "edf150c38385bc552fb30e2b6721fb832e47976c"


def digital_root(c: int) -> int:
    c = int(c)
    return 0 if c == 0 else 1 + ((c - 1) % 9)


def syzygy_of(z: int) -> int:
    return 9 - int(z)


def current_of(z: int) -> int:
    return abs(2 * int(z) - 9)


def gate_of(z: int) -> int:
    z = int(z)
    return digital_root((z * (z + 1)) // 2)


def gate_number(z: int) -> int:
    z = int(z)
    return (z * (z + 1)) // 2


INITIAL_ZONES: Dict[int, Dict[str, object]] = {
    0: {"id": 0, "name": "Zone-0: Pandemonium / Barker Index", "syzygyPair": 9, "current": "Abyss", "activation": 0.12, "conductivity": 0.85, "polarCharge": 0.0, "phaseAngle": 0.0, "deformationStress": 0.05, "chronodemon": "Lur-0 (Murrumur)", "archetypeWeight": 0.82},
    1: {"id": 1, "name": "Zone-1: Plex / Origin Surge", "syzygyPair": 8, "current": "Plex", "activation": 0.65, "conductivity": 0.72, "polarCharge": 0.42, "phaseAngle": 0.628, "deformationStress": 0.14, "chronodemon": "Du-1 (Oddod)", "archetypeWeight": 0.74},
    2: {"id": 2, "name": "Zone-2: Lemur / Cryptic Weft", "syzygyPair": 7, "current": "Lemur", "activation": 0.48, "conductivity": 0.60, "polarCharge": -0.31, "phaseAngle": 1.256, "deformationStress": 0.22, "chronodemon": "Tri-2 (Gharab)", "archetypeWeight": 0.68},
    3: {"id": 3, "name": "Zone-3: Barker / Surge Channel", "syzygyPair": 6, "current": "Barker", "activation": 0.54, "conductivity": 0.78, "polarCharge": 0.55, "phaseAngle": 1.884, "deformationStress": 0.18, "chronodemon": "Kra-3 (Bubastis)", "archetypeWeight": 0.86},
    4: {"id": 4, "name": "Zone-4: Mid-Decad Anchor", "syzygyPair": 5, "current": "Plex", "activation": 0.38, "conductivity": 0.64, "polarCharge": -0.15, "phaseAngle": 2.513, "deformationStress": 0.09, "chronodemon": "Tet-4 (Lurmur)", "archetypeWeight": 0.91},
    5: {"id": 5, "name": "Zone-5: Hyper-Grounded Flux", "syzygyPair": 4, "current": "Lemur", "activation": 0.42, "conductivity": 0.68, "polarCharge": 0.18, "phaseAngle": 3.141, "deformationStress": 0.11, "chronodemon": "Pent-5 (Subtle-Gharab)", "archetypeWeight": 0.77},
    6: {"id": 6, "name": "Zone-6: Barker / Return Spine", "syzygyPair": 3, "current": "Barker", "activation": 0.59, "conductivity": 0.81, "polarCharge": -0.48, "phaseAngle": 3.769, "deformationStress": 0.25, "chronodemon": "Hex-6 (Chrono-Spine)", "archetypeWeight": 0.83},
    7: {"id": 7, "name": "Zone-7: Lemur / Phase Threshold", "syzygyPair": 2, "current": "Lemur", "activation": 0.71, "conductivity": 0.88, "polarCharge": 0.62, "phaseAngle": 4.398, "deformationStress": 0.31, "chronodemon": "Hept-7 (Gate-Master)", "archetypeWeight": 0.88},
    8: {"id": 8, "name": "Zone-8: Plex / Vortex Terminal", "syzygyPair": 1, "current": "Plex", "activation": 0.79, "conductivity": 0.92, "polarCharge": -0.74, "phaseAngle": 5.026, "deformationStress": 0.38, "chronodemon": "Oct-8 (Vortex-Loom)", "archetypeWeight": 0.93},
    9: {"id": 9, "name": "Zone-9: Pandemonium / Terminal Horizon", "syzygyPair": 0, "current": "Abyss", "activation": 0.88, "conductivity": 0.96, "polarCharge": 0.91, "phaseAngle": 5.654, "deformationStress": 0.45, "chronodemon": "Enn-9 (Syzygetic-Apex)", "archetypeWeight": 0.98},
}

ORIGINAL_GATES: List[Dict[str, object]] = [
    {"id": "gate-0-9", "source": 0, "target": 9, "label": "Abyssal Chasm (0::9)", "flux": 0.94, "permeability": 0.91, "isOpen": True, "resistance": 0.08},
    {"id": "gate-1-8", "source": 1, "target": 8, "label": "Murmur Current (1::8)", "flux": 0.82, "permeability": 0.85, "isOpen": True, "resistance": 0.12},
    {"id": "gate-2-7", "source": 2, "target": 7, "label": "Sub-Crypt Bridge (2::7)", "flux": 0.74, "permeability": 0.79, "isOpen": True, "resistance": 0.18},
    {"id": "gate-3-6", "source": 3, "target": 6, "label": "Barker Loop (3::6)", "flux": 0.88, "permeability": 0.86, "isOpen": True, "resistance": 0.11},
    {"id": "gate-4-5", "source": 4, "target": 5, "label": "Centroid Fold (4::5)", "flux": 0.65, "permeability": 0.70, "isOpen": True, "resistance": 0.22},
    {"id": "gate-1-2", "source": 1, "target": 2, "label": "Lemurian Ingress (1->2)", "flux": 0.58, "permeability": 0.75, "isOpen": True, "resistance": 0.25},
    {"id": "gate-2-4", "source": 2, "target": 4, "label": "Mesochron Descent (2->4)", "flux": 0.49, "permeability": 0.68, "isOpen": True, "resistance": 0.29},
    {"id": "gate-4-7", "source": 4, "target": 7, "label": "Barker Ascendance (4->7)", "flux": 0.63, "permeability": 0.77, "isOpen": True, "resistance": 0.21},
    {"id": "gate-7-8", "source": 7, "target": 8, "label": "Crown Egress (7->8)", "flux": 0.85, "permeability": 0.90, "isOpen": True, "resistance": 0.14},
    {"id": "gate-8-9", "source": 8, "target": 9, "label": "Terminal Horizon Incursion (8->9)", "flux": 0.91, "permeability": 0.95, "isOpen": True, "resistance": 0.09},
    {"id": "gate-9-1", "source": 9, "target": 1, "label": "Cyclic Re-entry (9->1)", "flux": 0.87, "permeability": 0.89, "isOpen": True, "resistance": 0.10},
]


def ccru_edges() -> List[Dict[str, object]]:
    edges: Dict[Tuple[int, int], Dict[str, object]] = {}

    def add(source: int, target: int, kind: str, name: str) -> None:
        key = (source, target)
        edge = edges.setdefault(
            key,
            {"source": source, "target": target, "kinds": [], "names": []},
        )
        if kind not in edge["kinds"]:
            edge["kinds"].append(kind)
        edge["names"].append(name)

    for z in ZONES:
        paired = syzygy_of(z)
        lo, hi = min(z, paired), max(z, paired)
        add(z, paired, "syzygy", "Syzygy {}::{}".format(hi, lo))
        add(z, current_of(z), "current", "Current {}::{}->{}".format(hi, lo, current_of(z)))
        add(z, gate_of(z), "gate", "Gt-{}".format(gate_number(z)))

    return [
        deepcopy(edges[key])
        for key in sorted(edges.keys())
    ]


def full_numogram_gates(base: List[Dict[str, object]]) -> List[Dict[str, object]]:
    if not base:
        raise ValueError("base gate list must be non-empty")

    mean_flux = sum(float(g["flux"]) for g in base) / len(base)
    mean_permeability = sum(float(g["permeability"]) for g in base) / len(base)
    mean_resistance = sum(float(g["resistance"]) for g in base) / len(base)
    have = {(int(g["source"]), int(g["target"])) for g in base}

    added: List[Dict[str, object]] = []
    for edge in ccru_edges():
        key = (int(edge["source"]), int(edge["target"]))
        if key in have:
            continue
        added.append({
            "id": "ccru-{}-{}".format(key[0], key[1]),
            "source": key[0],
            "target": key[1],
            "label": "CCRU {} ({}->{})".format(" + ".join(edge["names"]), key[0], key[1]),
            "flux": mean_flux,
            "permeability": mean_permeability,
            "isOpen": True,
            "resistance": mean_resistance,
        })

    return deepcopy(base) + added


def region_of(z: int) -> str:
    z = int(z)
    if z in PLEX:
        return "Plex"
    if z in WARP:
        return "Warp"
    return "Time-Circuit"


DEMON = {0: "Uttunul", 1: "Mur Mur", 2: "Oddubb", 3: "Djynxx", 4: "Katak"}

FULL_NUMOGRAM_GATES: List[Dict[str, object]] = full_numogram_gates(ORIGINAL_GATES)

CCRU_ZONES: Dict[int, Dict[str, object]] = {}
for z in ZONES:
    hi, lo = max(z, syzygy_of(z)), min(z, syzygy_of(z))
    zone = deepcopy(INITIAL_ZONES[z])
    zone["name"] = (
        "Zone-{}: {} · Syzygy {}::{} · Current {}::{} → {} · Gate Gt-{} → {}"
        .format(z, region_of(z), hi, lo, hi, lo, current_of(z), gate_number(z), gate_of(z))
    )
    zone["current"] = region_of(z)
    zone["chronodemon"] = "{} ({}::{})".format(DEMON[lo], hi, lo)
    CCRU_ZONES[z] = zone


def gate_strength(gate: Dict[str, object]) -> float:
    """Selection strength used by Orange's runtime: flux * (1 - resistance)."""
    return float(gate["flux"]) * (1.0 - float(gate["resistance"]))


def transition_matrix_from_gates(
    gates: List[Dict[str, object]] = FULL_NUMOGRAM_GATES,
) -> Tuple[Tuple[float, ...], ...]:
    matrix = [[0.0 for _ in ZONES] for _ in ZONES]
    for gate in gates:
        if not bool(gate["isOpen"]):
            continue
        source, target = int(gate["source"]), int(gate["target"])
        matrix[source][target] = max(matrix[source][target], gate_strength(gate))
    return tuple(tuple(row) for row in matrix)


def topology_mask_from_gates(
    gates: List[Dict[str, object]] = FULL_NUMOGRAM_GATES,
) -> Tuple[Tuple[float, ...], ...]:
    matrix = [[0.0 for _ in ZONES] for _ in ZONES]
    for gate in gates:
        if bool(gate["isOpen"]):
            matrix[int(gate["source"])][int(gate["target"])] = 1.0
    return tuple(tuple(row) for row in matrix)


FULL_NUMOGRAM_TRANSITION_MATRIX = transition_matrix_from_gates()
FULL_NUMOGRAM_TOPOLOGY_MASK = topology_mask_from_gates()


def topology_fingerprint_payload() -> Dict[str, object]:
    return {
        "source_repository": ORANGE_SOURCE_REPOSITORY,
        "source_path": ORANGE_SOURCE_PATH,
        "source_blob_sha": ORANGE_SOURCE_BLOB_SHA,
        "zone_count": ZONE_COUNT,
        "gate_count": len(FULL_NUMOGRAM_GATES),
        "edges": [
            {
                "source": int(g["source"]),
                "target": int(g["target"]),
                "flux": float(g["flux"]),
                "permeability": float(g["permeability"]),
                "resistance": float(g["resistance"]),
            }
            for g in FULL_NUMOGRAM_GATES
        ],
    }


if len(FULL_NUMOGRAM_GATES) != 29:
    raise RuntimeError("Orange full Numogram port must contain exactly 29 gates")
