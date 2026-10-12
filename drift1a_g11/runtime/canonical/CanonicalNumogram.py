"""
CanonicalNumogram.py -- Canonical Numogram 1.1
Amelia Interface Programme, Stage I (Numogram Reconstruction)

PURPOSE
    A purely structural reconstruction of the CCRU Decimal Numogram and
    Pandemonium Matrix, derived from rules and checked against the Green
    Book (Ccru: Writings 1997-2003). This module holds NO dynamics: no
    activation, intensity, probability or randomness.

TWO TIERS OF RULE
    CCRU_RULE           A rule the CCRU states (Green Book text or glossary).
                        Example: "Prowl. Territorial relation of a demon to a
                        current, in which the poles of the demon include one
                        side of a Syzygy and its Tractor zone."
    PROGRAMME_INFERRED  A rule this programme inferred from the Green Book's
                        data because the text gives values but no rule.
                        Example: the pitch formula. Each inferred rule is
                        listed in INFERRED_RULES with the evidence it was
                        fitted to; FidelityAssay.py reports its fit.

    The sealed digest (digest()) covers CCRU_RULE structure only, so that
    revising an inferred rule never changes the sealed canonical structure.
    digest(include_inferred=True) covers both.

SEPARATION
    This file derives. It never reads GreenBookTranscription.py.
    FidelityAssay.py compares the two.

COMPATIBILITY
    Python 3.8+ standard library only (Chaquopy 3.8 compatible).
"""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass, field
from typing import Dict, FrozenSet, List, Optional, Sequence, Set, Tuple

SPEC_VERSION = "CanonicalNumogram-1.1.1"

CCRU_RULE = "CCRU_RULE"
PROGRAMME_INFERRED = "PROGRAMME_INFERRED"

REGION_WARP = "WARP"
REGION_TC = "TIME_CIRCUIT"
REGION_PLEX = "PLEX"

ZONES: Tuple[int, ...] = tuple(range(10))
BASE_MAX = 9

# Step types along the Numogram (Glossary: Current, Channel, Syzygy)
SYZYGY = "syzygy"     # crossing between syzygetic twins
CURRENT = "current"   # riding a current from a side of its syzygy to the tractor
GATE = "gate"         # passing through a gate along its channel

RULE_PERMISSIVE = "permissive"   # any canonical edge, in any order
RULE_LEMURIAN = "lemurian"       # PROGRAMME_INFERRED traversal rule (see INFERRED_RULES)

# ---------------------------------------------------------------------------
# Rule registers
# ---------------------------------------------------------------------------

CCRU_RULES: Dict[str, str] = {
    "zygonovism": "Ten zones grouped into five syzygies by nine-sum twinning.",
    "current": "The arithmetical difference of each syzygy defines a current to a tractor zone.",
    "gate": "Each zone number digitally cumulated defines a gate; its reduction sets the channel.",
    "time_systems": "Central three syzygies compose the Time-Circuit; upper and lower currents fold "
                    "back into (a half of) themselves: Warp (upper) and Plex (lower).",
    "binary_cycle": "Digital reduction of binary powers cycles 1,2,4,8,7,5 = the time-circuit zones.",
    "net_span": "Each demon is a zone-net couple of descending value (net-span), called by a "
                "mesh-serial (00-44).",
    "phase": "Phase: set of demons with the same primary pole. Door: net-span #::0. "
             "Phase-limit: final demon of a phase.",
    "classes": "Chronodemon: both poles in the Time-Circuit (3 syzygetic, 12 cyclic). "
               "Amphidemon: one pole inside, one outside (24). Xenodemon: both poles outside; "
               "Chaotic Xenodemon links Plex and Warp (4, trackless rites).",
    "feed": "Feed: zygonovic differential production of a current (the syzygetic demon feeds its current).",
    "prowl": "Prowl: the demon's poles include one side of a syzygy and its tractor zone.",
    "shadow": "Shadow: the demon's poles include one side of a syzygy and the twin of its tractor zone.",
    "haunt": "Haunt: polar coincidence of a demon and a channel; also direct nesting of a gate.",
    "cipher": "Ciphering: the same set of digits irrespective of order.",
    "click": "Clicking: exact (ordered) ciphering; operation of a demonic mesh-number.",
    "decademon": "Decademon: one of four demons whose net-span digits sum to ten.",
    "imps": "Imps: third descending net-span digit; 120 in number; allotted by secondary pole; "
            "doors have no imps.",
    "major_minor": "Major rite follows the order of the net-span; minor rite is inverse to it.",
    "secret": "Secret rite: any rite involving one or more gates.",
    "cyclic": "Cyclic Chronodemon: its major and minor rites mutually encompass the Time-Circuit.",
    "rite": "A rite for each way in which the net-span can be traced across the flows of the Numogram.",
}

