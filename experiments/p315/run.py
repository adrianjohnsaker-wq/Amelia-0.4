#!/usr/bin/env python3
"""P3.15 — Full Numogram Latent Morphospace Access Assay."""
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
from typing import Dict, List, Sequence, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from FullNumogram import CCRU_ZONES, FULL_NUMOGRAM_GATES, ORANGE_SOURCE_BLOB_SHA, gate_strength

WORLD_COUNT = 192
WORLD_SEED_BASE = 3150000
REWIRE_COUNT = 64
REWIRE_SEED_BASE = 3153000
LABEL_COUNT = 64
LABEL_SEED_BASE = 3154000
BOOTSTRAP_SEED = 3155000
BOOTSTRAP_DRAWS = 5000
STEPS = 90
PRIMARY_START = 15
PRIMARY_STOP = 55
PERTURB_STEP = 55
STEP_SIZE = 0.045
CAPTURE_THRESHOLD = 0.85
CAPTURE_STREAK = 5
LOCAL_GAIN_WEIGHT = 5.0
GATE_WEIGHT = 0.08
MOMENTUM_WEIGHT = 0.04
ALPHA = 0.05


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def torus_delta(a, b):
    d = abs(a - b)
    return min(d, 1.0 - d)


def torus_distance_sq(x, y, cx, cy):
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

    def raw_value(self, x, y):
        value = 0.0
        for cx, cy, amp, sigma in self.peaks:
            d2 = torus_distance_sq(x, y, cx, cy)
            value += amp * math.exp(-d2 / (2.0 * sigma * sigma))
        for fx, fy, phase, amp in self.waves:
            value += amp * math.sin(2.0 * math.pi * (fx * x + fy * y) + phase)
        return value

    def value(self, x, y):
        raw = self.raw_value(x % 1.0, y % 1.0)
        span = max(1e-12, self.raw_max - self.raw_min)
        return max(0.0, min(1.0, (raw - self.raw_min) / span))


def make_world(seed):
    rng = random.Random(seed)
    peaks = tuple((rng.random(), rng.random(), rng.uniform(0.80, 1.20), rng.uniform(0.075, 0.155)) for _ in range(4))
    waves = tuple((rng.randint(1, 4), rng.randint(1, 4), rng.uniform(0.0, 2.0 * math.pi), rng.uniform(0.035, 0.095)) for _ in range(4))
    start = (rng.random(), rng.random())
    angle = rng.uniform(0.0, 2.0 * math.pi)
    magnitude = rng.uniform(0.18, 0.25)
    perturb = (magnitude * math.cos(angle), magnitude * math.sin(angle))
    provisional = World(seed, peaks, waves, start, perturb, 0.0, 1.0)
    sampled = [provisional.raw_value(ix / 32.0, iy / 32.0) for ix in range(33) for iy in range(33)]
    return World(seed, peaks, waves, start, perturb, min(sampled), max(sampled))


def clone_gates():
    return [dict(gate) for gate in FULL_NUMOGRAM_GATES]


def edge_set(gates):
    return {(int(g["source"]), int(g["target"])) for g in gates if bool(g["isOpen"])}


def strongly_connected(gates):
    edges = edge_set(gates)
    adj = {z: [] for z in range(10)}
    rev = {z: [] for z in range(10)}
    for s, t in edges:
        adj[s].append(t)
        rev[t].append(s)

    def visit(graph, start):
        seen = {start}
        stack = [start]
        while stack:
            node = stack.pop()
            for nxt in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return seen

    return len(visit(adj, 0)) == 10 and len(visit(rev, 0)) == 10


def self_loop_count(gates):
    return sum(1 for g in gates if int(g["source"]) == int(g["target"]))


def degree_signature(gates):
    out_degree = [0] * 10
    in_degree = [0] * 10
    for g in gates:
        out_degree[int(g["source"])] += 1
        in_degree[int(g["target"])] += 1
    return tuple(out_degree), tuple(in_degree)


