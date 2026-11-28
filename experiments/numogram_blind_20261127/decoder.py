#!/usr/bin/env python3
"""A deliberately narrow, supervised reader of 0.4 transition outputs."""
import json
import math
import sys

EVENT_KEYS = {"origin", "destination", "probabilities", "neutral_probabilities", "challenge"}
TRIAL_KEYS = {"case_id", "condition", "events"}
INPUT_KEYS = {"calibration", "trials"}


def validate_event(e):
    if set(e) != EVENT_KEYS:
        raise ValueError("decoder received non-whitelisted event keys")
    origin, dest, challenge = int(e["origin"]), int(e["destination"]), int(e["challenge"])
    if not 0 <= origin < 10 or not 0 <= dest < 10 or not 0 <= challenge < 4:
        raise ValueError("out-of-range event")
    for key in ("probabilities", "neutral_probabilities"):
        a = e[key]
        if len(a) != 10 or any(not math.isfinite(float(x)) or float(x) < 0 for x in a):
            raise ValueError("invalid probability vector")
        if abs(sum(float(x) for x in a) - 1.0) > .0001:
            raise ValueError("probability vector does not sum to one")


def read_trial(calibration, trial):
    if set(trial) != TRIAL_KEYS or len(trial["events"]) != 8:
        raise ValueError("non-whitelisted trial keys or wrong number of events")
    for event in trial["events"]:
        validate_event(event)
    probability_costs = [0.0] * 4
    gate_log_scores = [0.0] * 4
    for e in trial["events"]:
        origin = int(e["origin"])
        dest = int(e["destination"])
        challenge = int(e["challenge"])
        difference = [float(a) - float(b) for a, b in zip(e["probabilities"], e["neutral_probabilities"])]
        for goal in range(4):
            code = (goal + challenge) % 4
            prototype = calibration["delta_means"][origin][code]
            probability_costs[goal] += sum((difference[i] - float(prototype[i])) ** 2 for i in range(10))
            probability = max(1e-12, float(calibration["transition_means"][origin][code][dest]))
            gate_log_scores[goal] += math.log(probability)
    return {"case_id": trial["case_id"], "condition": trial["condition"],
            "probability_reader": min(range(4), key=lambda g: probability_costs[g]),
            "gate_only_reader": max(range(4), key=lambda g: gate_log_scores[g]),
            "probability_costs": probability_costs, "gate_log_scores": gate_log_scores}


def main():
    incoming = json.load(sys.stdin)
    if set(incoming) != INPUT_KEYS:
        raise ValueError("decoder received non-whitelisted top-level keys")
    records = [read_trial(incoming["calibration"], t) for t in incoming["trials"]]
    print(json.dumps({"records": records}, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
