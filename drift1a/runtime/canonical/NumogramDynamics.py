"""
NumogramDynamics.py -- executable dynamics contracts D0-D3
Amelia Interface Programme, Stage II preparation

WHAT THIS FILE IS
    The CCRU specifies which passages exist, not how traffic moves along them.
    Every law here is therefore a PROGRAMME HYPOTHESIS (Register 2). Each variant
    is an executable contract: a transition law P(e | state, t) over a TYPED
    GRAPH, its parameters, its textual warrant, and its provenance dependencies.

    The laws are graph-generic. They run unchanged on the canonical Numogram and
    on every null interface (NullInterfaces.py); nothing in a law reads a
    canonical region label. Two hashes seal a contract:
        law_hash()       the law and its parameters only (identical across graphs)
        contract_hash()  the law, its parameters and the digest of the graph it
                         runs on (one per canonical or null instance)

THE VARIANTS (hierarchy sealed in PREREGISTRATION)
    D0  uniform          P(e | z) = 1 / |E(z)|                       calibration baseline
    D1  typed weights    P(e | z) proportional to w(type e),
                         sealed 2 : 1 : 1 (current : syzygy : gate)  minimal textual weighting
    D2  gated channels   currents and syzygies always open; a gate with arithmetic
                         number n opens by a pre-registered schedule:
                         D2a  Gt-n open iff n >= 1 and (t + 1) mod n == 0
                         D2b  Gt-n open with probability 1/n (never for n = 0)
                         then uniform over open edges                underdetermined family
    D3  Lemurian         uniform over permitted edges; from a TRANSIENT node (one
        traversal        outside every terminal strongly connected component of the
                         structural graph) a current edge is permitted only if the
                         previous step was a syzygy crossing. On the canonical graph
                         the transient nodes are exactly the Time-Circuit, so this is
                         the inferred rite rule stated structurally. 78 of 79 rites;
                         6::2 held out and never special-cased.

    If no edge is permitted at (state, t) the walker HOLDS: it stays, time advances,
    and the step is recorded as a hold. On the canonical graph no law ever holds
    (every zone has a syzygy edge); on some null graphs laws can.

STRUCTURAL FACT (canonical)
    Warp {3, 6} and Plex {0, 9} are closed; the Time-Circuit is transient under
    every law. Only three gates leave it (Gt-3, Gt-15, Gt-36). Re-entry belongs to
    the embodiment (NumogramInterface.py), not to the graph.

SOURCE DISCIPLINE
    Gt-00 is disputed (L4693). Edges carry a structural 'disputed' flag; every
    contract has a gt00 parameter and source_branches() returns both branches.
    No law reads a Matrix attribute, so none depends on the eight registered
    printed deviations.

COMPATIBILITY
    Python 3.8+ standard library only. Reproducible from (contract, start, steps, seed).
"""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass
from fractions import Fraction
from functools import reduce
from math import gcd
from typing import Dict, FrozenSet, List, Optional, Sequence, Tuple

import CanonicalNumogram as C

DYNAMICS_VERSION = "NumogramDynamics-1.2.0"

GT00_INCLUDE = "include"
GT00_EXCLUDE = "exclude"
HOLD = "hold"

WARRANT = {
    "flows": "L4491-4495: currents 'constitute the primary flows'; channels 'the secondary "
             "flows, time-holes, or secret interconnections'",
    "gates": "L4493-4494: 'Each zone number when digitally cumulated defines the value of a gate'",
    "gt00": "L4693-4696: Gt-00 'fundamentally disputed ... Many versions of the Numogram delete it'",
    "time_holes": "L4494-4495: channels are 'time-holes'; L4503-4505: gates 'open and close the ways "
                  "of sorcerous traffic'",
    "rites": "L5464-5771: the 79 printed rites of the Pandemonium Matrix; L6016, L6111, L6121",
}

_TYPE_ORDER = {C.SYZYGY: 0, C.CURRENT: 1, C.GATE: 2}


# ---------------------------------------------------------------------------
# Typed graphs
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Edge:
    src: int
    dst: int
    type: str
    label: str                        # current name, gate label, or 'syzygy'
    gate_number: Optional[int] = None  # arithmetic value of a gate (D2 reads only this)
    disputed: bool = False             # structural dispute flag (Gt-00)

    def key(self) -> str:
        return "%s:%d->%d" % (self.type, self.src, self.dst)

    def as_list(self) -> list:
        return [self.src, self.dst, self.type, self.label, self.gate_number, self.disputed]


