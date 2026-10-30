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


def fixed_derangement(n: int, seed: int) -> List[int]:
    rng = random.Random(seed)
    values = list(range(n))
    for _ in range(10000):
        rng.shuffle(values)
        if all(values[i] != i for i in range(n)):
            return list(values)
    raise RuntimeError("could not generate registered history derangement")


def develop_entries(
    seeds: Sequence[int],
    prefix: str,
) -> List[Dict[str, object]]:
    entries: List[Dict[str, object]] = []
    for index, seed in enumerate(seeds):
        dev_tape, post_tape = make_tapes(seed)
        process = DynamicNumogramProcess(current_zone=seed % 10)
        dev_records = run_dynamic_tape(process, dev_tape)
        entries.append({
            "lineage": "{}{:03d}".format(prefix, index),
            "seed": int(seed),
            "dev_tape": dev_tape,
            "post_tape": post_tape,
            "process": process,
            "dev_records": dev_records,
            "dev_forms": extract_forms(dev_records),
        })
    return entries


def run_focal_arms(
    entries: List[Dict[str, object]],
    permutation_seed: int,
) -> None:
    donor_map = fixed_derangement(len(entries), permutation_seed)
    canonical_permeabilities = original_gate_permeability(FULL_NUMOGRAM_GATES)

    for index, entry in enumerate(entries):
        seed = int(entry["seed"])
        post_tape = entry["post_tape"]
        dev_tape = entry["dev_tape"]

        shocked = copy.deepcopy(entry["process"])
        shock_process(
            shocked,
            seed,
            canonical_permeabilities,
        )

        retained = copy.deepcopy(shocked)
        reset = copy.deepcopy(shocked)
        reset.memory = IntegratedMemorySystem()

        permuted = copy.deepcopy(shocked)
        donor = entries[donor_map[index]]
        permuted.memory = copy.deepcopy(donor["process"].memory)
        permuted.deformation_tensor = list(donor["process"].deformation_tensor)

        shock_zone = int(shocked.current_zone)
        fresh = DynamicNumogramProcess(current_zone=shock_zone)
        replay = copy.deepcopy(shocked)

        retained_records = run_dynamic_tape(retained, post_tape)
        reset_records = run_dynamic_tape(reset, post_tape)
        permuted_records = run_dynamic_tape(permuted, post_tape)
        fresh_records = run_dynamic_tape(fresh, post_tape)
        static_records = run_static_tape(shock_zone, post_tape)
        replay_records = run_dynamic_tape(replay, dev_tape)

        entry["donor_lineage"] = donor["lineage"]
        entry["shock_zone"] = shock_zone
        entry["post"] = {
            "retained": retained_records,
            "reset": reset_records,
            "permuted": permuted_records,
            "fresh": fresh_records,
            "static": static_records,
            "replay": replay_records,
        }
        entry["post_forms"] = {
            arm: extract_forms(records)
            for arm, records in entry["post"].items()
        }


