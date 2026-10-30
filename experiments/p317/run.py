#!/usr/bin/env python3
"""P3.17 — Ingression / Developmental Canalization Atlas.

Registration: experiments/p317/REGISTRATION.md
The first complete valid run is the result.
"""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import math
import os
import random
import statistics
import sys
from collections import defaultdict
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
P316_DIR = os.path.join(REPO_ROOT, "experiments", "p316")
if P316_DIR not in sys.path:
    sys.path.insert(0, P316_DIR)

from FullNumogram import FULL_NUMOGRAM_GATES
from DynamicNumogram import (
    DynamicNumogramProcess,
    IntegratedMemorySystem,
    degree_signature,
    edge_set,
    self_loop_count,
)

DISCOVERY_COUNT = 96
CONFIRM_COUNT = 96
TOTAL_COUNT = DISCOVERY_COUNT + CONFIRM_COUNT
LINEAGE_SEED_BASE = 3170000
REWIRE_COUNT = 24
REWIRE_SEED_BASE = 3173000
HISTORY_PERMUTATION_SEED = 3174000

DEV_STEPS = 128
POST_STEPS = 128
FORM_LENGTHS = (3, 4, 5)
DISCOVERY_MIN_LINEAGES = 8
DISCOVERY_MIN_OCCURRENCES = 12
DISCOVERY_MIN_NON_ECHO = 0.90
CONFIRM_MIN_LINEAGES = 8
CONFIRM_MIN_NON_ECHO = 0.90
MAX_CANDIDATES = 20
ALPHA = 0.05

PRIOR_POINTER_PATHS = {
    (1, 7),
    (1, 7, 8, 9),
    (1, 2, 7),
    (7, 8),
    (1, 7, 8),
    (1, 8, 7),
}


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


def weighted_choice(rng: random.Random, weights: Sequence[float]) -> int:
    total = sum(weights)
    point = rng.random() * total
    cumulative = 0.0
    for index, weight in enumerate(weights):
        cumulative += weight
        if point <= cumulative:
            return index
    return len(weights) - 1


def transition_matrix(seed: int) -> List[List[float]]:
    rng = random.Random(seed)
    matrix: List[List[float]] = []
    for _ in range(10):
        raw = [rng.expovariate(1.0) + 0.05 for _ in range(10)]
        total = sum(raw)
        matrix.append([value / total for value in raw])
    return matrix


def sample_markov_tape(
    matrix: Sequence[Sequence[float]],
    seed: int,
    length: int,
) -> List[int]:
    rng = random.Random(seed)
    current = rng.randrange(10)
    tape = [current]
    while len(tape) < length:
        current = weighted_choice(rng, matrix[current])
        tape.append(current)
    return tape


def ngrams(values: Sequence[int], n: int) -> set:
    return {
        tuple(values[i:i+n])
        for i in range(0, len(values) - n + 1)
    }


def make_tapes(seed: int) -> Tuple[List[int], List[int]]:
    dev_matrix = transition_matrix(seed * 17 + 11)
    post_matrix = transition_matrix(seed * 17 + 13)
    dev = sample_markov_tape(dev_matrix, seed * 31 + 7, DEV_STEPS)
    forbidden = ngrams(dev, 4)

    # Re-sample the independent post trajectory until no exact 4-gram is
    # shared with development. The matrix itself is not changed by rejection.
    for attempt in range(10000):
        post = sample_markov_tape(
            post_matrix,
            seed * 37 + 19 + attempt * 1000003,
            POST_STEPS,
        )
        if not (ngrams(post, 4) & forbidden):
            return dev, post
    raise RuntimeError("could not construct registered 4-gram-separated post tape")


def hysteresis_bin(value: float) -> int:
    if value < 0.20:
        return 0
    if value < 0.40:
        return 1
    if value < 0.60:
        return 2
    return 3


def most_active_zone(process: DynamicNumogramProcess) -> int:
    return max(
        range(10),
        key=lambda z: (float(process.zones[z]["activation"]), -z),
    )


def dominant_strain_zone(process: DynamicNumogramProcess) -> int:
    return max(
        range(10),
        key=lambda z: (float(process.memory.zone_strain_history[z]), -z),
    )


def step_record(
    process: DynamicNumogramProcess,
    input_zone: int,
    step: int,
) -> Dict[str, object]:
    decision = process.step(input_zone)
    readout = process.memory.read_memory_bias()
    return {
        "step": step,
        "input": int(input_zone),
        "from": int(decision["from_zone"]),
        "zone": int(decision["to_zone"]),
        "top_activation": most_active_zone(process),
        "dominant_strain": dominant_strain_zone(process),
        "hysteresis": float(readout.hysteresis_tension),
        "hbin": hysteresis_bin(float(readout.hysteresis_tension)),
        "mean_abs_bias": sum(abs(float(x)) for x in readout.bias_vector) / 10.0,
    }