def rewired_gates(seed):
    canonical = clone_gates()
    signature = degree_signature(canonical)
    loops = self_loop_count(canonical)
    canonical_edges = edge_set(canonical)

    for restart in range(32):
        rng = random.Random(seed + restart * 100003)
        gates = clone_gates()
        accepted = 0
        attempts = 0
        while accepted < 160 and attempts < 50000:
            attempts += 1
            i, j = rng.sample(range(len(gates)), 2)
            a, b = int(gates[i]["source"]), int(gates[i]["target"])
            c, d = int(gates[j]["source"]), int(gates[j]["target"])
            if a == c or b == d:
                continue
            new1, new2 = (a, d), (c, b)
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

        if accepted < 80 or degree_signature(gates) != signature or self_loop_count(gates) != loops:
            continue
        if len(canonical_edges.symmetric_difference(edge_set(gates))) < 20:
            continue
        for index, gate in enumerate(gates):
            gate["id"] = "rewired-{}-{}-{}".format(index, gate["source"], gate["target"])
        return gates
    raise RuntimeError("failed to generate degree-preserving rewire")


def canonical_phase_map():
    return {z: float(CCRU_ZONES[z]["phaseAngle"]) for z in range(10)}


def shuffled_phase_map(seed):
    rng = random.Random(seed)
    phases = [float(CCRU_ZONES[z]["phaseAngle"]) for z in range(10)]
    while True:
        permuted = list(phases)
        rng.shuffle(permuted)
        if permuted != phases:
            return {z: permuted[z] for z in range(10)}


def outgoing(gates):
    result = {z: [] for z in range(10)}
    for gate in gates:
        if bool(gate["isOpen"]):
            result[int(gate["source"])].append(dict(gate))
    for zone in result:
        result[zone].sort(key=lambda gate: (int(gate["target"]), str(gate["id"])))
    return result


def normalized_gate_strengths(gates):
    values = [gate_strength(gate) for gate in gates]
    lo, hi = min(values), max(values)
    span = max(1e-12, hi - lo)
    return {str(gate["id"]): (gate_strength(gate) - lo) / span for gate in gates}


def capture_held(values):
    streak = 0
    for value in values[:PERTURB_STEP]:
        if value >= CAPTURE_THRESHOLD:
            streak += 1
            if streak >= CAPTURE_STREAK:
                return True
        else:
            streak = 0
    return False


def run_controller(world, gates, phase_map):
    graph = outgoing(gates)
    strengths = normalized_gate_strengths(gates)
    current_zone = world.seed % 10
    x, y = world.start
    previous_dx = 0.0
    previous_dy = 0.0
    trajectory = []
    values = []
    improving_moves = 0
    moving_steps = 0

    for step in range(STEPS):
        if step == PERTURB_STEP:
            x = (x + world.perturb[0]) % 1.0
            y = (y + world.perturb[1]) % 1.0

        current_value = world.value(x, y)
        candidates = graph[current_zone]
        if not candidates:
            raise RuntimeError("topology exposed a zone with no outgoing gate")

        best = None
        for gate in candidates:
            target = int(gate["target"])
            if target == current_zone:
                nx, ny = x, y
                dx, dy = 0.0, 0.0
                momentum = 0.0
            else:
                angle = float(phase_map[target])
                dx = STEP_SIZE * math.cos(angle)
                dy = STEP_SIZE * math.sin(angle)
                nx, ny = (x + dx) % 1.0, (y + dy) % 1.0
                prev_norm = math.hypot(previous_dx, previous_dy)
                if prev_norm > 1e-12:
                    momentum = (dx * previous_dx + dy * previous_dy) / (STEP_SIZE * prev_norm)
                else:
                    momentum = 0.0

            next_value = world.value(nx, ny)
            local_gain = next_value - current_value
            strength = strengths[str(gate["id"])]
            score = LOCAL_GAIN_WEIGHT * local_gain + GATE_WEIGHT * strength + MOMENTUM_WEIGHT * momentum
            key = (score, next_value, -target)
            if best is None or key > best[0]:
                best = (key, target, nx, ny, dx, dy, next_value)

        _, target, nx, ny, dx, dy, next_value = best
        if target != current_zone:
            moving_steps += 1
            if next_value > current_value:
                improving_moves += 1

        current_zone = target
        x, y = nx, ny
        previous_dx, previous_dy = dx, dy
        values.append(next_value)
        trajectory.append([step, current_zone, round(x, 8), round(y, 8), round(next_value, 8)])

    pre_values = values[:PERTURB_STEP]
    pre_peak = max(pre_values)
    recovery_threshold = 0.95 * pre_peak
    recovery = None
    for index in range(PERTURB_STEP, STEPS):
        if values[index] >= recovery_threshold:
            recovery = index - PERTURB_STEP
            break

    return {
        "primary": statistics.mean(values[PRIMARY_START:PRIMARY_STOP]),
        "capture": capture_held(values),
        "best_pre": pre_peak,
        "improving_fraction": improving_moves / moving_steps if moving_steps else 0.0,
        "post_mean": statistics.mean(values[60:STEPS]),
        "recovery_steps": 35 if recovery is None else recovery,
        "trajectory": trajectory,
    }


