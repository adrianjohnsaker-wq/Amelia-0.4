"""
OUTSIDE-1 v2.1 Publication Series
Prospective publication-grade evidence wrapper around the frozen v2 apparatus.

This module does NOT change:
- canonical Numogram graph/dynamics/interface
- D3 traversal law
- N1 degree-matched null
- 12-passage trace
- one destination-zone fragment per passage
- target generator/category logic
- language composition prompt
- blind judge prompt
- D1 threshold, D2 threshold, or positive-control gate

It adds:
- canonical-json-v1-sorted-keys-utf8 envelopes
- UTC timestamps
- event IDs and parent hashes
- externally recomputable payload/event/channel digests
- source/build registration
- method transcripts for language-model calls
- raw entropy records for blind assignment, judge order, and post-ranking target draw
- machine-auditable publication ledger

W001-W006 remain frozen pilot/procedural evidence and are excluded from this series.
The publication series begins at W007 and contains 100 prospective workings W007-W106.
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import re
import secrets
import sys
from datetime import datetime, timezone
from typing import Dict, List, Sequence

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import Outside1_v2 as O

SERIES_ID = "OUTSIDE-1-v2.1-publication"
VERSION = "2.1.0"
SERIES_START = 7
SERIES_STOP = 106
SERIES_N = 100
REGISTRATION_FILE = "outside1_v2_1_registration.json"
CALIBRATION_SEAL = "outside1_v2_1_calibration_seal.json"
PILOT_FREEZE = "outside1_v2_pilot_freeze.json"
LEDGER = os.path.join(HERE, "ledger_v2_1_publication.jsonl")
SERIALIZATION = "canonical-json-v1-sorted-keys-utf8"

D1_CAST_START = 198001
D1_CAST_STOP = 199001
D1_MAX = 0.50
D2_SEEDS = tuple(range(197001, 197005))
D2_REQUIRED = 6
CONTROL_TRIALS = 20
CONTROL_REQUIRED = 10

PROTOCOL = {
    "series_id": SERIES_ID,
    "version": VERSION,
    "registration_date": "2026-10-04",
    "pilot_block": {
        "designation": "OUTSIDE-1 v2 pilot/procedural evidence",
        "freeze_file": PILOT_FREEZE,
        "workings": ["W001","W002","W003","W004","W005","W006"],
        "inferential_use": "excluded",
    },
    "frozen_parent": {
        "apparatus_protocol_sha256": O.PROTOCOL_SHA256,
        "canonical_runtime_digest": O.CANONICAL_DIGEST,
        "graph_digest": "9760268dd784186434ea3d86efd2f8ae9f861b245f64f58c97f70f1e75fb3087",
        "law": "D3 Lemurian traversal",
        "null": "N1 degree-matched typed rewiring",
        "passages": 12,
        "reader_rule": "one source-locked fragment per recorded passage from destination zone only",
        "compose_prompt": "unchanged from OUTSIDE-1 v2.0.0",
        "judge_prompt": "unchanged from OUTSIDE-1 v2.0.0",
        "target_generator": "unchanged from OUTSIDE-1 v2.0.0",
    },
    "publication_series": {
        "first_working": "W007",
        "last_working": "W106",
        "n_workings": SERIES_N,
        "question": O.PROTOCOL["question"],
        "cast": O.PROTOCOL["cast"],
        "no_interim_analysis": True,
        "arm_identity_release": "after W106 final analysis only",
    },
    "calibration": {
        "D1": {
            "fresh_casts": [D1_CAST_START, D1_CAST_STOP - 1],
            "n": 1000,
            "statistic": "mean canonical/null Jaccard overlap of dealt fragment-text sets",
            "pass_max": D1_MAX,
        },
        "D2": {
            "fresh_seeds": list(D2_SEEDS),
            "panel": "4 fresh seeds x canonical/null = 8 compositions",
            "criterion": "independent source-list identification >= 6/8",
            "supplementary_audit": "all dealt fragments must appear verbatim in each composition",
        },
        "positive_control": {
            "fresh_trials": CONTROL_TRIALS,
            "criterion_first_place_min": CONTROL_REQUIRED,
            "target": "fixed preregistered control randomization before composition",
            "signal": "one concrete target-bearing word appended to dealt fragments",
            "role": "instrument sensitivity only; not contact evidence",
        },
        "gate": "D1 PASS AND D2 PASS AND positive-control >=10/20 before W007",
    },
    "evidence_schema": {
        "serialization": SERIALIZATION,
        "required_event_fields": [
            "schema_version","series_id","event_seq","event_id","event_type",
            "working_id","created_utc","serialization","protocol_sha256",
            "registration_sha256","parent_event_hash","payload_sha256","payload","event_hash"
        ],
        "raw_channels": [
            "cast input","canonical trace","null trace","canonical fragments","null fragments",
            "slot assignment entropy","judge-order entropy","composition prompt/output/method",
            "judge prompt/output/method","pre-draw state commitment","target-draw entropy","resolution"
        ],
        "language_method_required": [
            "provider","model","interface","reasoning_effort","temperature_status",
            "provider_request_id_status","generation_time_status"
        ],
        "no_backfill": True,
    },
    "primary": O.PROTOCOL["primary"],
    "stop_rule": (
        "No W007 may be admitted until v2.1 registration is sealed and fresh D1, D2, "
        "and 20-trial positive control all pass under this evidence schema. "
        "No W001-W006 record may be repaired into publication evidence."
    ),
}
PROTOCOL_SHA256 = O.sha(PROTOCOL)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00","Z")


def canonical_json(x) -> str:
    return O.canonical_json(x)


def sha(x) -> str:
    return O.sha(x)


def file_sha256(path: str) -> str:
    return O.file_sha256(path)


def registration_path() -> str:
    return os.path.join(HERE, REGISTRATION_FILE)


def load_registration() -> dict:
    with open(registration_path(), encoding="utf-8") as f:
        return json.load(f)


def check_registration() -> dict:
    r = load_registration()
    if r["protocol_sha256"] != PROTOCOL_SHA256:
        raise RuntimeError("v2.1 protocol hash mismatch")
    if r["parent_protocol_sha256"] != O.PROTOCOL_SHA256:
        raise RuntimeError("frozen parent protocol mismatch")
    if r["canonical_runtime_digest"] != O.CANONICAL_DIGEST:
        raise RuntimeError("canonical digest mismatch")
    return r


def calibration_open() -> dict:
    check_registration()
    p = os.path.join(HERE, CALIBRATION_SEAL)
    if not os.path.exists(p):
        raise RuntimeError("publication calibration seal absent")
    with open(p, encoding="utf-8") as f:
        x = json.load(f)
    if not (x.get("D1",{}).get("pass") and x.get("D2",{}).get("pass") and x.get("positive_control",{}).get("pass")):
        raise RuntimeError("publication calibration gate not passed")
    return x


# ---------------------------------------------------------------------------
# Deterministic audit helpers
# ---------------------------------------------------------------------------

def channel_digest(x) -> str:
    return sha(x)


def keyed_permutation4(entropy_hex: str, domain: str) -> List[int]:
    raw = bytes.fromhex(entropy_hex)
    scored = []
    for i in range(4):
        d = hashlib.sha256(raw + domain.encode("utf-8") + bytes([i])).digest()
        scored.append((d, i))
    scored.sort()
    return [i for _,i in scored]


def binary_choice(entropy_hex: str, domain: str) -> int:
    raw = bytes.fromhex(entropy_hex)
    d = hashlib.sha256(raw + domain.encode("utf-8")).digest()
    return d[0] & 1


def target_choice(entropy_hex: str) -> int:
    raw = bytes.fromhex(entropy_hex)
    d = hashlib.sha256(raw + b":target-draw").digest()
    return int.from_bytes(d, "big") % 4


def language_method(provider: str, model: str, interface: str,
                    reasoning_effort: str = "not_exposed",
                    temperature_status: str = "not_exposed",
                    provider_request_id_status: str = "not_exposed",
                    generation_time_status: str = "sealed_immediately_after_generation") -> dict:
    return {
        "provider": provider,
        "model": model,
        "interface": interface,
        "reasoning_effort": reasoning_effort,
        "temperature_status": temperature_status,
        "provider_request_id_status": provider_request_id_status,
        "generation_time_status": generation_time_status,
    }


def validate_method(m: dict) -> None:
    req = PROTOCOL["evidence_schema"]["language_method_required"]
    missing = [k for k in req if k not in m]
    if missing:
        raise ValueError("method transcript missing: " + ",".join(missing))


# ---------------------------------------------------------------------------
# Fresh publication-series diagnostics
# ---------------------------------------------------------------------------

def diagnose_D1() -> dict:
    check_registration()
    lx = O.lexicon()
    sims, lens = [], []
    rows = []
    for s in range(D1_CAST_START, D1_CAST_STOP):
        k = (s % 100) + 1
        tc = O.trace(O.graph("canonical", k), s)
        tn = O.trace(O.graph("null", k), s)
        fc = O.deal(tc, lx)
        fn = O.deal(tn, lx)
        jc = O.jaccard([f["text"] for f in fc], [f["text"] for f in fn])
        sims.append(jc); lens.append(len(fc))
        rows.append({
            "seed":s,"working_number":k,
            "canonical_trace_sha256":channel_digest(tc),
            "null_trace_sha256":channel_digest(tn),
            "canonical_fragments_sha256":channel_digest(fc),
            "null_fragments_sha256":channel_digest(fn),
            "jaccard":jc,
        })
    mean = sum(sims)/len(sims)
    return {
        "diagnostic":"D1",
        "created_utc":utc_now(),
        "n":len(sims),
        "mean_jaccard_canonical_null":mean,
        "mean_fragments_per_trace":sum(lens)/len(lens),
        "threshold_max":D1_MAX,
        "pass":mean <= D1_MAX,
        "rows":rows,
        "rows_sha256":channel_digest(rows),
    }


def d2_panel() -> List[dict]:
    check_registration()
    out=[]
    lx=O.lexicon()
    for s in D2_SEEDS:
        number=(s-D2_SEEDS[0])+1
        for arm in ("canonical","null"):
            tr=O.trace(O.graph(arm,number),s)
            fr=O.deal(tr,lx)
            prompt=O.COMPOSE_PROMPT.format(
                fragments="\n".join("%d. %s"%(i+1,f["text"]) for i,f in enumerate(fr))
            )
            out.append({
                "panel_id":"D2-%d-%s"%(s,arm),
                "seed":s,"arm":arm,
                "trace":tr,
                "trace_sha256":channel_digest(tr),
                "fragments":fr,
                "fragments_sha256":channel_digest(fr),
                "compose_prompt":prompt,
                "compose_prompt_sha256":hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            })
    return out


# ---------------------------------------------------------------------------
# Fresh v2.1 positive-control materials
# ---------------------------------------------------------------------------

def _pc_rng(label: str) -> random.Random:
    h=hashlib.sha256(("OUTSIDE1-v2.1-control:"+label).encode("utf-8")).hexdigest()
    return random.Random(int(h[:16],16))


def positive_control_trial(i: int) -> dict:
    if not 1 <= i <= CONTROL_TRIALS:
        raise ValueError(i)
    ident="PC%02d"%i
    quartet=O.target_quartet(ident)
    rr=_pc_rng(ident)
    target_index=rr.randrange(4)
    word=O.signal_word(quartet[target_index]["text"])
    cast=O._synthetic_cast(int(hashlib.sha256((ident+":cast").encode()).hexdigest()[:16],16))
    seed=O.seed_of(ident,cast)
    tr=O.trace(O.graph("canonical",i),seed)
    fr=O.deal(tr)
    texts=[f["text"] for f in fr]+[word]
    order=list(range(4)); rr.shuffle(order)
    labels="ABCD"
    candidates=[{"label":labels[k],"scene":quartet[idx]["text"],"pool_index":idx} for k,idx in enumerate(order)]
    prompt=O.COMPOSE_PROMPT.format(
        fragments="\n".join("%d. %s"%(n+1,t) for n,t in enumerate(texts))
    )
    return {
        "id":ident,
        "cast":cast,
        "seed":seed,
        "trace":tr,
        "trace_sha256":channel_digest(tr),
        "fragments":texts,
        "fragments_sha256":channel_digest(texts),
        "compose_prompt":prompt,
        "compose_prompt_sha256":hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "candidates":candidates,
        "target_index":target_index,
        "target_label":labels[order.index(target_index)],
        "signal_word":word,
    }


def positive_control_public(i:int)->dict:
    x=positive_control_trial(i)
    return {
        "id":x["id"],
        "fragments":x["fragments"],
        "compose_prompt":x["compose_prompt"],
        "compose_prompt_sha256":x["compose_prompt_sha256"],
        "candidates":[{"label":c["label"],"scene":c["scene"]} for c in x["candidates"]],
    }


def resolve_positive_control(rankings: Dict[str,Sequence[str]]) -> dict:
    hits=0; rank_sum=0; rows=[]
    for i in range(1,CONTROL_TRIALS+1):
        x=positive_control_trial(i)
        ranking=list(rankings[x["id"]])
        if sorted(ranking)!=list("ABCD"):
            raise ValueError("bad ranking "+x["id"])
        rank=ranking.index(x["target_label"])+1
        hits += rank==1; rank_sum += rank
        rows.append({"id":x["id"],"rank":rank})
    return {
        "created_utc":utc_now(),
        "hits_first":hits,
        "mean_rank":rank_sum/CONTROL_TRIALS,
        "criterion":CONTROL_REQUIRED,
        "pass":hits>=CONTROL_REQUIRED,
        "rows":rows,
        "rows_sha256":channel_digest(rows),
    }
