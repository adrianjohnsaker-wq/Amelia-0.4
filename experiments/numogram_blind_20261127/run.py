#!/usr/bin/env python3
"""Source-isolated, blinded 0.4 tensor-Numogram preparation; no model calls."""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
if (ROOT / "source" / "Numogram.py").exists():
    sys.path.insert(0, str(ROOT / "source"))
else:
    sys.path.insert(0, str(REPO))
import Numogram  # noqa: E402
import P312AssayCore  # noqa: E402
import ProcessFieldMemory  # noqa: E402
import decoder  # noqa: E402

WORDS = ("qevral", "lumeth", "sorvak", "tivren")
NEUTRAL = "neutral-bridge-input"
NTRAIN = 80
NSTEPS = 8
ALPHABET = "ABCD"
EXPECTED_BLOBS = {"Numogram.py": "7b2707d285f8bb4498d5830a120e976dc9f12eed",
                  "FullNumogram.py": "abe5ef6f96d7d18c5d77691b97a23d50f5149d05",
                  "P312AssayCore.py": "d66558307259928c0fdc58a0d2f159671ccab4f7",
                  "ProcessFieldMemory.py": "22242425a36effb6361c9a08d8feb93e216445db"}


def canonical(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha_text(x):
    return hashlib.sha256(x.encode("utf-8")).hexdigest()


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(("blob " + str(len(data)) + "\0").encode() + data).hexdigest()


def source_root():
    return ROOT / "source" if (ROOT / "source" / "Numogram.py").exists() else REPO


def verify_inputs():
    for name, expected in EXPECTED_BLOBS.items():
        if git_blob(source_root() / name) != expected:
            raise RuntimeError("0.4 source blob mismatch: " + name)
    scenarios = json.loads((ROOT / "scenarios.json").read_text())
    if len(scenarios) != 12 or len({s["id"] for s in scenarios}) != 12:
        raise ValueError("need exactly twelve unique public questions")
    for row in scenarios:
        if set(row) != {"id", "question", "options"} or len(row["options"]) != 4:
            raise ValueError("invalid public question")
        if any(w in canonical(row).lower() for w in WORDS):
            raise ValueError("source symbol leaked into public question")
    return scenarios


def vector(x):
    return [float(a) for a in x.tolist()]


def predict(system, origin, context):
    probabilities, fallback = system.predict_transitions(origin, context)
    if fallback:
        raise RuntimeError("Numogram fallback invalidates this calibration")
    return vector(probabilities)


def calibrate():
    # Only taught code labels are used; no private source target or test seed.
    sums = [[[0.0] * 10 for _ in range(4)] for _ in range(10)]
    raw = [[[0.0] * 10 for _ in range(4)] for _ in range(10)]
    neutral = P312AssayCore._context_for_text(NEUTRAL)
    contexts = [P312AssayCore._context_for_text(word) for word in WORDS]
    for seed in range(20000, 20000 + NTRAIN):
        system = Numogram.TensorBasedNumogramSystem(seed=seed, dimension=3)
        for origin in range(10):
            baseline = predict(system, origin, neutral)
            for code in range(4):
                p = predict(system, origin, contexts[code])
                for i in range(10):
                    sums[origin][code][i] += (p[i] - baseline[i]) / NTRAIN
                    raw[origin][code][i] += p[i] / NTRAIN
    return {"delta_means": sums, "transition_means": raw, "training_seeds": NTRAIN}


class Source:
    def __init__(self):
        self.process = subprocess.Popen([sys.executable, str(ROOT / "source_agent.py")],
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        text=True, bufsize=1)

    def request(self, payload):
        if self.process.poll() is not None:
            raise RuntimeError("controlled source process stopped")
        self.process.stdin.write(canonical(payload) + "\n")
        self.process.stdin.flush()
        line = self.process.stdout.readline()
        if not line:
            raise RuntimeError("controlled source returned no response")
        answer = json.loads(line)
        if not answer.get("ok"):
            raise RuntimeError("controlled source rejected request: " + str(answer.get("error")))
        return answer

    def close(self):
        if self.process.poll() is None:
            self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=5)