INFERRED_RULES: Dict[str, Dict[str, str]] = {
    "pitch": {
        "rule": "pitch = b(i) + b(j), where b(z) = z for z <= 4 and z - 9 for z >= 5. "
                "Positive = Ana, negative = Cth, zero = Null.",
        "evidence": "Pitch values of all 45 Matrix entries; the text states the range Ana-7 to "
                    "Cth-7, fifteen tones, and null pitch for syzygetic demons.",
    },
    "zone_mesh_tag": {
        "rule": "Sarkonian mesh-tag of zone z = 2^z - 1.",
        "evidence": "Ten zone tags stated in the Zone system notes.",
    },
    "demon_sarkon_tag": {
        "rule": "Sarkon-tag of demon i::j = 2^i + 2^j - 1 (zone-set bitmask minus one).",
        "evidence": "Two stated tags: Lurgo 0002, Katak 0047.",
    },
    "phase_population": {
        "rule": "Phase n contains 2^n impulse-entities (descending digit-strings headed by n).",
        "evidence": "Nine stated phase populations (Zones 1-9).",
    },
    "imps_allotted": {
        "rule": "Demon i::j is allotted the j imps i::j::k (k < j).",
        "evidence": "Glossary: 120 imps, allotted by secondary pole, doors none.",
    },
    "imps_hosted": {
        "rule": "Demon i::j hosts cumulation(j) imps (all i::b::c with b <= j).",
        "evidence": "Katak hosts 10 imps; Lurgo has no imps.",
    },
    "lemurian_traversal": {
        "rule": "A step along a Time-Circuit current must immediately follow the syzygetic "
                "crossing into its source zone. Syzygy crossings and gates are otherwise "
                "unrestricted; steps inside Warp and Plex are unrestricted. Rites are simple "
                "routes (no zone repeated).",
        "evidence": "All listed Matrix rites; Lurgo has one path; Katak has two paths and is the "
                    "only syzygetic demon with a nonsyzygetic rite.",
    },
    "sub_rites": {
        "rule": "Sub-rites of a rite = number of alternative edge readings of the same route "
                "minus one (a fold-back current is identified with its syzygy crossing).",
        "evidence": "Sub-rite counts of the Matrix rites.",
    },
    "direct_nesting_haunt": {
        "rule": "A fold-back syzygetic demon haunts the undisputed involutionary gate at its "
                "tractor (reading of the glossary's 'direct nesting of a gate').",
        "evidence": "Uttunul (9::0) haunts Gt-45.",
    },
    "nesting": {
        "rule": "A demon nests every other demon whose poles both lie on its rite(s).",
        "evidence": "Lurgo nests 8::0, 8::1, 9::0, 9::1, 9::8.",
    },
}

# Current names (Green Book glossary: Surge, Hold, Sink, Warp, Plex Current)
CURRENT_NAMES: Dict[Tuple[int, int], str] = {
    (8, 1): "Surge", (7, 2): "Hold", (5, 4): "Sink", (6, 3): "Warp", (9, 0): "Plex",
}

# ---------------------------------------------------------------------------
# Arithmetic primitives
# ---------------------------------------------------------------------------


