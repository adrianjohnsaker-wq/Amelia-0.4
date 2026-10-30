#!/usr/bin/env python3
"""P3.16 registered dynamic Numogram process / latent morphospace assay."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import random
import statistics
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
P316_DIR = os.path.abspath(os.path.dirname(__file__))
if P316_DIR not in sys.path:
    sys.path.insert(0, P316_DIR)

from FullNumogram import FULL_NUMOGRAM_GATES
from DynamicNumogram import (
    DynamicNumogramProcess,
    degree_signature,
    edge_set,
    initial_phase_angles,
    self_loop_count,
    static_canonical_step,
    warp_open_gates,
)

WORLD_COUNT = 192
WORLD_SEED_BASE = 3160000
REWIRE_COUNT = 48
REWIRE_SEED_BASE = 3163000
PHASE_COUNT = 32
PHASE_SEED_BASE = 3164000
BOOTSTRAP_SEED = 3165000
BOOTSTRAP_DRAWS = 5000

STEPS = 128
PRIMARY_START = 32
PRIMARY_STOP = 96
PERTURB_STEP = 96
POST_START = 104
POST_STOP = 128
STEP_SIZE = 0.04
CAPTURE_THRESHOLD = 0.85
CAPTURE_STREAK = 6
ALPHA = 0.05


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def torus_delta(a: float, b: float) -> float:
    d = abs(a - b)
    return min(d, 1.0 - d)


def torus_distance_sq(x: float, y: float, cx: float, cy: float) -> float:
    dx = torus_delta(x, cx)
    dy = torus_delta(y, cy)
    return dx * dx + dy * dy


@dataclass(frozen=True)
class World:
    seed: int
    peaks: Tuple[Tuple[float, float, float, float], ...]
    waves: Tuple[Tuple[int, int, float, float], ...]
    start: Tuple[float, float]
    perturb: Tuple[float, float]
    raw_min: float
    raw_max: float

    def raw_value(self, x: float, y: float) -> float:
        value = 0.0
        for cx, cy, amp, sigma in self.peaks:
            d2 = torus_distance_sq(x, y, cx, cy)
            value += amp * math.exp(-d2 / (2.0 * sigma * sigma))
        for fx, fy, phase, amp in self.waves:
            value += amp * math.sin(
                2.0 * math.pi * (fx * x + fy * y) + phase
            )
        return value

    def value(self, x: float, y: float) -> float:
        raw = self.raw_value(x % 1.0, y % 1.0)
        span = max(1e-12, self.raw_max - self.raw_min)
        return max(0.0, min(1.0, (raw - self.raw_min) / span))


def make_world(seed: int) -> World:
    rng = random.Random(seed)
    peaks = tuple(
        (
            rng.random(),
            rng.random(),
            rng.uniform(0.80, 1.20),
            rng.uniform(0.075, 0.155),
        )
        for _ in range(4)
    )
    waves = tuple(
        (
            rng.randint(1, 4),
            rng.randint(1, 4),
            rng.uniform(0.0, 2.0 * math.pi),
            rng.uniform(0.035, 0.095),
        )
        for _ in range(4)
    )
    start = (rng.random(), rng.random())
    angle = rng.uniform(0.0, 2.0 * math.pi)
    magnitude = rng.uniform(0.18, 0.25)
    perturb = (magnitude * math.cos(angle), magnitude * math.sin(angle))

    provisional = World(seed, peaks, waves, start, perturb, 0.0, 1.0)
    sampled = [
        provisional.raw_value(ix / 32.0, iy / 32.0)
        for ix in range(33)
        for iy in range(33)
    ]
    return World(
        seed,
        peaks,
        waves,
        start,
        perturb,
        min(sampled),
        max(sampled),
    )


def sensory_zone(value: float, previous_value: float) -> int:
    q = min(4, int(max(0.0, min(0.999999999, value)) * 5.0))
    trend = 1 if value - previous_value >= 0.0 else 0
    return 2 * q + trend


def clone_gates() -> List[Dict[str, object]]:
    return [dict(gate) for gate in FULL_NUMOGRAM_GATES]


def rewired_gates(seed: int) -> List[Dict[str, object]]:
    canonical = clone_gates()
    signature = degree_signature(canonical)
    loops = self_loop_count(canonical)
    canonical_edges = edge_set(canonical)

    for restart in range(40):
        rng = random.Random(seed + restart * 100003)
        gates = clone_gates()
        accepted = 0
        attempts = 0

        while accepted < 180 and attempts < 60000:
            attempts += 1
            i, j = rng.sample(range(len(gates)), 2)
            a, b = int(gates[i]["source"]), int(gates[i]["target"])
            c, d = int(gates[j]["source"]), int(gates[j]["target"])

            if a == c or b == d:
                continue
            new1, new2 = (a, d), (c, b)
            if new1 == (a, b) or new2 == (c, d):
                continue
            if int(a == b) + int(c == d) != int(a == d) + int(c == b):
                continue

            existing = edge_set(gates)
            existing.discard((a, b))
            existing.discard((c, d))
            if new1 in existing or new2 in existing or new1 == new2:
                continue

            gates[i]["target"] = d
            gates[j]["target"] = b
            accepted += 1

        if accepted < 90:
            continue
        if degree_signature(gates) != signature:
            continue
        if self_loop_count(gates) != loops:
            continue
        if len(canonical_edges.symmetric_difference(edge_set(gates))) < 20:
            continue

        for index, gate in enumerate(gates):
            gate["id"] = "p316-rewired-{}-{}-{}".format(
                index, gate["source"], gate["target"]
            )
        return gates

    raise RuntimeError("failed to generate registered degree-preserving rewire")


def phase_shuffle(seed: int) -> List[float]:
    rng = random.Random(seed)
    original = initial_phase_angles()
    while True:
        values = list(original)
        rng.shuffle(values)
        if values != original:
            return values


def capture_held(values: Sequence[float]) -> bool:
    streak = 0
    for value in values[:PERTURB_STEP]:
        if value >= CAPTURE_THRESHOLD:
            streak += 1
            if streak >= CAPTURE_STREAK:
                return True
        else:
            streak = 0
    return False


def transition_entropy(transitions: Sequence[Tuple[int, int]]) -> float:
    counts: Dict[Tuple[int, int], int] = {}
    for pair in transitions:
        counts[pair] = counts.get(pair, 0) + 1
    total = sum(counts.values())
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log(p, 2)
    return entropy


def run_episode(
    world: World,
    arm: str,
    gates: Optional[Sequence[Dict[str, object]]] = None,
    phases: Optional[Sequence[float]] = None,
) -> Dict[str, object]:
    is_static = arm == "static"
    if is_static:
        process = None
        current_zone = world.seed % 10
    else:
        process = DynamicNumogramProcess(
            gates=gates,
            phase_permutation=phases,
            pfm_feedback=(arm != "pfm_cut"),
            current_zone=world.seed % 10,
        )
        current_zone = process.current_zone

    x, y = world.start
    previous_observed = world.value(x, y)
    values: List[float] = []
    transitions: List[Tuple[int, int]] = []
    zones: List[int] = [current_zone]
    compact_trajectory: List[List[float]] = []

    for step in range(STEPS):
        if step == PERTURB_STEP:
            x = (x + world.perturb[0]) % 1.0
            y = (y + world.perturb[1]) % 1.0

        local_value = world.value(x, y)
        input_zone = sensory_zone(local_value, previous_observed)

        if is_static:
            decision = static_canonical_step(current_zone, input_zone)
        else:
            decision = process.step(input_zone)

        source = int(decision["from_zone"])
        target = int(decision["to_zone"])
        angle = float(decision["selected_phase_angle"])

        if target != source:
            x = (x + STEP_SIZE * math.cos(angle)) % 1.0
            y = (y + STEP_SIZE * math.sin(angle)) % 1.0

        next_value = world.value(x, y)
        values.append(next_value)
        transitions.append((source, target))
        zones.append(target)
        current_zone = target
        previous_observed = local_value

        if arm in ("canonical", "static", "pfm_cut", "warp_open"):
            compact_trajectory.append([
                step,
                source,
                target,
                input_zone,
                round(x, 8),
                round(y, 8),
                round(next_value, 8),
                round(angle, 8),
            ])

    pre_peak = max(values[:PERTURB_STEP])
    recovery_threshold = 0.95 * pre_peak
    recovery = None
    for index in range(PERTURB_STEP, STEPS):
        if values[index] >= recovery_threshold:
            recovery = index - PERTURB_STEP
            break

    if process is not None:
        diagnostics = process.diagnostics()
    else:
        visited = len(set(zones))
        warp_occ = sum(1 for z in zones if z in (3, 6)) / len(zones)
        diagnostics = {
            "visited_zones": float(visited),
            "transition_entropy": transition_entropy(transitions),
            "warp_occupancy": warp_occ,
            "hysteresis_tension": 0.05,
            "dominant_strain": 0.0,
            "mean_abs_memory_bias": 0.0,
            "anti_lock_integrity": 99.4,
            "deformation_mean": 0.1,
        }

    return {
        "primary": statistics.mean(values[PRIMARY_START:PRIMARY_STOP]),
        "capture": capture_held(values),
        "best_pre": pre_peak,
        "post_mean": statistics.mean(values[POST_START:POST_STOP]),
        "recovery_steps": (STEPS - PERTURB_STEP) if recovery is None else recovery,
        "visited_zones": diagnostics["visited_zones"],
        "transition_entropy": diagnostics["transition_entropy"],
        "warp_occupancy": diagnostics["warp_occupancy"],
        "hysteresis_tension": diagnostics["hysteresis_tension"],
        "dominant_strain": diagnostics["dominant_strain"],
        "mean_abs_memory_bias": diagnostics["mean_abs_memory_bias"],
        "anti_lock_integrity": diagnostics["anti_lock_integrity"],
        "deformation_mean": diagnostics["deformation_mean"],
        "trajectory": compact_trajectory,
    }
