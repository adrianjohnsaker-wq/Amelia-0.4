#!/usr/bin/env python3
"""P3.18 developmental competence decomposition and Warp developmental gain."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
import os
import random
import statistics
import sys
from collections import Counter
from typing import Dict, List, Sequence, Tuple

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
P316_DIR = os.path.join(REPO_ROOT, "experiments", "p316")
if P316_DIR not in sys.path:
    sys.path.insert(0, P316_DIR)
P318_DIR = os.path.abspath(os.path.dirname(__file__))
if P318_DIR not in sys.path:
    sys.path.insert(0, P318_DIR)

from DynamicNumogram import DynamicNumogramProcess, IntegratedMemorySystem
from WarpDevelopmentOperator import install_warp_development_gain, WarpDevelopmentMemory

P317_PATH = os.path.join(REPO_ROOT, "experiments", "p317", "run.py")
spec = importlib.util.spec_from_file_location("p317_frozen", P317_PATH)
p317 = importlib.util.module_from_spec(spec)
assert spec is not None and spec.loader is not None
spec.loader.exec_module(p317)

LINEAGE_COUNT = 192
LINEAGE_SEED_BASE = 3180000
DONOR_SEED = 3184000
SHUFFLE_SEED_BASE = 3185000
ALPHA_PRIMARY = 0.01
ALPHA_COMPONENT = 0.05
WARP_GAIN = 1.5
WARP_BUDGET = 8
SENTINEL = "L4|P1-2-3-6|A0|H3"

PANEL = (
    "L3|P1-1-1|A3|H3",
    "L4|P1-1-1-1|A3|H3",
    "L5|P1-1-8-9-1|A3|H3",
    "L3|P2-3-6|A0|H3",
    "L3|P8-9-0|A3|H3",
    "L3|P1-1-2|A0|H3",
    "L4|P2-3-6-3|A0|H3",
    "L4|P1-2-3-6|A0|H3",
    "L4|P9-1-1-1|A3|H3",
    "L4|P3-6-3-6|A3|H2",
    "L4|P1-1-1-1|A6|H3",
    "L4|P6-3-6-3|A3|H2",
    "L5|P3-6-3-6-3|A3|H2",
)

ARMS = (
    "FULL_OWN",
    "BLANK",
    "PFM_ONLY",
    "TENSOR_ONLY",
    "DONOR_PFM",
    "STRAIN_HYSTERESIS",
    "STRAIN_ONLY",
    "HYSTERESIS_ONLY",
    "RECENT_EVENTS_ONLY",
    "FLAT_MAGNITUDE",
    "SHUFFLED_STRAIN",
    "WARP_DEVELOPMENT_GAIN",
)

COMPONENT_ARMS = (
    "STRAIN_HYSTERESIS",
    "STRAIN_ONLY",
    "HYSTERESIS_ONLY",
    "RECENT_EVENTS_ONLY",
    "FLAT_MAGNITUDE",
    "SHUFFLED_STRAIN",
)


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def exact_upper_sign_p(wins: int, losses: int) -> float:
    n = wins + losses
    if n == 0:
        return 1.0
    return sum(math.comb(n, k) for k in range(wins, n + 1)) / float(2 ** n)


def paired_presence_test(left: Sequence[bool], right: Sequence[bool]) -> Dict[str, object]:
    left_only = 0
    right_only = 0
    for a, b in zip(left, right):
        if a and not b:
            left_only += 1
        elif b and not a:
            right_only += 1
    return {
        "left_only": left_only,
        "right_only": right_only,
        "discordant": left_only + right_only,
        "p_upper": exact_upper_sign_p(left_only, right_only),
    }


def holm_adjust(raw: Dict[str, float]) -> Dict[str, float]:
    ordered = sorted(raw.items(), key=lambda kv: (kv[1], kv[0]))
    m = len(ordered)
    adjusted: Dict[str, float] = {}
    running = 0.0
    for rank, (name, p) in enumerate(ordered):
        candidate = min(1.0, (m - rank) * p)
        running = max(running, candidate)
        adjusted[name] = running
    return adjusted


def strain_entropy(values: Sequence[float]) -> float:
    positive = [max(0.0, float(v)) for v in values]
    total = sum(positive)
    if total <= 0:
        return 0.0
    entropy = 0.0
    for value in positive:
        if value > 0:
            p = value / total
            entropy -= p * math.log(p, 2)
    return entropy


def tensor_norm(values: Sequence[float]) -> float:
    return math.sqrt(sum(float(v) ** 2 for v in values))


def memory_bias_magnitude(memory: IntegratedMemorySystem) -> float:
    readout = memory.read_memory_bias()
    return statistics.mean(abs(float(v)) for v in readout.bias_vector)


def copy_memory(source: IntegratedMemorySystem) -> IntegratedMemorySystem:
    return copy.deepcopy(source)


def blank_memory() -> IntegratedMemorySystem:
    return IntegratedMemorySystem()


def component_memory(
    source: IntegratedMemorySystem,
    mode: str,
    seed: int,
) -> IntegratedMemorySystem:
    if mode == "FULL":
        return copy_memory(source)

    memory = IntegratedMemorySystem()

    if mode == "STRAIN_HYSTERESIS":
        memory.zone_strain_history = list(source.zone_strain_history)
        memory.hysteresis_tension = float(source.hysteresis_tension)
    elif mode == "STRAIN_ONLY":
        memory.zone_strain_history = list(source.zone_strain_history)
        memory.hysteresis_tension = 0.05
    elif mode == "HYSTERESIS_ONLY":
        memory.zone_strain_history = [0.0] * 10
        memory.hysteresis_tension = float(source.hysteresis_tension)
    elif mode == "RECENT_EVENTS_ONLY":
        memory.events = copy.deepcopy(source.events[-48:])
        memory.zone_strain_history = [0.0] * 10
        memory.hysteresis_tension = 0.05
    elif mode == "FLAT_MAGNITUDE":
        mass = sum(float(v) for v in source.zone_strain_history)
        per_zone = max(0.0, min(1.0, mass / 10.0))
        memory.zone_strain_history = [per_zone] * 10
        memory.hysteresis_tension = float(source.hysteresis_tension)
    elif mode == "SHUFFLED_STRAIN":
        values = list(source.zone_strain_history)
        rng = random.Random(SHUFFLE_SEED_BASE + seed)
        rng.shuffle(values)
        memory.zone_strain_history = values
        memory.hysteresis_tension = float(source.hysteresis_tension)
    else:
        raise ValueError("unknown component memory mode " + mode)

    return memory


def arm_pre_metrics(process: DynamicNumogramProcess) -> Dict[str, float]:
    return {
        "hysteresis": float(process.memory.hysteresis_tension),
        "strain_mass": sum(float(v) for v in process.memory.zone_strain_history),
        "strain_entropy": strain_entropy(process.memory.zone_strain_history),
        "memory_bias_magnitude": memory_bias_magnitude(process.memory),
        "tensor_norm": tensor_norm(process.deformation_tensor),
    }


def warp_stats(records: Sequence[Dict[str, object]]) -> Dict[str, float]:
    touches = 0
    entries = 0
    occupancy = 0
    for row in records:
        source = int(row["from"])
        target = int(row["zone"])
        if source in (3, 6) or target in (3, 6):
            touches += 1
        if source not in (3, 6) and target in (3, 6):
            entries += 1
        if target in (3, 6):
            occupancy += 1
    n = max(1, len(records))
    return {
        "warp_transition_count": float(touches),
        "warp_entry_count": float(entries),
        "warp_occupancy": occupancy / n,
    }


def score_post(records: Sequence[Dict[str, object]]) -> Dict[str, object]:
    forms = p317.extract_forms(records)
    occurrences = forms.get(SENTINEL, [])
    starts = [int(x["start"]) for x in occurrences]
    return {
        "sentinel_present": bool(occurrences),
        "sentinel_count": len(occurrences),
        "first_appearance": min(starts) if starts else None,
        "recurred": len(occurrences) >= 2,
        "panel_breadth": sum(1 for identifier in PANEL if identifier in forms),
        "panel_present_ids": [identifier for identifier in PANEL if identifier in forms],
        "post_warp_occupancy": warp_stats(records)["warp_occupancy"],
    }


def make_arm(
    shocked: DynamicNumogramProcess,
    arm: str,
    seed: int,
    donor_memory: IntegratedMemorySystem,
) -> DynamicNumogramProcess:
    process = copy.deepcopy(shocked)

    if arm == "FULL_OWN":
        return process
    if arm == "BLANK":
        process.memory = blank_memory()
        process.deformation_tensor = [0.1] * 10
    elif arm == "PFM_ONLY":
        process.memory = copy_memory(shocked.memory)
        process.deformation_tensor = [0.1] * 10
    elif arm == "TENSOR_ONLY":
        process.memory = blank_memory()
        process.deformation_tensor = list(shocked.deformation_tensor)
    elif arm == "DONOR_PFM":
        process.memory = copy_memory(donor_memory)
        process.deformation_tensor = [0.1] * 10
    elif arm == "STRAIN_HYSTERESIS":
        process.memory = component_memory(shocked.memory, "STRAIN_HYSTERESIS", seed)
        process.deformation_tensor = [0.1] * 10
    elif arm == "STRAIN_ONLY":
        process.memory = component_memory(shocked.memory, "STRAIN_ONLY", seed)
        process.deformation_tensor = [0.1] * 10
    elif arm == "HYSTERESIS_ONLY":
        process.memory = component_memory(shocked.memory, "HYSTERESIS_ONLY", seed)
        process.deformation_tensor = [0.1] * 10
    elif arm == "RECENT_EVENTS_ONLY":
        process.memory = component_memory(shocked.memory, "RECENT_EVENTS_ONLY", seed)
        process.deformation_tensor = [0.1] * 10
    elif arm == "FLAT_MAGNITUDE":
        process.memory = component_memory(shocked.memory, "FLAT_MAGNITUDE", seed)
        process.deformation_tensor = [0.1] * 10
    elif arm == "SHUFFLED_STRAIN":
        process.memory = component_memory(shocked.memory, "SHUFFLED_STRAIN", seed)
        process.deformation_tensor = [0.1] * 10
    else:
        raise ValueError("unsupported arm " + arm)

    return process


def develop_all() -> Tuple[List[Dict[str, object]], List[int]]:
    donor_map = p317.fixed_derangement(LINEAGE_COUNT, DONOR_SEED)
    rows: List[Dict[str, object]] = []

    for index in range(LINEAGE_COUNT):
        seed = LINEAGE_SEED_BASE + index
        dev_tape, post_tape = p317.make_tapes(seed)

        canonical = DynamicNumogramProcess(current_zone=seed % 10)
        canonical_dev = p317.run_dynamic_tape(canonical, dev_tape)

        warp_gain = DynamicNumogramProcess(current_zone=seed % 10)
        install_warp_development_gain(
            warp_gain,
            gain=WARP_GAIN,
            event_budget=WARP_BUDGET,
        )
        warp_dev = p317.run_dynamic_tape(warp_gain, dev_tape)
        if not isinstance(warp_gain.memory, WarpDevelopmentMemory):
            raise AssertionError("Warp gain memory installation failed")
        gain_uses = int(warp_gain.memory.warp_gain_used)
        warp_gain.memory.disable_warp_gain()

        rows.append({
            "index": index,
            "seed": seed,
            "dev_tape": dev_tape,
            "post_tape": post_tape,
            "canonical_mature": canonical,
            "canonical_dev": canonical_dev,
            "canonical_dev_warp": warp_stats(canonical_dev),
            "warp_mature": warp_gain,
            "warp_dev": warp_dev,
            "warp_dev_warp": warp_stats(warp_dev),
            "warp_gain_uses": gain_uses,
            "warp_gain_log": list(warp_gain.memory.warp_gain_log),
        })

    return rows, donor_map


def run_all_arms(
    rows: List[Dict[str, object]],
    donor_map: Sequence[int],
) -> Dict[str, List[Dict[str, object]]]:
    results: Dict[str, List[Dict[str, object]]] = {arm: [] for arm in ARMS}
    canonical_permeabilities = p317.original_gate_permeability(p317.FULL_NUMOGRAM_GATES)

    shocked_canonical: List[DynamicNumogramProcess] = []
    shocked_warp: List[DynamicNumogramProcess] = []

    for row in rows:
        seed = int(row["seed"])

        c = copy.deepcopy(row["canonical_mature"])
        p317.shock_process(c, seed, canonical_permeabilities)
        shocked_canonical.append(c)

        w = copy.deepcopy(row["warp_mature"])
        p317.shock_process(w, seed, canonical_permeabilities)
        if isinstance(w.memory, WarpDevelopmentMemory):
            w.memory.disable_warp_gain()
        shocked_warp.append(w)

    for index, row in enumerate(rows):
        seed = int(row["seed"])
        post_tape = row["post_tape"]
        donor_memory = shocked_canonical[int(donor_map[index])].memory

        for arm in ARMS:
            if arm == "WARP_DEVELOPMENT_GAIN":
                process = copy.deepcopy(shocked_warp[index])
            else:
                process = make_arm(
                    shocked_canonical[index],
                    arm,
                    seed,
                    donor_memory,
                )

            pre = arm_pre_metrics(process)
            records = p317.run_dynamic_tape(process, post_tape)
            score = score_post(records)

            results[arm].append({
                "lineage": "P318-{:03d}".format(index),
                "seed": seed,
                "donor_lineage": (
                    "P318-{:03d}".format(donor_map[index])
                    if arm == "DONOR_PFM"
                    else None
                ),
                "pre": pre,
                "score": score,
                "post_records": records,
                "development_warp": (
                    row["warp_dev_warp"]
                    if arm == "WARP_DEVELOPMENT_GAIN"
                    else row["canonical_dev_warp"]
                ),
                "warp_gain_uses": (
                    row["warp_gain_uses"]
                    if arm == "WARP_DEVELOPMENT_GAIN"
                    else 0
                ),
            })

    return results


def presence(results: Dict[str, List[Dict[str, object]]], arm: str) -> List[bool]:
    return [bool(row["score"]["sentinel_present"]) for row in results[arm]]


def prevalence(results: Dict[str, List[Dict[str, object]]], arm: str) -> int:
    return sum(presence(results, arm))


def arm_summary(results: Dict[str, List[Dict[str, object]]], arm: str) -> Dict[str, object]:
    rows = results[arm]
    present_rows = [row for row in rows if bool(row["score"]["sentinel_present"])]
    first = [
        int(row["score"]["first_appearance"])
        for row in present_rows
        if row["score"]["first_appearance"] is not None
    ]
    return {
        "lineages": len(rows),
        "sentinel_lineages": len(present_rows),
        "sentinel_prevalence": len(present_rows) / len(rows),
        "sentinel_occurrences": sum(int(row["score"]["sentinel_count"]) for row in rows),
        "median_first_appearance": statistics.median(first) if first else None,
        "recurrence_fraction": (
            sum(1 for row in present_rows if bool(row["score"]["recurred"])) / len(present_rows)
            if present_rows else 0.0
        ),
        "mean_panel_breadth": statistics.mean(float(row["score"]["panel_breadth"]) for row in rows),
        "distinct_panel_forms_seen": sorted({
            identifier
            for row in rows
            for identifier in row["score"]["panel_present_ids"]
        }),
        "mean_pre_hysteresis": statistics.mean(float(row["pre"]["hysteresis"]) for row in rows),
        "mean_pre_strain_mass": statistics.mean(float(row["pre"]["strain_mass"]) for row in rows),
        "mean_pre_strain_entropy": statistics.mean(float(row["pre"]["strain_entropy"]) for row in rows),
        "mean_pre_memory_bias": statistics.mean(float(row["pre"]["memory_bias_magnitude"]) for row in rows),
        "mean_pre_tensor_norm": statistics.mean(float(row["pre"]["tensor_norm"]) for row in rows),
        "development_warp_entry_fraction": (
            sum(1 for row in rows if float(row["development_warp"]["warp_entry_count"]) > 0) / len(rows)
        ),
        "mean_development_warp_transitions": statistics.mean(
            float(row["development_warp"]["warp_transition_count"]) for row in rows
        ),
        "mean_development_warp_occupancy": statistics.mean(
            float(row["development_warp"]["warp_occupancy"]) for row in rows
        ),
        "mean_post_warp_occupancy": statistics.mean(
            float(row["score"]["post_warp_occupancy"]) for row in rows
        ),
        "mean_warp_gain_uses": statistics.mean(float(row["warp_gain_uses"]) for row in rows),
    }


def classify_mechanism(
    summaries: Dict[str, Dict[str, object]],
    component_adjusted: Dict[str, float],
) -> Dict[str, object]:
    pfm_count = int(summaries["PFM_ONLY"]["sentinel_lineages"])
    threshold = 0.75 * pfm_count

    sufficient: Dict[str, bool] = {}
    for arm in COMPONENT_ARMS:
        sufficient[arm] = (
            component_adjusted[arm] <= ALPHA_COMPONENT
            and int(summaries[arm]["sentinel_lineages"]) >= threshold
        )

    if sufficient["HYSTERESIS_ONLY"]:
        label = "GLOBAL_HYSTERETIC_MATURITY"
    elif sufficient["FLAT_MAGNITUDE"]:
        label = "GENERIC_STRAIN_MAGNITUDE_PLUS_HYSTERESIS"
    elif sufficient["SHUFFLED_STRAIN"] and not sufficient["FLAT_MAGNITUDE"]:
        label = "STRAIN_HETEROGENEITY_WITHOUT_ZONE_IDENTITY"
    elif sufficient["STRAIN_HYSTERESIS"] and not sufficient["SHUFFLED_STRAIN"]:
        label = "ZONE_SPECIFIC_STRAIN_ARCHITECTURE"
    elif sufficient["RECENT_EVENTS_ONLY"]:
        label = "RECENT_EVENT_CONTENT"
    else:
        label = "DISTRIBUTED_COMBINATION_OR_UNRESOLVED"

    return {
        "label": label,
        "pfm_only_75pct_threshold_lineages": threshold,
        "sufficient": sufficient,
    }
