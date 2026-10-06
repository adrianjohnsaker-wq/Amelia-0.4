"""
OUTSIDE-2 -- Numogram-as-reader. Amelia Interface Programme.

Successor to OUTSIDE-1 v2.1 (closed 6 October 2026 for instrument fault; see
publication_v2_1/OUTSIDE1_V2_1_CLOSURE.json). Registered as a separate experiment under the
operator's standing rule that a failed language-mediated reader is replaced by a
Numogram-as-reader design, not repaired.

Design in one paragraph. The querent holds the fixed question and makes a 32-toss physical cast.
The cast seeds a twelve-passage D3 Lemurian trace through the sealed canonical Numogram and, with
the same seed, through a fresh N1 degree-matched null. There is no language layer in evaluation:
the Numogram trace is the reading. Each working has a quartet of four candidate scenes fixed before
the cast; each candidate is a disjoint pair of zones, and its displayed scene is composed of the
registered source-locked fragments of those two zones. Every candidate is therefore expressible by
the reader by construction. A candidate's score in an arm is the mid-percentile of the number of
passages that reached its two zones, against that arm's own frozen reference distribution, so that
no zone is favoured by the diagram's base rates. Candidates are ranked by score (mid-ranks for
ties). Only after the reading event is sealed is the target drawn from the quartet with operating-
system entropy. P1 and P2 are exact randomization tests over the target draw, conditional on the
sealed scores, evaluated once, after W100.

Commands (run from amelia-1/outside):
  register              write outside2_registration.json (refuses to overwrite a different one)
  reference             build outside2_reference.json from registered reference seeds
  calibrate             run the registered pre-data gate (C1 coverage, C2 type-I, C3 on-channel control)
  cast W### TOSSES      admit a working: cast event, then sealed reading event
  resolve W###          draw the target with OS entropy and write the resolution event
  feedback W###         print the querent feedback (target scene and both readings, arms unlabelled)
  status | verify       ledger state and chain verification
  analyse               final P1/P2; refuses unless W013-W100 are all resolved
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import secrets
import sys
from datetime import datetime, timezone
from typing import Dict, List, Sequence

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import Outside1_v2 as O  # frozen mechanics: graph(), trace(), seed_of(), lexicon(), deal()

SERIES_ID = "OUTSIDE-2-numogram-reader"
VERSION = "1.0.0"
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

# Pre-data gate (calibration on synthetic casts only)
CAL_POOL_PER_WORKING = 1000
C1_BAND = (0.18, 0.32)       # rank-1 share of a candidate containing zone z, given z in quartet
C2_SERIES = 1000
C2_MAX = 0.065               # empirical rejection rate at alpha 0.05 with no signal
C3_SERIES = 200
C3_MIN = 0.95                # power with one target-bearing passage planted in every working
C3_CURVE = (0.10, 0.20, 0.30, 0.45, 0.60)  # descriptive sensitivity curve (fraction of workings planted)
ALPHA = 0.05

PROTOCOL = {
    "series_id": SERIES_ID,
    "version": VERSION,
    "registration_date": "2026-10-06",
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
    },
    "reader": {
        "kind": "Numogram-as-reader; no language layer in evaluation",
        "reading": "the ordered destination zones of the twelve recorded passages, per arm",
        "score": "for candidate zone pair S: c = number of passages whose destination is in S; score = P(C < c) + 0.5 P(C = c) under the same arm's frozen reference distribution of C for S",
        "reference": "REF_CASTS = 4000 reference casts per graph (canonical, and each working's null), seeds int(SHA-256('OUTSIDE-2:reference:' + graph tag + ':' + i)[:16], 16); frozen in outside2_reference.json before any working",
        "ranking": "candidates ranked by score, higher first; ties take mid-ranks",
    },
    "target_pool": {
        "quartet": "for working W: zones 0-9 shuffled by random.Random(int(SHA-256('OUTSIDE-2:quartet:' + W)[:16], 16)); candidates are the disjoint pairs (z0,z1), (z2,z3), (z4,z5), (z6,z7)",
        "expressibility": "every candidate is a set of zones the reader emits; coverage is tested in C1",
        "displayed_scene": "the registered lexicon_v2 fragments of the candidate's two zones, in zone order; display only, no role in scoring; no demon names",
        "draw": "target index = int(SHA-256(32 bytes OS entropy || ':target-draw'), big-endian) mod 4, only after the reading event is sealed",
    },
    "primary": {
        "P1": "one-sided exact randomization test over the target draw: T1 = sum over workings of the canonical arm's mid-rank of the target; p1 = P(T1' <= T1)",
        "P2": "one-sided exact randomization test over the target draw: T2 = sum over workings of (null mid-rank - canonical mid-rank) of the target; p2 = P(T2' >= T2)",
        "alpha": ALPHA,
        "interpretation": "P1 alone = departure from chance somewhere in the canonical apparatus; P2 = canonical-specific advantage over the same-cast null. The Numogram-specificity claim requires P2.",
        "no_interim_analysis": True,
    },
    "calibration_gate": {
        "data": "synthetic casts only, from registered seeds int(SHA-256('OUTSIDE-2:calibration:' + W + ':' + i)[:16], 16), i < 1000",
        "C1_coverage": "for both arms and every zone z: among calibration casts of workings whose quartet contains z, the share in which the candidate containing z is ranked first (a tie for first counts its share 1/k) lies in [0.18, 0.32]",
        "C2_type_I": "1000 simulated series with no signal: empirical rejection at alpha 0.05 <= 0.065 for P1 and for P2",
        "C3_on_channel_control": "200 simulated series in which one of the twelve canonical passages per working is replaced by a passage into a zone of the target pair: rejection >= 0.95 for P1 and for P2",
        "C3_curve": "descriptive power at planted fractions 0.10, 0.20, 0.30, 0.45, 0.60 of workings; reported, not gated",
        "rule": "W013 may not be admitted unless C1, C2 and C3 all pass. If any fails, the apparatus is not modified within this registration.",
    },
    "evidence": {
        "serialization": SERIALIZATION,
        "events_per_working": ["CAST", "READING", "RESOLVED"],
        "fields": ["series_id", "event_seq", "event_id", "event_type", "working", "created_utc",
                   "protocol_sha256", "registration_sha256", "parent_event_hash", "payload_sha256",
                   "payload", "event_hash"],
        "no_backfill": True,
        "arm_labels": "recorded openly in the ledger: scoring is mechanical, so there is no judge to blind; querent feedback shows the readings unlabelled",
    },
    "claims": {
        "permitted_on_success": "register 1 (P1 and/or P2 departures) and register 2 (canonical-specific structure if P2); access, not agency or communication",
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
            "mean_canonical_target_rank": t1 / (2 * len(rows)), "n": len(rows)}


# ---------------------------------------------------------------------------
# calibration gate (synthetic casts only)
# ---------------------------------------------------------------------------

def calibrate() -> dict:
    check_registered()
    if os.path.exists(LEDGER):
        raise RuntimeError("calibration must precede any working")
    ref = reference()
    if ref["registration_sha256"] != registration_sha256():
        raise RuntimeError("reference not bound to this registration")
    pool = {}
    for w in WORKINGS:
        pool[w] = []
        for i in range(CAL_POOL_PER_WORKING):
            s = _h16("OUTSIDE-2:calibration:%s:%d" % (w, i))
            pool[w].append((dsts("canonical", w, s), dsts("null", w, s)))
    # C1 coverage
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
    c1_pass = all(C1_BAND[0] <= v <= C1_BAND[1] for a in c1 for v in c1[a].values()) and \
        all(len(c1[a]) == 10 for a in c1)

    rng = random.Random(_h16("OUTSIDE-2:calibration-series"))

    def series(frac: float) -> dict:
        rows = []
        for w in WORKINGS:
            q = ref["workings"][w]["quartet"]
            dc, dn = pool[w][rng.randrange(CAL_POOL_PER_WORKING)]
            dc = list(dc)
            t = rng.randrange(4)
            if frac > 0 and rng.random() < frac:
                dc[rng.randrange(PASSAGES)] = rng.choice(q[t])
            x = read(w, dc, dn)
            rows.append({"can": x["canonical"]["ranks2"], "nul": x["null"]["ranks2"], "target": t})
        return primary(rows)

    def rate(frac: float, n: int) -> dict:
        p1 = p2 = 0
        for _ in range(n):
            r = series(frac)
            p1 += r["p1"] <= ALPHA
            p2 += r["p2"] <= ALPHA
        return {"series": n, "P1": p1 / n, "P2": p2 / n}

    c2 = rate(0.0, C2_SERIES)
    c3 = rate(1.0, C3_SERIES)
    curve = {str(f): rate(f, C3_SERIES) for f in C3_CURVE}
    result = {
        "series_id": SERIES_ID,
        "registration_sha256": registration_sha256(),
        "reference_sha256": fsha(os.path.join(HERE, REFERENCE_FILE)),
        "C1_coverage": {"band": list(C1_BAND), "rank1_share_by_zone": c1, "pass": c1_pass},
        "C2_type_I": dict(c2, max=C2_MAX, **{"pass": c2["P1"] <= C2_MAX and c2["P2"] <= C2_MAX}),
        "C3_on_channel_control": dict(c3, min=C3_MIN, **{"pass": c3["P1"] >= C3_MIN and c3["P2"] >= C3_MIN}),
        "C3_curve_descriptive": curve,
    }
    result["gate_pass"] = result["C1_coverage"]["pass"] and result["C2_type_I"]["pass"] and \
        result["C3_on_channel_control"]["pass"]
    result["sealed_utc"] = _now()
    _write_once(CALIBRATION_FILE, result)
    return result


# ---------------------------------------------------------------------------
# ledger
# ---------------------------------------------------------------------------

def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4] + "Z"


def entries() -> List[dict]:
    if not os.path.exists(LEDGER):
        return []
    with open(LEDGER, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def verify() -> dict:
    prev = "0" * 64
    es = entries()
    for i, e in enumerate(es, 1):
        body = {k: v for k, v in e.items() if k != "event_hash"}
        if e["event_seq"] != i or e["parent_event_hash"] != prev or sha(body) != e["event_hash"] \
                or sha(e["payload"]) != e["payload_sha256"]:
            return {"chain_ok": False, "at": i}
        prev = e["event_hash"]
    return {"chain_ok": True, "events": len(es), "head": prev}


def _append(etype: str, w: str, payload: dict) -> dict:
    es = entries()
    seq = len(es) + 1
    e = {
        "series_id": SERIES_ID, "event_seq": seq, "event_id": "%s.%06d.%s" % (w, seq, etype),
        "event_type": etype, "working": w, "created_utc": _now(),
        "protocol_sha256": PROTOCOL_SHA256, "registration_sha256": registration_sha256(),
        "parent_event_hash": es[-1]["event_hash"] if es else "0" * 64,
        "payload_sha256": sha(payload), "payload": payload,
    }
    e["event_hash"] = sha(e)
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(cj(e) + "\n")
    return e


def _gate_ok() -> None:
    check_registered()
    cal = _load(CALIBRATION_FILE)
    if not cal or not cal.get("gate_pass") or cal["registration_sha256"] != registration_sha256():
        raise RuntimeError("calibration gate not passed for this registration")
    if not verify()["chain_ok"]:
        raise RuntimeError("ledger chain broken")


def _state() -> Dict[str, List[str]]:
    st: Dict[str, List[str]] = {}
    for e in entries():
        st.setdefault(e["working"], []).append(e["event_type"])
    return st


def cast(w: str, tosses: str) -> dict:
    _gate_ok()
    wnum(w)
    st = _state()
    nxt = next((x for x in WORKINGS if st.get(x) != ["CAST", "READING", "RESOLVED"]), None)
    if w != nxt or st.get(w):
        raise RuntimeError("next admissible working is %s" % nxt)
    seed = O.seed_of(w, tosses)
    e1 = _append("CAST", w, {"tosses": tosses, "seed": seed})
    x = read(w, dsts("canonical", w, seed), dsts("null", w, seed))
    x["cast_event_hash"] = e1["event_hash"]
    x["reference_sha256"] = fsha(os.path.join(HERE, REFERENCE_FILE))
    e2 = _append("READING", w, x)
    return {"cast": e1["event_hash"], "reading": e2["event_hash"]}


def resolve(w: str) -> dict:
    _gate_ok()
    if _state().get(w) != ["CAST", "READING"]:
        raise RuntimeError("%s is not awaiting resolution" % w)
    rd = [e for e in entries() if e["working"] == w and e["event_type"] == "READING"][0]
    ent = secrets.token_bytes(32)
    t = int.from_bytes(hashlib.sha256(ent + b":target-draw").digest(), "big") % 4
    x = rd["payload"]
    payload = {"reading_event_hash": rd["event_hash"], "entropy_hex": ent.hex(), "target_index": t,
               "target_pair": x["quartet"][t],
               "canonical_target_rank": x["canonical"]["ranks2"][t] / 2,
               "null_target_rank": x["null"]["ranks2"][t] / 2}
    e = _append("RESOLVED", w, payload)
    return {"resolved": e["event_hash"], "target_pair": x["quartet"][t]}


def scene(pair: Sequence[int]) -> List[str]:
    lx = O.lexicon()
    return [f["text"] for z in pair for f in lx["zones"][str(z)]]


def feedback(w: str) -> dict:
    es = [e for e in entries() if e["working"] == w]
    if [e["event_type"] for e in es] != ["CAST", "READING", "RESOLVED"]:
        raise RuntimeError("%s not resolved" % w)
    x, r = es[1]["payload"], es[2]["payload"]
    lx = O.lexicon()

    def render(ds):
        return O.deal([{"dst": d} for d in ds], lx)

    arms = [("canonical", x["canonical"]["dst"]), ("null", x["null"]["dst"])]
    order = random.Random(_h16("OUTSIDE-2:feedback:" + w)).sample(arms, 2)
    return {"working": w, "target_scene": scene(r["target_pair"]),
            "readings_unlabelled": {"R%d" % (i + 1): [f["text"] for f in render(ds)] for i, (_, ds) in enumerate(order)}}


def status() -> dict:
    st = _state()
    done = [w for w in WORKINGS if st.get(w) == ["CAST", "READING", "RESOLVED"]]
    nxt = next((w for w in WORKINGS if w not in done), None)
    return {"series_id": SERIES_ID, "registered": _load(REGISTRATION_FILE) is not None,
            "calibration_gate": (_load(CALIBRATION_FILE) or {}).get("gate_pass"),
            "resolved": len(done), "of": N, "next": nxt, **verify()}


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
    elif c == "resolve":
        out = resolve(a[2])
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
