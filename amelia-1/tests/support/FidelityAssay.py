"""
FidelityAssay.py -- Numogram Fidelity Assay 2.0 (Green Book)
Amelia Interface Programme, Stage I

Compares the derived structure (CanonicalNumogram.py) with the transcription of
the Green Book (GreenBookTranscription.py). Neither module reads the other; this
module is the only place they meet.

TIERS
    A  CCRU-stated rules against printed values. Verdict:
         PASS                              every check agrees
         PASS_WITH_REGISTERED_DEVIATIONS   every disagreement is registered below,
                                           with the evidence that the printed value,
                                           not the rule, departs
         FAIL                              any unregistered disagreement
    B  Programme-inferred rules against printed values. Reported as fit rates;
       each disagreement is listed. Tier B never changes the Tier A verdict.

Run:  python FidelityAssay.py            (summary)
      python FidelityAssay.py --json     (full report)
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from typing import Dict, List

import CanonicalNumogram as C
import GreenBookTranscription as G

ASSAY_VERSION = "FidelityAssay-2.2.0"

# ---------------------------------------------------------------------------
# Status codes (Stage I doctrine: the engine is normative with respect to explicit
# CCRU rules, diplomatic with respect to printed evidence, and non-reparative with
# respect to programme inference)
# ---------------------------------------------------------------------------

CONSISTENT = "CONSISTENT"            # derived value equals the printed value
SOURCE_CONFLICT = "SOURCE_CONFLICT"  # an explicit CCRU rule and a printed value disagree;
                                     # the engine follows the rule, the print is retained
INFERRED_MISFIT = "INFERRED_MISFIT"  # a programme-inferred rule fails to reproduce a print;
                                     # the print stands, the rule is not repaired
UNREGISTERED = "UNREGISTERED_FAILURE"

# Frozen anomaly sentinels: printed entries that the inferred rules do not explain.
# They are never used to tune an inferred rule. A successor rule earns credit for them
# only if it is frozen first, has independent warrant, keeps the existing fits, and
# then predicts them.
ANOMALY_SENTINELS: Dict[str, Dict[str, object]] = {
    "6::2": {
        "entry_line": 5584,
        "misfits": ["pitch.6::2", "rite.6::2.256", "subrites.6::2.256", "riteset.6::2"],
        "frozen": True,
        "use": "holdout for any successor to the pitch or traversal rules",
    },
}

# Glossary line of the rule behind each deviation kind
_RULE_LINES = {"clicks": 7096, "ciphers": 7093, "prowls": 7280, "shadows": 7301}

# ---------------------------------------------------------------------------
# Registered deviations: printed values that depart from the CCRU's own rules
# ---------------------------------------------------------------------------

_CLICK_NOTE = ("Glossary (L7096): clicking is exact matching, the 'cryptographic operation of a "
               "demonic Mesh-Number'. Nine mesh-numbers equal gate numbers (00, 01, 03, 06, 10, "
               "15, 21, 28, 36). The Matrix, headed 'Extracts', records four (Mesh-00, 01, 03, 36) "
               "and omits Mesh-06, 10, 15, 21, 28. The engine follows the glossary.")

KNOWN_DEVIATIONS: Dict[str, Dict[str, str]] = {
    "matrix.4::0.clicks": {"kind": "OMISSION", "note": _CLICK_NOTE},
    "matrix.5::0.clicks": {"kind": "OMISSION", "note": _CLICK_NOTE},
    "matrix.6::0.clicks": {"kind": "OMISSION", "note": _CLICK_NOTE},
    "matrix.7::0.clicks": {"kind": "OMISSION", "note": _CLICK_NOTE},
    "matrix.8::0.clicks": {"kind": "OMISSION", "note": _CLICK_NOTE},
    "matrix.6::0.ciphers": {
        "kind": "OMISSION",
        "note": "Glossary (L7093): ciphering is 'the same set of digits (irrespective of order)'. "
                "Net-span 6::0 and Gt-06 share {0, 6}, exactly as 3::0 shares {0, 3} with Gt-03, "
                "which the Matrix records for 3::0 (L5490). The 6::0 entry (L5572) omits Gt-06."},
    "matrix.8::4.prowls": {
        "kind": "CONTRADICTION",
        "note": "Glossary (L7280, L7301): Prowl = one side of a syzygy plus its tractor; Shadow = "
                "one side plus the twin of its tractor. Sink current: sides 5 and 4, tractor 1, "
                "tractor-twin 8. So 8::4 shadows the Sink current, as its partner 8::5 is printed "
                "doing (L5701). The 8::4 entry (L5693) prints 'Prowls Sink-Current'. All other "
                "printed prowl and shadow relations follow the definitions."},
    "matrix.8::4.shadows": {"kind": "CONTRADICTION", "note": "See matrix.8::4.prowls."},
}

# Tier B: notes on printed values that the inferred rules do not reproduce
TIER_B_NOTES: Dict[str, str] = {
    "pitch.6::2": "The pitch rule fits 44 of 45 entries. Under the rule each tone Ana-k and "
                  "Cth-k occurs equally often. With 6::2 printed as Cth-2 (L5585) instead of "
                  "Cth-1, Cth-2 occurs five times and Cth-1 four, and the symmetry breaks at "
                  "that single entry.",
    "rite.6::2.256": "Djuddha Rt-2 [256] (L5589) opens with a step along the Hold current from "
                     "Zone-2 without first crossing the 7::2 syzygy. Every other listed rite "
                     "obeys the traversal rule; its nearest valid route is [2756]. The same "
                     "entry carries the pitch anomaly.",
    "riteset.4::0": "The one generated route not printed, [451890], is the variant of [41890] "
                    "that reaches Zone-1 by crossing to Zone-5 and taking the Sink current "
                    "instead of Gt-10. The Matrix gives [41890] one sub-rite (L5512), so the "
                    "variant appears to be counted there rather than listed.",
    "subrites.4::0.41890": "See riteset.4::0.",
    "riteset.4::1": "As for 4::0: the generated [451] is the Sink-current variant of [41], "
                    "which the Matrix gives one sub-rite (L5519).",
    "subrites.4::1.41": "See riteset.4::1.",
    "riteset.4::3": "Generated [41872563] is not printed. Unexplained.",
    "riteset.6::4": "Generated [4187256] is not printed. Unexplained.",
    "riteset.6::2": "See rite.6::2.256.",
    "subrites.6::2.256": "See rite.6::2.256.",
    "subrites.6::3.X": "The Warp crossing 6->3 has two readings under the rule (crossing, Gt-21); "
                       "the Matrix gives two sub-rites, which would need three (e.g. the Warp "
                       "current counted separately). Unresolved.",
    "subrites.6::5.54187236": "Rule gives three alternative readings; the Matrix prints two sub-rites.",
    "secret_gate_possible": "Under the reading 'a gate is possible on this route', a rite "
                            "that can be read either through a gate or through the Sink "
                            "current would count as secret, and so be unlabelled. The Matrix "
                            "labels such rites Mj or Mn, so the printed labels favour the reading "
                            "'every valid reading requires a gate' (30 of 31 against 22 of 31).",
    "secret_gate_required.4::1.41": "Under the traversal rule [41] can only be read through "
                                    "Gt-10, yet it is labelled Mj (L5519); the same entry is "
                                    "behind riteset.4::1.",
    "subrites.7::1.72541": "Rule gives one alternative reading (Zone-4 to Zone-1 by the Sink current "
                           "or Gt-10); the Matrix prints none, although it counts the same "
                           "alternative for [27541] (L5486).",
}


# ---------------------------------------------------------------------------
# Assay
# ---------------------------------------------------------------------------

class _Report:
    def __init__(self) -> None:
        self.checks: List[Dict[str, object]] = []

    def check(self, cid: str, tier: str, rule: str, line, derived, printed) -> None:
        ok = _norm(derived) == _norm(printed)
        rec = {"id": cid, "tier": tier, "rule": rule, "line": line,
               "derived": _norm(derived), "printed": _norm(printed),
               "result": "PASS" if ok else "FAIL"}
        if ok:
            rec["status"] = CONSISTENT
        elif tier == "A" and cid in KNOWN_DEVIATIONS:
            attr = cid.split(".")[-1]
            rec["status"] = SOURCE_CONFLICT
            rec["deviation"] = KNOWN_DEVIATIONS[cid]
            rec["conflict"] = {"rule_id": rule, "rule_value": rec["derived"],
                               "printed_value": rec["printed"],
                               "source_line_rule": _RULE_LINES.get(attr),
                               "source_line_printed": line}
        elif tier == "B":
            rec["status"] = INFERRED_MISFIT
        else:
            rec["status"] = UNREGISTERED
        if not ok:
            note = TIER_B_NOTES.get(cid) or TIER_B_NOTES.get(cid.split(".")[0])
            if note:
                rec["note"] = note
        self.checks.append(rec)


def _norm(x):
    if isinstance(x, (set, frozenset)):
        return sorted(_norm(v) for v in x)
    if isinstance(x, dict):
        return {str(k): _norm(v) for k, v in sorted(x.items(), key=lambda kv: str(kv[0]))}
    if isinstance(x, (list, tuple)):
        return [_norm(v) for v in x]
    return x


def _ns(i: int, j: int) -> str:
    return "%d::%d" % (i, j)


def run(ng: C.CanonicalNumogram = None) -> Dict[str, object]:
    ng = ng or C.CanonicalNumogram()
    R = _Report()
    A, B = "A", "B"
    TC = {z for z, r in ng.region_of_zone.items() if r == C.REGION_TC}

    # --- System ---------------------------------------------------------
    S = G.SYSTEM
    R.check("system.time_circuit", A, "time_systems", S["time_systems_line"],
            list(ng.time_circuit_cycle), list(S["time_circuit_syzygies"]))
    R.check("system.binary_cycle", A, "binary_cycle", S["binary_cycle_line"],
            ng.binary_cycle, S["binary_cycle"])
    R.check("system.demons", A, "net_span", S["line"], len(ng.demons), S["demons"])
    R.check("system.mesh_range", A, "net_span", S["line"],
            (min(d.mesh for d in ng.demons.values()), max(d.mesh for d in ng.demons.values())),
            S["mesh_range"])
    R.check("system.syzygetic_null_pitch", A, "net_span", S["line"],
            {_ns(*k) for k, d in ng.demons.items() if d.syzygetic},
            {_ns(*e["net_span"]) for e in G.MATRIX if e["pitch"] == S["syzygetic_pitch"]})

    # --- Zones ----------------------------------------------------------
    for z, note in sorted(G.ZONE_NOTES.items()):
        zi = ng.zone_info[z]
        R.check("zone.%d.twin" % z, A, "zygonovism", note["line"], C.twin(z), note["twin"])
        R.check("zone.%d.region" % z, A, "time_systems", note["line"], zi.region, note["region"])
        R.check("zone.%d.region_ordinal" % z, A, "binary_cycle", note["line"],
                zi.region_ordinal, note["region_ordinal"])
        R.check("zone.%d.tractor_of" % z, A, "current", note["line"], zi.tractor_of, note["tractor_of"])
        if note["termini_ordinals"] is not None:
            R.check("zone.%d.channel_termini" % z, A, "gate", note["line"], zi.channel_termini,
                    sorted(C.cumulation(o) for o in note["termini_ordinals"]))

    # --- Gates ----------------------------------------------------------
    for n, gn in sorted(G.GATE_NOTES.items()):
        g = ng.gates[gn["source"]]
        R.check("gate.%d.course" % n, A, "gate", gn["line"],
                (g.number, g.zone, g.target), (n, gn["source"], gn["target"]))
    R.check("gate.0.disputed", A, "gate", G.GATE_NOTES[0]["line"],
            [g.number for g in ng.gates.values() if g.disputed], [0])
    R.check("gate.10.sole_pro_cyclic", A, "time_systems", G.GATE_NOTES[10]["line"],
            [g.number for g in ng.gates.values() if g.orientation == "pro"], [10])
    R.check("gate.28.sole_counter_cyclic", A, "time_systems", G.GATE_NOTES[28]["line"],
            [g.number for g in ng.gates.values() if g.orientation == "counter"], [28])
    R.check("gate.36.sole_tc_to_plex", A, "gate", G.GATE_NOTES[36]["line"],
            [c.gate for c in ng.channels.values()
             if c.source_region == C.REGION_TC and c.target_region == C.REGION_PLEX], [36])
    R.check("gate.3.torque_to_warp", A, "gate", G.GATE_NOTES[3]["line"],
            (ng.channels[3].source_region, ng.channels[3].target_region),
            (G.GATE_NOTES[3]["from_region"], G.GATE_NOTES[3]["to_region"]))
    R.check("gate.15.into_warp", A, "gate", G.GATE_NOTES[15]["line"],
            ng.channels[15].target_region, G.GATE_NOTES[15]["to_region"])
    R.check("gate.3.consolidation", A, "gate", G.GATE_NOTES[3]["line"],
            (C.cumulation(2), C.nth_prime(2), G.ZONE_NOTES[2]["mesh_tag"]),
            (G.GATE_NOTES[3]["consolidated_to"],) * 3)
    R.check("gate.45.involutionary_count", A, "gate", G.GATE_NOTES[45]["line"],
            sum(1 for g in ng.gates.values() if g.involutionary),
            G.GATE_NOTES[45]["involutionary_count"])

    # --- Glossary counts --------------------------------------------------
    gc = G.GLOSSARY_COUNTS
    classes = Counter(d.demon_class for d in ng.demons.values())
    amphi = [d for d in ng.demons.values() if d.demon_class == "Amphidemon"]
    R.check("glossary.amphidemons", A, "classes", gc["amphidemons"]["line"],
            (len(amphi), sum(d.amphi_kind == "warping" for d in amphi),
             sum(d.amphi_kind == "plexing" for d in amphi)),
            (gc["amphidemons"]["count"], gc["amphidemons"]["warping"], gc["amphidemons"]["plexing"]))
    R.check("glossary.chronodemons", A, "classes", gc["chronodemons"]["line"],
            (classes["Syzygetic Chronodemon"] + classes["Cyclic Chronodemon"],
             classes["Syzygetic Chronodemon"], classes["Cyclic Chronodemon"]),
            (gc["chronodemons"]["count"], gc["chronodemons"]["syzygetic"], gc["chronodemons"]["cyclic"]))
    chaotic = [k for k, d in ng.demons.items() if d.demon_class == "Chaotic Xenodemon"]
    R.check("glossary.chaotic_xenodemons", A, "classes", gc["chaotic_xenodemons"]["line"],
            (len(chaotic), all(not ng.routes(i, j) and not ng.routes(j, i) for i, j in chaotic)),
            (gc["chaotic_xenodemons"]["count"], gc["chaotic_xenodemons"]["trackless"]))
    R.check("glossary.decademons", A, "decademon", gc["decademons"]["line"],
            sum(1 for d in ng.demons.values() if d.decademon), gc["decademons"]["count"])
    R.check("glossary.imps", A, "imps", gc["imps"]["line"],
            (sum(d.imps_allotted for d in ng.demons.values()),
             any(d.imps_allotted for d in ng.demons.values() if d.is_door)),
            (gc["imps"]["count"], gc["imps"]["doors_have_imps"]))
    R.check("glossary.current_names", A, "current", gc["current_names"]["lines"],
            {_ns(*k): c.name for k, c in ng.currents.items()},
            {_ns(*k): v for k, v in gc["current_names"]["names"].items()})
    R.check("glossary.time_circuit_currents", A, "time_systems", gc["time_circuit_currents"]["line"],
            [ng.currents[k].name for k in ng.time_circuit_cycle], gc["time_circuit_currents"]["names"])

    # --- Matrix, entry by entry ------------------------------------------
    for e in G.MATRIX:
        i, j = e["net_span"]
        d = ng.demons[(i, j)]
        p = "matrix.%s." % _ns(i, j)
        L = e["line"]
        R.check(p + "mesh", A, "net_span", L, d.mesh, e["mesh"])
        R.check(p + "phase_list", A, "phase", e["phase_list_line"], (d.phase, d.mesh),
                (i, e["phase_list_mesh"]))
        R.check(p + "class", A, "classes", L, d.demon_class, e["class"])
        R.check(p + "feeds", A, "feed", L, d.feeds, e["feeds"])
        R.check(p + "prowls", A, "prowl", L, d.prowls, sorted(e["prowls"]))
        R.check(p + "shadows", A, "shadow", L, d.shadows, sorted(e["shadows"]))
        invol = {g.number for g in ng.gates.values() if g.involutionary}
        R.check(p + "haunts", A, "haunt", L, d.haunts,
                sorted(h for h in e["haunts"] if h not in invol))
        R.check(p + "ciphers", A, "cipher", L, d.cipher_gates, set(e["ciphers"]))
        R.check(p + "clicks", A, "click", L, d.click_gates, e["clicks"])
        R.check(p + "door", A, "phase", L, d.is_door, e["door"])
        R.check(p + "phase_limit", A, "phase", L, d.is_phase_limit, e["phase_limit"])
        R.check(p + "decademon", A, "decademon", L, d.decademon, e["decademon"])

        # rites: structural checks (Tier A)
        routes = [(n, r, lab, sub) for (n, r, lab, sub) in e["rites"] if r not in ("X", "?")]
        if d.syzygetic:
            R.check(p + "rites.syzygetic_crossing", A, "rite", L,
                    True, any(r == "X" for (_, r, _, _) in e["rites"]))
        if d.demon_class == "Chaotic Xenodemon":
            R.check(p + "rites.trackless", A, "classes", L,
                    not ng.routes(i, j) and not ng.routes(j, i),
                    any(r == "?" for (_, r, _, _) in e["rites"]))
        for (n, r, lab, sub) in routes:
            z = [int(c) for c in r]
            q = p + "rite.%s." % r
            R.check(q + "valid", A, "rite", L, ng.is_valid_route(z), True)
            R.check(q + "poles", A, "net_span", L, {z[0], z[-1]}, {i, j})
            if lab:
                R.check(q + "direction", A, "major_minor", L,
                        "Mj" if z[0] == i else "Mn", lab)
            if d.demon_class == "Amphidemon":
                R.check(q + "starts_in_time_circuit", A, "classes", L, z[0] in TC, True)
        if d.demon_class == "Cyclic Chronodemon":
            cover = set()
            for (n, r, lab, sub) in routes:
                if lab:
                    cover |= {int(c) for c in r}
            R.check(p + "rites.encompass_time_circuit", A, "cyclic", L, cover, TC)

    # --- Detailed entries -------------------------------------------------
    lu, ka = G.DETAILED["lurgo"], G.DETAILED["katak"]
    R.check("lurgo.mesh_click", A, "click", lu["mesh_clicks_gate"]["line"],
            ng.demons[(1, 0)].click_gates, [lu["mesh_clicks_gate"]["gate"]])
    R.check("lurgo.net_span_click", A, "click", lu["net_span_clicks_gate"]["line"],
            ng.demons[(1, 0)].net_span_click_gates, [lu["net_span_clicks_gate"]["gate"]])
    R.check("katak.ciphers_gt45", A, "cipher", ka["ciphers_gate"]["line"],
            45 in ng.demons[(5, 4)].cipher_gates, True)
    mk = ka["mesh_ciphers_net_span"]
    R.check("katak.mesh_ciphers_4::1", A, "cipher", mk["line"],
            (sorted("%02d" % ng.demons[(5, 4)].mesh) == sorted("%d%d" % mk["net_span"]),
             ng.demons[mk["net_span"]].mesh), (True, mk["mesh_of_that_demon"]))
    R.check("katak.sole_syzygetic_phase_limit", A, "phase", ka["sole_syzygetic_phase_limit"]["line"],
            [_ns(*k) for k, d in ng.demons.items() if d.syzygetic and d.is_phase_limit], ["5::4"])
    R.check("katak.feeds", A, "feed", ka["feeds"]["line"], ng.demons[(5, 4)].feeds,
            [ka["feeds"]["current"]])

    # === Tier B: inferred rules =============================================
    for e in G.MATRIX:
        i, j = e["net_span"]
        R.check("pitch.%s" % _ns(i, j), B, "pitch", e["line"],
                ng.demons[(i, j)].pitch_label, e["pitch"])
    R.check("pitch.extremes", B, "pitch", S["line"],
            (C.pitch_label(max(d.pitch for d in ng.demons.values())),
             C.pitch_label(min(d.pitch for d in ng.demons.values()))), S["pitch_extremes"])
    R.check("pitch.tone_count", B, "pitch", gc["pitch_tones"]["line"],
            len({d.pitch for d in ng.demons.values()}), gc["pitch_tones"]["count"])
    for z, note in sorted(G.ZONE_NOTES.items()):
        R.check("zone.%d.mesh_tag" % z, B, "zone_mesh_tag", note["mesh_tag_line"],
                ng.zone_info[z].mesh_tag, note["mesh_tag"])
        if note["phase_population"] is not None:
            R.check("zone.%d.phase_population" % z, B, "phase_population", note["phase_line"],
                    ng.zone_info[z].phase_population, note["phase_population"])
    R.check("lurgo.sarkon_tag", B, "demon_sarkon_tag", lu["sarkon_tag"]["line"],
            ng.demons[(1, 0)].sarkon_tag, lu["sarkon_tag"]["value"])
    R.check("katak.sarkon_tag", B, "demon_sarkon_tag", ka["sarkon_tag"]["line"],
            ng.demons[(5, 4)].sarkon_tag, ka["sarkon_tag"]["value"])
    R.check("lurgo.imps_hosted", B, "imps_hosted", lu["imps_hosted"]["line"],
            ng.demons[(1, 0)].imps_hosted, lu["imps_hosted"]["value"])
    R.check("katak.imps_hosted", B, "imps_hosted", ka["imps_hosted"]["line"],
            ng.demons[(5, 4)].imps_hosted, ka["imps_hosted"]["value"])
    invol = {g.number for g in ng.gates.values() if g.involutionary}
    for e in G.MATRIX:
        i, j = e["net_span"]
        R.check("direct_nesting_haunt.%s" % _ns(i, j), B, "direct_nesting_haunt", e["line"],
                ng.demons[(i, j)].direct_nesting_haunts,
                sorted(h for h in e["haunts"] if h in invol))
    # Secret rites (Glossary L7296: 'any rite involving one or more gates'). Two readings
    # are kept as separate observables; the printed Mj/Mn labels on cyclic chronodemon
    # rites (labelled = not secret) decide between them.
    for e in G.MATRIX:
        if e["class"] != "Cyclic Chronodemon":
            continue
        i, j = e["net_span"]
        for (n, r, lab, sub) in e["rites"]:
            z = [int(c) for c in r]
            rd = ng.route_readings(z, C.RULE_LEMURIAN)
            for name, secret in (("secret_gate_required", all(C.GATE in x for x in rd)),
                                 ("secret_gate_possible", any(C.GATE in x for x in rd))):
                R.check("%s.%s.%s" % (name, _ns(i, j), r), B, name, e["line"],
                        "unlabelled" if secret else "labelled",
                        "labelled" if lab else "unlabelled")
    R.check("lurgo.nests", B, "nesting", lu["nests"]["line"],
            ng.nests(1, 0), [tuple(x) for x in lu["nests"]["net_spans"]])

    def rite_strings(i, j):
        return sorted("".join(map(str, r.route)) for r in ng.rites(i, j))

    R.check("lurgo.paths", B, "lemurian_traversal", lu["paths"]["line"],
            rite_strings(1, 0), sorted(lu["paths"]["routes"]))
    R.check("katak.paths", B, "lemurian_traversal", ka["paths"]["line"],
            sorted(("".join(map(str, r.route)), r.kind) for r in ng.rites(5, 4)),
            sorted(zip(ka["paths"]["routes"], ka["paths"]["kinds"])))
    nonsyz = [_ns(*k) for k, d in ng.demons.items() if d.syzygetic
              and any(r.kind != "syzygetic" for r in ng.rites(*k))]
    R.check("katak.sole_syzygetic_with_nonsyzygetic_rite", B, "lemurian_traversal",
            ka["sole_syzygetic_with_nonsyzygetic_rite"]["line"], nonsyz, ["5::4"])
    kr = [r for r in ng.rites(5, 4) if r.kind != "syzygetic"]
    R.check("katak.rite_encircles_time_circuit", B, "lemurian_traversal",
            ka["nonsyzygetic_rite_encircles_time_circuit"]["line"],
            [set(r.route) == TC for r in kr], [True])

    for e in G.MATRIX:
        i, j = e["net_span"]
        for (n, r, lab, sub) in e["rites"]:
            if r == "?":
                continue
            z = [i, j] if r == "X" else [int(c) for c in r]
            R.check("rite.%s.%s" % (_ns(i, j), r), B, "lemurian_traversal", e["line"],
                    ng.is_valid_route(z, C.RULE_LEMURIAN), True)
            R.check("subrites.%s.%s" % (_ns(i, j), r), B, "sub_rites", e["line"],
                    len(ng.route_readings(z, C.RULE_LEMURIAN)) - 1, sub)
        listed = sorted({r if r != "X" else None for (_, r, _, _) in e["rites"]} - {None, "?"})
        gen = sorted("".join(map(str, x.route)) for x in ng.rites(i, j) if x.kind != "syzygetic")
        R.check("riteset.%s" % _ns(i, j), B, "lemurian_traversal", e["line"], gen, listed)

    # === Summary =============================================================
    tier_a = [c for c in R.checks if c["tier"] == A]
    fails_a = [c for c in tier_a if c["result"] == "FAIL"]
    unregistered = [c for c in fails_a if "deviation" not in c]
    verdict = ("FAIL" if unregistered else
               "PASS_WITH_REGISTERED_DEVIATIONS" if fails_a else "PASS")
    tier_b: Dict[str, Dict[str, int]] = {}
    for c in R.checks:
        if c["tier"] == B:
            t = tier_b.setdefault(c["rule"], {"pass": 0, "total": 0})
            t["total"] += 1
            t["pass"] += c["result"] == "PASS"
    return {
        "assay": ASSAY_VERSION,
        "engine": C.SPEC_VERSION,
        "canonical_digest": ng.digest(),
        "full_digest": ng.digest(include_inferred=True),
        "source": G.SOURCE,
        "tier_a": {"verdict": verdict, "checks": len(tier_a),
                   "pass": len(tier_a) - len(fails_a),
                   "registered_deviations": [c["id"] for c in fails_a if "deviation" in c],
                   "unregistered_failures": [c["id"] for c in unregistered]},
        "tier_b": tier_b,
        "status_counts": dict(Counter(c["status"] for c in R.checks)),
        "anomaly_sentinels": ANOMALY_SENTINELS,
        "tier_b_failures": [{"id": c["id"], "derived": c["derived"], "printed": c["printed"],
                             "note": c.get("note")}
                            for c in R.checks if c["tier"] == B and c["result"] == "FAIL"],
        "checks": R.checks,
    }


def attribute_status(report: Dict[str, object], net_span: str) -> Dict[str, str]:
    """Per-attribute status of one demon, for Stage VII: only UNCONTESTED attributes
    count toward the primary correspondence score; the rest go to a diagnostic table."""
    out: Dict[str, str] = {}
    for c in report["checks"]:
        cid = c["id"]
        parts = cid.split(".")
        if parts[0] == "matrix" and parts[1] == net_span and "rite" not in cid:
            key = parts[2]
        elif parts[0] in ("pitch", "riteset") and parts[1] == net_span:
            key = parts[0]
        elif parts[0] in ("rite", "subrites") and parts[1] == net_span:
            key = "rites"
        else:
            continue
        status = {CONSISTENT: "UNCONTESTED", SOURCE_CONFLICT: "SOURCE_CONFLICTED",
                  INFERRED_MISFIT: "INFERRED_MISFIT"}.get(c["status"], c["status"])
        if out.get(key, "UNCONTESTED") == "UNCONTESTED":
            out[key] = status
    return out


def main(argv: List[str]) -> None:
    rep = run()
    if "--json" in argv:
        print(json.dumps(rep, indent=1))
        return
    a = rep["tier_a"]
    print("%s on %s" % (rep["assay"], rep["engine"]))
    print("canonical digest  %s" % rep["canonical_digest"])
    print("full digest       %s" % rep["full_digest"])
    print("source            %s (extraction sha256 %s...)" % (
        rep["source"]["title"], rep["source"]["extraction_sha256"][:16]))
    print("\nTier A (CCRU-stated rules): %s  %d/%d" % (a["verdict"], a["pass"], a["checks"]))
    for cid in a["registered_deviations"]:
        print("   registered deviation: %s" % cid)
    for cid in a["unregistered_failures"]:
        print("   UNREGISTERED FAILURE: %s" % cid)
    print("\nStatus counts: %s" % ", ".join("%s %d" % kv for kv in sorted(rep["status_counts"].items())))
    print("Frozen anomaly sentinels: %s" % ", ".join(sorted(rep["anomaly_sentinels"])))
    print("\nTier B (programme-inferred rules): fit")
    for rule, t in sorted(rep["tier_b"].items()):
        print("   %-22s %3d/%-3d" % (rule, t["pass"], t["total"]))
    print("\nTier B disagreements:")
    for f in rep["tier_b_failures"]:
        print("   %-34s derived=%s printed=%s" % (f["id"], f["derived"], f["printed"]))


if __name__ == "__main__":
    main(sys.argv[1:])