def digit_sum(n: int) -> int:
    if n < 0:
        raise ValueError("digit_sum is defined for non-negative integers")
    return sum(int(d) for d in str(n))


def reduction_path(n: int) -> Tuple[int, ...]:
    """Digital reduction ('plexing') with its intermediate stages."""
    path = [n]
    while path[-1] >= 10:
        path.append(digit_sum(path[-1]))
    return tuple(path)


def digital_reduction(n: int) -> int:
    return reduction_path(n)[-1]


def cumulation(n: int) -> int:
    """Digital cumulation: n + (n-1) + ... + 0."""
    if n < 0:
        raise ValueError("cumulation is defined for non-negative integers")
    return n * (n + 1) // 2


def twin(z: int) -> int:
    _check_zone(z)
    return BASE_MAX - z


def nth_prime(n: int) -> int:
    """CCRU ordination: zeroth prime = 1, first prime = 2, second prime = 3."""
    if n == 0:
        return 1
    found, k = 0, 1
    while found < n:
        k += 1
        if all(k % d for d in range(2, int(k ** 0.5) + 1)):
            found += 1
    return k


def _check_zone(z: int) -> None:
    if z not in ZONES:
        raise ValueError("zone must be an integer 0-9, got %r" % (z,))


def pitch_label(p: int) -> str:
    return "Null" if p == 0 else ("Ana-%d" % p if p > 0 else "Cth-%d" % -p)


# ---------------------------------------------------------------------------
# Structural records
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Syzygy:
    upper: int
    lower: int

    @property
    def label(self) -> str:
        return "%d::%d" % (self.upper, self.lower)

    @property
    def zones(self) -> FrozenSet[int]:
        return frozenset((self.upper, self.lower))


@dataclass(frozen=True)
class Current:
    syzygy: Tuple[int, int]
    name: str
    value: int
    tractor: int
    tractor_twin: int
    folds_back: bool


@dataclass(frozen=True)
class Zone:
    zone: int
    region: str
    region_ordinal: int          # 1-based position within its region
    syzygy: Tuple[int, int]
    tractor_of: Optional[str]    # name of the current whose tractor this zone is
    gate: int                    # gate number of the zone
    channel_termini: Tuple[int, ...]   # gate numbers whose channels end here
    mesh_tag: int                # PROGRAMME_INFERRED
    phase_population: int        # PROGRAMME_INFERRED


@dataclass(frozen=True)
class Gate:
    zone: int
    number: int
    reduction: Tuple[int, ...]
    target: int
    disputed: bool               # Gt-00 (Green Book: 'fundamentally disputed')
    involutionary: bool          # channel returns to its own zone
    orientation: Optional[str]   # 'pro' / 'counter' for Time-Circuit-internal channels

    @property
    def label(self) -> str:
        return "Gt-%02d" % self.number


@dataclass(frozen=True)
class Channel:
    gate: int
    source: int
    target: int
    stages: Tuple[int, ...]
    source_region: str
    target_region: str

    @property
    def crosses_regions(self) -> bool:
        return self.source_region != self.target_region


@dataclass(frozen=True)
class Rite:
    route: Tuple[int, ...]
    kind: str                    # 'major' or 'minor' (or 'syzygetic' for the crossing)
    gate_possible: bool          # at least one valid reading uses a gate
    gate_required: bool          # every valid reading uses a gate
    readings: int                # number of valid edge-type readings