def discovery_candidates(
    entries: Sequence[Dict[str, object]],
) -> Tuple[List[Dict[str, object]], set]:
    developmental_repertoire: set = set()
    for entry in entries:
        developmental_repertoire.update(entry["dev_forms"].keys())

    form_lineages: Dict[str, set] = defaultdict(set)
    form_occurrences: Dict[str, int] = defaultdict(int)
    form_non_echo_lineages: Dict[str, set] = defaultdict(set)
    examples: Dict[str, List[Dict[str, object]]] = defaultdict(list)

    for entry in entries:
        lineage = str(entry["lineage"])
        post_forms = entry["post_forms"]["retained"]
        post_tape = entry["post_tape"]
        for identifier, occurrences in post_forms.items():
            form_lineages[identifier].add(lineage)
            form_occurrences[identifier] += len(occurrences)

            meta = parse_form_id(identifier)
            path = tuple(meta["path"])
            if path not in ngrams(post_tape, len(path)):
                form_non_echo_lineages[identifier].add(lineage)

            if len(examples[identifier]) < 8:
                for occurrence in occurrences[: 8 - len(examples[identifier])]:
                    examples[identifier].append({
                        "lineage": lineage,
                        "start": occurrence["start"],
                        "end": occurrence["end"],
                    })

    candidates: List[Dict[str, object]] = []
    for identifier in form_lineages:
        meta = parse_form_id(identifier)
        path = tuple(meta["path"])

        if identifier in developmental_repertoire:
            continue
        if path in PRIOR_POINTER_PATHS:
            continue

        lineage_count = len(form_lineages[identifier])
        occurrence_count = form_occurrences[identifier]
        non_echo_count = len(form_non_echo_lineages[identifier])
        non_echo_fraction = (
            non_echo_count / lineage_count if lineage_count else 0.0
        )

        if lineage_count < DISCOVERY_MIN_LINEAGES:
            continue
        if occurrence_count < DISCOVERY_MIN_OCCURRENCES:
            continue
        if non_echo_fraction < DISCOVERY_MIN_NON_ECHO:
            continue

        candidates.append({
            "form_id": identifier,
            "length": meta["length"],
            "path": list(path),
            "top_activation": meta["top_activation"],
            "hbin": meta["hbin"],
            "discovery_lineages": sorted(form_lineages[identifier]),
            "discovery_lineage_count": lineage_count,
            "discovery_occurrences": occurrence_count,
            "discovery_non_echo_lineages": sorted(
                form_non_echo_lineages[identifier]
            ),
            "discovery_non_echo_fraction": non_echo_fraction,
            "contains_prior_pointer_material": path_has_prior_material(path),
            "examples": examples[identifier],
        })

    candidates.sort(
        key=lambda item: (
            -int(item["discovery_lineage_count"]),
            -int(item["discovery_occurrences"]),
            str(item["form_id"]),
        )
    )
    return candidates[:MAX_CANDIDATES], developmental_repertoire


def binomial_upper_tail(successes: int, trials: int) -> float:
    if trials <= 0:
        return 1.0
    numerator = sum(
        math.comb(trials, k)
        for k in range(successes, trials + 1)
    )
    return numerator / float(2 ** trials)


def paired_sign_test(
    canonical_presence: Sequence[bool],
    control_presence: Sequence[bool],
) -> Dict[str, object]:
    canonical_only = 0
    control_only = 0
    for a, b in zip(canonical_presence, control_presence):
        if a and not b:
            canonical_only += 1
        elif b and not a:
            control_only += 1
    discordant = canonical_only + control_only
    return {
        "canonical_only": canonical_only,
        "control_only": control_only,
        "discordant": discordant,
        "p_upper": binomial_upper_tail(canonical_only, discordant),
    }


def presence_vector(
    entries: Sequence[Dict[str, object]],
    arm: str,
    identifier: str,
) -> List[bool]:
    return [
        identifier in entry["post_forms"][arm]
        for entry in entries
    ]


def candidate_lineage_details(
    entries: Sequence[Dict[str, object]],
    arm: str,
    identifier: str,
) -> List[Dict[str, object]]:
    details: List[Dict[str, object]] = []
    path = tuple(parse_form_id(identifier)["path"])
    for entry in entries:
        occurrences = entry["post_forms"][arm].get(identifier, [])
        if not occurrences:
            continue
        starts = [int(item["start"]) for item in occurrences]
        intervals = [
            starts[i] - starts[i - 1]
            for i in range(1, len(starts))
        ]
        tape = (
            entry["dev_tape"]
            if arm == "replay"
            else entry["post_tape"]
        )
        details.append({
            "lineage": entry["lineage"],
            "seed": entry["seed"],
            "count": len(occurrences),
            "first_step": min(starts),
            "step_ranges": [
                [int(item["start"]), int(item["end"])]
                for item in occurrences
            ],
            "recurred_after_first": len(occurrences) >= 2,
            "recurrence_intervals": intervals,
            "input_echo": path in ngrams(tape, len(path)),
        })
    return details