def run_dynamic_tape(
    process: DynamicNumogramProcess,
    tape: Sequence[int],
) -> List[Dict[str, object]]:
    return [
        step_record(process, int(symbol), step)
        for step, symbol in enumerate(tape)
    ]


def run_static_tape(
    current_zone: int,
    tape: Sequence[int],
) -> List[Dict[str, object]]:
    records: List[Dict[str, object]] = []
    zone = int(current_zone)
    for step, symbol in enumerate(tape):
        temp = DynamicNumogramProcess(current_zone=zone)
        decision = temp.step(int(symbol))
        readout = temp.memory.read_memory_bias()
        zone = int(decision["to_zone"])
        records.append({
            "step": step,
            "input": int(symbol),
            "from": int(decision["from_zone"]),
            "zone": zone,
            "top_activation": most_active_zone(temp),
            "dominant_strain": dominant_strain_zone(temp),
            "hysteresis": float(readout.hysteresis_tension),
            "hbin": hysteresis_bin(float(readout.hysteresis_tension)),
            "mean_abs_bias": sum(abs(float(x)) for x in readout.bias_vector) / 10.0,
        })
    return records


def original_gate_permeability(gates: Sequence[Dict[str, object]]) -> List[float]:
    return [float(gate["permeability"]) for gate in gates]


def shock_process(
    process: DynamicNumogramProcess,
    seed: int,
    original_permeabilities: Sequence[float],
) -> None:
    process.current_zone = (int(seed) * 7 + 3) % 10
    for zone in range(10):
        z = process.zones[zone]
        z["activation"] = 0.5 + 0.10 * (float(z["activation"]) - 0.5)
        z["phaseAngle"] = (float(z["phaseAngle"]) + math.pi) % (2.0 * math.pi)
        z["conductivity"] = 0.5 + 0.25 * (float(z["conductivity"]) - 0.5)
        z["polarCharge"] = 0.0
        z["deformationStress"] = 0.1 + 0.20 * (float(z["deformationStress"]) - 0.1)

    if len(process.gates) != len(original_permeabilities):
        raise RuntimeError("gate count changed before registered shock")
    for index, gate in enumerate(process.gates):
        gate["permeability"] = float(original_permeabilities[index])


def form_id(
    path: Sequence[int],
    top_activation: int,
    hbin: int,
) -> str:
    return "L{}|P{}|A{}|H{}".format(
        len(path),
        "-".join(str(int(z)) for z in path),
        int(top_activation),
        int(hbin),
    )


def parse_form_id(identifier: str) -> Dict[str, object]:
    parts = identifier.split("|")
    return {
        "length": int(parts[0][1:]),
        "path": tuple(int(x) for x in parts[1][1:].split("-")),
        "top_activation": int(parts[2][1:]),
        "hbin": int(parts[3][1:]),
    }


def extract_forms(
    records: Sequence[Dict[str, object]],
) -> Dict[str, List[Dict[str, object]]]:
    found: Dict[str, List[Dict[str, object]]] = defaultdict(list)
    for n in FORM_LENGTHS:
        for start in range(0, len(records) - n + 1):
            chunk = records[start:start+n]
            path = tuple(int(item["zone"]) for item in chunk)
            end = chunk[-1]
            identifier = form_id(
                path,
                int(end["top_activation"]),
                int(end["hbin"]),
            )
            found[identifier].append({
                "start": int(chunk[0]["step"]),
                "end": int(end["step"]),
                "path": list(path),
                "top_activation": int(end["top_activation"]),
                "dominant_strain": int(end["dominant_strain"]),
                "hbin": int(end["hbin"]),
                "hysteresis": float(end["hysteresis"]),
            })
    return found


def path_has_prior_material(path: Sequence[int]) -> bool:
    seq = tuple(int(x) for x in path)
    for prior in PRIOR_POINTER_PATHS:
        if len(prior) > len(seq):
            continue
        for start in range(0, len(seq) - len(prior) + 1):
            if seq[start:start+len(prior)] == prior:
                return True
    return False


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
            gate["id"] = "p317-rewired-{}-{}-{}".format(
                index, gate["source"], gate["target"]
            )
        return gates

    raise RuntimeError("failed to generate registered P3.17 rewire")
