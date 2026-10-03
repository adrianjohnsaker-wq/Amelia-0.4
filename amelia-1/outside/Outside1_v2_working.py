"""
OUTSIDE-1 v2 working-series runner.

Operational wrapper for the already sealed OUTSIDE-1 v2 apparatus. This file does
not alter Outside1_v2.py, its registered protocol, canonical modules or lexicon.
It only enforces the prospective W001-W100 state machine:
cast -> traces/fragments -> sealed readings -> sealed blind rankings -> target draw.

Arm identity and running statistics are never returned before W100.
"""
from __future__ import annotations

import json
import os
import re
import secrets
import sys
from typing import Dict, List, Sequence

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import Outside1_v2 as O

VERSION = "OUTSIDE-1-v2-working-runner-1.0.0"
CONTROL_RESULT = os.path.join(HERE, "outside1_v2_control_result.json")
LEDGER = os.path.join(HERE, "ledger_v2_workings.jsonl")
MAX_WORKINGS = 100


def _load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _control_open():
    O.check_registered()
    r = _load_json(CONTROL_RESULT)
    if not r.get("pass") or int(r.get("hits_first", 0)) < int(r.get("criterion", 10)):
        raise RuntimeError("positive control has not passed")
    return r


def entries():
    if not os.path.exists(LEDGER):
        return []
    with open(LEDGER, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def verify_chain():
    prev = "0" * 64
    for e in entries():
        if e.get("prev") != prev:
            return False
        body = {k: v for k, v in e.items() if k != "hash"}
        if O.sha(body) != e.get("hash"):
            return False
        prev = e["hash"]
    return True


def append(kind, ident, data):
    es = entries()
    prev = es[-1]["hash"] if es else "0" * 64
    e = {"kind": kind, "id": ident, "data": data, "prev": prev}
    e["hash"] = O.sha(e)
    with open(LEDGER, "a", encoding="utf-8") as f:
        f.write(O.canonical_json(e) + "\n")
    return e


def find(kind, ident, slot=None):
    for e in entries():
        if e["kind"] == kind and e["id"] == ident:
            if slot is None or e["data"].get("slot") == slot:
                return e
    return None


def _wn(working):
    if not re.fullmatch(r"W\d{3}", working):
        raise ValueError("working must be W001..W100")
    n = int(working[1:])
    if not 1 <= n <= MAX_WORKINGS:
        raise ValueError("working outside W001..W100")
    return n


def _require_order(working):
    n = _wn(working)
    casts = {int(e["id"][1:]) for e in entries() if e["kind"] == "cast"}
    if casts and n != max(casts) + 1:
        raise RuntimeError("workings must be cast in sequence")
    if not casts and n != 1:
        raise RuntimeError("first working must be W001")
    if n > 1 and not find("resolved", "W%03d" % (n - 1)):
        raise RuntimeError("previous working is not resolved")


def prepare(working, tosses):
    _control_open()
    if not verify_chain():
        raise RuntimeError("ledger chain invalid")
    _require_order(working)
    if find("cast", working):
        raise RuntimeError("working already cast")

    n = _wn(working)
    seed = O.seed_of(working, tosses)
    arms = {}
    for arm in ("canonical", "null"):
        tr = O.trace(O.graph(arm, n), seed)
        fr = O.deal(tr)
        arms[arm] = {"trace": tr, "fragments": fr}

    slot_arms = ["canonical", "null"]
    secrets.SystemRandom().shuffle(slot_arms)
    slot_map = {"R1": slot_arms[0], "R2": slot_arms[1]}

    quartet = O.target_quartet(working)
    judge_orders = {}
    for slot in ("R1", "R2"):
        order = list(range(4))
        secrets.SystemRandom().shuffle(order)
        judge_orders[slot] = order

    append("cast", working, {
        "tosses": tosses,
        "seed": seed,
        "slot_map": slot_map,
        "arms": arms,
        "quartet": quartet,
        "judge_orders": judge_orders,
    })

    public = {"working": working, "slots": {}}
    for slot in ("R1", "R2"):
        fr = arms[slot_map[slot]]["fragments"]
        public["slots"][slot] = {
            "fragments": [x["text"] for x in fr],
            "compose_prompt": O.COMPOSE_PROMPT.format(
                fragments="\n".join("%d. %s" % (i + 1, x["text"]) for i, x in enumerate(fr))
            ),
        }
    return public


def seal_reading(working, slot, reading):
    if slot not in ("R1", "R2"):
        raise ValueError("slot must be R1/R2")
    c = find("cast", working)
    if not c:
        raise RuntimeError("working not cast")
    if find("reading", working, slot):
        raise RuntimeError("reading already sealed")
    arm = c["data"]["slot_map"][slot]
    frags = [x["text"] for x in c["data"]["arms"][arm]["fragments"]]
    for f in frags:
        if f not in reading:
            raise ValueError("reading omits dealt fragment: %s" % f)
    wc = len(re.findall(r"\b[\w’'-]+\b", reading))
    if not 90 <= wc <= 160:
        raise ValueError("reading must be 90-160 words, got %d" % wc)
    return append("reading", working, {"slot": slot, "text": reading, "word_count": wc})


def judge_material(working, slot):
    c = find("cast", working)
    r = find("reading", working, slot)
    if not c or not r:
        raise RuntimeError("cast/reading not sealed")
    order = c["data"]["judge_orders"][slot]
    labels = "ABCD"
    candidates = [
        {"label": labels[k], "scene": c["data"]["quartet"][idx]["text"], "pool_index": idx}
        for k, idx in enumerate(order)
    ]
    return {
        "working": working,
        "slot": slot,
        "reading": r["data"]["text"],
        "candidates": [{"label": x["label"], "scene": x["scene"]} for x in candidates],
        "judge_prompt": O.JUDGE_PROMPT.format(
            reading=r["data"]["text"],
            candidates="\n".join("%s. %s" % (x["label"], x["scene"]) for x in candidates),
        ),
    }


def seal_ranking(working, slot, ranking):
    if slot not in ("R1", "R2"):
        raise ValueError("slot must be R1/R2")
    if not find("reading", working, slot):
        raise RuntimeError("reading not sealed")
    if find("ranking", working, slot):
        raise RuntimeError("ranking already sealed")
    if sorted(ranking) != list("ABCD"):
        raise ValueError("ranking must be permutation A-D")
    return append("ranking", working, {"slot": slot, "ranking": list(ranking)})


def _rank_for_pool_index(cast_data, slot, ranking, pool_index):
    order = cast_data["judge_orders"][slot]
    labels = "ABCD"
    label = labels[order.index(pool_index)]
    return list(ranking).index(label) + 1


def draw(working):
    if find("resolved", working):
        raise RuntimeError("working already resolved")
    c = find("cast", working)
    if not c:
        raise RuntimeError("working not cast")
    rs = {s: find("reading", working, s) for s in ("R1", "R2")}
    ks = {s: find("ranking", working, s) for s in ("R1", "R2")}
    if not all(rs.values()) or not all(ks.values()):
        raise RuntimeError("both readings and rankings must be sealed before draw")

    target_index = secrets.randbelow(4)
    slot_ranks = {
        s: _rank_for_pool_index(c["data"], s, ks[s]["data"]["ranking"], target_index)
        for s in ("R1", "R2")
    }
    arm_ranks = {
        c["data"]["slot_map"][s]: slot_ranks[s] for s in ("R1", "R2")
    }
    append("resolved", working, {
        "target_index": target_index,
        "slot_ranks": slot_ranks,
        "arm_ranks": arm_ranks,
    })
    return {
        "working": working,
        "target_scene": c["data"]["quartet"][target_index]["text"],
        "readings_unlabelled": {
            "R1": rs["R1"]["data"]["text"],
            "R2": rs["R2"]["data"]["text"],
        },
    }


def _convolve(values_by_working):
    dist = {0: 1}
    for vals in values_by_working:
        nxt = {}
        for a, ca in dist.items():
            for v in vals:
                nxt[a + v] = nxt.get(a + v, 0) + ca
        dist = nxt
    return dist


def _tail_p(dist, observed, upper=True):
    total = sum(dist.values())
    good = sum(c for v, c in dist.items() if (v >= observed if upper else v <= observed))
    return good / total


def analyse():
    if len([e for e in entries() if e["kind"] == "resolved"]) != MAX_WORKINGS:
        raise RuntimeError("analysis forbidden before W100 resolved")
    p1_obs = 0
    p2_obs = 0
    p1_null = []
    p2_null = []
    hit_c = hit_n = 0
    ranks_c = []
    ranks_n = []

    for n in range(1, MAX_WORKINGS + 1):
        w = "W%03d" % n
        c = find("cast", w)["data"]
        rr = find("resolved", w)["data"]
        cr = rr["arm_ranks"]["canonical"]
        nr = rr["arm_ranks"]["null"]
        ranks_c.append(cr); ranks_n.append(nr)
        hit_c += cr == 1; hit_n += nr == 1
        p1_obs += cr
        p2_obs += nr - cr

        # Under the registered target draw each pool index 0..3 is equiprobable.
        slot_for_c = next(s for s,a in c["slot_map"].items() if a == "canonical")
        slot_for_n = next(s for s,a in c["slot_map"].items() if a == "null")
        kc = find("ranking", w, slot_for_c)["data"]["ranking"]
        kn = find("ranking", w, slot_for_n)["data"]["ranking"]
        vals_c, vals_d = [], []
        for idx in range(4):
            rc = _rank_for_pool_index(c, slot_for_c, kc, idx)
            rn = _rank_for_pool_index(c, slot_for_n, kn, idx)
            vals_c.append(rc)
            vals_d.append(rn - rc)
        p1_null.append(vals_c)
        p2_null.append(vals_d)

    d1 = _convolve(p1_null)
    d2 = _convolve(p2_null)
    # P1: lower rank sum = stronger correspondence. P2: positive null-canonical = canonical better.
    p1_p = _tail_p(d1, p1_obs, upper=False)
    p2_p = _tail_p(d2, p2_obs, upper=True)
    return {
        "P1": {"canonical_rank_sum": p1_obs, "p_one_sided_exact": p1_p, "held": p1_p <= 0.05},
        "P2": {"sum_null_minus_canonical": p2_obs, "p_one_sided_exact": p2_p, "held": p2_p <= 0.05},
        "secondary": {
            "canonical_first_place_hits": hit_c,
            "null_first_place_hits": hit_n,
            "canonical_rank_distribution": {str(k): ranks_c.count(k) for k in range(1,5)},
            "null_rank_distribution": {str(k): ranks_n.count(k) for k in range(1,5)},
        },
    }


def public_status():
    es = entries()
    return {
        "version": VERSION,
        "chain_ok": verify_chain(),
        "workings_cast": sum(e["kind"] == "cast" for e in es),
        "workings_resolved": sum(e["kind"] == "resolved" for e in es),
        "analysis_locked": sum(e["kind"] == "resolved" for e in es) < MAX_WORKINGS,
    }


def main(argv: Sequence[str]):
    if len(argv) < 2:
        raise SystemExit("commands: status")
    if argv[1] == "status":
        print(json.dumps(public_status(), sort_keys=True))
        return 0
    raise SystemExit("runner is driven through imported functions; CLI exposes status only")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
