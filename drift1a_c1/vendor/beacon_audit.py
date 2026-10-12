"""
audit_beacon_outside2.py -- independent audit of the OUTSIDE-2 target draws.

Outside2.py verify() confirms that each recorded beacon randomness is SHA-256 of the recorded
signature. That relation can be satisfied by an invented signature. This script closes the gap:
it establishes that every recorded signature is a genuine drand quicknet signature for the
registered round, so that no target in the ledger can have been chosen by the operator.

It is deliberately independent of Outside2.py: the round rule, the target rule and the ledger
hashing are re-implemented here from the registered protocol text, and the script reads the
ledger and registration as data.

Checks
  Global
    G1  the embedded quicknet public key, period, genesis time, group hash and beacon id hash to
        the chain hash recorded in outside2_registration.json (binds the key to the registration)
    G2  the registration's beacon parameters equal those audited here
    G3  known-answer test: genuine round 1000000 verifies and the same signature fails for round
        1000001 (proves the BLS implementation in use is working)
    G4  ledger hash chain links and event digests recompute
  Per resolved working
    R1  beacon round = ceil((t_reading + 600 - genesis) / 3) + 1 from the READING timestamp
    R2  RESOLVED round equals the READING round; reading_event_hash links
    R3  randomness = SHA-256(signature)
    R4  BLS signature valid for the round under the quicknet key (min-sig, G1 signatures,
        DST BLS_SIG_BLS12381G1_XMD:SHA-256_SSWU_RO_NUL_, message SHA-256(round as uint64 BE))
    R5  target index = SHA-256(randomness || W + ':target-draw') mod 4, and target pair matches
    R6  RESOLVED written at or after the round time
    R7  (--online) at least two independent drand relays return the same randomness and signature

Timing extension: verifies RFC3161 tokens for every READING, including unresolved workings.
Missing tokens are INCOMPLETE; invalid or late tokens are FAIL. Archived GitHub push receipts
are reported separately. TSA tokens prove existence, not publication or cast uniqueness.

Usage
  python3 audit_beacon_outside2.py [--ledger PATH] [--registration PATH] [--online] [--json OUT]
Requires requirements-audit.txt dependencies and OpenSSL. Exit status: 0 all checks pass; 1 a check failed;
2 incomplete (BLS library unavailable, or --online and fewer than two relays reachable).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import struct
import sys
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))

QUICKNET = {
    "chain_hash": "52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971",
    "public_key": "83cf0f2896adee7eb8b5f01fcad3912212c437e0073e911fb90022d3e760183c8c4b450b6a0a6c3ac6a5776a2d1064510d1fec758c921cc22b0e17e63aaf4bcb5ed66304de9cf809bd274ca73bab4af5a6e9c76a4bc09e76eae8991ef5ece45a",
    "group_hash": "f477d5c89f21a17c863a7f937c6a6d15859414d2be09cd448d4279af331c5d3e",
    "beacon_id": "quicknet",
    "genesis_time": 1692803367,
    "period": 3,
    "scheme": "bls-unchained-g1-rfc9380",
    "dst": b"BLS_SIG_BLS12381G1_XMD:SHA-256_SSWU_RO_NUL_",
}
DELAY = 600
RELAYS = [
    "https://api.drand.sh",
    "https://api2.drand.sh",
    "https://api3.drand.sh",
    "https://drand.cloudflare.com",
]
KAT = {  # genuine quicknet round, fetched from two relays on 6 October 2026
    "round": 1000000,
    "randomness": "b22aad4794f7451896f7a371aa46106fd84d919f3f569acd5b2fddf1d1440af3",
    "signature": "83ad29e4c409f9470fc2ef02f90214df49e02b441a1a241a82d622d9f608ef98fd8b11a029f1bee9d9e83b45088abe72",
}


# ---------------------------------------------------------------------------
# protocol rules, re-implemented from the registered text
# ---------------------------------------------------------------------------

def cj(x) -> str:
    return json.dumps(x, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha(x) -> str:
    return hashlib.sha256(cj(x).encode("utf-8")).hexdigest()


def unix(stamp: str) -> float:
    return datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc).timestamp()


def registered_round(t_reading: float) -> int:
    return math.ceil((t_reading + DELAY - QUICKNET["genesis_time"]) / QUICKNET["period"]) + 1


def round_time(r: int) -> int:
    return QUICKNET["genesis_time"] + (r - 1) * QUICKNET["period"]


def target_index(w: str, randomness_hex: str) -> int:
    d = hashlib.sha256(bytes.fromhex(randomness_hex) + (w + ":target-draw").encode("utf-8")).digest()
    return int.from_bytes(d, "big") % 4


def chain_hash_from_key() -> str:
    h = hashlib.sha256()
    h.update(struct.pack(">I", QUICKNET["period"]))
    h.update(struct.pack(">q", QUICKNET["genesis_time"]))
    h.update(bytes.fromhex(QUICKNET["public_key"]))
    h.update(bytes.fromhex(QUICKNET["group_hash"]))
    h.update(QUICKNET["beacon_id"].encode("ascii"))
    return h.hexdigest()


# ---------------------------------------------------------------------------
# BLS verification (py_ecc)
# ---------------------------------------------------------------------------

class BLS:
    def __init__(self):
        from py_ecc.bls.hash_to_curve import hash_to_G1
        from py_ecc.bls.point_compression import decompress_G1, decompress_G2
        from py_ecc.optimized_bls12_381 import (G2, FQ12, curve_order, final_exponentiate,
                                                 is_inf, multiply, neg, pairing)
        self.h2g1, self.dG1 = hash_to_G1, decompress_G1
        self.G2, self.FQ12, self.r = G2, FQ12, curve_order
        self.fe, self.is_inf, self.mul, self.neg, self.pairing = final_exponentiate, is_inf, multiply, neg, pairing
        pk = bytes.fromhex(QUICKNET["public_key"])
        self.pk = decompress_G2((int.from_bytes(pk[:48], "big"), int.from_bytes(pk[48:], "big")))
        if not is_inf(multiply(self.pk, curve_order)):
            raise ValueError("public key not in G2 subgroup")

    def verify(self, rnd: int, signature_hex: str) -> bool:
        try:
            sig = self.dG1(int.from_bytes(bytes.fromhex(signature_hex), "big"))
        except Exception:
            return False
        if self.is_inf(sig) or not self.is_inf(self.mul(sig, self.r)):
            return False
        msg = hashlib.sha256(struct.pack(">Q", rnd)).digest()
        h = self.h2g1(msg, QUICKNET["dst"], hashlib.sha256)
        x = self.pairing(self.neg(self.G2), sig, final_exponentiate=False) * \
            self.pairing(self.pk, h, final_exponentiate=False)
        return self.fe(x) == self.FQ12.one()


def fetch_round(relay: str, rnd: int, timeout: float = 15.0):
    url = "%s/%s/public/%d" % (relay, QUICKNET["chain_hash"], rnd)
    try:
        with urllib.request.urlopen(url, timeout=timeout) as f:
            d = json.loads(f.read().decode("utf-8"))
        return {"round": d.get("round"), "randomness": d.get("randomness"), "signature": d.get("signature")}
    except Exception as e:  # network failure is reported, never counted as agreement
        return {"error": "%s: %s" % (type(e).__name__, e)}


# ---------------------------------------------------------------------------
# audit
# ---------------------------------------------------------------------------

def audit(ledger_path: str, registration_path: str, online: bool, timing_dir=None) -> dict:
    report = {"audit": "OUTSIDE-2 beacon audit", "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "ledger": os.path.abspath(ledger_path), "global": {}, "workings": {}, "complete": True}
    g = report["global"]

    with open(registration_path, encoding="utf-8") as f:
        reg = json.load(f)
    rb = reg.get("beacon", {})
    g["G1_key_bound_to_registered_chain_hash"] = chain_hash_from_key() == rb.get("chain_hash") == QUICKNET["chain_hash"]
    g["G2_registration_parameters"] = (rb.get("genesis_time"), rb.get("period"), rb.get("scheme")) == \
        (QUICKNET["genesis_time"], QUICKNET["period"], QUICKNET["scheme"]) and \
        reg.get("protocol", {}).get("series_id") == "OUTSIDE-2-numogram-reader"

    try:
        bls = BLS()
        g["G3_known_answer"] = bls.verify(KAT["round"], KAT["signature"]) and \
            not bls.verify(KAT["round"] + 1, KAT["signature"]) and \
            hashlib.sha256(bytes.fromhex(KAT["signature"])).hexdigest() == KAT["randomness"]
    except ImportError as e:
        bls = None
        g["G3_known_answer"] = None
        report["complete"] = False
        report["incomplete_reason"] = "py_ecc not available (%s); install with: pip install py_ecc" % e

    events = []
    if os.path.exists(ledger_path):
        with open(ledger_path, encoding="utf-8") as f:
            events = [json.loads(x) for x in f if x.strip()]
    prev, chain_ok = "0" * 64, True
    for i, e in enumerate(events, 1):
        body = {k: v for k, v in e.items() if k != "event_hash"}
        if e.get("event_seq") != i or e.get("parent_event_hash") != prev or sha(body) != e.get("event_hash") \
                or sha(e.get("payload")) != e.get("payload_sha256"):
            chain_ok = False
        prev = e.get("event_hash")
    g["G4_ledger_chain"] = chain_ok
    g["events"] = len(events)
    g["head"] = prev

    by_w = {}
    for e in events:
        by_w.setdefault(e["working"], {})[e["event_type"]] = e
    relays_short = False
    for w in sorted(by_w):
        ev = by_w[w]
        if "RESOLVED" not in ev:
            report["workings"][w] = {"status": "awaiting resolution"}
            continue
        rd, rs = ev["READING"], ev["RESOLVED"]
        p, r = rd["payload"], rs["payload"]
        rnd = registered_round(unix(rd["created_utc"]))
        row = {
            "round": r.get("beacon_round"),
            "R1_round_rule": p.get("beacon_round") == rnd,
            "R2_links": r.get("beacon_round") == p.get("beacon_round") and r.get("reading_event_hash") == rd["event_hash"],
            "R3_randomness_is_hash_of_signature": hashlib.sha256(bytes.fromhex(r["signature"])).hexdigest() == r["randomness"],
            "R4_bls_signature": bls.verify(int(r["beacon_round"]), r["signature"]) if bls else None,
            "R5_target": r.get("target_index") == target_index(w, r["randomness"])
                         and r.get("target_pair") == p["quartet"][target_index(w, r["randomness"])],
            "R6_resolved_after_round": unix(rs["created_utc"]) >= round_time(int(r["beacon_round"])),
        }
        if online:
            got = {relay: fetch_round(relay, int(r["beacon_round"])) for relay in RELAYS}
            ok = [v for v in got.values() if "error" not in v]
            agree = [v for v in ok if v["randomness"] == r["randomness"] and v["signature"] == r["signature"]
                     and v["round"] == r["beacon_round"]]
            # a reachable relay that disagrees is a failure; too few reachable relays is incomplete
            row["R7_relays"] = {"reachable": len(ok), "agreeing": len(agree),
                                "pass": False if len(agree) < len(ok) else (True if len(ok) >= 2 else None)}
            if len(ok) < 2:
                relays_short = True
        checks = [v for k, v in row.items() if k.startswith("R") and k != "round"]
        flat = [c["pass"] if isinstance(c, dict) else c for c in checks]
        row["status"] = "PASS" if all(x is True for x in flat) else ("FAIL" if False in flat else "INCOMPLETE")
        report["workings"][w] = row

    if online and relays_short:
        report["complete"] = False
        report.setdefault("incomplete_reason", "fewer than two relays reachable for at least one round")
    from outside2_timing import audit_readings, TIMING
    report["timing"] = audit_readings(events, reg, timing_dir or TIMING)
    if any(v["status"] == "INCOMPLETE" for v in report["timing"].values()):
        report["complete"] = False
    timing_fails = [w for w, v in report["timing"].items() if v["status"] == "FAIL"]
    fails = [w for w, v in report["workings"].items() if v.get("status") == "FAIL"]
    gfail = [k for k, v in g.items() if k[:2] in ("G1", "G2", "G3", "G4") and v is False]
    report["resolved_audited"] = sum(1 for v in report["workings"].values() if "status" in v and v["status"] != "awaiting resolution")
    report["failures"] = {"global": gfail, "workings": fails, "timing": timing_fails}
    report["verdict"] = "FAIL" if (fails or gfail or timing_fails) else ("PASS" if report["complete"] else "INCOMPLETE")
    report["not_checked"] = "TSA proves existence, not public availability or absence of unpublished casts; GitHub receipts are archived server assertions; no online TSA revocation check"
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--ledger", default=os.path.join(HERE, "ledger_outside2.jsonl"))
    ap.add_argument("--registration", default=os.path.join(HERE, "outside2_registration.json"))
    ap.add_argument("--timing-dir", help="directory containing W###.tsr and W###_PUSH.json")
    ap.add_argument("--online", action="store_true", help="also compare every round with independent drand relays")
    ap.add_argument("--json", help="write the full report to this path")
    a = ap.parse_args()
    rep = audit(a.ledger, a.registration, a.online, a.timing_dir)
    text = json.dumps(rep, indent=1, sort_keys=True)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    print(text)
    return {"PASS": 0, "FAIL": 1}.get(rep["verdict"], 2)


if __name__ == "__main__":
    sys.exit(main())
