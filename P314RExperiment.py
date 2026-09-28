"""Amelia P3.14R — prospective replication of the 666 operator signal.

Fresh-seed confirmatory replication of the exploratory P3.14A observation that
666 ranked at the 100th percentile overall but failed cross-seed split
replication. Partial progress never exposes inferential statistics.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import statistics
import time
from typing import Any, Dict, List, Optional, Sequence, Tuple

from Numogram import TensorBasedNumogramSystem, ZONE_COUNT

SCHEMA = "amelia-p3.14r-666-replication-v1"
PROTOCOL_ID = "AMELIA-P3.14R-666-FRESH-SEED-REPLICATION-V1"

DISCOVERY_EVIDENCE_SHA256 = (
    "fda4127884f25d679fe563a7a70d56b63d5e33ff295fd53c38ef241bb002a391"
)

TARGET_CODE = 666
ORIGINAL_ROOT9_TARGETS = (333, 360, 666)

SEEDS: Tuple[int, ...] = tuple(range(3001, 3041))
COHORT_A: Tuple[int, ...] = tuple(range(3001, 3021))
COHORT_B: Tuple[int, ...] = tuple(range(3021, 3041))

DIMENSION = 3
BURN_IN_STEPS = 32
PULSE_REPEATS = 8
PULSE_STEPS = 24
PULSE_AMPLITUDE = 0.20
WASHOUT_STEPS = 32
OBSERVATION_STEPS = 64
LATE_STEPS = 32

PRIMARY_ALPHA = 0.05
SPLIT_PERCENTILE_GATE = 90.0
LATE_PERCENTILE_GATE = 90.0
DISPERSION_QUANTILE_GATE = 0.75

SCHEDULE_SEED = 666314
SHAMS_PER_CHUNK = 5
CODES_PER_CHUNK = 1

CHECKPOINT_NAME = "p314r-checkpoint.json"
FINAL_SUMMARY_NAME = "p314r-final-summary.json"


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


def digital_root(value: int) -> int:
    n = abs(int(value))
    if n == 0:
        return 0
    return 1 + ((n - 1) % 9)


def decimal_digits(value: int) -> Tuple[int, ...]:
    n = int(value)
    if n < 100 or n > 999:
        raise ValueError("P3.14R is frozen to three-digit integers")
    return tuple(int(ch) for ch in str(n))


def _control_codes() -> List[int]:
    # Exact P3.14A root-9 null pool.
    return [
        code
        for code in range(100, 1000)
        if digital_root(code) == 9
        and code not in ORIGINAL_ROOT9_TARGETS
    ]


def _schedule() -> List[int]:
    codes = _control_codes() + [TARGET_CODE]
    rng = random.Random(SCHEDULE_SEED)
    rng.shuffle(codes)
    return codes


def _protocol_dict() -> Dict[str, Any]:
    return {
        "schema": SCHEMA,
        "protocol_id": PROTOCOL_ID,
        "antecedent_discovery": {
            "source_stage": "P3.14A",
            "evidence_sha256": DISCOVERY_EVIDENCE_SHA256,
            "observed_target": 666,
            "observed_overall_percentile": 100.0,
            "observed_rank_p": 0.0102,
            "observed_bh_q": 0.0408,
            "observed_discovery_percentile": 100.0,
            "observed_confirmatory_percentile": 41.2,
            "observed_late_percentile": 94.8,
            "observed_stability": True,
            "status": "exploratory candidate; original preregistered gate failed",
        },
        "target_code": TARGET_CODE,
        "reference_population": {
            "definition": (
                "all three-digit digital-root-9 integers excluding "
                "333, 360 and 666, exactly matching P3.14A"
            ),
            "control_count": len(_control_codes()),
        },
        "seeds": {
            "all": list(SEEDS),
            "cohort_a": list(COHORT_A),
            "cohort_b": list(COHORT_B),
            "balance": (
                "each 20-seed cohort contains every seed mod 10 start-zone twice"
            ),
        },
        "dimension": DIMENSION,
        "start_zone_rule": "seed mod 10",
        "burn_in_steps": BURN_IN_STEPS,
        "pulse": {
            "encoder": "ordered decimal digits -> one-hot Numogram zone_bias",
            "repeats": PULSE_REPEATS,
            "steps": PULSE_STEPS,
            "amplitude": PULSE_AMPLITUDE,
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
        "primary_gate": {
            "overall_upper_rank_p_max": PRIMARY_ALPHA,
            "cohort_a_percentile_min": SPLIT_PERCENTILE_GATE,
            "cohort_b_percentile_min": SPLIT_PERCENTILE_GATE,
            "late_percentile_min": LATE_PERCENTILE_GATE,
            "cross_seed_dispersion_quantile_max": DISPERSION_QUANTILE_GATE,
        },
        "secondary_seed_regime": {
            "endpoint_1": "code×seed interaction dispersion",
            "endpoint_2": "variance across start_zone=seed mod 10 group means",
            "multiplicity": "Holm correction over two secondary p-values",
            "decision_role": "mechanistic secondary; never rescues primary",
        },
        "execution": {
            "checkpointed": True,
            "schedule_seed": SCHEDULE_SEED,
            "partial_inferential_results_visible": False,
        },
        "advance_rule": (
            "Only successful primary replication proceeds to P3.14B "
            "topology/label-shuffle falsification."
        ),
    }


PROTOCOL = _protocol_dict()
PROTOCOL_SHA256 = _sha256_payload(PROTOCOL)


def protocol_manifest() -> str:
    return _canonical({
        "status": "ready",
        "schema": SCHEMA,
        "protocol": PROTOCOL,
        "protocol_sha256": PROTOCOL_SHA256,
        "total_controls": len(_control_codes()),
        "total_codes_including_target": len(_schedule()),
        "total_seeds": len(SEEDS),
    })


def _zone_bias(digit: int) -> List[float]:
    d = int(digit)
    if d < 0 or d >= ZONE_COUNT:
        raise ValueError("digit must map to Numogram zone 0..9")
    bias = [0.0] * ZONE_COUNT
    bias[d] = PULSE_AMPLITUDE
    return bias


def _counts_from_path(path: Sequence[int]) -> Tuple[List[int], List[int]]:
    if len(path) != OBSERVATION_STEPS + 1:
        raise ValueError("observation path has unexpected length")
    occupancy = [0] * ZONE_COUNT
    transitions = [0] * (ZONE_COUNT * ZONE_COUNT)
    for origin, destination in zip(path[:-1], path[1:]):
        occupancy[int(destination)] += 1
        transitions[int(origin) * ZONE_COUNT + int(destination)] += 1
    return occupancy, transitions


def _phi_from_path(path: Sequence[int]) -> List[float]:
    occupancy, transitions = _counts_from_path(path)
    return (
        [0.5 * float(v) / float(OBSERVATION_STEPS) for v in occupancy] +
        [0.5 * float(v) / float(OBSERVATION_STEPS) for v in transitions]
    )


def _late_phi_from_path(path: Sequence[int]) -> List[float]:
    late_path = list(path[-(LATE_STEPS + 1):])
    occupancy = [0] * ZONE_COUNT
    transitions = [0] * (ZONE_COUNT * ZONE_COUNT)
    for origin, destination in zip(late_path[:-1], late_path[1:]):
        occupancy[int(destination)] += 1
        transitions[int(origin) * ZONE_COUNT + int(destination)] += 1
    return (
        [0.5 * float(v) / float(LATE_STEPS) for v in occupancy] +
        [0.5 * float(v) / float(LATE_STEPS) for v in transitions]
    )


def _jsd(p: Sequence[float], q: Sequence[float]) -> float:
    midpoint = [(float(a) + float(b)) * 0.5 for a, b in zip(p, q)]

    def kl(a: Sequence[float], b: Sequence[float]) -> float:
        total = 0.0
        for x, y in zip(a, b):
            if x > 0.0:
                total += x * math.log(x / y)
        return total

    return 0.5 * kl(p, midpoint) + 0.5 * kl(q, midpoint)


def _run_condition(code: Optional[int], seed: int) -> Dict[str, Any]:
    system = TensorBasedNumogramSystem(seed=int(seed), dimension=DIMENSION)
    current = int(seed) % ZONE_COUNT

    for _ in range(BURN_IN_STEPS):
        event = system.transition(current, {})
        current = int(event["to"])

    if code is None:
        pulse_schedule: Sequence[Optional[int]] = [None] * PULSE_STEPS
    else:
        pulse_schedule = list(decimal_digits(code)) * PULSE_REPEATS

    for digit in pulse_schedule:
        context = {} if digit is None else {"zone_bias": _zone_bias(int(digit))}
        event = system.transition(current, context)
        current = int(event["to"])

    for _ in range(WASHOUT_STEPS):
        event = system.transition(current, {})
        current = int(event["to"])

    path = [current]
    for _ in range(OBSERVATION_STEPS):
        event = system.transition(current, {})
        current = int(event["to"])
        path.append(current)

    return {
        "seed": int(seed),
        "start_zone": int(seed) % ZONE_COUNT,
        "observation_path": path,
    }


def _mean(values: Sequence[float]) -> float:
    return float(sum(float(v) for v in values) / len(values)) if values else 0.0


def _quantile(values: Sequence[float], q: float) -> float:
    xs = sorted(float(v) for v in values)
    if not xs:
        raise ValueError("quantile requires values")
    if len(xs) == 1:
        return xs[0]
    pos = (len(xs) - 1) * float(q)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return xs[lo]
    w = pos - lo
    return xs[lo] * (1.0 - w) + xs[hi] * w


def _percentile(score: float, null_scores: Sequence[float]) -> float:
    below = sum(1 for value in null_scores if float(value) < float(score))
    equal = sum(1 for value in null_scores if float(value) == float(score))
    return 100.0 * (below + 0.5 * equal) / float(len(null_scores))


def _upper_rank_p(score: float, null_scores: Sequence[float]) -> float:
    at_least = sum(1 for value in null_scores if float(value) >= float(score))
    return (1.0 + float(at_least)) / (1.0 + float(len(null_scores)))


def _mean_pairwise_jsd(paths: Sequence[Sequence[int]]) -> float:
    vectors = [_phi_from_path(path) for path in paths]
    values: List[float] = []
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            values.append(_jsd(vectors[i], vectors[j]))
    return _mean(values)


def _holm_two(p1: float, p2: float) -> Tuple[float, float]:
    pairs = [(0, float(p1)), (1, float(p2))]
    pairs.sort(key=lambda item: item[1])
    adjusted = [1.0, 1.0]
    i0, p0 = pairs[0]
    i1, p1v = pairs[1]
    adjusted[i0] = min(1.0, 2.0 * p0)
    adjusted[i1] = max(adjusted[i0], min(1.0, p1v))
    return float(adjusted[0]), float(adjusted[1])


def _atomic_write_json(path: str, value: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    temp = path + ".tmp"
    with open(temp, "w", encoding="utf-8") as handle:
        handle.write(_canonical(value))
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("checkpoint must be a JSON object")
    return value


def _write_create_only(path: str, text: str) -> None:
    with open(path, "x", encoding="utf-8") as handle:
        handle.write(text)


def _checkpoint_path(archive_dir: str) -> str:
    return os.path.join(os.path.abspath(archive_dir), CHECKPOINT_NAME)


def _new_checkpoint(
    numogram_sha256: str,
    experiment_sha256: str,
    protocol_file_sha256: str,
    build_revision: str,
) -> Dict[str, Any]:
    return {
        "schema": SCHEMA,
        "protocol_sha256": PROTOCOL_SHA256,
        "discovery_evidence_sha256": DISCOVERY_EVIDENCE_SHA256,
        "build": {
            "numogram_sha256": str(numogram_sha256),
            "experiment_sha256": str(experiment_sha256),
            "protocol_file_sha256": str(protocol_file_sha256),
            "revision": str(build_revision),
        },
        "schedule": _schedule(),
        "shams": {},
        "codes": {},
        "final_summary": None,
        "created_at_epoch_ms": int(time.time() * 1000),
    }


def _load_or_create_checkpoint(
    archive_dir: str,
    numogram_sha256: str,
    experiment_sha256: str,
    protocol_file_sha256: str,
    build_revision: str,
) -> Tuple[str, Dict[str, Any]]:
    os.makedirs(archive_dir, exist_ok=True)
    path = _checkpoint_path(archive_dir)

    if os.path.exists(path):
        checkpoint = _read_json(path)
    else:
        checkpoint = _new_checkpoint(
            numogram_sha256,
            experiment_sha256,
            protocol_file_sha256,
            build_revision,
        )
        _atomic_write_json(path, checkpoint)

    if checkpoint.get("schema") != SCHEMA:
        raise RuntimeError("checkpoint schema mismatch")
    if checkpoint.get("protocol_sha256") != PROTOCOL_SHA256:
        raise RuntimeError("checkpoint protocol digest mismatch")
    if checkpoint.get("schedule") != _schedule():
        raise RuntimeError("checkpoint schedule mismatch")

    expected_build = {
        "numogram_sha256": str(numogram_sha256),
        "experiment_sha256": str(experiment_sha256),
        "protocol_file_sha256": str(protocol_file_sha256),
        "revision": str(build_revision),
    }
    if checkpoint.get("build") != expected_build:
        raise RuntimeError(
            "checkpoint build fingerprint mismatch; do not resume across APK builds"
        )

    return path, checkpoint


def checkpoint_status(archive_dir: str) -> str:
    path = _checkpoint_path(archive_dir)
    if not os.path.exists(path):
        return _canonical({
            "status": "not_started",
            "schema": SCHEMA,
            "protocol_sha256": PROTOCOL_SHA256,
        })

    checkpoint = _read_json(path)

    if checkpoint.get("final_summary") is not None:
        return _canonical(checkpoint["final_summary"])

    completed_shams = len(checkpoint.get("shams", {}))
    completed_codes = len(checkpoint.get("codes", {}))
    total_codes = len(_schedule())
    completed_units = completed_shams + completed_codes * len(SEEDS)
    total_units = len(SEEDS) + total_codes * len(SEEDS)

    return _canonical({
        "status": "in_progress",
        "schema": SCHEMA,
        "protocol_sha256": PROTOCOL_SHA256,
        "completed_shams": completed_shams,
        "total_shams": len(SEEDS),
        "completed_codes": completed_codes,
        "total_codes": total_codes,
        "percent": round(100.0 * completed_units / float(total_units), 2),
    })


def _code_record(code: int, shams: Dict[str, Any]) -> Dict[str, Any]:
    runs = []

    for seed in SEEDS:
        run = _run_condition(code, seed)
        sham = shams[str(seed)]

        runs.append({
            "seed": int(seed),
            "start_zone": int(seed) % ZONE_COUNT,
            "observation_path": run["observation_path"],
            "jsd_to_sham": _jsd(
                _phi_from_path(run["observation_path"]),
                _phi_from_path(sham["observation_path"]),
            ),
            "late_jsd_to_sham": _jsd(
                _late_phi_from_path(run["observation_path"]),
                _late_phi_from_path(sham["observation_path"]),
            ),
        })

    effects = [float(run["jsd_to_sham"]) for run in runs]
    late_effects = [float(run["late_jsd_to_sham"]) for run in runs]
    split = len(COHORT_A)

    return {
        "code": int(code),
        "digital_root": digital_root(code),
        "primary_score": _mean(effects),
        "cohort_a_score": _mean(effects[:split]),
        "cohort_b_score": _mean(effects[split:]),
        "late_score": _mean(late_effects),
        "cross_seed_dispersion": _mean_pairwise_jsd(
            [run["observation_path"] for run in runs]
        ),
        "runs": runs,
    }


def _seed_regime_analysis(
    records: Dict[int, Dict[str, Any]],
    controls: List[int],
) -> Dict[str, Any]:
    all_codes = controls + [TARGET_CODE]
    effects = {
        code: [float(run["jsd_to_sham"]) for run in records[code]["runs"]]
        for code in all_codes
    }

    control_seed_means = [
        _mean([effects[code][index] for code in controls])
        for index in range(len(SEEDS))
    ]
    control_grand = _mean([
        value
        for code in controls
        for value in effects[code]
    ])

    interaction_dispersion: Dict[int, float] = {}
    for code in all_codes:
        code_mean = _mean(effects[code])
        residuals = [
            effects[code][index]
            - code_mean
            - control_seed_means[index]
            + control_grand
            for index in range(len(SEEDS))
        ]
        interaction_dispersion[code] = float(statistics.pstdev(residuals))

    target_interaction = interaction_dispersion[TARGET_CODE]
    control_interactions = [interaction_dispersion[code] for code in controls]
    interaction_p = _upper_rank_p(target_interaction, control_interactions)

    start_zone_variance: Dict[int, float] = {}
    for code in all_codes:
        group_means = []
        for zone in range(ZONE_COUNT):
            values = [
                effects[code][index]
                for index, seed in enumerate(SEEDS)
                if int(seed) % ZONE_COUNT == zone
            ]
            group_means.append(_mean(values))
        start_zone_variance[code] = float(statistics.pvariance(group_means))

    target_zone = start_zone_variance[TARGET_CODE]
    control_zones = [start_zone_variance[code] for code in controls]
    zone_p = _upper_rank_p(target_zone, control_zones)

    q_interaction, q_zone = _holm_two(interaction_p, zone_p)

    per_seed = []
    for index, seed in enumerate(SEEDS):
        target_effect = effects[TARGET_CODE][index]
        null = [effects[code][index] for code in controls]
        per_seed.append({
            "seed": int(seed),
            "start_zone": int(seed) % ZONE_COUNT,
            "effect_jsd": target_effect,
            "percentile_vs_controls_same_seed": _percentile(target_effect, null),
        })

    return {
        "interaction_dispersion": {
            "target": target_interaction,
            "percentile": _percentile(target_interaction, control_interactions),
            "rank_p_upper": interaction_p,
            "holm_q": q_interaction,
            "held": q_interaction <= PRIMARY_ALPHA,
        },
        "start_zone_variance": {
            "target": target_zone,
            "percentile": _percentile(target_zone, control_zones),
            "rank_p_upper": zone_p,
            "holm_q": q_zone,
            "held": q_zone <= PRIMARY_ALPHA,
        },
        "per_seed_target_effects": per_seed,
    }


def _finalize(
    archive_dir: str,
    checkpoint: Dict[str, Any],
) -> Dict[str, Any]:
    controls = _control_codes()
    records = {
        int(code): record
        for code, record in checkpoint["codes"].items()
    }

    if set(records.keys()) != set(_schedule()):
        raise RuntimeError("cannot finalize before all codes complete")

    target = records[TARGET_CODE]
    control_records = [records[code] for code in controls]

    primary_null = [float(record["primary_score"]) for record in control_records]
    cohort_a_null = [float(record["cohort_a_score"]) for record in control_records]
    cohort_b_null = [float(record["cohort_b_score"]) for record in control_records]
    late_null = [float(record["late_score"]) for record in control_records]
    dispersion_null = [
        float(record["cross_seed_dispersion"])
        for record in control_records
    ]

    primary = {
        "target_code": TARGET_CODE,
        "control_count": len(controls),
        "primary_score_mean_jsd": float(target["primary_score"]),
        "primary_percentile": _percentile(
            float(target["primary_score"]), primary_null
        ),
        "rank_p_upper": _upper_rank_p(
            float(target["primary_score"]), primary_null
        ),
        "cohort_a_percentile": _percentile(
            float(target["cohort_a_score"]), cohort_a_null
        ),
        "cohort_b_percentile": _percentile(
            float(target["cohort_b_score"]), cohort_b_null
        ),
        "late_percentile": _percentile(
            float(target["late_score"]), late_null
        ),
        "cross_seed_dispersion": float(target["cross_seed_dispersion"]),
        "dispersion_75pct_threshold": _quantile(
            dispersion_null, DISPERSION_QUANTILE_GATE
        ),
    }

    primary["overall_rank_held"] = (
        primary["rank_p_upper"] <= PRIMARY_ALPHA
    )
    primary["split_replication_held"] = (
        primary["cohort_a_percentile"] >= SPLIT_PERCENTILE_GATE
        and primary["cohort_b_percentile"] >= SPLIT_PERCENTILE_GATE
    )
    primary["late_persistence_held"] = (
        primary["late_percentile"] >= LATE_PERCENTILE_GATE
    )
    primary["reproducibility_held"] = (
        primary["cross_seed_dispersion"]
        <= primary["dispersion_75pct_threshold"]
    )
    primary["replication_held"] = (
        primary["overall_rank_held"]
        and primary["split_replication_held"]
        and primary["late_persistence_held"]
        and primary["reproducibility_held"]
    )

    seed_regime = _seed_regime_analysis(records, controls)

    evidence = {
        "schema": SCHEMA,
        "protocol": PROTOCOL,
        "protocol_sha256": PROTOCOL_SHA256,
        "discovery_evidence_sha256": DISCOVERY_EVIDENCE_SHA256,
        "build": checkpoint["build"],
        "shams": checkpoint["shams"],
        "code_records": checkpoint["codes"],
        "primary_replication": primary,
        "secondary_seed_regime": seed_regime,
    }

    canonical = _canonical(evidence)
    digest = _sha256_bytes(canonical.encode("utf-8"))
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    filename = "p314r-666-replication-{}.json".format(stamp)
    archive_path = os.path.join(os.path.abspath(archive_dir), filename)

    _write_create_only(archive_path, canonical)
    _write_create_only(
        archive_path + ".sha256",
        digest + "  " + filename + "\n",
    )

    return {
        "schema": SCHEMA,
        "status": "completed",
        "protocol_sha256": PROTOCOL_SHA256,
        "discovery_evidence_sha256": DISCOVERY_EVIDENCE_SHA256,
        "build": checkpoint["build"],
        "primary_replication": primary,
        "secondary_seed_regime": {
            "interaction_dispersion": seed_regime["interaction_dispersion"],
            "start_zone_variance": seed_regime["start_zone_variance"],
        },
        "replication_held": bool(primary["replication_held"]),
        "advance_to_p314b": bool(primary["replication_held"]),
        "next_required_stage": (
            "P3.14B topology/label-shuffle falsification"
            if primary["replication_held"]
            else (
                "stop 666 operator-specificity claim; preserve secondary "
                "seed-regime findings as a separate mechanistic result"
            )
        ),
        "evidence_sha256": digest,
        "archive_file": archive_path,
    }


def run_next(
    archive_dir: str,
    numogram_sha256: str,
    experiment_sha256: str,
    protocol_file_sha256: str,
    build_revision: str,
) -> str:
    """Execute one checkpoint chunk and return progress or final results."""
    try:
        path, checkpoint = _load_or_create_checkpoint(
            archive_dir,
            numogram_sha256,
            experiment_sha256,
            protocol_file_sha256,
            build_revision,
        )

        if checkpoint.get("final_summary") is not None:
            return _canonical(checkpoint["final_summary"])

        shams = checkpoint["shams"]

        if len(shams) < len(SEEDS):
            remaining = [
                seed
                for seed in SEEDS
                if str(seed) not in shams
            ][:SHAMS_PER_CHUNK]

            for seed in remaining:
                shams[str(seed)] = _run_condition(None, seed)

            _atomic_write_json(path, checkpoint)

            return _canonical({
                "status": "progress",
                "phase": "sham_reference",
                "protocol_sha256": PROTOCOL_SHA256,
                "completed_shams": len(shams),
                "total_shams": len(SEEDS),
                "completed_codes": 0,
                "total_codes": len(_schedule()),
                "percent": round(
                    100.0 * len(shams)
                    / float(len(SEEDS) + len(_schedule()) * len(SEEDS)),
                    2,
                ),
                "partial_inferential_results_withheld": True,
            })

        codes = checkpoint["codes"]
        pending = [
            code
            for code in checkpoint["schedule"]
            if str(code) not in codes
        ]

        for code in pending[:CODES_PER_CHUNK]:
            codes[str(code)] = _code_record(int(code), shams)
            _atomic_write_json(path, checkpoint)

        if len(codes) < len(checkpoint["schedule"]):
            completed_units = len(SEEDS) + len(codes) * len(SEEDS)
            total_units = len(SEEDS) + len(checkpoint["schedule"]) * len(SEEDS)

            return _canonical({
                "status": "progress",
                "phase": "root9_population",
                "protocol_sha256": PROTOCOL_SHA256,
                "completed_shams": len(SEEDS),
                "total_shams": len(SEEDS),
                "completed_codes": len(codes),
                "total_codes": len(checkpoint["schedule"]),
                "percent": round(
                    100.0 * completed_units / float(total_units),
                    2,
                ),
                "partial_inferential_results_withheld": True,
            })

        summary = _finalize(archive_dir, checkpoint)
        checkpoint["final_summary"] = summary
        _atomic_write_json(path, checkpoint)

        final_summary_path = os.path.join(
            os.path.abspath(archive_dir),
            FINAL_SUMMARY_NAME,
        )
        if not os.path.exists(final_summary_path):
            _write_create_only(final_summary_path, _canonical(summary))

        return _canonical(summary)

    except Exception as error:
        return _canonical({
            "status": "error",
            "schema": SCHEMA,
            "error_type": type(error).__name__,
            "message": str(error),
            "protocol_sha256": PROTOCOL_SHA256,
        })
