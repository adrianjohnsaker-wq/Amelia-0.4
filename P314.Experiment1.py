"""Amelia P3.14 — Experiment 1A: Numogram numerical-operator specificity.

Purpose
-------
Test whether the prespecified codes 333, 137, 666 and 360 leave unusually
strong, reproducible autonomous dynamical traces in the frozen Numogram core
relative to the exhaustive population of three-digit integers with the same
digital root.

This module deliberately excludes:
- language-model rendering,
- ProcessFieldMemory,
- CCRU/occult semantic labels,
- adaptive parameter tuning,
- network access.

The code is presented only as a sequence of zone-address pulses. The pulse is
then removed. All inferential measurements are made after a washout period.

Primary null:
Within each digital-root stratum, the prespecified target label is exchangeable
with other three-digit integers under the autonomous persistence score.

Primary code-level score:
Mean paired Jensen-Shannon divergence between the post-washout observation
distribution of a code-conditioned Numogram and a same-seed sham Numogram.

The observation distribution allocates half its probability mass to 10-zone
occupancy and half to 100 directed transition frequencies.

Publication gate:
1) family-level stratified randomization p <= 0.05;
2) at least one target has BH-adjusted q <= 0.05;
3) that target is >= 90th percentile in both seed halves;
4) its late-window score is >= 90th percentile;
5) its cross-seed dispersion is no worse than the 75th percentile of its
   digital-root controls.

P3.14A is only the first half of Experiment 1. A positive result must next
survive a topology/label-shuffle falsification stage before Experiment 2.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import statistics
import time
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import Numogram as _numogram_module
from Numogram import TensorBasedNumogramSystem, ZONE_COUNT


SCHEMA = "amelia-p3.14-exp1a-v1"
PROTOCOL_ID = "AMELIA-P3.14-EXP1A-NUMERICAL-OPERATOR-SPECIFICITY-V1"

TARGET_CODES: Tuple[int, ...] = (333, 137, 666, 360)
TARGET_ROOTS: Tuple[int, ...] = tuple(sorted({2, 9}))

DIMENSION = 3
DISCOVERY_SEEDS: Tuple[int, ...] = tuple(range(1001, 1013))
CONFIRMATORY_SEEDS: Tuple[int, ...] = tuple(range(2001, 2013))
ALL_SEEDS: Tuple[int, ...] = DISCOVERY_SEEDS + CONFIRMATORY_SEEDS

BURN_IN_STEPS = 32
PULSE_REPEATS = 8
PULSE_STEPS = 24          # all targets are three digits: 3 * 8
PULSE_AMPLITUDE = 0.20    # matches the native +0.2 magnetism scale
WASHOUT_STEPS = 32
OBSERVATION_STEPS = 64
LATE_STEPS = 32

FAMILY_RANDOMIZATION_DRAWS = 50_000
FAMILY_RANDOMIZATION_SEED = 314_001

ALPHA = 0.05
SPLIT_PERCENTILE_GATE = 90.0
LATE_PERCENTILE_GATE = 90.0
DISPERSION_QUANTILE_GATE = 0.75


def _canonical(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_payload(value: Any) -> str:
    return _sha256_bytes(_canonical(value).encode("utf-8"))


def _source_sha256(path: str) -> str:
    try:
        with open(path, "rb") as handle:
            return _sha256_bytes(handle.read())
    except Exception as error:
        # Chaquopy normally exposes an extracted module path, but provenance
        # must not make the scientific run impossible if a runtime packages
        # Python sources differently. The GitHub build manifest still seals
        # exact source hashes before installation.
        return "runtime-unavailable:" + type(error).__name__


def digital_root(value: int) -> int:
    n = abs(int(value))
    if n == 0:
        return 0
    return 1 + ((n - 1) % 9)


def decimal_digits(value: int) -> Tuple[int, ...]:
    n = int(value)
    if n < 100 or n > 999:
        raise ValueError("Experiment 1A is frozen to three-digit integers 100..999")
    return tuple(int(ch) for ch in str(n))


def _protocol_dict() -> Dict[str, Any]:
    return {
        "schema": SCHEMA,
        "protocol_id": PROTOCOL_ID,
        "targets": list(TARGET_CODES),
        "reference_population": {
            "range": [100, 999],
            "matching": "same digital root as each target",
            "target_codes_excluded_from_null_pool": True,
        },
        "dimension": DIMENSION,
        "discovery_seeds": list(DISCOVERY_SEEDS),
        "confirmatory_seeds": list(CONFIRMATORY_SEEDS),
        "start_zone_rule": "seed mod 10",
        "burn_in_steps": BURN_IN_STEPS,
        "pulse": {
            "encoder": "ordered decimal digits -> one-hot Numogram zone_bias",
            "repeats": PULSE_REPEATS,
            "steps": PULSE_STEPS,
            "amplitude": PULSE_AMPLITUDE,
            "interpretive_semantics": "none",
        },
        "washout_steps": WASHOUT_STEPS,
        "observation_steps": OBSERVATION_STEPS,
        "late_steps": LATE_STEPS,
        "primary_state_vector": {
            "zone_occupancy_mass": 0.5,
            "directed_transition_mass": 0.5,
            "dimensions": 110,
        },
        "primary_score": (
            "mean paired Jensen-Shannon divergence between post-washout "
            "code-conditioned and same-seed sham state vectors"
        ),
        "primary_null": (
            "target code exchangeable with other 3-digit integers of the "
            "same digital root"
        ),
        "multiplicity": "Benjamini-Hochberg over four target-code rank p-values",
        "family_test": {
            "method": "stratified Monte Carlo randomization",
            "draws": FAMILY_RANDOMIZATION_DRAWS,
            "seed": FAMILY_RANDOMIZATION_SEED,
            "composition": "3 root-9 controls + 1 root-2 control",
        },
        "gate": {
            "family_p_max": ALPHA,
            "individual_bh_q_max": ALPHA,
            "discovery_percentile_min": SPLIT_PERCENTILE_GATE,
            "confirmatory_percentile_min": SPLIT_PERCENTILE_GATE,
            "late_percentile_min": LATE_PERCENTILE_GATE,
            "dispersion_quantile_max": DISPERSION_QUANTILE_GATE,
        },
        "advance_rule": (
            "P3.14A support is necessary but not sufficient for Experiment 2; "
            "a separate topology/label-shuffle falsification must also pass."
        ),
    }


def protocol_manifest() -> str:
    protocol = _protocol_dict()
    protocol_digest = _sha256_payload(protocol)
    return _canonical({
        "status": "ready",
        "schema": SCHEMA,
        "protocol": protocol,
        "protocol_sha256": protocol_digest,
        "numogram_source_sha256": _source_sha256(_numogram_module.__file__),
        "experiment_source_sha256": _source_sha256(__file__),
    })


def _zone_bias(digit: int) -> List[float]:
    d = int(digit)
    if d < 0 or d >= ZONE_COUNT:
        raise ValueError("digit must map to a Numogram zone 0..9")
    bias = [0.0] * ZONE_COUNT
    bias[d] = PULSE_AMPLITUDE
    return bias


def _step(system: TensorBasedNumogramSystem, current: int, context: Dict[str, Any]) -> Dict[str, Any]:
    return system.transition(current, context)


def _counts(events: Sequence[Dict[str, Any]]) -> Tuple[List[int], List[int]]:
    occupancy = [0] * ZONE_COUNT
    transitions = [0] * (ZONE_COUNT * ZONE_COUNT)
    for event in events:
        origin = int(event["from"])
        destination = int(event["to"])
        occupancy[destination] += 1
        transitions[origin * ZONE_COUNT + destination] += 1
    return occupancy, transitions


def _phi(occupancy: Sequence[int], transitions: Sequence[int]) -> List[float]:
    occ_total = float(sum(occupancy))
    edge_total = float(sum(transitions))
    if occ_total <= 0.0 or edge_total <= 0.0:
        raise ValueError("observation counts must be non-empty")
    return (
        [0.5 * float(v) / occ_total for v in occupancy] +
        [0.5 * float(v) / edge_total for v in transitions]
    )


def _entropy_from_occupancy(occupancy: Sequence[int]) -> float:
    total = float(sum(occupancy))
    if total <= 0.0:
        return 0.0
    h = 0.0
    for count in occupancy:
        if count:
            p = float(count) / total
            h -= p * math.log(p)
    return h / math.log(float(ZONE_COUNT))


def _recurrence_from_transitions(transitions: Sequence[int]) -> float:
    total = int(sum(transitions))
    if total <= 0:
        return 0.0
    distinct = sum(1 for count in transitions if count > 0)
    return 1.0 - (float(distinct) / float(total))


def _jsd(p: Sequence[float], q: Sequence[float]) -> float:
    if len(p) != len(q):
        raise ValueError("JSD vectors must have equal length")
    m = [(float(a) + float(b)) * 0.5 for a, b in zip(p, q)]

    def kl(a: Sequence[float], b: Sequence[float]) -> float:
        total = 0.0
        for x, y in zip(a, b):
            if x > 0.0:
                total += x * math.log(x / y)
        return total

    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def _run_condition(code: Optional[int], seed: int) -> Dict[str, Any]:
    system = TensorBasedNumogramSystem(seed=int(seed), dimension=DIMENSION)
    current = int(seed) % ZONE_COUNT

    for _ in range(BURN_IN_STEPS):
        event = _step(system, current, {})
        current = int(event["to"])

    if code is None:
        pulse_schedule: Sequence[Optional[int]] = [None] * PULSE_STEPS
    else:
        digits = decimal_digits(code)
        pulse_schedule = list(digits) * PULSE_REPEATS
        if len(pulse_schedule) != PULSE_STEPS:
            raise RuntimeError("pulse schedule violates frozen 24-step contract")

    for digit in pulse_schedule:
        context: Dict[str, Any]
        if digit is None:
            context = {}
        else:
            context = {"zone_bias": _zone_bias(int(digit))}
        event = _step(system, current, context)
        current = int(event["to"])

    for _ in range(WASHOUT_STEPS):
        event = _step(system, current, {})
        current = int(event["to"])

    observation: List[Dict[str, Any]] = []
    for _ in range(OBSERVATION_STEPS):
        event = _step(system, current, {})
        observation.append(event)
        current = int(event["to"])

    late = observation[-LATE_STEPS:]
    occupancy, transitions = _counts(observation)
    late_occupancy, late_transitions = _counts(late)
    observation_path = [int(observation[0]["from"])] + [
        int(event["to"]) for event in observation
    ]

    return {
        "seed": int(seed),
        "start_zone": int(seed) % ZONE_COUNT,
        "observation_path": observation_path,
        "occupancy": occupancy,
        "transitions": transitions,
        "late_occupancy": late_occupancy,
        "late_transitions": late_transitions,
        "phi": _phi(occupancy, transitions),
        "late_phi": _phi(late_occupancy, late_transitions),
        "entropy": _entropy_from_occupancy(occupancy),
        "recurrence": _recurrence_from_transitions(transitions),
    }


def _mean(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    return float(sum(float(v) for v in values) / len(values))


def _quantile(values: Sequence[float], q: float) -> float:
    xs = sorted(float(v) for v in values)
    if not xs:
        raise ValueError("quantile requires values")
    if len(xs) == 1:
        return xs[0]
    pos = (len(xs) - 1) * float(q)
    lower = int(math.floor(pos))
    upper = int(math.ceil(pos))
    if lower == upper:
        return xs[lower]
    weight = pos - lower
    return xs[lower] * (1.0 - weight) + xs[upper] * weight


def _percentile(score: float, null_scores: Sequence[float]) -> float:
    if not null_scores:
        raise ValueError("percentile requires a null population")
    below = sum(1 for value in null_scores if float(value) < float(score))
    equal = sum(1 for value in null_scores if float(value) == float(score))
    # Mid-rank percentile handles exact ties without favoring the target.
    return 100.0 * (below + 0.5 * equal) / float(len(null_scores))


def _upper_rank_p(score: float, null_scores: Sequence[float]) -> float:
    if not null_scores:
        raise ValueError("rank p requires a null population")
    at_least = sum(1 for value in null_scores if float(value) >= float(score))
    return (1.0 + float(at_least)) / (1.0 + float(len(null_scores)))


def _mean_pairwise_jsd(vectors: Sequence[Sequence[float]]) -> float:
    if len(vectors) < 2:
        return 0.0
    values: List[float] = []
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            values.append(_jsd(vectors[i], vectors[j]))
    return _mean(values)


def _bh_qvalues(p_values: Dict[int, float]) -> Dict[int, float]:
    items = sorted(p_values.items(), key=lambda item: item[1])
    m = len(items)
    raw_adjusted: List[Tuple[int, float]] = []
    for rank, (code, p) in enumerate(items, start=1):
        raw_adjusted.append((code, min(1.0, float(p) * m / rank)))

    monotone: Dict[int, float] = {}
    running = 1.0
    for code, q in reversed(raw_adjusted):
        running = min(running, q)
        monotone[code] = running
    return monotone


def _public_run_record(run: Dict[str, Any], sham: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "seed": run["seed"],
        "start_zone": run["start_zone"],
        "observation_path": run["observation_path"],
        "entropy": round(float(run["entropy"]), 12),
        "recurrence": round(float(run["recurrence"]), 12),
        "jsd_to_sham": round(_jsd(run["phi"], sham["phi"]), 12),
        "late_jsd_to_sham": round(_jsd(run["late_phi"], sham["late_phi"]), 12),
    }


def _summarize_code(code: int, runs: Sequence[Dict[str, Any]], shams: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    full_jsd = [_jsd(run["phi"], sham["phi"]) for run, sham in zip(runs, shams)]
    late_jsd = [_jsd(run["late_phi"], sham["late_phi"]) for run, sham in zip(runs, shams)]

    discovery_count = len(DISCOVERY_SEEDS)
    disc = full_jsd[:discovery_count]
    conf = full_jsd[discovery_count:]

    entropy_delta = [
        float(sham["entropy"]) - float(run["entropy"])
        for run, sham in zip(runs, shams)
    ]
    recurrence_delta = [
        float(run["recurrence"]) - float(sham["recurrence"])
        for run, sham in zip(runs, shams)
    ]

    score = _mean(full_jsd)
    late_score = _mean(late_jsd)

    return {
        "code": int(code),
        "digital_root": digital_root(code),
        "primary_score_mean_jsd": score,
        "discovery_score_mean_jsd": _mean(disc),
        "confirmatory_score_mean_jsd": _mean(conf),
        "late_score_mean_jsd": late_score,
        "late_retention_ratio": (late_score / score) if score > 0.0 else 0.0,
        "cross_seed_dispersion_mean_pairwise_jsd": _mean_pairwise_jsd(
            [run["phi"] for run in runs]
        ),
        "mean_entropy_delta_vs_sham": _mean(entropy_delta),
        "mean_recurrence_delta_vs_sham": _mean(recurrence_delta),
        "runs": [
            _public_run_record(run, sham)
            for run, sham in zip(runs, shams)
        ],
    }


def _determinism_sentinel() -> Dict[str, Any]:
    a = _run_condition(333, DISCOVERY_SEEDS[0])
    b = _run_condition(333, DISCOVERY_SEEDS[0])
    comparable_a = {
        "occupancy": a["occupancy"],
        "transitions": a["transitions"],
        "late_occupancy": a["late_occupancy"],
        "late_transitions": a["late_transitions"],
    }
    comparable_b = {
        "occupancy": b["occupancy"],
        "transitions": b["transitions"],
        "late_occupancy": b["late_occupancy"],
        "late_transitions": b["late_transitions"],
    }
    held = comparable_a == comparable_b
    return {
        "held": held,
        "code": 333,
        "seed": DISCOVERY_SEEDS[0],
        "run_a_sha256": _sha256_payload(comparable_a),
        "run_b_sha256": _sha256_payload(comparable_b),
    }


def _family_randomization(
    code_summaries: Dict[int, Dict[str, Any]],
    controls_by_root: Dict[int, List[int]],
) -> Dict[str, Any]:
    root_stats: Dict[int, Tuple[float, float]] = {}
    for root, controls in controls_by_root.items():
        values = [
            float(code_summaries[code]["primary_score_mean_jsd"])
            for code in controls
        ]
        mean = statistics.mean(values)
        sd = statistics.pstdev(values)
        if sd <= 0.0:
            raise RuntimeError("root reference population has zero variance")
        root_stats[root] = (float(mean), float(sd))

    def z(code: int) -> float:
        root = digital_root(code)
        mean, sd = root_stats[root]
        return (
            float(code_summaries[code]["primary_score_mean_jsd"]) - mean
        ) / sd

    observed = _mean([z(code) for code in TARGET_CODES])

    rng = random.Random(FAMILY_RANDOMIZATION_SEED)
    root9 = controls_by_root[9]
    root2 = controls_by_root[2]
    at_least = 0

    for _ in range(FAMILY_RANDOMIZATION_DRAWS):
        selected = rng.sample(root9, 3) + [rng.choice(root2)]
        statistic = _mean([z(code) for code in selected])
        if statistic >= observed:
            at_least += 1

    p = (1.0 + at_least) / (1.0 + FAMILY_RANDOMIZATION_DRAWS)

    return {
        "observed_mean_root_standardized_score": observed,
        "draws": FAMILY_RANDOMIZATION_DRAWS,
        "seed": FAMILY_RANDOMIZATION_SEED,
        "upper_tail_p": p,
        "held_at_alpha_0_05": p <= ALPHA,
        "root_reference": {
            str(root): {"mean": mean, "sd": sd}
            for root, (mean, sd) in root_stats.items()
        },
    }


def _write_create_only(path: str, text: str) -> None:
    parent = os.path.dirname(path)
    os.makedirs(parent, exist_ok=True)
    with open(path, "x", encoding="utf-8") as handle:
        handle.write(text)


def _archive_evidence(archive_dir: str, evidence: Dict[str, Any]) -> Tuple[str, str]:
    canonical = _canonical(evidence)
    digest = _sha256_bytes(canonical.encode("utf-8"))
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    nonce = str(time.time_ns())[-9:]
    filename = "p314-exp1a-{}-{}.json".format(stamp, nonce)
    archive_path = os.path.join(os.path.abspath(archive_dir), filename)
    _write_create_only(archive_path, canonical)
    _write_create_only(archive_path + ".sha256", digest + "  " + filename + "\n")
    return archive_path, digest


def run_experiment(archive_dir: str) -> str:
    started_ns = time.time_ns()

    protocol = _protocol_dict()
    protocol_digest = _sha256_payload(protocol)
    sentinel = _determinism_sentinel()

    if not sentinel["held"]:
        return _canonical({
            "schema": SCHEMA,
            "status": "determinism_failed",
            "protocol_sha256": protocol_digest,
            "determinism_sentinel": sentinel,
            "operator_specificity_held": False,
        })

    # Same-seed sham reference is generated once and reused for every code.
    shams: List[Dict[str, Any]] = [
        _run_condition(None, seed)
        for seed in ALL_SEEDS
    ]

    root_universes: Dict[int, List[int]] = {
        root: [
            code
            for code in range(100, 1000)
            if digital_root(code) == root
        ]
        for root in TARGET_ROOTS
    }

    all_codes = sorted(set(
        code
        for codes in root_universes.values()
        for code in codes
    ))

    code_summaries: Dict[int, Dict[str, Any]] = {}
    for code in all_codes:
        runs = [_run_condition(code, seed) for seed in ALL_SEEDS]
        code_summaries[code] = _summarize_code(code, runs, shams)

    target_set = set(TARGET_CODES)
    controls_by_root: Dict[int, List[int]] = {
        root: [
            code
            for code in root_universes[root]
            if code not in target_set
        ]
        for root in TARGET_ROOTS
    }

    target_results: Dict[int, Dict[str, Any]] = {}
    p_values: Dict[int, float] = {}

    for target in TARGET_CODES:
        root = digital_root(target)
        controls = controls_by_root[root]
        target_summary = code_summaries[target]

        full_null = [
            float(code_summaries[code]["primary_score_mean_jsd"])
            for code in controls
        ]
        discovery_null = [
            float(code_summaries[code]["discovery_score_mean_jsd"])
            for code in controls
        ]
        confirmatory_null = [
            float(code_summaries[code]["confirmatory_score_mean_jsd"])
            for code in controls
        ]
        late_null = [
            float(code_summaries[code]["late_score_mean_jsd"])
            for code in controls
        ]
        dispersion_null = [
            float(code_summaries[code]["cross_seed_dispersion_mean_pairwise_jsd"])
            for code in controls
        ]

        full_score = float(target_summary["primary_score_mean_jsd"])
        p = _upper_rank_p(full_score, full_null)
        p_values[target] = p

        result = {
            "code": target,
            "digital_root": root,
            "control_count": len(controls),
            "primary_score_mean_jsd": full_score,
            "primary_percentile": _percentile(full_score, full_null),
            "rank_p_upper": p,
            "discovery_score_mean_jsd": target_summary["discovery_score_mean_jsd"],
            "discovery_percentile": _percentile(
                target_summary["discovery_score_mean_jsd"], discovery_null
            ),
            "confirmatory_score_mean_jsd": target_summary["confirmatory_score_mean_jsd"],
            "confirmatory_percentile": _percentile(
                target_summary["confirmatory_score_mean_jsd"], confirmatory_null
            ),
            "late_score_mean_jsd": target_summary["late_score_mean_jsd"],
            "late_percentile": _percentile(
                target_summary["late_score_mean_jsd"], late_null
            ),
            "late_retention_ratio": target_summary["late_retention_ratio"],
            "cross_seed_dispersion_mean_pairwise_jsd": (
                target_summary["cross_seed_dispersion_mean_pairwise_jsd"]
            ),
            "dispersion_75pct_threshold": _quantile(
                dispersion_null, DISPERSION_QUANTILE_GATE
            ),
            "dispersion_percentile": _percentile(
                target_summary["cross_seed_dispersion_mean_pairwise_jsd"],
                dispersion_null
            ),
            "mean_entropy_delta_vs_sham": target_summary["mean_entropy_delta_vs_sham"],
            "mean_recurrence_delta_vs_sham": target_summary["mean_recurrence_delta_vs_sham"],
        }
        result["split_replication_held"] = (
            result["discovery_percentile"] >= SPLIT_PERCENTILE_GATE
            and result["confirmatory_percentile"] >= SPLIT_PERCENTILE_GATE
        )
        result["late_persistence_held"] = (
            result["late_percentile"] >= LATE_PERCENTILE_GATE
        )
        result["reproducibility_held"] = (
            result["cross_seed_dispersion_mean_pairwise_jsd"]
            <= result["dispersion_75pct_threshold"]
        )
        target_results[target] = result

    q_values = _bh_qvalues(p_values)
    confirmed_targets: List[int] = []
    for target in TARGET_CODES:
        result = target_results[target]
        q = q_values[target]
        result["bh_q"] = q
        result["individual_held"] = (
            q <= ALPHA
            and result["split_replication_held"]
            and result["late_persistence_held"]
            and result["reproducibility_held"]
        )
        if result["individual_held"]:
            confirmed_targets.append(target)

    family = _family_randomization(code_summaries, controls_by_root)

    operator_specificity_held = (
        bool(family["held_at_alpha_0_05"])
        and len(confirmed_targets) >= 1
    )

    # Raw evidence preserves every 65-zone post-washout observation path
    # (initial observation origin + 64 destinations) for every code and sham.
    # Occupancy, directed-transition counts and all published statistics can
    # therefore be independently reconstructed while keeping the archive small.
    evidence = {
        "schema": SCHEMA,
        "protocol": protocol,
        "protocol_sha256": protocol_digest,
        "source_fingerprints": {
            "numogram_sha256": _source_sha256(_numogram_module.__file__),
            "experiment_sha256": _source_sha256(__file__),
        },
        "determinism_sentinel": sentinel,
        "shams": [
            {
                "seed": sham["seed"],
                "start_zone": sham["start_zone"],
                "observation_path": sham["observation_path"],
                "entropy": round(float(sham["entropy"]), 12),
                "recurrence": round(float(sham["recurrence"]), 12),
            }
            for sham in shams
        ],
        "code_summaries": {
            str(code): code_summaries[code]
            for code in all_codes
        },
        "target_results": {
            str(code): target_results[code]
            for code in TARGET_CODES
        },
        "family_randomization": family,
        "confirmed_targets": confirmed_targets,
        "operator_specificity_held": operator_specificity_held,
    }

    archive_path, evidence_digest = _archive_evidence(archive_dir, evidence)
    elapsed_s = (time.time_ns() - started_ns) / 1_000_000_000.0

    summary = {
        "schema": SCHEMA,
        "status": "success",
        "protocol_sha256": protocol_digest,
        "numogram_source_sha256": evidence["source_fingerprints"]["numogram_sha256"],
        "experiment_source_sha256": evidence["source_fingerprints"]["experiment_sha256"],
        "determinism_sentinel": sentinel,
        "family_randomization": family,
        "target_results": {
            str(code): target_results[code]
            for code in TARGET_CODES
        },
        "confirmed_targets": confirmed_targets,
        "operator_specificity_held": operator_specificity_held,
        "advance_to_experiment_2": False,
        "next_required_stage": (
            "P3.14B topology/label-shuffle falsification"
            if operator_specificity_held
            else "none; Experiment 1A did not meet the preregistered gate"
        ),
        "archive_file": archive_path,
        "evidence_sha256": evidence_digest,
        "elapsed_seconds": elapsed_s,
    }
    return _canonical(summary)
