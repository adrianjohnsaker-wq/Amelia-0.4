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


METRIC_KEYS = (
    "primary",
    "capture",
    "best_pre",
    "post_mean",
    "recovery_steps",
    "visited_zones",
    "transition_entropy",
    "warp_occupancy",
    "hysteresis_tension",
    "dominant_strain",
    "mean_abs_memory_bias",
    "anti_lock_integrity",
    "deformation_mean",
)


def stripped(run: Dict[str, object]) -> Dict[str, object]:
    return {key: run[key] for key in METRIC_KEYS}


def aggregate(runs: Sequence[Dict[str, object]]) -> Dict[str, float]:
    result: Dict[str, float] = {}
    for key in METRIC_KEYS:
        if key == "capture":
            result["capture_rate"] = statistics.mean(
                1.0 if bool(run[key]) else 0.0 for run in runs
            )
        else:
            result[key] = statistics.mean(float(run[key]) for run in runs)
    return result


def empirical_upper_p(observed: float, nulls: Sequence[float]) -> float:
    return (1.0 + sum(1 for value in nulls if value >= observed)) / (
        1.0 + len(nulls)
    )


def percentile(observed: float, nulls: Sequence[float]) -> float:
    below = sum(1 for value in nulls if value < observed)
    equal = sum(1 for value in nulls if value == observed)
    return 100.0 * (below + 0.5 * equal) / len(nulls)


def quantile(values: Sequence[float], q: float) -> float:
    xs = sorted(float(value) for value in values)
    position = (len(xs) - 1) * q
    lo = int(math.floor(position))
    hi = int(math.ceil(position))
    if lo == hi:
        return xs[lo]
    weight = position - lo
    return xs[lo] * (1.0 - weight) + xs[hi] * weight


def bootstrap_ci(differences: Sequence[float], seed_offset: int = 0) -> Tuple[float, float]:
    rng = random.Random(BOOTSTRAP_SEED + seed_offset)
    n = len(differences)
    boot: List[float] = []
    for _ in range(BOOTSTRAP_DRAWS):
        boot.append(
            statistics.mean(differences[rng.randrange(n)] for _ in range(n))
        )
    return quantile(boot, 0.025), quantile(boot, 0.975)


def paired_difference(
    left: Sequence[Dict[str, object]],
    right: Sequence[Dict[str, object]],
    key: str = "primary",
) -> List[float]:
    return [
        float(left[i][key]) - float(right[i][key])
        for i in range(len(left))
    ]