@dataclass(frozen=True)
class TypedGraph:
    n: int
    edges: Tuple[Edge, ...]
    family: str = "canonical"
    meta: Tuple[Tuple[str, str], ...] = ()
    regions: Optional[Tuple[Tuple[int, str], ...]] = None   # canonical only; never read by laws

    def nodes(self) -> Tuple[int, ...]:
        return tuple(range(self.n))

    def digest(self) -> str:
        blob = json.dumps({"n": self.n, "family": self.family, "meta": [list(m) for m in self.meta],
                           "edges": sorted(e.as_list() for e in self.edges)},
                          sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    def out_edges(self, gt00: str = GT00_INCLUDE) -> Dict[int, Tuple[Edge, ...]]:
        out: Dict[int, List[Edge]] = {z: [] for z in self.nodes()}
        for e in self.edges:
            if e.disputed and gt00 == GT00_EXCLUDE:
                continue
            out[e.src].append(e)
        return {z: tuple(sorted(v, key=lambda x: (_TYPE_ORDER[x.type], x.dst, x.label)))
                for z, v in out.items()}


def terminal_classes(n: int, edges: Dict[int, Sequence[Edge]]) -> List[FrozenSet[int]]:
    """Terminal strongly connected components of the structural graph, excluding
    the whole node set (a strongly connected graph has no episodic structure)."""
    succ = {z: {e.dst for e in edges.get(z, ())} for z in range(n)}
    reach = {}
    for z in succ:
        seen, stack = {z}, [z]
        while stack:
            for w in succ[stack.pop()]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        reach[z] = seen
    comps = {frozenset(w for w in reach[z] if z in reach[w]) for z in succ}
    everything = frozenset(succ)
    return sorted((c for c in comps if c != everything and all(succ[z] <= c for z in c)), key=min)


_CANON_CACHE: Dict[str, object] = {}


def canonical_graph(engine: Optional[C.CanonicalNumogram] = None) -> TypedGraph:
    if engine is None and "graph" in _CANON_CACHE:
        return _CANON_CACHE["graph"]
    ng = engine or C.CanonicalNumogram()
    es = []
    for e in ng.typed_edges():
        if e["type"] == C.GATE:
            es.append(Edge(e["src"], e["dst"], C.GATE, "Gt-%02d" % e["gate"], e["gate"],
                           bool(e.get("disputed"))))
        elif e["type"] == C.CURRENT:
            es.append(Edge(e["src"], e["dst"], C.CURRENT, e["current"]))
        else:
            es.append(Edge(e["src"], e["dst"], C.SYZYGY, C.SYZYGY))
    g = TypedGraph(n=10, edges=tuple(es), family="canonical",
                   meta=(("engine", C.SPEC_VERSION), ("canonical_digest", ng.digest())),
                   regions=tuple(sorted(ng.region_of_zone.items())))
    if engine is None:
        _CANON_CACHE["graph"] = g
    return g


def canonical_digest() -> str:
    return dict(canonical_graph().meta)["canonical_digest"]


# ---------------------------------------------------------------------------
# Contracts
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class State:
    zone: int
    prev_type: Optional[str] = None      # type of the step that entered this zone


class Contract:
    """Base class. A contract is a transition law plus its declaration."""

    variant = ""
    name = ""
    law = ""
    markov_order = 1
    time_homogeneous = True

    def __init__(self, graph: Optional[TypedGraph] = None, gt00: str = GT00_INCLUDE):
        if gt00 not in (GT00_INCLUDE, GT00_EXCLUDE):
            raise ValueError("gt00 must be 'include' or 'exclude'")
        self.graph = graph or canonical_graph()
        self.gt00 = gt00
        self.edges = self.graph.out_edges(gt00)
        self.terminal = terminal_classes(self.graph.n, self.edges)
        self._in_terminal = {z for c in self.terminal for z in c}
        self.transient = frozenset(z for z in self.graph.nodes() if z not in self._in_terminal)

    # -- declarations ---------------------------------------------------------------
    def parameters(self) -> Dict[str, object]:
        return {"gt00": self.gt00}

    def warrant(self) -> List[str]:
        return []

    def provenance_dependencies(self) -> Dict[str, List[str]]:
        return {
            "CCRU_RULE": ["zygonovism", "current", "gate", "time_systems"],
            "REPRESENTATION": ["current edge from each side of its syzygy to the tractor",
                               "parallel edges counted separately"],
            "PROGRAMME_INFERRED": [],
            "SOURCE_DISPUTE": ["Gt-00 (L4693): branch via gt00"] if self.gt00 == GT00_INCLUDE
            else ["Gt-00 (L4693): excluded branch"],
            "SOURCE_CONFLICT": [],
        }

    def law_declaration(self) -> Dict[str, object]:
        return {
            "dynamics_version": DYNAMICS_VERSION,
            "variant": self.variant, "name": self.name, "law": self.law,
            "markov_order": self.markov_order, "time_homogeneous": self.time_homogeneous,
            "parameters": {k: str(v) for k, v in self.parameters().items()},
            "warrant": self.warrant(),
            "provenance_dependencies": self.provenance_dependencies(),
            "inferred_rules_used": {k: C.INFERRED_RULES[k]["rule"]
                                    for k in self.provenance_dependencies()["PROGRAMME_INFERRED"]},
            "canonical_digest": canonical_digest(),
        }

    def declaration(self) -> Dict[str, object]:
        d = self.law_declaration()
        d["graph_family"] = self.graph.family
        d["graph_digest"] = self.graph.digest()
        return d

    def law_hash(self) -> str:
        return _sha(self.law_declaration())

    def contract_hash(self) -> str:
        return _sha(self.declaration())

    # -- the law ------------------------------------------------------------------
    def weights(self, state: State, t: int, rng: Optional[random.Random]) -> List[Tuple[Edge, object]]:
        raise NotImplementedError

    def probabilities(self, state: State, t: int = 0,
                      rng: Optional[random.Random] = None) -> List[Tuple[Edge, Fraction]]:
        """Exact distribution over permitted edges; empty if none is permitted (hold)."""
        w = [(e, Fraction(x)) for e, x in self.weights(state, t, rng) if x > 0]
        total = sum(x for _, x in w)
        if total == 0:
            return []
        return [(e, x / total) for e, x in w]

    def step(self, state: State, t: int, rng: random.Random) -> Tuple[Optional[Edge], State]:
        probs = self.probabilities(state, t, rng)
        if not probs:
            return None, State(state.zone, HOLD)
        u = Fraction(rng.random())
        acc = Fraction(0)
        for e, p in probs:
            acc += p
            if u < acc:
                return e, State(e.dst, e.type)
        e = probs[-1][0]
        return e, State(e.dst, e.type)

    def run(self, start: int, steps: int, seed: int) -> "Trace":
        if not 0 <= start < self.graph.n:
            raise ValueError("start zone outside the graph")
        rng = random.Random(seed)
        state = State(start, None)
        records = []
        for t in range(steps):
            e, state = self.step(state, t, rng)
            if e is None:
                records.append((t, state.zone, HOLD, HOLD, state.zone))
            else:
                records.append((t, e.src, e.type, e.label, e.dst))
        return Trace(contract_hash=self.contract_hash(), start=start, steps=steps,
                     seed=seed, records=tuple(records))

    # -- state space for exact analysis ------------------------------------------------
    def states(self) -> List[State]:
        return [State(z, None) for z in self.graph.nodes()]

    def canonical_state(self, s: State) -> State:
        return State(s.zone, None)


class D0Uniform(Contract):
    variant, name = "D0", "uniform"
    law = "P(e | z) = 1 / |E(z)| over the outgoing typed edges of z (parallel edges counted separately)"

    def weights(self, state, t, rng):
        return [(e, 1) for e in self.edges[state.zone]]

    def warrant(self):
        return ["Minimal-assumption baseline; no textual warrant claimed."]


class D1TypedWeights(Contract):
    variant, name = "D1", "typed weights"
    law = "P(e | z) = w(type e) / sum_{e' in E(z)} w(type e'); w_current > w_gate > 0, w_syzygy > 0"

    def __init__(self, w_current, w_syzygy, w_gate, graph=None, gt00=GT00_INCLUDE):
        self.w = {C.CURRENT: Fraction(str(w_current)), C.SYZYGY: Fraction(str(w_syzygy)),
                  C.GATE: Fraction(str(w_gate))}
        if not (self.w[C.CURRENT] > self.w[C.GATE] > 0 and self.w[C.SYZYGY] > 0):
            raise ValueError("D1 requires w_current > w_gate > 0 and w_syzygy > 0 "
                             "(currents are primary flows, channels secondary)")
        super().__init__(graph, gt00)

    def parameters(self):
        p = super().parameters()
        p.update({"w_current": self.w[C.CURRENT], "w_syzygy": self.w[C.SYZYGY],
                  "w_gate": self.w[C.GATE]})
        return p

    def weights(self, state, t, rng):
        return [(e, self.w[e.type]) for e in self.edges[state.zone]]

    def warrant(self):
        return [WARRANT["flows"]]


class D2GatedChannels(Contract):
    variant, name = "D2", "gated channels"
    time_homogeneous = False
    SCHEDULES = {
        "D2a": "deterministic: Gt-n open at step t iff n >= 1 and (t + 1) mod n == 0, i.e. on "
               "steps n, 2n, 3n, ... counting from 1 (Gt-00 never open)",
        "D2b": "stochastic: Gt-n open at each step with probability 1/n (Gt-00 never open)",
    }

    def __init__(self, schedule: str, graph=None, gt00=GT00_INCLUDE):
        if schedule not in self.SCHEDULES:
            raise ValueError("D2 schedule must be one of %s" % sorted(self.SCHEDULES))
        self.schedule = schedule
        self.law = ("currents and syzygies always open; gates follow schedule %s: %s; "
                    "uniform over open edges; the gate's arithmetic number is the edge's "
                    "gate_number" % (schedule, self.SCHEDULES[schedule]))
        super().__init__(graph, gt00)

    def parameters(self):
        p = super().parameters()
        p["schedule"] = self.schedule
        return p

    def gate_open(self, gate_number: int, t: int, rng: Optional[random.Random]) -> bool:
        if not gate_number:
            return False
        if self.schedule == "D2a":
            return (t + 1) % gate_number == 0
        if rng is None:
            raise ValueError("D2b needs a random source to decide gate openings")
        return rng.random() < 1.0 / gate_number

    def open_probability(self, gate_number: int, t: int) -> Fraction:
        if not gate_number:
            return Fraction(0)
        if self.schedule == "D2a":
            return Fraction(1 if (t + 1) % gate_number == 0 else 0)
        return Fraction(1, gate_number)

    def weights(self, state, t, rng):
        out = []
        for e in self.edges[state.zone]:
            if e.type == C.GATE:
                if self.gate_open(e.gate_number, t, rng):
                    out.append((e, 1))
            else:
                out.append((e, 1))
        return out

    def exact_probabilities(self, state: State, t: int) -> List[Tuple[Edge, Fraction]]:
        """Exact marginal transition probabilities, averaging independent gate draws."""
        es = self.edges[state.zone]
        gates = [e for e in es if e.type == C.GATE]
        others = [e for e in es if e.type != C.GATE]
        acc: Dict[Edge, Fraction] = {}
        qs = [self.open_probability(g.gate_number, t) for g in gates]
        for mask in range(2 ** len(gates)):
            pw = Fraction(1)
            live = list(others)
            for k, g in enumerate(gates):
                if mask >> k & 1:
                    pw *= qs[k]
                    live.append(g)
                else:
                    pw *= 1 - qs[k]
            if pw == 0 or not live:
                continue
            for e in live:
                acc[e] = acc.get(e, Fraction(0)) + pw / len(live)
        return [(e, p) for e, p in acc.items() if p > 0]

    def period(self) -> int:
        nums = [e.gate_number for e in self.graph.edges if e.type == C.GATE and e.gate_number]
        return reduce(lambda a, b: a * b // gcd(a, b), nums, 1)

    def warrant(self):
        return [WARRANT["gates"], WARRANT["time_holes"],
                "Schedules are UNDERDETERMINED by the text; D2a and D2b are a pre-registered "
                "family and are reported together."]


class D3Lemurian(Contract):
    variant, name = "D3", "Lemurian traversal"
    markov_order = 2
    law = ("uniform over permitted edges; from a transient node (outside every terminal strongly "
           "connected component of the structural graph) a current edge is permitted only if "
           "the previous step was a syzygy crossing; nodes in terminal components unrestricted; "
           "state = (node, type of previous step)")

    def permitted(self, state: State) -> List[Edge]:
        return [e for e in self.edges[state.zone]
                if not (e.type == C.CURRENT and state.zone in self.transient
                        and state.prev_type != C.SYZYGY)]

    def weights(self, state, t, rng):
        return [(e, 1) for e in self.permitted(state)]

    def provenance_dependencies(self):
        d = super().provenance_dependencies()
        d["PROGRAMME_INFERRED"] = ["lemurian_traversal"]
        return d

    def warrant(self):
        return [WARRANT["rites"],
                "Fit: admits 78 of 79 printed rites; reproduces the printed rite set exactly for "
                "40 of 45 demons (FidelityAssay 2.2). The misfit is the frozen anomaly sentinel "
                "and is not special-cased."]

    def states(self):
        return [State(z, t) for z in self.graph.nodes() for t in (None, C.SYZYGY, C.CURRENT, C.GATE)]

    def canonical_state(self, s: State) -> State:
        if s.zone in self.transient:
            return State(s.zone, C.SYZYGY if s.prev_type == C.SYZYGY else None)
        return State(s.zone, None)


# ---------------------------------------------------------------------------
# Traces
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Trace:
    contract_hash: str
    start: int
    steps: int
    seed: int
    records: Tuple[Tuple[int, int, str, str, int], ...]   # (t, src, type, label, dst)

    def zones(self) -> List[int]:
        return [self.start] + [r[4] for r in self.records]

    def digest(self) -> str:
        return _sha({"contract": self.contract_hash, "start": self.start, "steps": self.steps,
                     "seed": self.seed, "records": [list(r) for r in self.records]})


# ---------------------------------------------------------------------------
# Exact analysis (time-homogeneous contracts)
# ---------------------------------------------------------------------------

def transition_kernel(contract: Contract) -> Dict[State, Dict[State, Fraction]]:
    """Exact kernel over the contract's reduced state space; a hold is a self-transition."""
    if not contract.time_homogeneous:
        raise ValueError("kernel is time-dependent; use D2GatedChannels.exact_probabilities")
    seen: Dict[State, Dict[State, Fraction]] = {}
    frontier = [contract.canonical_state(s) for s in contract.states()]
    while frontier:
        s = frontier.pop()
        if s in seen:
            continue
        row: Dict[State, Fraction] = {}
        probs = contract.probabilities(s)
        if not probs:
            row[s] = Fraction(1)
        for e, p in probs:
            ns = contract.canonical_state(State(e.dst, e.type))
            row[ns] = row.get(ns, Fraction(0)) + p
            frontier.append(ns)
        seen[s] = row
    return seen


def _solve(A: List[List[Fraction]], b: List[Fraction]) -> Optional[List[Fraction]]:
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None:
            return None
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]


def absorption(contract: Contract) -> Dict[int, Dict[str, object]]:
    """For each transient start node (entered fresh): exact probability of ending in
    each terminal class, and the expected number of steps before leaving the
    transient set. On the canonical graph the keys p_warp and p_plex are added.
    Returns None entries if a state can never be absorbed under the law."""
    K = transition_kernel(contract)
    trans_states = sorted((s for s in K if s.zone in contract.transient),
                          key=lambda s: (s.zone, str(s.prev_type)))
    idx = {s: i for i, s in enumerate(trans_states)}
    n = len(trans_states)
    I_Q = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for s, i in idx.items():
        for ns, p in K[s].items():
            if ns in idx:
                I_Q[i][idx[ns]] -= p
    steps = _solve(I_Q, [Fraction(1)] * n)
    per_class = {}
    for cls in contract.terminal:
        b = [sum((p for ns, p in K[s].items() if ns.zone in cls), Fraction(0)) for s in trans_states]
        per_class[tuple(sorted(cls))] = _solve(I_Q, b)
    regions = dict(contract.graph.regions) if contract.graph.regions else None
    result: Dict[int, Dict[str, object]] = {}
    for s in trans_states:
        if s.prev_type is not None:
            continue
        i = idx[s]
        r: Dict[str, object] = {
            "p_exit": {k: (v[i] if v else None) for k, v in per_class.items()},
            "expected_steps_transient": steps[i] if steps else None,
        }
        if regions:
            for k, v in per_class.items():
                reg = regions[k[0]]
                r["p_" + reg.lower()] = v[i] if v else None
            r["expected_steps_in_time_circuit"] = r["expected_steps_transient"]
        result[s.zone] = r
    return result


def closed_region_check(contract: Contract) -> bool:
    """True if no permitted edge leaves a terminal class under any state (sanity check)."""
    cls_of = {z: c for c in contract.terminal for z in c}
    for s in contract.states():
        if s.zone not in cls_of:
            continue
        for t in range(3):
            probs = (contract.exact_probabilities(s, t) if isinstance(contract, D2GatedChannels)
                     else contract.probabilities(s, t, random.Random(0)))
            for e, p in probs:
                if e.dst not in cls_of[s.zone]:
                    return False
    return True


# ---------------------------------------------------------------------------
# Source sensitivity
# ---------------------------------------------------------------------------

def source_branches(factory, **kwargs) -> Dict[str, Contract]:
    """Both Gt-00 branches of a contract, for source-robustness classification."""
    return {GT00_INCLUDE: factory(gt00=GT00_INCLUDE, **kwargs),
            GT00_EXCLUDE: factory(gt00=GT00_EXCLUDE, **kwargs)}


def classify_robustness(values: Dict[str, float], conclusion: Dict[str, bool],
                        tolerance: float = 0.0) -> str:
    """source-robust: same value on every branch; source-sensitive: values differ but
    the conclusion holds on every branch; source-dependent: the conclusion changes.
    A programme-confirming result may not be source-dependent."""
    vals = list(values.values())
    if len(set(conclusion.values())) > 1:
        return "source-dependent"
    if max(vals) - min(vals) <= tolerance:
        return "source-robust"
    return "source-sensitive"


# ---------------------------------------------------------------------------
# Pre-registration (sealed before Stage II)
# ---------------------------------------------------------------------------

D1_PRIMARY_WEIGHTS = (2, 1, 1)                    # (w_current, w_syzygy, w_gate)
D1_SENSITIVITY_WEIGHTS = ((3, 1, 1), (2, 2, 1))   # secondary analyses only

PREREGISTRATION = {
    "hierarchy": {
        "D0": "calibration baseline; no textual preference",
        "D1": "minimal textual weighting: currents primary, channels secondary; ratio 2:1:1 "
              "adds exactly current > gate and nothing else; not fitted, never adjusted after "
              "calibration",
        "D2": "family {D2a periodic gate-time, D2b stochastic gate-hazard} for an "
              "underdetermined temporal reading; neither privileged",
        "D3": "strongest reconstruction of printed rite behaviour (78 of 79); 6::2 held out",
    },
    "d1_primary": list(D1_PRIMARY_WEIGHTS),
    "d1_sensitivity": [list(w) for w in D1_SENSITIVITY_WEIGHTS],
    "interpretation_rules": [
        "An effect under both D2a and D2b is robust to the unresolved gate-timing reading; an "
        "effect under one only is schedule-specific, not a D2 or Numogram result.",
        "D2a and D2b are one hypothesis family: their p-values are not combined and they are "
        "not counted as two independent confirmations.",
        "D1 sensitivity weights are secondary; the Stage II primary D1 is 2:1:1.",
        "Success is read against this hierarchy as sealed; it is not re-framed after the fact "
        "around whichever variant performs best.",
        "Laws run unchanged on every graph; no null-specific modification is permitted.",
    ],
}


def registry(gt00: str = GT00_INCLUDE, d1_weights: Tuple[object, object, object] = D1_PRIMARY_WEIGHTS,
             graph: Optional[TypedGraph] = None) -> Dict[str, Contract]:
    """The pre-registered Stage II family, on the canonical graph or any null graph."""
    return {
        "D0": D0Uniform(graph, gt00=gt00),
        "D1": D1TypedWeights(*d1_weights, graph=graph, gt00=gt00),
        "D2a": D2GatedChannels("D2a", graph=graph, gt00=gt00),
        "D2b": D2GatedChannels("D2b", graph=graph, gt00=gt00),
        "D3": D3Lemurian(graph, gt00=gt00),
    }


def family_hash(gt00: str = GT00_INCLUDE) -> str:
    """Seal over the pre-registration and every primary LAW hash (graph-independent)."""
    return _sha({"preregistration": PREREGISTRATION,
                 "laws": {k: c.law_hash() for k, c in registry(gt00).items()}})


def _sha(obj) -> str:
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    print(DYNAMICS_VERSION, "on", C.SPEC_VERSION)
    for key, c in registry().items():
        print("\n%s  %s\n   law: %s\n   law hash:      %s\n   contract hash: %s"
              % (key, c.name, c.law, c.law_hash(), c.contract_hash()))
        print("   depends on inferred rules: %s" % (c.provenance_dependencies()["PROGRAMME_INFERRED"] or "none"))
        if c.time_homogeneous:
            print("   start  P(Warp)   P(Plex)   E[steps in Time-Circuit]")
            for z, r in sorted(absorption(c).items()):
                print("   %d      %-9s %-9s %s" % (z, r["p_warp"], r["p_plex"],
                                                   r["expected_steps_in_time_circuit"]))
    print("\nD2a gate schedule period: %d steps" % D2GatedChannels("D2a").period())
    print("Family seal (laws + pre-registration): %s" % family_hash())