def aggregate(runs):
    return {
        "primary": statistics.mean(float(run["primary"]) for run in runs),
        "capture_rate": statistics.mean(1.0 if run["capture"] else 0.0 for run in runs),
        "best_pre": statistics.mean(float(run["best_pre"]) for run in runs),
        "improving_fraction": statistics.mean(float(run["improving_fraction"]) for run in runs),
        "post_mean": statistics.mean(float(run["post_mean"]) for run in runs),
        "recovery_steps": statistics.mean(float(run["recovery_steps"]) for run in runs),
    }


def empirical_upper_p(observed, nulls):
    return (1.0 + sum(1 for value in nulls if value >= observed)) / (1.0 + len(nulls))


def percentile(observed, nulls):
    below = sum(1 for value in nulls if value < observed)
    equal = sum(1 for value in nulls if value == observed)
    return 100.0 * (below + 0.5 * equal) / len(nulls)


def quantile(values, q):
    xs = sorted(float(value) for value in values)
    position = (len(xs) - 1) * q
    lo = int(math.floor(position))
    hi = int(math.ceil(position))
    if lo == hi:
        return xs[lo]
    weight = position - lo
    return xs[lo] * (1.0 - weight) + xs[hi] * weight


def bootstrap_ci(differences):
    rng = random.Random(BOOTSTRAP_SEED)
    n = len(differences)
    boot = []
    for _ in range(BOOTSTRAP_DRAWS):
        boot.append(statistics.mean(differences[rng.randrange(n)] for _ in range(n)))
    return quantile(boot, 0.025), quantile(boot, 0.975)