def confirm_candidates(
    candidates: List[Dict[str, object]],
    confirm_entries: Sequence[Dict[str, object]],
) -> List[Dict[str, object]]:
    confirm_developmental_repertoire: set = set()
    for entry in confirm_entries:
        confirm_developmental_repertoire.update(entry["dev_forms"].keys())

    k = len(candidates)
    family_alpha = ALPHA / (2.0 * k) if k else 0.0
    confirmed_rows: List[Dict[str, object]] = []

    for candidate in candidates:
        identifier = str(candidate["form_id"])
        path = tuple(candidate["path"])

        vectors = {
            arm: presence_vector(confirm_entries, arm, identifier)
            for arm in (
                "retained",
                "reset",
                "permuted",
                "fresh",
                "static",
                "replay",
            )
        }

        retained_details = candidate_lineage_details(
            confirm_entries, "retained", identifier
        )
        retained_count = sum(vectors["retained"])
        non_echo_count = sum(
            1 for detail in retained_details
            if not bool(detail["input_echo"])
        )
        non_echo_fraction = (
            non_echo_count / retained_count if retained_count else 0.0
        )

        reset_test = paired_sign_test(
            vectors["retained"], vectors["reset"]
        )
        permuted_test = paired_sign_test(
            vectors["retained"], vectors["permuted"]
        )

        absent_confirm_dev = identifier not in confirm_developmental_repertoire

        held = (
            retained_count >= CONFIRM_MIN_LINEAGES
            and float(reset_test["p_upper"]) <= family_alpha
            and float(permuted_test["p_upper"]) <= family_alpha
            and non_echo_fraction >= CONFIRM_MIN_NON_ECHO
            and absent_confirm_dev
        )

        intervals = [
            interval
            for detail in retained_details
            for interval in detail["recurrence_intervals"]
        ]
        recurrence_fraction = (
            sum(
                1 for detail in retained_details
                if bool(detail["recurred_after_first"])
            ) / retained_count
            if retained_count
            else 0.0
        )

        confirmed_rows.append({
            **candidate,
            "confirm_family_alpha": family_alpha,
            "confirm_developmental_absent": absent_confirm_dev,
            "confirm_retained_lineages": retained_count,
            "confirm_reset_lineages": sum(vectors["reset"]),
            "confirm_permuted_lineages": sum(vectors["permuted"]),
            "confirm_fresh_lineages": sum(vectors["fresh"]),
            "confirm_static_lineages": sum(vectors["static"]),
            "confirm_replay_lineages": sum(vectors["replay"]),
            "confirm_non_echo_fraction": non_echo_fraction,
            "reset_sign_test": reset_test,
            "permuted_sign_test": permuted_test,
            "retained_recurrence_fraction": recurrence_fraction,
            "median_recurrence_interval": (
                statistics.median(intervals) if intervals else None
            ),
            "confirm_retained_details": retained_details,
            "confirmed_new_ingression_form": held,
        })

    return confirmed_rows


def score_rewired_candidates(
    candidates: Sequence[Dict[str, object]],
    confirm_entries: Sequence[Dict[str, object]],
) -> Dict[str, object]:
    candidate_ids = [str(item["form_id"]) for item in candidates]
    per_candidate_counts = {
        identifier: []
        for identifier in candidate_ids
    }
    controllers: List[Dict[str, object]] = []

    for controller_index in range(REWIRE_COUNT):
        gates = rewired_gates(REWIRE_SEED_BASE + controller_index)
        original_permeabilities = original_gate_permeability(gates)
        counts = {identifier: 0 for identifier in candidate_ids}

        for entry in confirm_entries:
            seed = int(entry["seed"])
            process = DynamicNumogramProcess(
                gates=gates,
                current_zone=seed % 10,
            )
            run_dynamic_tape(process, entry["dev_tape"])
            shock_process(
                process,
                seed,
                original_permeabilities,
            )
            post_records = run_dynamic_tape(process, entry["post_tape"])
            forms = extract_forms(post_records)
            for identifier in candidate_ids:
                if identifier in forms:
                    counts[identifier] += 1

        controllers.append({
            "controller": controller_index,
            "seed": REWIRE_SEED_BASE + controller_index,
            "edges": sorted(list(edge_set(gates))),
            "candidate_lineage_counts": counts,
        })
        for identifier in candidate_ids:
            per_candidate_counts[identifier].append(counts[identifier])

    return {
        "controllers": controllers,
        "per_candidate_counts": per_candidate_counts,
    }


