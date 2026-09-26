"""Amelia P3.12 matched causal incorporation assay core.

This module does not replace the live Numogram singleton. It constructs three
fresh throwaway TensorBasedNumogramSystem instances with the same seed and
runs the same two prompt-derived contexts through each:

A_ABSENT   : no ProcessFieldMemory calls.
B_RETAINED : one ProcessFieldMemory instance retains event 1 into event 2.
C_RESET    : the exact same ProcessFieldMemory module is reloaded before each
             event, so event 2 starts from a zeroed PFM state.

The second event is the predeclared critical comparison.

ProcessFieldMemory is imported from the repository's existing
process_field_memory.py source. P3.12 does not reimplement its update law.
"""

import hashlib
import importlib
import json

import Numogram
import process_field_memory as ProcessFieldMemory


ASSAY_SCHEMA = "amelia-p3.12-causal-incorporation-assay-v1"
ZONE_COUNT = 10
INITIAL_ZONE = 3
CONDITIONS = ("A_ABSENT", "B_RETAINED", "C_RESET")

_BRANCH_SYSTEMS = {}
_BRANCH_SEALED_DIGESTS = {}


def _canonical(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _sha256_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _context_for_text(user_text):
    """Exact Python port of EventModulePlanner.numogramContext."""
    digest = hashlib.sha256(user_text.encode("utf-8")).hexdigest()
    zone_bias = []

    for zone in range(ZONE_COUNT):
        offset = (zone * 6) % (len(digest) - 6)
        chunk = digest[offset:offset + 6]
        raw = int(chunk, 16) / float(0xFFFFFF)
        zone_bias.append((raw - 0.5) * 0.18)

    return {
        "schema": "amelia-p3.10-input-field-v1",
        "zone_bias": zone_bias,
        "input_digest": digest,
    }


def _event_type(origin, destination):
    """Exact logical ordering used by EventModulePlanner.eventType."""
    if destination == origin:
        return "RECURRENCE"
    if origin + destination == 9:
        return "SYZYGETIC_CONJUNCTION"
    if destination == 0 or destination == 9:
        return "TERMINAL_INGRESSION"
    if abs(destination - origin) >= 5:
        return "INTENSIVE_CROSSING"
    return "TRANSITIONAL_PREHENSION"


def _pfm_payload(user_text, transition):
    return {
        "schema": "amelia-p3.10-module-event-v1",
        "user_input": user_text,
        "transition": transition,
        "event_plan": {
            "schema": "amelia-p3.12-assay-event-plan-v1",
            "event_type": _event_type(
                int(transition["from"]),
                int(transition["to"]),
            ),
        },
    }


def _reload_pfm():
    global ProcessFieldMemory
    ProcessFieldMemory = importlib.reload(ProcessFieldMemory)
    return ProcessFieldMemory


def _call_pfm(user_text, transition):
    raw = ProcessFieldMemory.amelia_event(
        _canonical(_pfm_payload(user_text, transition))
    )
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise RuntimeError("ProcessFieldMemory returned a non-object payload")
    if parsed.get("schema") != "amelia-p3.11-process-field-memory-v1":
        raise RuntimeError("Unexpected ProcessFieldMemory schema")
    if parsed.get("status") != "contribution_ready":
        raise RuntimeError("ProcessFieldMemory did not produce a contribution")
    return parsed


def _system_digest(system):
    """Digest all transition-relevant mutable Numogram state."""
    generator_state = system._torch_generator.get_state().tolist()
    payload = {
        "status": system.status(),
        "transition_tensor": [
            [round(float(cell), 10) for cell in row]
            for row in system.transition_tensor.tolist()
        ],
        "zone_magnetism": [
            [round(float(cell), 10) for cell in row]
            for row in system.zone_magnetism.tolist()
        ],
        "transition_history": system.transition_history,
        "generator_state": generator_state,
        "last_fallback_triggered": bool(system._last_fallback_triggered),
    }
    return _sha256_text(_canonical(payload))


def _run_branch(condition, prompt_one, prompt_two, seed, dimension):
    if condition not in CONDITIONS:
        raise ValueError("unknown P3.12 condition")

    system = Numogram.TensorBasedNumogramSystem(
        seed=int(seed),
        dimension=int(dimension),
    )
    current_zone = INITIAL_ZONE

    pfm_event_one = None
    pfm_event_two = None

    if condition == "B_RETAINED":
        _reload_pfm()
    elif condition == "C_RESET":
        _reload_pfm()

    context_one = _context_for_text(prompt_one)
    event_one = system.transition(current_zone, context_one)
    current_zone = int(event_one["to"])

    if condition == "B_RETAINED":
        pfm_event_one = _call_pfm(prompt_one, event_one)
    elif condition == "C_RESET":
        _reload_pfm()
        pfm_event_one = _call_pfm(prompt_one, event_one)

    context_two = _context_for_text(prompt_two)
    event_two = system.transition(current_zone, context_two)
    current_zone = int(event_two["to"])

    if condition == "B_RETAINED":
        pfm_event_two = _call_pfm(prompt_two, event_two)
    elif condition == "C_RESET":
        # This is the intervention: erase PFM state immediately before the
        # critical second event while leaving the Numogram sequence untouched.
        _reload_pfm()
        pfm_event_two = _call_pfm(prompt_two, event_two)

    sealed_digest = _system_digest(system)
    _BRANCH_SYSTEMS[condition] = system
    _BRANCH_SEALED_DIGESTS[condition] = sealed_digest

    return {
        "condition": condition,
        "prompt_one_digest": context_one["input_digest"],
        "prompt_two_digest": context_two["input_digest"],
        "event_one": event_one,
        "event_two": event_two,
        "pfm_event_one": pfm_event_one,
        "pfm_event_two": pfm_event_two,
        "system_status_after_event_two": system.status(),
        "sealed_system_digest": sealed_digest,
    }


def _events_identical(branches, key):
    reference = _canonical(branches["A_ABSENT"][key])
    return all(
        _canonical(branches[name][key]) == reference
        for name in CONDITIONS
    )


def run_assay(prompt_one, prompt_two, seed=3606, dimension=3):
    if not isinstance(prompt_one, str) or not prompt_one.strip():
        raise ValueError("prompt_one must be non-empty")
    if not isinstance(prompt_two, str) or not prompt_two.strip():
        raise ValueError("prompt_two must be non-empty")

    # New assay invalidates any previously retained branch handles.
    _BRANCH_SYSTEMS.clear()
    _BRANCH_SEALED_DIGESTS.clear()

    branches = {
        condition: _run_branch(
            condition,
            prompt_one,
            prompt_two,
            int(seed),
            int(dimension),
        )
        for condition in CONDITIONS
    }

    event_one_match = _events_identical(branches, "event_one")
    event_two_match = _events_identical(branches, "event_two")

    b_second = branches["B_RETAINED"]["pfm_event_two"]
    c_second = branches["C_RESET"]["pfm_event_two"]

    a_absent = (
        branches["A_ABSENT"]["pfm_event_one"] is None
        and branches["A_ABSENT"]["pfm_event_two"] is None
    )
    b_depth = int((b_second or {}).get("history_depth", -1))
    c_depth = int((c_second or {}).get("history_depth", -1))

    causal_memory_contrast = (
        event_one_match
        and event_two_match
        and a_absent
        and b_depth == 2
        and c_depth == 1
    )

    result = {
        "schema": ASSAY_SCHEMA,
        "seed": int(seed),
        "dimension": int(dimension),
        "initial_zone": INITIAL_ZONE,
        "prompt_one": prompt_one,
        "prompt_two": prompt_two,
        "branches": branches,
        "primary_endpoint": {
            "event_one_identical_across_conditions": event_one_match,
            "event_two_identical_across_conditions": event_two_match,
            "a_pfm_absent": a_absent,
            "b_second_history_depth": b_depth,
            "c_second_history_depth": c_depth,
            "causal_memory_contrast_held": causal_memory_contrast,
        },
    }
    result["assay_digest"] = _sha256_text(_canonical(result))
    return _canonical(result)


def get_branch_status(condition):
    if condition not in CONDITIONS:
        raise ValueError("unknown P3.12 condition")
    system = _BRANCH_SYSTEMS.get(condition)
    sealed = _BRANCH_SEALED_DIGESTS.get(condition)

    if system is None or sealed is None:
        return _canonical({
            "schema": "amelia-p3.12-branch-status-v1",
            "condition": condition,
            "status": "absent",
        })

    current = _system_digest(system)
    return _canonical({
        "schema": "amelia-p3.12-branch-status-v1",
        "condition": condition,
        "status": "ready",
        "sealed_system_digest": sealed,
        "current_system_digest": current,
        "state_unchanged_from_seal": current == sealed,
        "system": system.status(),
    })