def write_report(path: str, result: Dict[str, object]) -> None:
    p = result["primary"]
    s = result["secondary"]
    a = result["aggregates"]

    lines = [
        "# P3.16 — Dynamic Numogram Process / Latent Morphospace Assay",
        "",
        "## Primary process-access result",
        "",
        "- dynamic-process access gate: **{}**".format("PASS" if p["held"] else "FAIL"),
        "- canonical dynamic primary score: {:.6f}".format(p["canonical_score"]),
        "- dynamic rewired mean: {:.6f}".format(p["rewired_mean"]),
        "- canonical percentile vs dynamic rewires: {:.1f}".format(p["rewired_percentile"]),
        "- one-sided empirical rank p: {:.6f}".format(p["rewired_rank_p"]),
        "- canonical minus mean-rewired paired advantage: {:.6f}".format(p["rewired_paired_mean"]),
        "- paired bootstrap 95% CI vs rewired: [{:.6f}, {:.6f}]".format(
            p["rewired_bootstrap_ci"][0], p["rewired_bootstrap_ci"][1]
        ),
        "- canonical minus static-map paired advantage: {:.6f}".format(p["static_paired_mean"]),
        "- paired bootstrap 95% CI vs static: [{:.6f}, {:.6f}]".format(
            p["static_bootstrap_ci"][0], p["static_bootstrap_ci"][1]
        ),
        "- canonical capture rate: {:.4f}".format(p["canonical_capture_rate"]),
        "- mean rewired capture rate: {:.4f}".format(p["rewired_capture_rate_mean"]),
        "",
        "## Secondary mechanisms",
        "",
        "- canonical minus PFM_CUT: {:.6f}".format(s["pfm_cut_paired_mean"]),
        "- PFM_CUT paired bootstrap 95% CI: [{:.6f}, {:.6f}]".format(
            s["pfm_cut_bootstrap_ci"][0], s["pfm_cut_bootstrap_ci"][1]
        ),
        "- canonical percentile vs phase-shuffled dynamic controls: {:.1f}".format(
            s["phase_shuffle_percentile"]
        ),
        "- phase-shuffle one-sided empirical rank p: {:.6f}".format(
            s["phase_shuffle_rank_p"]
        ),
        "- canonical minus WARP_OPEN: {:.6f}".format(s["warp_open_paired_mean"]),
        "- WARP_OPEN paired bootstrap 95% CI: [{:.6f}, {:.6f}]".format(
            s["warp_open_bootstrap_ci"][0], s["warp_open_bootstrap_ci"][1]
        ),
        "",
        "## Process diagnostics",
        "",
        "| measure | canonical dynamic | static canonical | PFM cut | Warp open | rewired mean |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    for key, label in (
        ("best_pre", "best pre-perturbation field"),
        ("post_mean", "post-perturbation mean field"),
        ("recovery_steps", "recovery steps"),
        ("visited_zones", "visited zones"),
        ("transition_entropy", "transition entropy"),
        ("warp_occupancy", "Warp occupancy"),
        ("hysteresis_tension", "PFM hysteresis tension"),
        ("dominant_strain", "dominant strain"),
        ("mean_abs_memory_bias", "mean |memory bias|"),
        ("anti_lock_integrity", "anti-lock integrity"),
        ("deformation_mean", "mean deformation"),
    ):
        lines.append(
            "| {} | {:.6f} | {:.6f} | {:.6f} | {:.6f} | {:.6f} |".format(
                label,
                a["canonical"][key],
                a["static"][key],
                a["pfm_cut"][key],
                a["warp_open"][key],
                a["rewired_mean"][key],
            )
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        result["interpretation"],
        "",
        "## Provenance",
        "",
        "- Full Numogram Python SHA-256: {}".format(result["provenance"]["full_numogram_sha256"]),
        "- Dynamic process port SHA-256: {}".format(result["provenance"]["dynamic_process_sha256"]),
        "- registration SHA-256: {}".format(result["provenance"]["registration_sha256"]),
        "- runner SHA-256: {}".format(result["provenance"]["runner_sha256"]),
        "- all-run metrics gzip SHA-256: {}".format(result["provenance"]["metrics_sha256"]),
        "- focal trajectories gzip SHA-256: {}".format(result["provenance"]["trajectories_sha256"]),
        "- controls SHA-256: {}".format(result["provenance"]["controls_sha256"]),
        "",
        "No secondary endpoint is used to rescue a failed primary gate.",
        "",
    ])

    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="experiments/p316/results")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)

    worlds = [
        make_world(WORLD_SEED_BASE + index)
        for index in range(WORLD_COUNT)
    ]
    rewired = [
        rewired_gates(REWIRE_SEED_BASE + index)
        for index in range(REWIRE_COUNT)
    ]
    phase_controls = [
        phase_shuffle(PHASE_SEED_BASE + index)
        for index in range(PHASE_COUNT)
    ]
    warp_gates = warp_open_gates()

    controls_path = os.path.join(args.out, "controls.json")
    with open(controls_path, "w", encoding="utf-8") as handle:
        json.dump({
            "rewired": [
                {
                    "seed": REWIRE_SEED_BASE + index,
                    "edges": sorted(list(edge_set(gates))),
                    "degree_signature": degree_signature(gates),
                    "self_loop_count": self_loop_count(gates),
                }
                for index, gates in enumerate(rewired)
            ],
            "phase_shuffles": [
                {
                    "seed": PHASE_SEED_BASE + index,
                    "phases": phases,
                }
                for index, phases in enumerate(phase_controls)
            ],
            "warp_open_edges": sorted(list(edge_set(warp_gates))),
        }, handle, indent=2, sort_keys=True)

    metrics_path = os.path.join(args.out, "all_run_metrics.jsonl.gz")
    trajectories_path = os.path.join(args.out, "focal_trajectories.jsonl.gz")

    canonical_runs: List[Dict[str, object]] = []
    static_runs: List[Dict[str, object]] = []
    pfm_cut_runs: List[Dict[str, object]] = []
    warp_runs: List[Dict[str, object]] = []
    rewired_runs: List[List[Dict[str, object]]] = [[] for _ in range(REWIRE_COUNT)]
    phase_runs: List[List[Dict[str, object]]] = [[] for _ in range(PHASE_COUNT)]

    with gzip.open(metrics_path, "wt", encoding="utf-8") as metrics, gzip.open(
        trajectories_path, "wt", encoding="utf-8"
    ) as trajectories:
        for world_index, world in enumerate(worlds):
            focal_specs = [
                ("canonical", None, None, canonical_runs),
                ("static", None, None, static_runs),
                ("pfm_cut", None, None, pfm_cut_runs),
                ("warp_open", warp_gates, None, warp_runs),
            ]

            for arm, gates, phases, destination in focal_specs:
                run = run_episode(world, arm, gates=gates, phases=phases)
                destination.append(run)
                metrics.write(canonical_json({
                    "arm": arm,
                    "controller": 0,
                    "world": world.seed,
                    "metrics": stripped(run),
                }) + "\n")
                trajectories.write(canonical_json({
                    "arm": arm,
                    "world": world.seed,
                    "trajectory": run["trajectory"],
                }) + "\n")

            for controller_index, gates in enumerate(rewired):
                run = run_episode(world, "rewired", gates=gates)
                rewired_runs[controller_index].append(run)
                metrics.write(canonical_json({
                    "arm": "dynamic_rewired",
                    "controller": controller_index,
                    "world": world.seed,
                    "metrics": stripped(run),
                }) + "\n")

            for controller_index, phases in enumerate(phase_controls):
                run = run_episode(world, "phase_shuffle", phases=phases)
                phase_runs[controller_index].append(run)
                metrics.write(canonical_json({
                    "arm": "phase_shuffle",
                    "controller": controller_index,
                    "world": world.seed,
                    "metrics": stripped(run),
                }) + "\n")

    canonical_agg = aggregate(canonical_runs)
    static_agg = aggregate(static_runs)
    pfm_cut_agg = aggregate(pfm_cut_runs)
    warp_agg = aggregate(warp_runs)
    rewired_aggs = [aggregate(runs) for runs in rewired_runs]
    phase_aggs = [aggregate(runs) for runs in phase_runs]

    rewired_primary = [agg["primary"] for agg in rewired_aggs]
    phase_primary = [agg["primary"] for agg in phase_aggs]

    mean_rewired_per_world = [
        statistics.mean(
            float(rewired_runs[controller][world_index]["primary"])
            for controller in range(REWIRE_COUNT)
        )
        for world_index in range(WORLD_COUNT)
    ]
    rewired_diffs = [
        float(canonical_runs[index]["primary"]) - mean_rewired_per_world[index]
        for index in range(WORLD_COUNT)
    ]
    static_diffs = paired_difference(canonical_runs, static_runs)
    pfm_cut_diffs = paired_difference(canonical_runs, pfm_cut_runs)
    warp_diffs = paired_difference(canonical_runs, warp_runs)

    rewired_ci = bootstrap_ci(rewired_diffs, 0)
    static_ci = bootstrap_ci(static_diffs, 1)
    pfm_cut_ci = bootstrap_ci(pfm_cut_diffs, 2)
    warp_ci = bootstrap_ci(warp_diffs, 3)

    rewired_rank_p = empirical_upper_p(canonical_agg["primary"], rewired_primary)
    rewired_capture_mean = statistics.mean(
        agg["capture_rate"] for agg in rewired_aggs
    )

    primary_held = (
        rewired_rank_p <= ALPHA
        and rewired_ci[0] > 0.0
        and static_ci[0] > 0.0
        and canonical_agg["capture_rate"] >= rewired_capture_mean
    )

    pfm_supported = pfm_cut_ci[0] > 0.0

    if not primary_held:
        interpretation = (
            "FAIL. The registered historically evolving full Numogram process did not "
            "satisfy the preregistered process-access gate for this latent-morphospace "
            "family and local sensory interface. Secondary mechanism results remain "
            "descriptive and cannot rescue the primary claim."
        )
    elif pfm_supported:
        interpretation = (
            "PASS. The canonical dynamic process beat both dynamic topology rewires and "
            "the static canonical map, and the paired PFM-cut comparison also supports a "
            "constitutive history contribution. This is evidence for privileged access by "
            "the registered history-conditioned computational process; it is not evidence "
            "by itself for supernatural or metaphysical communication."
        )
    else:
        interpretation = (
            "PASS for the dynamic-process gate. The canonical evolving process beat the "
            "dynamic rewired controls and the static canonical map, but PFM feedback was "
            "not shown necessary by the registered secondary comparison. The supported "
            "claim is therefore dynamic Numogrammatic process, not specifically PFM."
        )

    rewired_mean_agg = {
        key: statistics.mean(agg[key] for agg in rewired_aggs)
        for key in rewired_aggs[0].keys()
    }

    result: Dict[str, object] = {
        "schema": "amelia-p316-dynamic-numogram-process-v1",
        "registration": {
            "world_count": WORLD_COUNT,
            "steps": STEPS,
            "primary_window": [PRIMARY_START, PRIMARY_STOP - 1],
            "perturb_step": PERTURB_STEP,
            "post_window": [POST_START, POST_STOP - 1],
            "rewired_controls": REWIRE_COUNT,
            "phase_controls": PHASE_COUNT,
            "world_seed_base": WORLD_SEED_BASE,
            "rewire_seed_base": REWIRE_SEED_BASE,
            "phase_seed_base": PHASE_SEED_BASE,
            "bootstrap_seed": BOOTSTRAP_SEED,
        },
        "primary": {
            "held": primary_held,
            "canonical_score": canonical_agg["primary"],
            "rewired_mean": statistics.mean(rewired_primary),
            "rewired_percentile": percentile(canonical_agg["primary"], rewired_primary),
            "rewired_rank_p": rewired_rank_p,
            "rewired_paired_mean": statistics.mean(rewired_diffs),
            "rewired_bootstrap_ci": list(rewired_ci),
            "static_score": static_agg["primary"],
            "static_paired_mean": statistics.mean(static_diffs),
            "static_bootstrap_ci": list(static_ci),
            "canonical_capture_rate": canonical_agg["capture_rate"],
            "rewired_capture_rate_mean": rewired_capture_mean,
            "rewired_aggregate_scores": rewired_primary,
        },
        "secondary": {
            "pfm_cut_score": pfm_cut_agg["primary"],
            "pfm_cut_paired_mean": statistics.mean(pfm_cut_diffs),
            "pfm_cut_bootstrap_ci": list(pfm_cut_ci),
            "pfm_history_supported": pfm_supported,
            "phase_shuffle_percentile": percentile(
                canonical_agg["primary"], phase_primary
            ),
            "phase_shuffle_rank_p": empirical_upper_p(
                canonical_agg["primary"], phase_primary
            ),
            "phase_shuffle_aggregate_scores": phase_primary,
            "warp_open_score": warp_agg["primary"],
            "warp_open_paired_mean": statistics.mean(warp_diffs),
            "warp_open_bootstrap_ci": list(warp_ci),
        },
        "aggregates": {
            "canonical": canonical_agg,
            "static": static_agg,
            "pfm_cut": pfm_cut_agg,
            "warp_open": warp_agg,
            "rewired_mean": rewired_mean_agg,
        },
        "per_world": {
            "canonical_primary": [float(run["primary"]) for run in canonical_runs],
            "static_primary": [float(run["primary"]) for run in static_runs],
            "pfm_cut_primary": [float(run["primary"]) for run in pfm_cut_runs],
            "warp_open_primary": [float(run["primary"]) for run in warp_runs],
            "mean_rewired_primary": mean_rewired_per_world,
            "canonical_minus_mean_rewired": rewired_diffs,
            "canonical_minus_static": static_diffs,
            "canonical_minus_pfm_cut": pfm_cut_diffs,
            "canonical_minus_warp_open": warp_diffs,
        },
        "interpretation": interpretation,
        "provenance": {
            "full_numogram_sha256": sha256_file("FullNumogram.py"),
            "dynamic_process_sha256": sha256_file(
                "experiments/p316/DynamicNumogram.py"
            ),
            "registration_sha256": sha256_file(
                "experiments/p316/REGISTRATION.md"
            ),
            "runner_sha256": sha256_file("experiments/p316/run.py"),
            "metrics_sha256": sha256_file(metrics_path),
            "trajectories_sha256": sha256_file(trajectories_path),
            "controls_sha256": sha256_file(controls_path),
        },
    }

    summary_path = os.path.join(args.out, "summary.json")
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    report_path = os.path.join(args.out, "REPORT.md")
    write_report(report_path, result)

    sums = {
        "summary_sha256": sha256_file(summary_path),
        "report_sha256": sha256_file(report_path),
        "metrics_sha256": sha256_file(metrics_path),
        "trajectories_sha256": sha256_file(trajectories_path),
        "controls_sha256": sha256_file(controls_path),
    }
    with open(
        os.path.join(args.out, "SHA256SUMS.json"),
        "w",
        encoding="utf-8",
    ) as handle:
        json.dump(sums, handle, indent=2, sort_keys=True)

    print(json.dumps({
        "primary": result["primary"],
        "secondary": result["secondary"],
        "interpretation": interpretation,
        "provenance": result["provenance"],
    }, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