@dataclass(frozen=True)
class Demon:
    upper: int
    lower: int
    mesh: int
    phase: int
    is_door: bool
    is_phase_limit: bool
    syzygetic: bool
    demon_class: str             # 'Syzygetic Chronodemon', 'Cyclic Chronodemon', 'Amphidemon', ...
    amphi_kind: Optional[str]    # 'warping' / 'plexing' for amphidemons
    pole_regions: Tuple[str, str]
    feeds: Tuple[str, ...]
    prowls: Tuple[str, ...]
    shadows: Tuple[str, ...]
    haunts: Tuple[int, ...]                # CCRU rule: polar coincidence with a channel
    cipher_gates: FrozenSet[int]
    click_gates: Tuple[int, ...]           # mesh-number clicks
    net_span_click_gates: Tuple[int, ...]  # ordered net-span clicks
    decademon: Optional[int]
    imps_allotted: int
    # PROGRAMME_INFERRED attributes
    pitch: int
    sarkon_tag: int
    imps_hosted: int
    direct_nesting_haunts: Tuple[int, ...]  # inferred reading of 'direct nesting of a gate'

    @property
    def net_span(self) -> str:
        return "%d::%d" % (self.upper, self.lower)

    @property
    def pitch_label(self) -> str:
        return pitch_label(self.pitch)


# ---------------------------------------------------------------------------
# The canonical engine
# ---------------------------------------------------------------------------