def write_report(path, result):
    primary = result["primary"]
    secondary = result["secondary"]
    lines = [
        "# P3.15 — Full Numogram Latent Morphospace Access Assay",
        "",
        "## Primary result",
        "",
        "- topology-access gate: **{}**".format("PASS" if primary["held"] else "FAIL"),
        "- canonical mean primary score: {:.6f}".format(primary["canonical_score"]),
        "- rewired-null mean: {:.6f}".format(primary["rewired_mean"]),
        "- canonical percentile vs rewired topologies: {:.1f}".format(primary["percentile"]),
        "- one-sided empirical rank p: {:.6f}".format(primary["rank_p"]),
        "- paired canonical-minus-mean-rewired advantage: {:.6f}".format(primary["paired_advantage_mean"]),
        "- bootstrap 95% CI: [{:.6f}, {:.6f}]".format(primary["bootstrap_ci"][0], primary["bootstrap_ci"][1]),
        "- canonical capture rate: {:.4f}".format(primary["canonical_capture_rate"]),
        "- mean rewired capture rate: {:.4f}".format(primary["rewired_capture_rate_mean"]),
        "",
        "## Secondary: canonical zone/phase labeling",
        "",
        "- canonical percentile vs label/phase shuffles: {:.1f}".format(secondary["label_shuffle_percentile"]),
        "- one-sided empirical rank p: {:.6f}".format(secondary["label_shuffle_rank_p"]),
        "",
        "## Additional secondary measures",
        "",
        "- canonical best pre-perturbation field: {:.6f}".format(secondary["canonical_best_pre"]),
        "- canonical improving-move fraction: {:.6f}".format(secondary["canonical_improving_fraction"]),
        "- canonical post-perturbation mean field: {:.6f}".format(secondary["canonical_post_mean"]),
        "- canonical mean recovery steps: {:.3f}".format(secondary["canonical_recovery_steps"]),
        "",
        "## Interpretation",
        "",
        result["interpretation"],
        "",
        "## Provenance",
        "",
        "- Orange fullNumogram source blob: {}".format(result["provenance"]["orange_source_blob_sha"]),
        "- FullNumogram.py SHA-256: {}".format(result["provenance"]["full_numogram_py_sha256"]),
        "- Numogram.py SHA-256: {}".format(result["provenance"]["numogram_py_sha256"]),
        "- raw trajectories gzip SHA-256: {}".format(result["provenance"]["raw_trajectories_sha256"]),
        "",
        "No alternative endpoint is used to rescue a failed primary gate.",
        "",
    ]
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="experiments/p315/results")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)

    if len(FULL_NUMOGRAM_GATES) != 29:
        raise RuntimeError("canonical Orange full Numogram must have 29 gates")
    worlds = [make_world(WORLD_SEED_BASE + index) for index in range(WORLD_COUNT)]
    canonical_gates = clone_gates()
    canonical_phases = canonical_phase_map()
    rewired = [rewired_gates(REWIRE_SEED_BASE + index) for index in range(REWIRE_COUNT)]
    label_maps = [shuffled_phase_map(LABEL_SEED_BASE + index) for index in range(LABEL_COUNT)]

    raw_path = os.path.join(args.out, "trajectories.jsonl.gz")
    canonical_runs = []
    rewired_runs = [[] for _ in range(REWIRE_COUNT)]
    label_runs = [[] for _ in range(LABEL_COUNT)]

    with gzip.open(raw_path, "wt", encoding="utf-8") as raw:
        for world_index, world in enumerate(worlds):
            run = run_controller(world, canonical_gates, canonical_phases)
            canonical_runs.append(run)
            raw.write(canonical_json({
                "arm": "canonical",
                "controller": 0,
                "world": world.seed,
                "trajectory": run["trajectory"],
            }) + "\n")

            for controller_index, gates in enumerate(rewired):
                run_r = run_controller(world, gates, canonical_phases)
                rewired_runs[controller_index].append(run_r)
                raw.write(canonical_json({
                    "arm": "rewired",
                    "controller": controller_index,
                    "world": world.seed,
                    "trajectory": run_r["trajectory"],
                }) + "\n")

            for controller_index, phases in enumerate(label_maps):
                run_l = run_controller(world, canonical_gates, phases)
                label_runs[controller_index].append(run_l)
                raw.write(canonical_json({
                    "arm": "label_shuffle",
                    "controller": controller_index,
                    "world": world.seed,
                    "trajectory": run_l["trajectory"],
                }) + "\n")

    canonical_agg = aggregate(canonical_runs)
    rewired_aggs = [aggregate(runs) for runs in rewired_runs]
    label_aggs = [aggregate(runs) for runs in label_runs]
    rewired_primary = [agg["primary"] for agg in rewired_aggs]
    label_primary = [agg["primary"] for agg in label_aggs]

    mean_rewired_per_world = [
        statistics.mean(
            float(rewired_runs[controller][world_index]["primary"])
            for controller in range(REWIRE_COUNT)
        )
        for world_index in range(WORLD_COUNT)
    ]
    differences = [
        float(canonical_runs[index]["primary"]) - mean_rewired_per_world[index]
        for index in range(WORLD_COUNT)
    ]
    ci = bootstrap_ci(differences)
    rank_p = empirical_upper_p(canonical_agg["primary"], rewired_primary)
    capture_mean = statistics.mean(agg["capture_rate"] for agg in rewired_aggs)

    primary_held = (
        rank_p <= ALPHA
        and ci[0] > 0.0
        and canonical_agg["capture_rate"] >= capture_mean
    )

    if primary_held:
        interpretation = (
            "PASS. Under the registered local-information interface, the canonical full "
            "Numogram outperformed the degree-preserving rewired topology ensemble on the "
            "primary latent-morphospace measure. This supports a topology-specific access "
            "effect for this morphospace family. It does not establish metaphysical or "
            "supernatural access."
        )
    else:
        interpretation = (
            "FAIL. Under the registered local-information interface, the canonical full "
            "Numogram did not satisfy the preregistered topology-access gate against "
            "degree-preserving rewired controls. Secondary measures are retained "
            "descriptively and do not rescue the primary claim."
        )

    result = {
        "schema": "amelia-p315-full-numogram-morphospace-v1",
        "registration": {
            "world_count": WORLD_COUNT,
            "steps": STEPS,
            "primary_window": [PRIMARY_START, PRIMARY_STOP - 1],
            "perturb_step": PERTURB_STEP,
            "rewired_controls": REWIRE_COUNT,
            "label_shuffle_controls": LABEL_COUNT,
            "world_seed_base": WORLD_SEED_BASE,
            "rewire_seed_base": REWIRE_SEED_BASE,
            "label_seed_base": LABEL_SEED_BASE,
            "bootstrap_seed": BOOTSTRAP_SEED,
        },
        "canonical_topology": {
            "gate_count": len(canonical_gates),
            "edge_set": sorted(list(edge_set(canonical_gates))),
            "degree_signature": degree_signature(canonical_gates),
            "self_loop_count": self_loop_count(canonical_gates),
        },
        "primary": {
            "held": primary_held,
            "canonical_score": canonical_agg["primary"],
            "rewired_mean": statistics.mean(rewired_primary),
            "percentile": percentile(canonical_agg["primary"], rewired_primary),
            "rank_p": rank_p,
            "paired_advantage_mean": statistics.mean(differences),
            "bootstrap_ci": list(ci),
            "canonical_capture_rate": canonical_agg["capture_rate"],
            "rewired_capture_rate_mean": capture_mean,
            "rewired_aggregate_scores": rewired_primary,
        },
        "secondary": {
            "label_shuffle_percentile": percentile(canonical_agg["primary"], label_primary),
            "label_shuffle_rank_p": empirical_upper_p(canonical_agg["primary"], label_primary),
            "label_shuffle_aggregate_scores": label_primary,
            "canonical_best_pre": canonical_agg["best_pre"],
            "canonical_improving_fraction": canonical_agg["improving_fraction"],
            "canonical_post_mean": canonical_agg["post_mean"],
            "canonical_recovery_steps": canonical_agg["recovery_steps"],
            "rewired_mean_best_pre": statistics.mean(agg["best_pre"] for agg in rewired_aggs),
            "rewired_mean_improving_fraction": statistics.mean(agg["improving_fraction"] for agg in rewired_aggs),
            "rewired_mean_post_mean": statistics.mean(agg["post_mean"] for agg in rewired_aggs),
            "rewired_mean_recovery_steps": statistics.mean(agg["recovery_steps"] for agg in rewired_aggs),
        },
        "per_world": {
            "canonical_primary": [float(run["primary"]) for run in canonical_runs],
            "mean_rewired_primary": mean_rewired_per_world,
            "paired_differences": differences,
        },
        "interpretation": interpretation,
        "provenance": {
            "orange_source_blob_sha": ORANGE_SOURCE_BLOB_SHA,
            "full_numogram_py_sha256": sha256_file("FullNumogram.py"),
            "numogram_py_sha256": sha256_file("Numogram.py"),
            "raw_trajectories_sha256": sha256_file(raw_path),
        },
    }

    summary_path = os.path.join(args.out, "summary.json")
    with open(summary_path, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)

    report_path = os.path.join(args.out, "REPORT.md")
    write_report(report_path, result)

    fingerprint = {
        "summary_sha256": sha256_file(summary_path),
        "report_sha256": sha256_file(report_path),
        "raw_trajectories_sha256": sha256_file(raw_path),
    }
    with open(os.path.join(args.out, "SHA256SUMS.json"), "w", encoding="utf-8") as handle:
        json.dump(fingerprint, handle, indent=2, sort_keys=True)

    print(json.dumps({
        "primary": result["primary"],
        "secondary": {
            "label_shuffle_percentile": result["secondary"]["label_shuffle_percentile"],
            "label_shuffle_rank_p": result["secondary"]["label_shuffle_rank_p"],
            "canonical_best_pre": result["secondary"]["canonical_best_pre"],
            "canonical_post_mean": result["secondary"]["canonical_post_mean"],
        },
        "interpretation": interpretation,
        "provenance": result["provenance"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
