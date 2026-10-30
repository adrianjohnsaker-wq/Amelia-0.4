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
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

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
        if not strongly_connected(gates):
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