class CanonicalNumogram:
    """Immutable structure of the Decimal Numogram and Pandemonium Matrix."""

    def __init__(self) -> None:
        self.zones: Tuple[int, ...] = ZONES
        self.syzygies: Tuple[Syzygy, ...] = self._derive_syzygies()
        self._syz_of_zone: Dict[int, Tuple[int, int]] = {
            z: (s.upper, s.lower) for s in self.syzygies for z in s.zones}
        self.currents: Dict[Tuple[int, int], Current] = self._derive_currents()
        self.autonomous_loops, self.time_circuit_cycle = self._derive_time_systems()
        self.region_of_syzygy = self._label_regions()
        self.region_of_zone: Dict[int, str] = {
            z: self.region_of_syzygy[self._syz_of_zone[z]] for z in self.zones}
        self.binary_cycle: Tuple[int, ...] = tuple(digital_reduction(2 ** k) for k in range(6))
        self.gates: Dict[int, Gate] = self._derive_gates()
        self.channels: Dict[int, Channel] = self._derive_channels()
        self.zone_info: Dict[int, Zone] = self._derive_zone_info()
        self._succ = {z: sorted(b for b in self.zones if b != z and self.step_types(z, b))
                      for z in self.zones}
        self.demons: Dict[Tuple[int, int], Demon] = self._derive_matrix()

    # -- syzygies, currents, time-systems ---------------------------------
    def _derive_syzygies(self) -> Tuple[Syzygy, ...]:
        seen: Set[int] = set()
        out: List[Syzygy] = []
        for z in sorted(ZONES, reverse=True):
            if z in seen:
                continue
            t = twin(z)
            seen.update((z, t))
            out.append(Syzygy(upper=max(z, t), lower=min(z, t)))
        return tuple(out)

    def syzygy_of(self, z: int) -> Tuple[int, int]:
        _check_zone(z)
        return self._syz_of_zone[z]

    def _derive_currents(self) -> Dict[Tuple[int, int], Current]:
        out = {}
        for s in self.syzygies:
            d = s.upper - s.lower
            k = (s.upper, s.lower)
            out[k] = Current(syzygy=k, name=CURRENT_NAMES[k], value=d, tractor=d,
                             tractor_twin=twin(d), folds_back=d in s.zones)
        return out

    def current_named(self, name: str) -> Current:
        for c in self.currents.values():
            if c.name == name:
                return c
        raise KeyError(name)

    def _derive_time_systems(self):
        step = {k: self._syz_of_zone[c.tractor] for k, c in self.currents.items()}
        loops = frozenset(k for k, v in step.items() if k == v)
        rest = [k for k in step if k not in loops]
        start = max(rest)
        cycle = [start]
        nxt = step[start]
        while nxt != start:
            if nxt in cycle or nxt in loops:
                raise AssertionError("currents do not compose a single cycle")
            cycle.append(nxt)
            nxt = step[nxt]
        if set(cycle) != set(rest):
            raise AssertionError("non-autonomous syzygies do not form one cycle")
        return loops, tuple(cycle)

    def _label_regions(self) -> Dict[Tuple[int, int], str]:
        """Upper autonomous loop = Warp, lower = Plex (CCRU). The Plex is the loop
        containing Zone-0, the lowest zone."""
        out = {k: REGION_TC for k in self.time_circuit_cycle}
        for k in self.autonomous_loops:
            out[k] = REGION_PLEX if 0 in k else REGION_WARP
        return out

    # -- gates and channels -----------------------------------------------
    def _derive_gates(self) -> Dict[int, Gate]:
        cyc = list(self.time_circuit_cycle)
        out = {}
        for z in self.zones:
            n = cumulation(z)
            path = reduction_path(n)
            t = path[-1]
            orient = None
            if (z != t and self.region_of_zone[z] == REGION_TC
                    and self.region_of_zone[t] == REGION_TC):
                a, b = cyc.index(self._syz_of_zone[z]), cyc.index(self._syz_of_zone[t])
                if (a + 1) % len(cyc) == b:
                    orient = "pro"
                elif (b + 1) % len(cyc) == a:
                    orient = "counter"
            out[z] = Gate(zone=z, number=n, reduction=path, target=t,
                          disputed=(n == 0), involutionary=(z == t), orientation=orient)
        return out

    def _derive_channels(self) -> Dict[int, Channel]:
        return {g.number: Channel(gate=g.number, source=z, target=g.target, stages=g.reduction,
                                  source_region=self.region_of_zone[z],
                                  target_region=self.region_of_zone[g.target])
                for z, g in self.gates.items()}

    def gate_numbers(self) -> FrozenSet[int]:
        return frozenset(g.number for g in self.gates.values())

    # -- zones ------------------------------------------------------------
    def _derive_zone_info(self) -> Dict[int, Zone]:
        out = {}
        for z in self.zones:
            r = self.region_of_zone[z]
            members = (list(self.binary_cycle) if r == REGION_TC else
                       sorted(k for k, v in self.region_of_zone.items() if v == r))
            tractor_of = next((c.name for c in self.currents.values() if c.tractor == z), None)
            termini = tuple(sorted(g.number for g in self.gates.values() if g.target == z))
            out[z] = Zone(zone=z, region=r, region_ordinal=members.index(z) + 1,
                          syzygy=self._syz_of_zone[z], tractor_of=tractor_of,
                          gate=cumulation(z), channel_termini=termini,
                          mesh_tag=2 ** z - 1, phase_population=2 ** z)
        return out

    # -- steps and routes -------------------------------------------------
    def step_types(self, a: int, b: int) -> FrozenSet[str]:
        """Edge types permitting a single move a -> b (a != b)."""
        _check_zone(a)
        _check_zone(b)
        if a == b:
            return frozenset()
        t = set()
        if twin(a) == b:
            t.add(SYZYGY)
        if self.currents[self._syz_of_zone[a]].tractor == b:
            t.add(CURRENT)
        if self.gates[a].target == b:
            t.add(GATE)
        return frozenset(t)

    def _step_options(self, a: int, b: int) -> List[str]:
        ts = set(self.step_types(a, b))
        if CURRENT in ts and SYZYGY in ts:        # fold-back current coincides with crossing
            ts.discard(CURRENT)
        return sorted(ts)

    def route_readings(self, route: Sequence[int], rule: str = RULE_LEMURIAN) -> List[Tuple[str, ...]]:
        """All edge-type readings of a route that satisfy the rule."""
        if len(route) < 2:
            return []
        steps = list(zip(route, route[1:]))
        opts = [self._step_options(a, b) for a, b in steps]
        if any(not o for o in opts):
            return []
        out = []
        for combo in itertools.product(*opts):
            ok = True
            if rule == RULE_LEMURIAN:
                for k, (t, (a, _)) in enumerate(zip(combo, steps)):
                    if (t == CURRENT and self.region_of_zone[a] == REGION_TC
                            and (k == 0 or combo[k - 1] != SYZYGY)):
                        ok = False
                        break
            if ok:
                out.append(combo)
        return out

    def is_valid_route(self, route: Sequence[int], rule: str = RULE_PERMISSIVE) -> bool:
        if len(set(route)) != len(route):
            return False
        return bool(self.route_readings(route, rule))

    def routes(self, a: int, b: int, max_len: int = 10,
               rule: str = RULE_PERMISSIVE) -> List[Tuple[int, ...]]:
        """All simple routes from a to b valid under the rule."""
        _check_zone(a)
        _check_zone(b)
        found: List[Tuple[int, ...]] = []

        def walk(path: List[int]) -> None:
            if path[-1] == b and len(path) > 1:
                if self.route_readings(path, rule):
                    found.append(tuple(path))
                return
            if len(path) >= max_len:
                return
            for n in self._succ[path[-1]]:
                if n not in path:
                    walk(path + [n])

        walk([a])
        return found

    # -- rites (PROGRAMME_INFERRED traversal rule) --------------------------
    def rites(self, i: int, j: int) -> List[Rite]:
        """Rites of demon i::j under the Lemurian traversal rule. The syzygetic
        crossing of a syzygetic demon is returned with kind 'syzygetic'."""
        out: List[Rite] = []
        if i + j == BASE_MAX:
            # the syzygetic crossing is one path, written [i//j] in the Green Book
            rd = self.route_readings((i, j), RULE_LEMURIAN)
            out.append(Rite(route=(i, j), kind="syzygetic",
                            gate_possible=any(GATE in x for x in rd),
                            gate_required=all(GATE in x for x in rd), readings=len(rd)))
        for a, b, kind in ((i, j, "major"), (j, i, "minor")):
            for r in self.routes(a, b, rule=RULE_LEMURIAN):
                if len(r) == 2 and SYZYGY in self.step_types(a, b):
                    continue
                rd = self.route_readings(r, RULE_LEMURIAN)
                out.append(Rite(route=r, kind=kind,
                                gate_possible=any(GATE in x for x in rd),
                                gate_required=all(GATE in x for x in rd), readings=len(rd)))
        return out

    def nests(self, i: int, j: int) -> Tuple[Tuple[int, int], ...]:
        zs: Set[int] = set()
        for r in self.rites(i, j):
            if r.kind != "syzygetic":
                zs.update(r.route)
        pairs = {(max(p), min(p)) for p in itertools.combinations(sorted(zs), 2)}
        pairs.discard((i, j))
        return tuple(sorted(pairs))

    # -- Pandemonium Matrix -------------------------------------------------
    def _derive_matrix(self) -> Dict[Tuple[int, int], Demon]:
        gates = self.gate_numbers()
        dec = sorted((i, 10 - i) for i in range(6, 10))
        out = {}
        for i in self.zones:
            for j in range(i):
                ri, rj = self.region_of_zone[i], self.region_of_zone[j]
                inside = (ri == REGION_TC) + (rj == REGION_TC)
                syz = i + j == BASE_MAX
                base = {2: "Chronodemon", 1: "Amphidemon", 0: "Xenodemon"}[inside]
                prefix = ("Syzygetic " if syz else "Cyclic " if inside == 2
                          else "Chaotic " if inside == 0 else "")
                amphi = None
                if inside == 1:
                    outer = rj if ri == REGION_TC else ri
                    amphi = "warping" if outer == REGION_WARP else "plexing"
                feeds, prowls, shadows = [], [], []
                for k, c in self.currents.items():
                    if (i, j) == k:
                        feeds.append(c.name)
                    for side in k:
                        if side != c.tractor and {i, j} == {side, c.tractor}:
                            prowls.append(c.name)
                        if {i, j} == {side, c.tractor_twin} and (i, j) != k:
                            shadows.append(c.name)
                # (a shadow is not assigned to the syzygy that feeds the current itself:
                #  for Warp and Plex the tractor-twin is a side, so the case is degenerate)
                haunts = sorted(n for n, ch in self.channels.items()
                                if ch.source != ch.target and {ch.source, ch.target} == {i, j})
                nest_haunts = []
                if syz and self.currents[(i, j)].folds_back:
                    nest_haunts = sorted(n for n, ch in self.channels.items()
                                         if ch.source == ch.target and ch.source in (i, j)
                                         and not self.gates[ch.source].disputed
                                         and ch.source == self.currents[(i, j)].tractor)
                mesh = cumulation(i - 1) + j
                cipher = frozenset(n for n in gates if sorted("%02d" % n) == sorted("%d%d" % (i, j)))
                out[(i, j)] = Demon(
                    upper=i, lower=j, mesh=mesh, phase=i,
                    is_door=(j == 0), is_phase_limit=(j == i - 1), syzygetic=syz,
                    demon_class=prefix + base, amphi_kind=amphi, pole_regions=(ri, rj),
                    feeds=tuple(feeds), prowls=tuple(sorted(set(prowls))),
                    shadows=tuple(sorted(set(shadows))), haunts=tuple(haunts),
                    cipher_gates=cipher,
                    click_gates=(mesh,) if mesh in gates else (),
                    net_span_click_gates=tuple(n for n in gates if n == 10 * i + j),
                    decademon=(dec.index((i, j)) + 1) if (i + j == 10) else None,
                    imps_allotted=j,
                    pitch=self._pitch(i) + self._pitch(j),
                    sarkon_tag=2 ** i + 2 ** j - 1,
                    imps_hosted=cumulation(j),
                    direct_nesting_haunts=tuple(nest_haunts),
                )
        return out

    @staticmethod
    def _pitch(z: int) -> int:
        return z if z <= 4 else z - 9

    def demon_by_mesh(self, mesh: int) -> Demon:
        for d in self.demons.values():
            if d.mesh == mesh:
                return d
        raise KeyError("no demon with mesh %r" % (mesh,))

    # -- typed directed multigraph (input for null interfaces) --------------
    def typed_edges(self) -> List[Dict[str, object]]:
        """The Numogram as a typed, directed multigraph on the ten zones.

        REPRESENTATION CONVENTION (an operational reading, stated so that null
        interfaces preserve the right object): the CCRU defines a current as 'the
        path between a syzygy and a tractor (zone)'. On zone nodes it is written
        as one current edge from EACH side of the syzygy to the tractor. Hence:
          - the Warp and Plex currents each contribute a self-loop at the tractor
            (3->3, 9->9) as well as an edge from the other side (6->3, 0->9);
          - gates Gt-00, Gt-01, Gt-45 are self-loops (Gt-00 flagged disputed);
          - the same ordered pair may carry several types (parallel edges):
            4->1 (current, gate), 6->3 (syzygy, current, gate), 3->6 (syzygy,
            gate), 0->9 (syzygy, current), 9->9 (current, gate).
        Null interfaces must preserve per-type in- and out-degree, including
        self-loops and parallel relations (see typed_degrees)."""
        edges: List[Dict[str, object]] = []
        for s in self.syzygies:
            edges.append({"type": SYZYGY, "src": s.upper, "dst": s.lower})
            edges.append({"type": SYZYGY, "src": s.lower, "dst": s.upper})
        for k, c in self.currents.items():
            for m in k:
                edges.append({"type": CURRENT, "src": m, "dst": c.tractor, "current": c.name})
        for z, g in self.gates.items():
            edges.append({"type": GATE, "src": z, "dst": g.target, "gate": g.number,
                          "disputed": g.disputed})
        return edges

    def typed_degrees(self) -> Dict[int, Dict[str, Tuple[int, int]]]:
        """Per zone and edge type: (in-degree, out-degree), self-loops counted
        once on each side."""
        out = {z: {t: [0, 0] for t in (SYZYGY, CURRENT, GATE)} for z in self.zones}
        for e in self.typed_edges():
            out[e["dst"]][e["type"]][0] += 1
            out[e["src"]][e["type"]][1] += 1
        return {z: {t: tuple(v) for t, v in d.items()} for z, d in out.items()}

    def multigraph_summary(self) -> Dict[str, object]:
        edges = self.typed_edges()
        pairs: Dict[Tuple[int, int], List[str]] = {}
        for e in edges:
            pairs.setdefault((e["src"], e["dst"]), []).append(e["type"])
        return {
            "edges": len(edges),
            "by_type": {t: sum(1 for e in edges if e["type"] == t) for t in (SYZYGY, CURRENT, GATE)},
            "self_loops": sorted((e["type"], e["src"]) for e in edges if e["src"] == e["dst"]),
            "parallel": {"%d->%d" % k: sorted(v) for k, v in sorted(pairs.items()) if len(v) > 1},
        }

    # -- serialisation and sealing ------------------------------------------
    def to_spec(self, include_inferred: bool = False) -> Dict[str, object]:
        spec = {
            "version": SPEC_VERSION,
            "zones": {str(z): {"region": zi.region, "ordinal": zi.region_ordinal,
                               "tractor_of": zi.tractor_of, "termini": list(zi.channel_termini)}
                      for z, zi in sorted(self.zone_info.items())},
            "syzygies": [s.label for s in self.syzygies],
            "currents": {c.name: {"syzygy": "%d::%d" % k, "tractor": c.tractor,
                                  "folds_back": c.folds_back}
                         for k, c in sorted(self.currents.items())},
            "time_circuit_cycle": ["%d::%d" % k for k in self.time_circuit_cycle],
            "multigraph": sorted("%s:%d->%d" % (e["type"], e["src"], e["dst"])
                                 for e in self.typed_edges()),
            "gates": {g.label: {"zone": g.zone, "reduction": list(g.reduction), "target": g.target,
                                "disputed": g.disputed, "involutionary": g.involutionary,
                                "orientation": g.orientation}
                      for g in sorted(self.gates.values(), key=lambda g: g.number)},
            "matrix": {"Mesh-%02d" % d.mesh: {
                "net_span": d.net_span, "class": d.demon_class, "amphi": d.amphi_kind,
                "door": d.is_door, "phase_limit": d.is_phase_limit,
                "feeds": list(d.feeds), "prowls": list(d.prowls), "shadows": list(d.shadows),
                "haunts": list(d.haunts), "ciphers": sorted(d.cipher_gates),
                "clicks": list(d.click_gates), "decademon": d.decademon,
                "imps_allotted": d.imps_allotted}
                for d in sorted(self.demons.values(), key=lambda d: d.mesh)},
        }
        if include_inferred:
            spec["inferred"] = {
                "rules": sorted(INFERRED_RULES),
                "pitch": {d.net_span: d.pitch for d in self.demons.values()},
                "sarkon_tag": {d.net_span: d.sarkon_tag for d in self.demons.values()},
                "imps_hosted": {d.net_span: d.imps_hosted for d in self.demons.values()},
                "direct_nesting_haunts": {d.net_span: list(d.direct_nesting_haunts)
                                          for d in self.demons.values() if d.direct_nesting_haunts},
                "zone_mesh_tag": {str(z): zi.mesh_tag for z, zi in self.zone_info.items()},
                "rites": {d.net_span: [{"route": "".join(map(str, r.route)), "kind": r.kind,
                                        "gate_possible": r.gate_possible,
                                        "gate_required": r.gate_required,
                                        "readings": r.readings}
                                       for r in self.rites(d.upper, d.lower)]
                          for d in self.demons.values()},
            }
        return spec

    def digest(self, include_inferred: bool = False) -> str:
        blob = json.dumps(self.to_spec(include_inferred), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    ng = CanonicalNumogram()
    print("%s" % SPEC_VERSION)
    print("canonical digest (CCRU rules):     %s" % ng.digest())
    print("full digest (with inferred rules): %s" % ng.digest(include_inferred=True))
    print("Run FidelityAssay.py for the comparison with the Green Book.")