def return_forms(
    entries: Sequence[Dict[str, object]],
    minimum_lineages: int = 8,
    limit: int = 40,
) -> List[Dict[str, object]]:
    developmental: Dict[str, set] = defaultdict(set)
    post: Dict[str, set] = defaultdict(set)
    post_occurrences: Dict[str, int] = defaultdict(int)

    for entry in entries:
        lineage = str(entry["lineage"])
        for identifier in entry["dev_forms"]:
            developmental[identifier].add(lineage)
        for identifier, occurrences in entry["post_forms"]["retained"].items():
            post[identifier].add(lineage)
            post_occurrences[identifier] += len(occurrences)

    rows: List[Dict[str, object]] = []
    for identifier in set(developmental) & set(post):
        if len(post[identifier]) < minimum_lineages:
            continue
        meta = parse_form_id(identifier)
        rows.append({
            "form_id": identifier,
            "path": list(meta["path"]),
            "developmental_lineages": len(developmental[identifier]),
            "post_lineages": len(post[identifier]),
            "post_occurrences": post_occurrences[identifier],
            "contains_prior_pointer_material": path_has_prior_material(
                meta["path"]
            ),
        })

    rows.sort(
        key=lambda item: (
            -int(item["post_lineages"]),
            -int(item["post_occurrences"]),
            str(item["form_id"]),
        )
    )
    return rows[:limit]


def write_lineage_archive(
    path: str,
    discovery_entries: Sequence[Dict[str, object]],
    confirm_entries: Sequence[Dict[str, object]],
) -> None:
    with gzip.open(path, "wt", encoding="utf-8") as handle:
        for cohort, entries in (
            ("discovery", discovery_entries),
            ("confirmation", confirm_entries),
        ):
            for entry in entries:
                row = {
                    "cohort": cohort,
                    "lineage": entry["lineage"],
                    "seed": entry["seed"],
                    "donor_lineage": entry["donor_lineage"],
                    "shock_zone": entry["shock_zone"],
                    "developmental_tape": entry["dev_tape"],
                    "post_tape": entry["post_tape"],
                    "developmental_records": entry["dev_records"],
                    "post_records": entry["post"],
                }
                handle.write(canonical_json(row) + "\n")


def add_rewired_to_candidates(
    rows: List[Dict[str, object]],
    rewired: Dict[str, object],
) -> None:
    counts = rewired["per_candidate_counts"]
    for row in rows:
        identifier = str(row["form_id"])
        values = list(counts.get(identifier, []))
        row["rewired_lineage_counts"] = values
        row["rewired_mean_lineages"] = (
            statistics.mean(values) if values else 0.0
        )
        row["rewired_max_lineages"] = max(values) if values else 0


