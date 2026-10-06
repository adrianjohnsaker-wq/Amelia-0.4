"""
OUTSIDE-2 -- Numogram-as-reader. Amelia Interface Programme. Version 1.1.0.

Successor to OUTSIDE-1 v2.1 (closed 6 October 2026 for instrument fault; see
publication_v2_1/OUTSIDE1_V2_1_CLOSURE.json). Registered as a separate experiment under the
operator's standing rule that a failed language-mediated reader is replaced by a
Numogram-as-reader design, not repaired.

Design. The querent holds the fixed question and makes a 32-toss physical cast. The cast seeds a
twelve-passage D3 Lemurian trace through the sealed canonical Numogram and, with the same seed,
through a fresh N1 degree-matched null. There is no language layer in evaluation: the trace is the
reading. Each working has a quartet of four candidate scenes fixed before the cast; each candidate
is a disjoint pair of zones, displayed through the registered source-locked fragments of those
zones, so every candidate is expressible by the reader by construction. A candidate's score in an
arm is the mid-percentile of the number of passages reaching its zones, against that arm's own
frozen reference distribution, so that no zone is favoured by base rates. After the reading is
sealed and published, the target is drawn from a public randomness beacon round fixed by the
reading's timestamp, so that the draw can be recomputed by anyone and cannot be repeated.
P1 and P2 are exact randomization tests over the target draw, evaluated once, after W100.

Version 1.1.0 supersedes the unpublished 1.0.0 registration (registration file SHA-256
83af4d296bc798af953639f9c1dfadad207bef321fbed2898db5b7831c940ef0) before publication and before
any working, after an independent review found that a locally drawn target could be re-drawn by
truncating the ledger, and that the calibration seal was not bound into the ledger.

Commands (run from amelia-1/outside):
  register                     write outside2_registration.json (refuses to overwrite a different one)
  reference                    build outside2_reference.json from registered reference seeds
  calibrate                    run the registered pre-data gate (C1-C4); deterministic and re-runnable
  cast W### TOSSES             admit a working: CAST and READING events, written together
  beacon W###                  print the beacon round fixed for this working and its public URL
  resolve W### RANDOMNESS SIG  resolve with the beacon round's randomness and signature (hex)
  feedback W###                querent feedback: target scene and both readings
  status | verify              ledger state; verify replays every event from first principles
  analyse                      final P1/P2; refuses unless W013-W100 are all resolved
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import random
import sys
from datetime import datetime, timezone
from typing import Dict, List, Sequence

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import Outside1_v2 as O  # frozen mechanics: graph(), trace(), seed_of(), lexicon(), deal()

SERIES_ID = "OUTSIDE-2-numogram-reader"
VERSION = "1.1.0"
FIRST, LAST = 13, 100
WORKINGS = ["W%03d" % i for i in range(FIRST, LAST + 1)]
N = len(WORKINGS)  # 88
PASSAGES = O.PASSAGES  # 12
REF_CASTS = 4000
REGISTRATION_FILE = "outside2_registration.json"
REFERENCE_FILE = "outside2_reference.json"
CALIBRATION_FILE = "outside2_calibration_seal.json"
LEDGER = os.path.join(HERE, "ledger_outside2.jsonl")
SERIALIZATION = "canonical-json-v1-sorted-keys-utf8"

# Public randomness beacon: drand League of Entropy, quicknet
BEACON = {
    "network": "drand quicknet",
    "chain_hash": "52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971",
    "genesis_time": 1692803367,
    "period": 3,
    "scheme": "bls-unchained-g1-rfc9380",
    "url": "https://api.drand.sh/52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971/public/{round}",
}
BEACON_DELAY = 600  # seconds between READING timestamp and the beacon round used

# Pre-data gate (calibration on synthetic casts only)
CAL_POOL_PER_WORKING = 1000
C1_BAND = (0.18, 0.32)
C2_SERIES = 1000
C2_MAX = 0.065
C3_SERIES = 200
C3_MIN = 0.95
C4_SERIES = 200
C4_K = 2
C4_MIN_P1 = 0.95
C4_MIN_P2 = 0.80
CURVE = (0.10, 0.20, 0.30, 0.45, 0.60)
ALPHA = 0.05

PROTOCOL = {
    "series_id": SERIES_ID,
    "version": VERSION,
    "registration_date": "2026-10-06",
    "supersedes": {
        "version": "1.0.0",
        "registration_file_sha256": "83af4d296bc798af953639f9c1dfadad207bef321fbed2898db5b7831c940ef0",
        "status": "never published; no working, reference-gated cast or target draw occurred under it",
        "reason": "independent pre-publication review: locally drawn target could be re-drawn by ledger truncation; calibration seal not bound into the ledger; RESOLVED events carried target ranks; on-channel control needed an apparatus-producible counterpart",
    },
    "predecessor": {
        "series": "OUTSIDE-1-v2.1-publication",
        "status": "CLOSED_INSTRUMENT_FAULT after W012",
        "closure_file": "publication_v2_1/OUTSIDE1_V2_1_CLOSURE.json",
        "pooling": "none; W007-W012 are never pooled with OUTSIDE-2",
    },
    "operator_ruling": (
        "6 October 2026: close OUTSIDE-1 v2.1 as the instrumentation is faulty; continue from W013 to "
        "W100 under the Numogram-as-reader design, with a target pool built only from what the reader "
        "can express, so that channel capacity is checked before any working."
    ),
    "frozen_mechanics": {
        "module": "Outside1_v2.py (graph, trace, seed_of; unchanged)",
        "canonical_runtime_digest": O.CANONICAL_DIGEST,
        "graph_digest": "9760268dd784186434ea3d86efd2f8ae9f861b245f64f58c97f70f1e75fb3087",
        "law": "D3 Lemurian traversal",
        "null": "N1 degree-matched typed rewiring, fresh instance per working: n1_degree_matched(93000 + k) for working Wk",
        "passages": PASSAGES,
    },
    "generation": {
        "querent": "holds the fixed question during the physical cast",
        "question": "what is the scene that will be shown at the close of this working?",
        "cast": "32 physical coin tosses H/T; seed = int(SHA-256(working id + ':' + tosses)[:16], 16)",
        "workings": [WORKINGS[0], WORKINGS[-1]],
        "n": N,
        "admission": "workings are admitted strictly in order; every cast the querent makes for a working is admitted; no cast may be discarded or repeated",
    },
    "reader": {
        "kind": "Numogram-as-reader; no language layer in evaluation",
        "reading": "the ordered destination zones of the twelve recorded passages, per arm",
        "score": "for candidate zone pair S: c = number of passages whose destination is in S; score = P(C < c) + 0.5 P(C = c) under the same arm's frozen reference distribution of C for S",
        "reference": "4000 reference casts per graph; graph tags 'canonical' and 'null:W###'; seeds int(SHA-256('OUTSIDE-2:reference:canonical:' + i)[:16], 16) and int(SHA-256('OUTSIDE-2:reference:null:' + W + ':' + i)[:16], 16), i < 4000; frozen in outside2_reference.json before any working",
        "ranking": "candidates ranked by score, higher first; ties take mid-ranks",
    },
    "target_pool": {
        "quartet": "for working W: zones 0-9 shuffled by random.Random(int(SHA-256('OUTSIDE-2:quartet:' + W)[:16], 16)); candidates are the disjoint pairs (z0,z1), (z2,z3), (z4,z5), (z6,z7)",
        "expressibility": "every candidate is a set of zones the reader emits; coverage is tested in C1",
        "displayed_scene": "the registered lexicon_v2 fragments of the candidate's two zones, in zone order; display only, no role in scoring; no demon names",
    },
    "target_draw": {
        "source": "drand quicknet public randomness beacon (chain hash 52db9ba7...e971, genesis 1692803367, period 3 s)",
        "round": "r = ceil((t_reading + 600 - 1692803367) / 3) + 1, where t_reading is the READING event's created_utc in Unix seconds; the first round at or after 600 s past the reading",
        "index": "target index = int(SHA-256(randomness bytes || UTF-8(W + ':target-draw')), big-endian) mod 4",
        "publication": "the commit containing the CAST and READING events is pushed to the public repository before the beacon round's time; a late push is recorded and reported, and never grounds for discarding the working",
        "audit": "anyone can fetch the round from the beacon, check randomness = SHA-256(signature) and recompute the target",
    },
    "primary": {
        "P1": "one-sided exact randomization test over the target draw: T1 = sum over workings of the canonical arm's mid-rank of the target; p1 = P(T1' <= T1)",
        "P2": "one-sided exact randomization test over the target draw: T2 = sum over workings of (null mid-rank - canonical mid-rank) of the target; p2 = P(T2' >= T2)",
        "alpha": ALPHA,
        "interpretation": "P1 alone: departure from chance in the canonical apparatus. P2: the effect follows the content of the canonical trace rather than the same-seed null trace. P2 does not by itself show that the canonical graph structure is necessary; that requires the registered follow-up of perturbation specificity (lesions to canonical relations).",
        "no_interim_analysis": True,
    },
    "early_closure": "The series may close before W100 only for a software or apparatus fault demonstrated on synthetic data and independently audited. Outcome-based stopping is prohibited. On any closure, all completed workings are analysed and reported with the same tests.",
    "calibration_gate": {
        "data": "synthetic casts only: pool seeds int(SHA-256('OUTSIDE-2:calibration:' + W + ':' + i)[:16], 16), i < 1000 per working; series sample the pool uniformly with replacement using random.Random(int(SHA-256('OUTSIDE-2:calibration-series')[:16], 16)) in the order C2, C3, C4, curve",
        "C1_coverage": "for both arms and every zone z: among pool casts of workings whose quartet contains z, the share in which the candidate containing z is ranked first (a k-way tie for first counts 1/k) lies in [0.18, 0.32]",
        "C2_type_I": "1000 simulated series with no signal: empirical rejection at alpha 0.05 <= 0.065 for P1 and for P2 (a code check; the tests are exact)",
        "C3_trace_plant_control": "200 series: in every working the destination of one uniformly chosen canonical passage is replaced by a uniformly chosen zone of the target pair (it may already lie there): rejection >= 0.95 for P1 and for P2",
        "C4_seed_selection_control": "200 series: in every working two pool casts are sampled and the one whose canonical trace has more passages in the target pair is used for both arms (first on ties): rejection >= 0.95 for P1 and >= 0.80 for P2. This signal is producible by the apparatus itself, entering through the cast",
        "curve": "descriptive: C3-type plant applied to each working independently with probability 0.10, 0.20, 0.30, 0.45, 0.60; 200 series each; reported, not gated",
        "thresholds": "set with knowledge of design-stage simulations on synthetic casts; no working data existed",
        "rule": "W013 may not be admitted unless C1-C4 all pass. If any fails, the apparatus is not modified within this registration. The calibration seal's SHA-256 is recorded in every CAST event.",
    },
    "evidence": {
        "serialization": SERIALIZATION,
        "events_per_working": ["CAST", "READING", "RESOLVED"],
        "atomicity": "CAST and READING are written in one append",
        "fields": ["series_id", "event_seq", "event_id", "event_type", "working", "created_utc",
                   "protocol_sha256", "registration_sha256", "parent_event_hash", "payload_sha256",
                   "payload", "event_hash"],
        "verify": "replays every event: chain links, payload digests, registration and protocol digests, calibration seal, seed from tosses, both traces and scores from the seed, beacon round from the READING timestamp, randomness = SHA-256(signature), and the target index",
        "no_backfill": True,
        "arm_labels": "recorded openly in the ledger; scoring is mechanical, so there is no judge to blind. Querent feedback presents the readings in an order fixed by the working id; this is presentation, not a blinding measure",
        "resolved_payload": "beacon round, randomness, signature, target index and pair only; target ranks are not written to the ledger",
    },
    "residual_trust": "The reading timestamp is written by the operator. The defence against re-casting a working is the public push before the beacon round, the admission rule, and the querent's own record of each cast. These are stated as procedural, not cryptographic, guarantees.",
    "claims": {
        "permitted_on_success": "register 1 (P1 and/or P2 departures) and register 2 (canonical-trace-specific information if P2); access, not agency or communication",
        "on_failure": "the registered claim that this canonical apparatus selects target-related information under these conditions is not supported",
    },
}


# ---------------------------------------------------------------------------
# serialization and registration
# ---------------------------------------------------------------------------

def cj(x) -> str:
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha(x) -> str:
    b = x if isinstance(x, bytes) else cj(x).encode("utf-8")
    return hashlib.sha256(b).hexdigest()


def fsha(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


PROTOCOL_SHA256 = sha(PROTOCOL)


def _h16(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], 16)


def registration_payload() -> dict:
    return {
        "series_id": SERIES_ID,
        "version": VERSION,
        "protocol": PROTOCOL,
        "protocol_sha256": PROTOCOL_SHA256,
        "beacon": BEACON,
        "canonical_runtime_digest": O.C.CanonicalNumogram().digest(),
        "graph_digest": O.D.canonical_graph().digest(),
        "sources": {
            "Outside2.py": fsha(__file__),
            "Outside1_v2.py": fsha(O.__file__),
            "lexicon_v2.json": fsha(os.path.join(HERE, O.LEXICON_FILE)),
            "CanonicalNumogram.py": fsha(O.C.__file__),
            "NumogramDynamics.py": fsha(O.D.__file__),
            "NumogramInterface.py": fsha(O.I.__file__),
            "NullInterfaces.py": fsha(O.N.__file__),
            "OUTSIDE1_V2_1_CLOSURE.json": fsha(os.path.join(HERE, "publication_v2_1", "OUTSIDE1_V2_1_CLOSURE.json")),
        },
    }


def _load(name: str):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def _write_once(name: str, payload) -> None:
    p = os.path.join(HERE, name)
    if os.path.exists(p):
        if _load(name) != payload:
            raise RuntimeError("%s exists and differs; refuse overwrite" % name)
        return
    with open(p, "w", encoding="utf-8") as f:
        json.dump(payload, f, sort_keys=True, indent=1, ensure_ascii=False)
        f.write("\n")


def register() -> dict:
    if O.C.CanonicalNumogram().digest() != O.CANONICAL_DIGEST:
        raise RuntimeError("canonical digest mismatch")
    p = registration_payload()
    _write_once(REGISTRATION_FILE, p)
    return p


def check_registered() -> dict:
    got = _load(REGISTRATION_FILE)
    if got is None:
        raise RuntimeError("not registered")
    if got != registration_payload():
        raise RuntimeError("registered apparatus differs from current files")
    return got


def registration_sha256() -> str:
    return fsha(os.path.join(HERE, REGISTRATION_FILE))


# ---------------------------------------------------------------------------
# quartet, traces, reference, scoring
# ---------------------------------------------------------------------------

def wnum(w: str) -> int:
    if w not in WORKINGS:
        raise ValueError("working outside OUTSIDE-2 range: %s" % w)
    return int(w[1:])


def quartet(w: str) -> List[List[int]]:
    z = list(range(10))
    random.Random(_h16("OUTSIDE-2:quartet:" + w)).shuffle(z)
    return [sorted(z[2 * i:2 * i + 2]) for i in range(4)]


_GRAPHS: Dict[str, object] = {}


def graph(arm: str, w: str):
    key = arm if arm == "canonical" else "null:" + w
    if key not in _GRAPHS:
        _GRAPHS[key] = O.graph("canonical", 0) if arm == "canonical" else O.graph("null", wnum(w))
    return _GRAPHS[key]


def dsts(arm: str, w: str, seed: int) -> List[int]:
    return [int(p["dst"]) for p in O.trace(graph(arm, w), seed)]


def count_in(ds: Sequence[int], pair: Sequence[int]) -> int:
    return sum(1 for d in ds if d in pair)


def _hist(vectors: List[List[int]], pair) -> List[int]:
    h = [0] * (PASSAGES + 1)
    for v in vectors:
        h[count_in(v, pair)] += 1
    return h


def build_reference() -> dict:
    check_registered()
    canon = [dsts("canonical", WORKINGS[0], _h16("OUTSIDE-2:reference:canonical:%d" % i)) for i in range(REF_CASTS)]
    out = {"series_id": SERIES_ID, "ref_casts": REF_CASTS, "registration_sha256": registration_sha256(), "workings": {}}
    for w in WORKINGS:
        nul = [dsts("null", w, _h16("OUTSIDE-2:reference:null:%s:%d" % (w, i))) for i in range(REF_CASTS)]
        q = quartet(w)
        out["workings"][w] = {
            "quartet": q,
            "canonical_hist": [_hist(canon, p) for p in q],
            "null_hist": [_hist(nul, p) for p in q],
        }
    _write_once(REFERENCE_FILE, out)
    return out


_REF = None


def reference() -> dict:
    global _REF
    if _REF is None:
        _REF = _load(REFERENCE_FILE)
        if _REF is None:
            raise RuntimeError("reference not built")
        if _REF["registration_sha256"] != registration_sha256():
            raise RuntimeError("reference not bound to this registration")
    return _REF


def midpct(hist: List[int], c: int) -> float:
    n = sum(hist)
    return (sum(hist[:c]) + 0.5 * hist[c]) / n


def scores(ds: Sequence[int], hists: List[List[int]], q) -> List[float]:
    return [midpct(hists[j], count_in(ds, q[j])) for j in range(4)]


def ranks2(sc: Sequence[float]) -> List[int]:
    """Doubled mid-ranks (2..8): rank 1 -> 2, a two-way tie for first -> 3, etc."""
    return [2 * sum(1 for t in sc if t > s) + sum(1 for t in sc if t == s) + 1 for s in sc]


def read(w: str, ds_c: Sequence[int], ds_n: Sequence[int]) -> dict:
    r = reference()["workings"][w]
    q = r["quartet"]
    sc_c = scores(ds_c, r["canonical_hist"], q)
    sc_n = scores(ds_n, r["null_hist"], q)
    return {"quartet": q, "canonical": {"dst": list(ds_c), "scores": sc_c, "ranks2": ranks2(sc_c)},
            "null": {"dst": list(ds_n), "scores": sc_n, "ranks2": ranks2(sc_n)}}


# ---------------------------------------------------------------------------
# exact tests
# ---------------------------------------------------------------------------

def exact_tail(values: List[List[int]], observed: int, lower: bool) -> float:
    """Each working contributes one of its 4 integer values with probability 1/4 (target draw)."""
    dist = {0: 1}
    for vals in values:
        nd: Dict[int, int] = {}
        for s, c in dist.items():
            for v in vals:
                nd[s + v] = nd.get(s + v, 0) + c
        dist = nd
    tot = 4 ** len(values)
    hit = sum(c for s, c in dist.items() if (s <= observed if lower else s >= observed))
    return hit / tot


def primary(rows: List[dict]) -> dict:
    """rows: per working {'can': ranks2[4], 'nul': ranks2[4], 'target': index}."""
    v1 = [r["can"] for r in rows]
    t1 = sum(r["can"][r["target"]] for r in rows)
    v2 = [[r["nul"][j] - r["can"][j] for j in range(4)] for r in rows]
    t2 = sum(v2[i][rows[i]["target"]] for i in range(len(rows)))
    return {"T1_doubled": t1, "p1": exact_tail(v1, t1, True),
            "T2_doubled": t2, "p2": exact_tail(v2, t2, False),
            "mean_canonical_target_rank": t1 / (2 * len(rows)),
            "mean_null_target_rank": sum(r["nul"][r["target"]] for r in rows) / (2 * len(rows)),
            "n": len(rows)}


# ---------------------------------------------------------------------------
# calibration gate (synthetic casts only; deterministic)
# ---------------------------------------------------------------------------

def calibrate() -> dict:
    check_registered()
    if os.path.exists(LEDGER):
        raise RuntimeError("calibration must precede any working")
    ref = reference()
    pool = {}
    for w in WORKINGS:
        pool[w] = []
        for i in range(CAL_POOL_PER_WORKING):
            s = _h16("OUTSIDE-2:calibration:%s:%d" % (w, i))
            pool[w].append((dsts("canonical", w, s), dsts("null", w, s)))
    share = {a: {z: [0.0, 0] for z in range(10)} for a in ("canonical", "null")}
    for w in WORKINGS:
        r = ref["workings"][w]
        q = r["quartet"]
        for dc, dn in pool[w]:
            for arm, ds, hk in (("canonical", dc, "canonical_hist"), ("null", dn, "null_hist")):
                sc = scores(ds, r[hk], q)
                top = max(sc)
                k = sum(1 for s in sc if s == top)
                for j in range(4):
                    for z in q[j]:
                        share[arm][z][1] += 1
                        if sc[j] == top:
                            share[arm][z][0] += 1.0 / k
    c1 = {a: {str(z): share[a][z][0] / share[a][z][1] for z in range(10) if share[a][z][1]} for a in share}
    c1_pass = all(len(c1[a]) == 10 for a in c1) and \
        all(C1_BAND[0] <= v <= C1_BAND[1] for a in c1 for v in c1[a].values())

    rng = random.Random(_h16("OUTSIDE-2:calibration-series"))

    def series(mode: str, frac: float = 0.0) -> dict:
        rows = []
        for w in WORKINGS:
            q = ref["workings"][w]["quartet"]
            t = rng.randrange(4)
            dc, dn = pool[w][rng.randrange(CAL_POOL_PER_WORKING)]
            if mode == "select":
                for _ in range(C4_K - 1):
                    ec, en = pool[w][rng.randrange(CAL_POOL_PER_WORKING)]
                    if count_in(ec, q[t]) > count_in(dc, q[t]):
                        dc, dn = ec, en
            dc = list(dc)
            if mode == "plant" and (frac >= 1.0 or rng.random() < frac):
                dc[rng.randrange(PASSAGES)] = rng.choice(q[t])
            x = read(w, dc, dn)
            rows.append({"can": x["canonical"]["ranks2"], "nul": x["null"]["ranks2"], "target": t})
        return primary(rows)

    def rate(n: int, mode: str, frac: float = 0.0) -> dict:
        p1 = p2 = 0
        for _ in range(n):
            r = series(mode, frac)
            p1 += r["p1"] <= ALPHA
            p2 += r["p2"] <= ALPHA
        return {"series": n, "P1": p1 / n, "P2": p2 / n}

    c2 = rate(C2_SERIES, "none")
    c3 = rate(C3_SERIES, "plant", 1.0)
    c4 = rate(C4_SERIES, "select")
    curve = {str(f): rate(C3_SERIES, "plant", f) for f in CURVE}
    result = {
        "series_id": SERIES_ID,
        "version": VERSION,
        "registration_sha256": registration_sha256(),
        "reference_sha256": fsha(os.path.join(HERE, REFERENCE_FILE)),
        "C1_coverage": {"band": list(C1_BAND), "rank1_share_by_zone": c1, "pass": c1_pass},
        "C2_type_I": dict(c2, max=C2_MAX, **{"pass": c2["P1"] <= C2_MAX and c2["P2"] <= C2_MAX}),
        "C3_trace_plant_control": dict(c3, min=C3_MIN, **{"pass": c3["P1"] >= C3_MIN and c3["P2"] >= C3_MIN}),
        "C4_seed_selection_control": dict(c4, k=C4_K, min_P1=C4_MIN_P1, min_P2=C4_MIN_P2,
                                          **{"pass": c4["P1"] >= C4_MIN_P1 and c4["P2"] >= C4_MIN_P2}),
        "curve_descriptive": curve,
    }
    result["gate_pass"] = all(result[k]["pass"] for k in
                              ("C1_coverage", "C2_type_I", "C3_trace_plant_control", "C4_seed_selection_control"))
    _write_once(CALIBRATION_FILE, result)
    return result


def calibration_sha256() -> str:
    return fsha(os.path.join(HERE, CALIBRATION_FILE))


# ---------------------------------------------------------------------------
# beacon
# ---------------------------------------------------------------------------

def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _unix(stamp: str) -> float:
    return datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc).timestamp()


def beacon_round(t_reading: float) -> int:
    return math.ceil((t_reading + BEACON_DELAY - BEACON["genesis_time"]) / BEACON["period"]) + 1


def round_time(r: int) -> int:
    return BEACON["genesis_time"] + (r - 1) * BEACON["period"]


def target_index(w: str, randomness_hex: str) -> int:
    d = hashlib.sha256(bytes.fromhex(randomness_hex) + (w + ":target-draw").encode("utf-8")).digest()
    return int.from_bytes(d, "big") % 4


# ---------------------------------------------------------------------------
# ledger
# ---------------------------------------------------------------------------

def entries() -> List[dict]:
    if not os.path.exists(LEDGER):
        return []
    with open(LEDGER, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def _event(etype: str, w: str, payload: dict, seq: int, parent: str, stamp: str) -> dict:
    e = {
        "series_id": SERIES_ID, "event_seq": seq, "event_id": "%s.%06d.%s" % (w, seq, etype),
        "event_type": etype, "working": w, "created_utc": stamp,
        "protocol_sha256": PROTOCOL_SHA256, "registration_sha256": registration_sha256(),
        "parent_event_hash": parent, "payload_sha256": sha(payload), "payload": payload,
    }
    e["event_hash"] = sha(e)
    return e


def _append(events: List[dict]) -> None:
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write("".join(cj(e) + "\n" for e in events))


def _gate_ok() -> None:
    check_registered()
    cal = _load(CALIBRATION_FILE)
    if not cal or not cal.get("gate_pass") or cal["registration_sha256"] != registration_sha256():
        raise RuntimeError("calibration gate not passed for this registration")
    v = verify()
    if not v["chain_ok"]:
        raise RuntimeError("ledger verification failed: %s" % v)


def _state() -> Dict[str, List[str]]:
    st: Dict[str, List[str]] = {}
    for e in entries():
        st.setdefault(e["working"], []).append(e["event_type"])
    return st


def _next(st) -> str:
    return next((x for x in WORKINGS if st.get(x) != ["CAST", "READING", "RESOLVED"]), None)


def cast(w: str, tosses: str) -> dict:
    _gate_ok()
    wnum(w)
    st = _state()
    nxt = _next(st)
    if w != nxt or st.get(w):
        raise RuntimeError("next admissible working is %s (state %s)" % (nxt, st.get(nxt)))
    seed = O.seed_of(w, tosses)
    x = read(w, dsts("canonical", w, seed), dsts("null", w, seed))
    es = entries()
    parent = es[-1]["event_hash"] if es else "0" * 64
    stamp = _utc_now()
    e1 = _event("CAST", w, {"tosses": tosses, "seed": seed, "calibration_sha256": calibration_sha256(),
                            "reference_sha256": fsha(os.path.join(HERE, REFERENCE_FILE))},
                len(es) + 1, parent, stamp)
    r = beacon_round(_unix(stamp))
    x.update({"cast_event_hash": e1["event_hash"], "beacon_round": r, "beacon_round_time_unix": round_time(r)})
    e2 = _event("READING", w, x, len(es) + 2, e1["event_hash"], stamp)
    _append([e1, e2])
    return {"cast": e1["event_hash"], "reading": e2["event_hash"], "beacon_round": r,
            "beacon_round_utc": datetime.fromtimestamp(round_time(r), timezone.utc).isoformat(),
            "push_before": "commit and push the ledger before the beacon round time"}


def beacon(w: str) -> dict:
    rd = [e for e in entries() if e["working"] == w and e["event_type"] == "READING"]
    if not rd:
        raise RuntimeError("%s has no reading" % w)
    r = rd[0]["payload"]["beacon_round"]
    return {"working": w, "round": r, "round_utc": datetime.fromtimestamp(round_time(r), timezone.utc).isoformat(),
            "url": BEACON["url"].format(round=r)}


def resolve(w: str, randomness: str, signature: str) -> dict:
    _gate_ok()
    if _state().get(w) != ["CAST", "READING"]:
        raise RuntimeError("%s is not awaiting resolution" % w)
    randomness, signature = randomness.lower().strip(), signature.lower().strip()
    if hashlib.sha256(bytes.fromhex(signature)).hexdigest() != randomness:
        raise RuntimeError("randomness is not SHA-256(signature)")
    es = entries()
    rd = [e for e in es if e["working"] == w and e["event_type"] == "READING"][0]
    r = rd["payload"]["beacon_round"]
    if datetime.now(timezone.utc).timestamp() < round_time(r):
        raise RuntimeError("beacon round %d not yet reached" % r)
    t = target_index(w, randomness)
    payload = {"reading_event_hash": rd["event_hash"], "beacon_round": r, "randomness": randomness,
               "signature": signature, "target_index": t, "target_pair": rd["payload"]["quartet"][t]}
    e = _event("RESOLVED", w, payload, len(es) + 1, es[-1]["event_hash"], _utc_now())
    _append([e])
    return {"resolved": e["event_hash"], "target_pair": payload["target_pair"]}


def verify() -> dict:
    """Replays the ledger from first principles. Truncation of the tail cannot be detected from the
    file alone; it is detected against the public repository history and the beacon record."""
    prev = "0" * 64
    es = entries()
    problems = []
    st: Dict[str, List[dict]] = {}
    reg = registration_sha256() if os.path.exists(os.path.join(HERE, REGISTRATION_FILE)) else None
    cal = calibration_sha256() if os.path.exists(os.path.join(HERE, CALIBRATION_FILE)) else None
    for i, e in enumerate(es, 1):
        body = {k: v for k, v in e.items() if k != "event_hash"}
        if e["event_seq"] != i or e["parent_event_hash"] != prev or sha(body) != e["event_hash"] \
                or sha(e["payload"]) != e["payload_sha256"]:
            problems.append((i, "chain"))
        if e["protocol_sha256"] != PROTOCOL_SHA256 or e["registration_sha256"] != reg:
            problems.append((i, "registration"))
        st.setdefault(e["working"], []).append(e)
        prev = e["event_hash"]
    order = [e["working"] for e in es]
    seen = []
    for w in order:
        if w not in seen:
            seen.append(w)
    if seen != WORKINGS[:len(seen)]:
        problems.append((0, "working order"))
    for w, ws in st.items():
        types = [e["event_type"] for e in ws]
        if types not in (["CAST", "READING"], ["CAST", "READING", "RESOLVED"]):
            problems.append((w, "event types %s" % types))
            continue
        c, rd = ws[0], ws[1]
        if c["payload"]["calibration_sha256"] != cal:
            problems.append((w, "calibration seal"))
        seed = O.seed_of(w, c["payload"]["tosses"])
        if seed != c["payload"]["seed"]:
            problems.append((w, "seed"))
        x = read(w, dsts("canonical", w, seed), dsts("null", w, seed))
        p = rd["payload"]
        if any(p[k] != x[k] for k in x) or p["cast_event_hash"] != c["event_hash"]:
            problems.append((w, "reading replay"))
        if p["beacon_round"] != beacon_round(_unix(rd["created_utc"])) or rd["created_utc"] != c["created_utc"]:
            problems.append((w, "beacon round"))
        if len(ws) == 3:
            r = ws[2]["payload"]
            if r["reading_event_hash"] != rd["event_hash"] or r["beacon_round"] != p["beacon_round"] \
                    or hashlib.sha256(bytes.fromhex(r["signature"])).hexdigest() != r["randomness"] \
                    or r["target_index"] != target_index(w, r["randomness"]) \
                    or r["target_pair"] != p["quartet"][r["target_index"]]:
                problems.append((w, "resolution"))
            if _unix(ws[2]["created_utc"]) < round_time(p["beacon_round"]):
                problems.append((w, "resolved before beacon round"))
    return {"chain_ok": not problems, "events": len(es), "head": prev, "problems": problems[:20]}


def scene(pair: Sequence[int]) -> List[str]:
    lx = O.lexicon()
    return [f["text"] for z in pair for f in lx["zones"][str(z)]]


def feedback(w: str) -> dict:
    es = [e for e in entries() if e["working"] == w]
    if [e["event_type"] for e in es] != ["CAST", "READING", "RESOLVED"]:
        raise RuntimeError("%s not resolved" % w)
    x, r = es[1]["payload"], es[2]["payload"]
    lx = O.lexicon()
    arms = [x["canonical"]["dst"], x["null"]["dst"]]
    order = random.Random(_h16("OUTSIDE-2:feedback:" + w)).sample(arms, 2)
    return {"working": w, "target_scene": scene(r["target_pair"]),
            "readings": {"R%d" % (i + 1): [f["text"] for f in O.deal([{"dst": d} for d in ds], lx)]
                         for i, ds in enumerate(order)}}


def status() -> dict:
    st = _state()
    done = [w for w in WORKINGS if st.get(w) == ["CAST", "READING", "RESOLVED"]]
    v = verify()
    return {"series_id": SERIES_ID, "version": VERSION, "registered": _load(REGISTRATION_FILE) is not None,
            "calibration_gate": (_load(CALIBRATION_FILE) or {}).get("gate_pass"),
            "resolved": len(done), "of": N, "next": _next(st), "chain_ok": v["chain_ok"],
            "events": v["events"], "head": v["head"]}


def analyse() -> dict:
    _gate_ok()
    st = _state()
    if any(st.get(w) != ["CAST", "READING", "RESOLVED"] for w in WORKINGS):
        raise RuntimeError("no interim analysis: all of W013-W100 must be resolved")
    rows = []
    for w in WORKINGS:
        es = [e for e in entries() if e["working"] == w]
        x, r = es[1]["payload"], es[2]["payload"]
        rows.append({"can": x["canonical"]["ranks2"], "nul": x["null"]["ranks2"], "target": r["target_index"]})
    return primary(rows)


def main(a: Sequence[str]) -> int:
    if len(a) < 2:
        raise SystemExit(__doc__)
    c = a[1]
    if c == "register":
        out = register()
    elif c == "reference":
        out = {"workings": len(build_reference()["workings"]), "sha256": fsha(os.path.join(HERE, REFERENCE_FILE))}
    elif c == "calibrate":
        out = calibrate()
    elif c == "cast":
        out = cast(a[2], a[3])
    elif c == "beacon":
        out = beacon(a[2])
    elif c == "resolve":
        out = resolve(a[2], a[3], a[4])
    elif c == "feedback":
        out = feedback(a[2])
    elif c == "status":
        out = status()
    elif c == "verify":
        out = verify()
    elif c == "analyse":
        out = analyse()
    else:
        raise SystemExit("unknown command")
    print(json.dumps(out, indent=1, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