def step_system(system, origin, word, challenge):
    context = P312AssayCore._context_for_text(word)
    neutral = P312AssayCore._context_for_text(NEUTRAL)
    before = predict(system, origin, neutral)
    event = system.transition(origin, context)
    pfm_input = P312AssayCore._pfm_payload(word, event)
    pfm = json.loads(ProcessFieldMemory.amelia_event(canonical(pfm_input)))
    if pfm.get("status") != "contribution_ready":
        raise RuntimeError("0.4 PFM rejected event")
    allowed = {"origin": int(origin), "destination": int(event["to"]),
               "probabilities": event["probabilities"], "neutral_probabilities": before,
               "challenge": int(challenge)}
    decoder.validate_event(allowed)
    return allowed, {"event": event, "pfm": pfm, "input_digest": context["input_digest"]}


def replay(seed, challenges, words):
    global ProcessFieldMemory
    ProcessFieldMemory = importlib.reload(ProcessFieldMemory)
    system = Numogram.TensorBasedNumogramSystem(seed=seed, dimension=3)
    origin, events, traces = 3, [], []
    for challenge, word in zip(challenges, words):
        allowed, trace = step_system(system, origin, word, challenge)
        events.append(allowed)
        traces.append(trace)
        origin = allowed["destination"]
    return events, traces


def render_prompt(scenario, suggestion):
    options = "\n".join("{}: {}".format(ALPHABET[i], value) for i, value in enumerate(scenario["options"]))
    return ("You are a secondary language relay. The source's private observation is not available to you. "
            "A fallible decoder indicates option {}. Using only that report, answer the public question "
            "in two lines: 'CHOICE: <letter>' and a concise, clearly tentative explanation. "
            "Do not add facts that are not in the options.\n\nQuestion: {}\n{}\n".format(
                ALPHABET[suggestion], scenario["question"], options))


def signal_audit(decoder_payload, prompts):
    dec = canonical(decoder_payload).lower()
    if any(w in dec for w in WORDS):
        raise RuntimeError("raw source symbol reached decoder input")
    for row in prompts:
        if any(w in row["prompt"].lower() for w in WORDS):
            raise RuntimeError("raw source symbol reached relay prompt")