def atlas_markdown(
    candidate_rows: Sequence[Dict[str, object]],
    return_rows: Sequence[Dict[str, object]],
    primary_held: bool,
) -> str:
    lines = [
        "# P3.17 — Ingression / Developmental Canalization Atlas",
        "",
        "Primary outcome: **{}**".format(
            "INGRESSION CONFIRMED"
            if primary_held
            else "NO CONFIRMED NEW INGRESSING FORM UNDER P3.17"
        ),
        "",
        "Forms below were discovered algorithmically from the HISTORY_RETAINED discovery cohort. Candidate identities were not named in advance.",
        "",
        "## New-form candidates",
        "",
    ]

    if not candidate_rows:
        lines.append("No candidate met the preregistered discovery rule.")
    else:
        for row in candidate_rows:
            lines.extend([
                "### {}{}".format(
                    row["form_id"],
                    " — CONFIRMED" if row["confirmed_new_ingression_form"] else "",
                ),
                "",
                "- path: {}".format("-".join(str(x) for x in row["path"])),
                "- endpoint class: dominant activation zone {} / H{}".format(
                    row["top_activation"], row["hbin"]
                ),
                "- discovery: {} lineages / {} occurrences / {:.3f} non-echo fraction".format(
                    row["discovery_lineage_count"],
                    row["discovery_occurrences"],
                    row["discovery_non_echo_fraction"],
                ),
                "- confirmation HISTORY_RETAINED: {} lineages".format(
                    row["confirm_retained_lineages"]
                ),
                "- HISTORY_RESET: {}; HISTORY_PERMUTED: {}; FRESH: {}; STATIC: {}; INPUT_REPLAY: {}".format(
                    row["confirm_reset_lineages"],
                    row["confirm_permuted_lineages"],
                    row["confirm_fresh_lineages"],
                    row["confirm_static_lineages"],
                    row["confirm_replay_lineages"],
                ),
                "- reset paired sign p: {:.8f}; permuted paired sign p: {:.8f}; family alpha: {:.8f}".format(
                    row["reset_sign_test"]["p_upper"],
                    row["permuted_sign_test"]["p_upper"],
                    row["confirm_family_alpha"],
                ),
                "- confirmation non-echo fraction: {:.3f}; absent from confirmation developmental repertoire: {}".format(
                    row["confirm_non_echo_fraction"],
                    row["confirm_developmental_absent"],
                ),
                "- canalization: {:.3f} of positive retained lineages recur after first appearance; median recurrence interval: {}".format(
                    row["retained_recurrence_fraction"],
                    row["median_recurrence_interval"],
                ),
                "- dynamic-rewired mean prevalence: {:.3f} lineages; max across rewires: {}".format(
                    row.get("rewired_mean_lineages", 0.0),
                    row.get("rewired_max_lineages", 0),
                ),
                "- contains shorter prior Pointer material: {}".format(
                    row["contains_prior_pointer_material"]
                ),
                "",
                "Confirmation retained lineage traces:",
            ])

            details = row["confirm_retained_details"]
            if not details:
                lines.append("- none")
            else:
                for detail in details:
                    ranges = ", ".join(
                        "{}–{}".format(a, b)
                        for a, b in detail["step_ranges"]
                    )
                    lines.append(
                        "- {} seed {}: {} occurrence(s), steps {}; input echo={}".format(
                            detail["lineage"],
                            detail["seed"],
                            detail["count"],
                            ranges,
                            detail["input_echo"],
                        )
                    )
            lines.append("")

    lines.extend([
        "## Developmental-return forms",
        "",
        "These forms existed during development and reappeared after shock. They are reported separately and never count as new ingression.",
        "",
    ])
    if not return_rows:
        lines.append("No return form met the atlas display threshold.")
    else:
        for row in return_rows:
            lines.append(
                "- {} — development {} lineages; post {} lineages; {} post occurrences; prior-material={}".format(
                    row["form_id"],
                    row["developmental_lineages"],
                    row["post_lineages"],
                    row["post_occurrences"],
                    row["contains_prior_pointer_material"],
                )
            )

    lines.extend([
        "",
        "## Epistemic boundary",
        "",
        "A confirmed P3.17 form would establish a recurrent, history-dependent computational form under this assay. It would not by itself identify an external entity or establish a metaphysical source.",
        "",
    ])
    return "\n".join(lines)


def report_markdown(result: Dict[str, object]) -> str:
    p = result["primary"]
    return "\n".join([
        "# P3.17 — Ingression / Developmental Canalization Result",
        "",
        "## Primary result",
        "",
        "- outcome: **{}**".format(p["outcome"]),
        "- discovery candidates entering confirmation: {}".format(
            p["candidate_count"]
        ),
        "- confirmed new ingression forms: {}".format(
            p["confirmed_count"]
        ),
        "- discovery developmental repertoire size: {}".format(
            p["discovery_developmental_repertoire_size"]
        ),
        "- confirmation developmental repertoire size: {}".format(
            p["confirmation_developmental_repertoire_size"]
        ),
        "",
        "## Interpretation",
        "",
        result["interpretation"],
        "",
        "## Evidence",
        "",
        "- atlas: experiments/p317/results/ATLAS.md",
        "- machine atlas: experiments/p317/results/atlas.json",
        "- lineage archive SHA-256: {}".format(
            result["provenance"]["lineages_sha256"]
        ),
        "- controls SHA-256: {}".format(
            result["provenance"]["controls_sha256"]
        ),
        "- registration SHA-256: {}".format(
            result["provenance"]["registration_sha256"]
        ),
        "- runner SHA-256: {}".format(
            result["provenance"]["runner_sha256"]
        ),
        "- frozen P3.16 engine SHA-256: {}".format(
            result["provenance"]["dynamic_engine_sha256"]
        ),
        "",
        "No secondary or return-form result rescues failure of the primary ingression criterion.",
        "",
    ])
