"""OUTSIDE-2 queue runner: procedure automation only; registered apparatus unchanged."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

REQUESTS = HERE / "admission_requests"
TIMING = HERE / "publication_outside2" / "timing"
BATCHES = HERE / "publication_outside2" / "batches"
LINE = re.compile(r"^\s*(W\d{3})\s*[:\-]?\s*(.*?)\s*$")
RELAYS = ["https://api.drand.sh", "https://api2.drand.sh",
          "https://api3.drand.sh", "https://drand.cloudflare.com"]
MAX_WORKINGS = int(os.environ.get("OUTSIDE2_QUEUE_MAX", "20"))
RESOLVE_MARGIN = 6
FETCH_PATIENCE = 180


class Halt(Exception):
    def __init__(self, message, evidence=None):
        super().__init__(message)
        self.evidence = evidence


def now_utc():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def parse_requests(folder=REQUESTS):
    """Malformed/conflicting requests halt before any new admission."""
    out = {}
    if not folder.exists():
        return out
    for f in sorted(folder.glob("*.txt")):
        for n, raw in enumerate(f.read_text().splitlines(), 1):
            text = raw.split("#", 1)[0].strip()
            if not text:
                continue
            m = LINE.match(text)
            if not m:
                raise Halt(f"{f.name} line {n}: cannot read {raw!r}")
            w, raw_t = m.group(1), m.group(2)
            tosses = re.sub(r"[\s,;]", "", raw_t.upper())
            if not re.fullmatch(r"[HT]{32}", tosses):
                raise Halt(f"{f.name} line {n}: {w} must have exactly 32 H/T tosses")
            row = {"working": w, "tosses": tosses, "source": f"{f.name}:{n}",
                   "file": f.name, "line": n}
            if w in out and out[w]["tosses"] != tosses:
                raise Halt(f"conflicting requests for {w}: {out[w]['source']} and {row['source']}")
            out.setdefault(w, row)
    return out


class Git:
    def __init__(self, root=ROOT, branch=None, remote="origin"):
        self.root, self.remote = Path(root), remote
        self.branch = branch or os.environ.get("TARGET_BRANCH", "amelia-1.0")

    def run(self, *args, check=True):
        p = subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True)
        if check and p.returncode:
            raise Halt("git %s failed: %s" % (" ".join(args), p.stderr.strip()[-500:]))
        return p.stdout.strip()

    def request_provenance(self, file_name):
        rel = str((REQUESTS / file_name).resolve().relative_to(self.root.resolve()))
        raw = self.run("log", "-1", "--format=%H%x1f%an%x1f%ae%x1f%aI", "--", rel)
        p = raw.split("\x1f") if raw else []
        if len(p) != 4:
            return {"file": rel, "commit": None, "note": "request provenance unavailable"}
        return {"file": rel, "commit": p[0], "author_name": p[1],
                "author_email": p[2], "author_time": p[3]}

    def latest_ledger_commit(self):
        return self.run("log", "-1", "--format=%H", "--",
                        "amelia-1/outside/ledger_outside2.jsonl") or None

    def publish(self, paths, message):
        rel = [str(Path(p).resolve().relative_to(self.root.resolve()))
               for p in paths if Path(p).exists()]
        if not rel:
            return None
        self.run("add", "--", *rel)
        if not self.run("diff", "--cached", "--name-only"):
            return None
        self.run("commit", "-q", "-m", message)
        for attempt in range(6):
            p = subprocess.run(["git", "push", self.remote, "HEAD:refs/heads/" + self.branch],
                               cwd=self.root, capture_output=True, text=True)
            if p.returncode == 0:
                return self.run("rev-parse", "HEAD")
            self.run("fetch", "-q", self.remote, self.branch)
            r = subprocess.run(["git", "rebase", f"{self.remote}/{self.branch}"],
                               cwd=self.root, capture_output=True, text=True)
            if r.returncode:
                subprocess.run(["git", "rebase", "--abort"], cwd=self.root, capture_output=True)
                raise Halt(f"cannot rebase onto {self.branch}: branch changed incompatibly")
            time.sleep(2 + attempt * 3)
        raise Halt("push failed after retries; evidence remains in the workflow artifact")


def write_once(path, obj):
    """Immutable JSON; identical existing content is accepted for restart safety."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        old = json.loads(path.read_text())
        if canonical(old) != canonical(obj):
            raise Halt(f"existing evidence {path.name} differs; refusing overwrite")
        return path
    with path.open("x", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    return path


def fetch_round_default(relay, rnd):
    import audit_beacon_outside2 as AB
    return AB.fetch_round(relay, rnd)


def validate_round_record(record, rnd, bls):
    ok = [x.get("response", {}) for x in record.get("responses", [])
          if "error" not in x.get("response", {})]
    if len(ok) < 2:
        raise Halt(f"round {rnd}: stored evidence has fewer than two reachable relays")
    vals = {(v.get("round"), v.get("randomness"), v.get("signature")) for v in ok}
    if len(vals) != 1:
        raise Halt(f"round {rnd}: stored relay evidence disagrees")
    (r, randomness, signature), = vals
    if r != rnd or not bls.verify(rnd, signature):
        raise Halt(f"round {rnd}: stored beacon evidence fails round/BLS verification")
    return dict(record, randomness=randomness, signature=signature,
                agreeing_relays=len(ok), bls_verified=True)


def authenticated_round(rnd, fetch, bls, clock=time.time, sleep=time.sleep):
    import Outside2 as O2
    wait = O2.round_time(rnd) + RESOLVE_MARGIN - clock()
    if wait > 0:
        sleep(wait)
    give_up = max(clock(), O2.round_time(rnd)) + FETCH_PATIENCE
    while True:
        got = {relay: fetch(relay, rnd) for relay in RELAYS}
        ok = {k: v for k, v in got.items() if "error" not in v}
        if len(ok) >= 2 or clock() > give_up:
            break
        sleep(10)
    record = {"round": rnd, "fetched_utc": now_utc(),
              "responses": [{"relay": k, "response": v} for k, v in got.items()]}
    if len(ok) < 2:
        raise Halt(f"round {rnd}: fewer than two relays answered", record)
    vals = {(v.get("round"), v.get("randomness"), v.get("signature")) for v in ok.values()}
    if len(vals) != 1:
        raise Halt(f"round {rnd}: reachable relays disagree", record)
    (r, randomness, signature), = vals
    if r != rnd:
        raise Halt(f"round {rnd}: relays returned round {r}", record)
    if not bls.verify(rnd, signature):
        raise Halt(f"round {rnd}: BLS signature does not verify", record)
    record.update({"randomness": randomness, "signature": signature,
                   "agreeing_relays": len(ok), "bls_verified": True})
    return record


def reading_for(O2, w):
    xs = [e for e in O2.entries() if e["working"] == w and e["event_type"] == "READING"]
    if len(xs) != 1:
        raise Halt(f"{w}: expected exactly one READING")
    return xs[0]


def receipt_object(w, req, git, reading, tsa, deadline, commit, pushed=None, reconstructed=False):
    provenance = git.request_provenance(req["file"]) if req else {"note": "request absent in checkout"}
    return {
        "schema": "OUTSIDE-2-queue-admission-2", "working": w, "synthetic": False,
        "reading_event_hash": reading["event_hash"], "request": req,
        "request_git_provenance": provenance,
        "beacon_round": reading["payload"]["beacon_round"], "beacon_deadline_unix": deadline,
        "pushed_commit": commit, "tsa": tsa,
        "github_timing": {
            "runner_push_completed_utc": (datetime.fromtimestamp(pushed, timezone.utc).isoformat()
                                          if pushed is not None else None),
            "runner_push_before_deadline": (pushed < deadline if pushed is not None else None),
            "run_id": os.environ.get("GITHUB_RUN_ID"),
            "reconstructed_after_partial_run": reconstructed,
            "note": "runner clock is not an independent publication timestamp; RFC 3161 is the "
                    "primary independent pre-beacon existence evidence. Event-feed availability "
                    "is not assumed."
        }
    }


def ensure_receipt(w, req, git, log):
    import Outside2 as O2
    import outside2_timing as T
    rd = reading_for(O2, w)
    reg = json.loads((HERE / "outside2_registration.json").read_text())
    end = T.deadline(rd, reg)
    tsa = T.verify_token(TIMING / (w + ".tsr"), rd["event_hash"], end)
    p = TIMING / (w + "_PUSH.json")
    if p.exists():
        old = json.loads(p.read_text())
        if old.get("reading_event_hash") != rd["event_hash"]:
            raise Halt(f"{w}: admission receipt is bound to another reading")
        return old
    obj = receipt_object(w, req, git, rd, tsa, end, git.latest_ledger_commit(),
                         None, reconstructed=True)
    write_once(p, obj)
    git.publish([p], f"Record OUTSIDE-2 {w} reconstructed admission receipt")
    log.append({"working": w, "step": "admission receipt reconstructed", "tsa": tsa["status"]})
    return obj


def admit_step(w, req, git, log):
    import Outside2 as O2
    import outside2_timing as T
    out = O2.cast(w, req["tosses"])
    rd = reading_for(O2, w)
    reg = json.loads((HERE / "outside2_registration.json").read_text())
    end = T.deadline(rd, reg)
    TIMING.mkdir(parents=True, exist_ok=True)
    try:
        resp = T.obtain_token(TIMING / w, rd["event_hash"])
        tsa = T.verify_token(resp, rd["event_hash"], end)
    except Exception as exc:
        tsa = {"status": "INCOMPLETE", "reason": f"{type(exc).__name__}: {exc}"}
    commit = git.publish([O2.LEDGER, TIMING / (w + ".tsq"), TIMING / (w + ".tsr")],
                         f"Admit OUTSIDE-2 {w} from queued request ({req['source']}); "
                         f"RFC3161 {tsa['status']}")
    pushed = time.time()
    receipt = receipt_object(w, req, git, rd, tsa, end, commit, pushed)
    rp = write_once(TIMING / (w + "_PUSH.json"), receipt)
    git.publish([rp], f"Record OUTSIDE-2 {w} admission receipt")
    log.append({"working": w, "step": "admitted", "beacon_round": out["beacon_round"],
                "tsa": tsa["status"], "push_before_deadline": pushed < end,
                "request_commit": receipt["request_git_provenance"].get("commit")})
    if tsa["status"] == "FAIL":
        raise Halt(f"{w}: timestamp token failed verification: {tsa.get('reason')}")
    return receipt


def resolve_step(w, req, git, log, fetch, bls, clock=time.time, sleep=time.sleep):
    import Outside2 as O2
    ensure_receipt(w, req, git, log)
    rd = reading_for(O2, w)
    rnd = rd["payload"]["beacon_round"]
    relay_path = TIMING / (w + "_RELAY_RESPONSES.json")
    if relay_path.exists():
        rec = validate_round_record(json.loads(relay_path.read_text()), rnd, bls)
    else:
        try:
            rec = authenticated_round(rnd, fetch, bls, clock, sleep)
        except Halt as h:
            if h.evidence:
                incident_relay = BATCHES / f"RELAY_INCIDENT_{w}_{os.environ.get('GITHUB_RUN_ID','local')}.json"
                write_once(incident_relay, h.evidence)
                git.publish([incident_relay], f"Record OUTSIDE-2 {w} relay incident evidence")
            raise
        write_once(relay_path, rec)
    O2.resolve(w, rec["randomness"], rec["signature"])
    v = O2.verify()
    vp = write_once(TIMING / (w + "_VERIFY.json"), dict(v, working=w, verified_utc=now_utc()))
    if not v["chain_ok"]:
        raise Halt(f"{w}: ledger replay failed after resolution: {v.get('problems')}")
    fp = write_once(TIMING / (w + "_FEEDBACK.json"), O2.feedback(w))
    git.publish([O2.LEDGER, relay_path, vp, fp],
                f"Resolve OUTSIDE-2 {w} from BLS-verified drand round {rnd} (queue)")
    log.append({"working": w, "step": "resolved", "beacon_round": rnd,
                "relays": rec["agreeing_relays"]})


def batch_audit(git, log, run_tag):
    import audit_beacon_outside2 as AB
    import Outside2 as O2
    rep = AB.audit(str(O2.LEDGER), str(HERE / "outside2_registration.json"), False, TIMING)
    worked = sorted({x["working"] for x in log if "working" in x})
    per, states = {}, []
    for w in worked:
        beacon = rep["workings"].get(w, {}).get("status")
        timing = rep.get("timing", {}).get(w, {}).get("status")
        relay = "NOT_APPLICABLE"
        rp = TIMING / (w + "_RELAY_RESPONSES.json")
        if rp.exists():
            rr = json.loads(rp.read_text())
            relay = "PASS" if rr.get("bls_verified") and int(rr.get("agreeing_relays", 0)) >= 2 else "FAIL"
        per[w] = {"beacon": beacon, "timing": timing, "relay": relay}
        for x in (beacon, timing, relay):
            if x not in (None, "NOT_APPLICABLE"):
                states.append(x)
    batch_verdict = ("FAIL" if "FAIL" in states else
                     "PASS" if states and all(x == "PASS" for x in states) else "INCOMPLETE")
    summary = {
        "schema": "OUTSIDE-2-queue-batch-2", "run": run_tag, "completed_utc": now_utc(),
        "steps": log, "batch_verdict": batch_verdict,
        "cumulative_audit_verdict": rep["verdict"],
        "cumulative_audit_failures": rep["failures"],
        "workings_this_run": per, "ledger_head": rep["global"].get("head"),
        "events": rep["global"].get("events"),
        "note": "batch_verdict evaluates only workings handled in this run; cumulative status may "
                "remain INCOMPLETE because of historical evidence gaps such as W015. No ranks or "
                "test statistics are computed by the queue runner."
    }
    p = write_once(BATCHES / f"BATCH_{run_tag}.json", summary)
    git.publish([p], f"OUTSIDE-2 queue batch audit {run_tag}: {batch_verdict} "
                     f"(cumulative {rep['verdict']})")
    return summary


def run():
    import Outside2 as O2
    import audit_beacon_outside2 as AB
    git = Git()
    tag = "%s_%s" % (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
                     os.environ.get("GITHUB_RUN_ID", "local"))
    log, incident = [], None
    try:
        bls = AB.BLS()
        kat = AB.KAT
        if not bls.verify(kat["round"], kat["signature"]) or bls.verify(kat["round"] + 1, kat["signature"]):
            raise Halt("BLS known-answer test failed")
        v = O2.verify()
        if not v["chain_ok"]:
            raise Halt(f"ledger replay failed before run: {v.get('problems')}")
        reqs = parse_requests()
        for w, req in reqs.items():
            casts = [e for e in O2.entries() if e["working"] == w and e["event_type"] == "CAST"]
            if casts and casts[0]["payload"]["tosses"] != req["tosses"]:
                raise Halt(f"{req['source']} conflicts with ledger cast for {w}")
        handled = 0
        while handled < MAX_WORKINGS:
            w = O2.status()["next"]
            if w is None:
                log.append({"step": "series complete"})
                break
            state = [e["event_type"] for e in O2.entries() if e["working"] == w]
            if state == ["CAST", "READING"]:
                resolve_step(w, reqs.get(w), git, log, fetch_round_default, bls)
                handled += 1
                continue
            if state:
                raise Halt(f"{w} in unexpected state {state}")
            if w not in reqs:
                log.append({"step": "queue empty", "next": w})
                break
            admit_step(w, reqs[w], git, log)
        if handled >= MAX_WORKINGS:
            log.append({"step": "stopped at per-run limit", "limit": MAX_WORKINGS})
    except Halt as h:
        incident = str(h)
    except Exception as exc:
        incident = f"{type(exc).__name__}: {exc}"
    if incident:
        log.append({"step": "HALT", "incident": incident, "utc": now_utc()})
        p = write_once(BATCHES / f"INCIDENT_{tag}.json",
                       {"run": tag, "incident": incident, "steps": log,
                        "ledger": [e["event_id"] for e in O2.entries()]})
        try:
            git.publish([p, O2.LEDGER], f"OUTSIDE-2 queue halted {tag}: {incident[:80]}")
        except Halt:
            pass
    summary = batch_audit(git, log, tag) if any("working" in x for x in log) else {"steps": log}
    summary["incident"] = incident
    return summary


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=1, ensure_ascii=False))
    sys.exit(1 if result.get("incident") else 0)