def journal(out, event):
    with (out / "progress.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(canonical(event) + "\n")
        handle.flush()


def selftest():
    scenarios = verify_inputs()
    # Boundary fixture: an invented, non-biological model tests whitelist and
    # plumbing only. Real trials require Torch and the unmodified 0.4 source.
    q = [0.1] * 10
    cal = {"delta_means": [[[0.0] * 10 for _ in range(4)] for _ in range(10)],
           "transition_means": [[[0.1] * 10 for _ in range(4)] for _ in range(10)],
           "training_seeds": NTRAIN}
    e = {"origin": 3, "destination": 3, "probabilities": q, "neutral_probabilities": q, "challenge": 0}
    trial = {"case_id": "fixture", "condition": "neutral", "events": [e] * NSTEPS}
    assert set(decoder.read_trial(cal, trial)) == {"case_id", "condition", "probability_reader", "gate_only_reader", "probability_costs", "gate_log_scores"}
    try:
        decoder.validate_event(dict(e, raw_source_word=WORDS[0]))
        raise RuntimeError("decoder accepted raw source data")
    except ValueError:
        pass
    src = Source()
    try:
        for s in scenarios:
            result = src.request({"op": "init", "case_id": s["id"]})
            assert len(result["commitment"]) == 64 and "goal" not in result
            for k in range(NSTEPS):
                reply = src.request({"op": "step", "case_id": s["id"], "challenge": k % 4})
                assert reply["message"] in WORDS and "goal" not in reply
        locked = src.request({"op": "lock", "decisions_sha256": "a" * 64})
        assert len(locked["reveals"]) == 12
    finally:
        src.close()
    prompt = render_prompt(scenarios[0], 2)
    signal_audit({"calibration": cal, "trials": [trial]}, [{"prompt": prompt}])
    print(canonical({"status": "PASS", "real_torch_used_in_fixture": False, "source_process": True,
                     "private_targets_hidden_before_lock": True, "decoder_rejects_raw_source_key": True,
                     "twelve_public_questions": True, "source_blobs_verified": True}))


def run():
    scenarios = verify_inputs()
    if Numogram.torch is None:
        raise RuntimeError("actual 0.4 TensorBasedNumogramSystem needs Torch; no surrogate is permitted")
    start_ns = time.time_ns()
    out = ROOT / "output"
    out.mkdir(exist_ok=True)
    journal(out, {"stage": "started", "time_ns": start_ns})
    calibration = calibrate()
    calibration_digest = sha_text(canonical(calibration))
    journal(out, {"stage": "calibrated", "sha256": calibration_digest, "time_ns": time.time_ns()})
    source = Source()
    cases = []
    commitments = {}
    try:
        for s in scenarios:
            answer = source.request({"op": "init", "case_id": s["id"]})
            commitments[s["id"]] = {"sha256": answer["commitment"], "received_ns": time.time_ns()}
            journal(out, {"stage": "source_commitment", "case_id": s["id"], **commitments[s["id"]]})
        for s in scenarios:
            cid = s["id"]
            seed = 1000000 + secrets.randbelow(2000000000)
            global ProcessFieldMemory
            ProcessFieldMemory = importlib.reload(ProcessFieldMemory)
            system = Numogram.TensorBasedNumogramSystem(seed=seed, dimension=3)
            origin = 3
            messages, challenges, events, traces, ledger = [], [], [], [], []
            for t in range(NSTEPS):
                offset = secrets.randbelow(4)
                challenge = (origin + offset) % 4
                salt = secrets.token_hex(16)
                challenge_hash = sha_text("{}|{}|{}|{}".format(cid, t, challenge, salt))
                created = time.time_ns()
                journal(out, {"stage": "challenge_committed", "case_id": cid, "t": t,
                              "sha256": challenge_hash, "time_ns": created})
                reply = source.request({"op": "step", "case_id": cid, "challenge": challenge})
                received = time.time_ns()
                if reply["step"] != t + 1 or reply["message"] not in WORDS:
                    raise RuntimeError("unexpected source reply")
                word = reply["message"]
                allowed, trace = step_system(system, origin, word, challenge)
                processed = time.time_ns()
                messages.append(word)
                challenges.append(challenge)
                events.append(allowed)
                traces.append(trace)
                ledger.append({"t": t, "challenge": challenge, "challenge_salt": salt,
                               "challenge_commitment": challenge_hash, "created_ns": created,
                               "source_reply_ns": received, "processed_ns": processed,
                               "source_message": word})
                journal(out, {"stage": "active_step", "case_id": cid, "t": t,
                              "challenge": challenge, "challenge_salt": salt, "challenge_commitment": challenge_hash,
                              "created_ns": created, "source_reply_ns": received, "processed_ns": processed,
                              "source_message": word, "numogram_event": allowed})
                origin = allowed["destination"]
            cases.append({"case_id": cid, "seed": seed, "challenges": challenges,
                          "messages": messages, "active_events": events,
                          "active_traces": traces, "ledger": ledger})
        trials = []
        controls = []
        for i, case in enumerate(cases):
            donor = cases[(i + 1) % len(cases)]
            neutral, neutral_trace = replay(case["seed"], case["challenges"], [NEUTRAL] * NSTEPS)
            yoked, yoked_trace = replay(case["seed"], case["challenges"], donor["messages"])
            for condition, events in (("active", case["active_events"]), ("neutral", neutral), ("yoked", yoked)):
                trials.append({"case_id": case["case_id"], "condition": condition, "events": events})
            controls.append({"case_id": case["case_id"], "yoke_donor": donor["case_id"],
                             "neutral_traces": neutral_trace, "yoked_traces": yoked_trace})
        dec_input = {"calibration": calibration, "trials": trials}
        raw = canonical(dec_input)
        if any(w in raw.lower() for w in WORDS):
            raise RuntimeError("source symbols leaked into decoder payload")
        proc = subprocess.run([sys.executable, str(ROOT / "decoder.py")], input=raw, capture_output=True,
                              text=True, timeout=120, check=True)
        decisions = json.loads(proc.stdout)
        if len(decisions["records"]) != len(scenarios) * 3:
            raise RuntimeError("decoder returned wrong record count")
        index = {(r["case_id"], r["condition"]): r for r in decisions["records"]}
        prompts = []
        for s in scenarios:
            for condition in ("active", "yoked"):
                decision = index[(s["id"], condition)]["probability_reader"]
                prompt = render_prompt(s, decision)
                prompts.append({"case_id": s["id"], "condition": condition, "prompt": prompt,
                                "prompt_sha256": sha_text(prompt), "suggestion": decision})
        signal_audit(dec_input, prompts)
        lock_hash = sha_text(canonical({"decisions": decisions, "prompts": prompts}))
        lock_time = time.time_ns()
        # Persist exact reader inputs and decisions before the source reveals a
        # target, so scoring cannot retroactively change the blinded choices.
        for name, obj in (("decoder_input.json", dec_input), ("decoder_decisions.json", decisions),
                          ("render_inputs.json", prompts),
                          ("decision_lock.json", {"sha256": lock_hash, "locked_ns": lock_time})):
            (out / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")
        journal(out, {"stage": "pre_reveal_lock", "sha256": lock_hash, "time_ns": lock_time})
        reveal = source.request({"op": "lock", "decisions_sha256": lock_hash})
        revealed_time = time.time_ns()
        journal(out, {"stage": "source_revealed", "time_ns": revealed_time})
        if reveal["locked_decisions_sha256"] != lock_hash:
            raise RuntimeError("source refused exact decision lock")
        persisted = {"decisions": json.loads((out / "decoder_decisions.json").read_text()),
                     "prompts": json.loads((out / "render_inputs.json").read_text())}
        if sha_text(canonical(persisted)) != lock_hash:
            raise RuntimeError("pre-reveal decision files changed")
        answer_key = reveal["reveals"]
        for case in cases:
            cid = case["case_id"]
            secret = answer_key[cid]
            check = sha_text("{}|{}|{}".format(cid, secret["goal"], secret["salt"]))
            if check != commitments[cid]["sha256"]:
                raise RuntimeError("source commitment mismatch")
            for challenge, word in zip(case["challenges"], case["messages"]):
                if word != WORDS[(secret["goal"] + challenge) % 4]:
                    raise RuntimeError("source codebook response mismatch")
        result = {"status": "complete", "scope": "0.4 headless component on remote runner; programmed process source",
                  "cases": len(cases), "steps_per_case": NSTEPS, "calibration_seeds": NTRAIN,
                  "calibration_sha256": calibration_digest, "decision_and_prompt_sha256": lock_hash,
                  "started_ns": start_ns, "locked_ns": lock_time, "revealed_ns": revealed_time,
                  "conditions": {}}
        for condition in ("active", "neutral", "yoked"):
            condition_records = [r for r in decisions["records"] if r["condition"] == condition]
            result["conditions"][condition] = {
                "probability_reader_correct": sum(r["probability_reader"] == answer_key[r["case_id"]]["goal"] for r in condition_records),
                "gate_only_reader_correct": sum(r["gate_only_reader"] == answer_key[r["case_id"]]["goal"] for r in condition_records),
                "total": len(condition_records)}
        result["direct_codebook_correct"] = sum(all(w == WORDS[(answer_key[c["case_id"]]["goal"] + k) % 4]
                                                    for w, k in zip(c["messages"], c["challenges"])) for c in cases)
        result["source_commitments_verified"] = True
        result["decoder_and_prompts_sealed_before_reveal"] = lock_time < revealed_time
        for name, obj in (("summary.json", result), ("source_cases.json", cases), ("source_commitments.json", commitments),
                          ("answer_key.json", answer_key), ("decoder_input.json", dec_input),
                          ("decoder_decisions.json", decisions), ("controls.json", controls),
                          ("render_inputs.json", prompts)):
            (out / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")
        journal(out, {"stage": "complete", "time_ns": time.time_ns(), "cases": len(cases)})
        print("AMELIA_BLIND_NUMOGRAM_STATUS=" + canonical(result), flush=True)
    except Exception as exc:
        failure = {"status": "failed", "error_type": type(exc).__name__, "message": str(exc),
                   "time_ns": time.time_ns(), "completed_cases": len(cases)}
        (out / "failure.json").write_text(json.dumps(failure, indent=2) + "\n")
        journal(out, {"stage": "failed", **failure})
        raise
    finally:
        source.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        selftest()
    else:
        run()
