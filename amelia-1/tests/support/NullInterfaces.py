"""
NullInterfaces.py -- the null interface families N1-N4
Amelia Interface Programme, Stage II preparation

Each family answers a different question. Every instance is a TypedGraph run
through exactly the same laws (NumogramDynamics) and the same interface
(NumogramInterface); only the graph changes.

    N1  typed degree-preserving rewiring
        Question: does the specific Numogram wiring matter?
        Directed edge swaps within each edge type preserve every node's in- and
        out-degree for that type. Swaps are rejected if they change the typed
        self-loop counts, the number of cross-type parallel relations, or create
        a duplicate same-type edge. Edge attributes (gate number, dispute flag,
        label) stay with the edge's source.
    N2  base-generalised Numograms
        Question: is anything specific to decimality?
        Broad controls b = 8, 12 (no Warp: the architecture changes). Architecture-
        matched control b = 64: two closed two-zone regions like decimal, and the
        same binary-cycle order (2 has order 6 modulo 63 as modulo 9), but a
        60-zone transient part spread over six current cycles. b = 46 is available
        as a secondary sensitivity case only.
        The four CCRU rules in genuine base-b arithmetic: twin_b(z) = b - 1 - z;
        current from each side of a syzygy to its difference; gate value C(z) =
        z(z + 1)/2 with channel end dr_b(C(z)), the base-b digital root. Time-systems
        are derived from the current composition, never assumed. Validated by
        base_graph(10) reproducing the canonical graph exactly.
    N3  arithmetic-label scramble
        Question: does the arithmetic assignment carry information beyond the graph?
        The typed graph is kept exactly; the gate arithmetic is permuted
        (gate from z gets value C(pi(z))). Only D2 reads gate arithmetic, so D0, D1
        and D3 must be IDENTICAL under N3; a difference there means an
        implementation error (a built-in negative control).
    N4a random episodic baseline
        Question: floor. Same node count, ten edges of each type, degree sequence
        not preserved, subject to episodic admissibility.
    N4b macroarchitecture-matched random graph
        Question: does the episodic macroarchitecture alone explain a result?
        N4a conditioned (by rejection from the same generator) on the canonical
        macro-shape: two closed regions of sizes {2, 2}, six transient zones, and
        both regions reachable from the transient set. About 1 draw in 22,000
        qualifies (about 1.5 s per instance). The canonical transient core is
        strongly connected; no qualifying random graph in 200,000 draws had that
        property, so N4b does not (and practically cannot) require it.

    Nested hierarchy: N4a (random floor) -> N4b (macroarchitecture) -> N1 (typed
    local structure) -> canonical (specific wiring); N2 isolates decimal arithmetic;
    N3 isolates the arithmetic labelling.

ADMISSIBILITY
    An instance must have at least one transient node and at least one proper
    terminal strongly connected component, or it cannot support an episode. This
    is required of N4 (as proposed) and, as a programme extension, of N1 too.
    Rejection counts are archived in each instance's meta, and census() measures
    how often unrestricted generation is inadmissible: evidence of how unusual the
    canonical episodic organisation is.

SEEDING
    Each instance is generated from H(family, specimen, seed, canonical digest), so
    canonical and null runs are paired by specimen and seed and no single null
    topology dominates. Each instance digest covers generator version, family,
    seed, parent canonical digest, constraints, rejection counts and the edge list.

Python 3.8+ standard library only.
"""

from __future__ import annotations

import hashlib
import random
from collections import Counter
from typing import Dict, List, Optional, Sequence, Tuple

import CanonicalNumogram as C
import NumogramDynamics as D

NULL_VERSION = "NullInterfaces-1.1.0"
TYPES = (C.SYZYGY, C.CURRENT, C.GATE)

NULL_LAYER_INVARIANTS = (
    "Same transduction API: normalised input u, fixed ObservationPacket out.",
    "Same dynamics contracts: D0-D3 applied without null-specific modification.",
    "Same episode rule: terminal-SCC termination on the structural graph; cap 1260.",
    "No observer access to interface identity or raw node count.",
    "Every instance carries its own digest: generator version, seed, parent canonical "
    "digest, constraints, rejection counts, typed edge list.",
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def instance_seed(family: str, specimen: str, seed: int) -> int:
    h = hashlib.sha256(("%s|%s|%d|%s" % (family, specimen, seed, D.canonical_digest())).encode())
    return int(h.hexdigest()[:16], 16)


def digital_root_base(n: int, b: int) -> int:
    """Repeated sum of base-b digits until below b."""
    if n < 0 or b < 2:
        raise ValueError("digital_root_base needs n >= 0 and b >= 2")
    while n >= b:
        s = 0
        while n:
            s += n % b
            n //= b
        n = s
    return n


def admissible(n: int, edges: Sequence[D.Edge]) -> bool:
    out = {z: [e for e in edges if e.src == z] for z in range(n)}
    term = D.terminal_classes(n, out)
    in_term = {z for c in term for z in c}
    return bool(term) and len(in_term) < n


def parallel_relations(edges: Sequence[D.Edge]) -> int:
    """Pairs of edges of different types sharing (src, dst)."""
    by_pair: Dict[Tuple[int, int], Counter] = {}
    for e in edges:
        by_pair.setdefault((e.src, e.dst), Counter())[e.type] += 1
    total = 0
    for cnt in by_pair.values():
        types = list(cnt.values())
        for i in range(len(types)):
            for j in range(i + 1, len(types)):
                total += types[i] * types[j]
    return total


def self_loops(edges: Sequence[D.Edge]) -> Dict[str, int]:
    return {t: sum(1 for e in edges if e.type == t and e.src == e.dst) for t in TYPES}


def typed_degrees(n: int, edges: Sequence[D.Edge]) -> Dict[int, Dict[str, Tuple[int, int]]]:
    out = {z: {t: [0, 0] for t in TYPES} for z in range(n)}
    for e in edges:
        out[e.dst][e.type][0] += 1
        out[e.src][e.type][1] += 1
    return {z: {t: tuple(v) for t, v in d.items()} for z, d in out.items()}


def _meta(**kw) -> Tuple[Tuple[str, str], ...]:
    base = {"generator": NULL_VERSION, "parent_canonical_digest": D.canonical_digest()}
    base.update({k: str(v) for k, v in kw.items()})
    return tuple(sorted(base.items()))


# ---------------------------------------------------------------------------
# Canonical and N2 (base-generalised)
# ---------------------------------------------------------------------------

def canonical() -> D.TypedGraph:
    return D.canonical_graph()


def base_graph(b: int, family: Optional[str] = None) -> D.TypedGraph:
    """The four CCRU rules in base b (b even)."""
    if b < 4 or b % 2:
        raise ValueError("base must be even and at least 4")
    edges: List[D.Edge] = []
    for z in range(b):
        edges.append(D.Edge(z, b - 1 - z, C.SYZYGY, C.SYZYGY))
    for lo in range(b // 2):
        hi = b - 1 - lo
        d = hi - lo
        for side in (hi, lo):
            edges.append(D.Edge(side, d, C.CURRENT, "%d::%d" % (hi, lo)))
    for z in range(b):
        cz = C.cumulation(z)
        edges.append(D.Edge(z, digital_root_base(cz, b), C.GATE, "Gt-%02d" % cz, cz, cz == 0))
    ts = time_systems(b)
    return D.TypedGraph(n=b, edges=tuple(edges), family=family or "N2-b%d" % b,
                        meta=_meta(base=b, time_systems=ts,
                                   rule="twin b-1-z; current to difference; gate dr_b(C(z))"))


def time_systems(b: int) -> Dict[str, list]:
    """Derived from the current composition: syzygy -> syzygy holding its tractor."""
    pairs = [(b - 1 - lo, lo) for lo in range(b // 2)]
    of = {z: p for p in pairs for z in p}
    step = {p: of[p[0] - p[1]] for p in pairs}
    loops = sorted(p for p in pairs if step[p] == p)
    cycles, seen = [], set(loops)
    for p in pairs:
        if p in seen:
            continue
        cyc, q = [], p
        while q not in cyc and q not in seen:
            cyc.append(q)
            q = step[q]
        if q in cyc:
            cycles.append(cyc[cyc.index(q):])
        seen.update(cyc)
    return {"loops": ["%d::%d" % p for p in loops],
            "cycles": [["%d::%d" % p for p in c] for c in cycles],
            "feeding_chains": sorted("%d::%d" % p for p in pairs
                                     if p not in loops and not any(p in c for c in cycles))}


def n2_base(b: int) -> D.TypedGraph:
    if b == 10:
        raise ValueError("base 10 is the canonical Numogram, not a null")
    return base_graph(b)


# ---------------------------------------------------------------------------
# N1 typed degree-preserving rewiring
# ---------------------------------------------------------------------------

def n1_degree_matched(seed: int, specimen: str = "", swaps_per_type: int = 200,
                      max_instances: int = 1000) -> D.TypedGraph:
    rng = random.Random(instance_seed("N1", specimen, seed))
    base = list(canonical().edges)
    n = 10
    loops0, par0 = self_loops(base), parallel_relations(base)
    canon_keys = sorted(e.key() for e in base)
    rejected_inadmissible = rejected_identical = 0
    for attempt in range(max_instances):
        edges = list(base)
        accepted = 0
        for t in TYPES:
            idx = [i for i, e in enumerate(edges) if e.type == t]
            for _ in range(swaps_per_type):
                i, j = rng.sample(idx, 2)
                a, b_ = edges[i], edges[j]
                if a.dst == b_.dst:
                    continue
                na = D.Edge(a.src, b_.dst, a.type, a.label, a.gate_number, a.disputed)
                nb = D.Edge(b_.src, a.dst, b_.type, b_.label, b_.gate_number, b_.disputed)
                trial = list(edges)
                trial[i], trial[j] = na, nb
                same = [(e.src, e.dst) for e in trial if e.type == t]
                if len(set(same)) != len(same):
                    continue
                if self_loops(trial) != loops0 or parallel_relations(trial) != par0:
                    continue
                edges = trial
                accepted += 1
        if sorted(e.key() for e in edges) == canon_keys:
            rejected_identical += 1
            continue
        if not admissible(n, edges):
            rejected_inadmissible += 1
            continue
        return D.TypedGraph(n=n, edges=tuple(edges), family="N1",
                            meta=_meta(seed=seed, specimen=specimen, swaps_per_type=swaps_per_type,
                                       accepted_swaps=accepted,
                                       rejected_inadmissible=rejected_inadmissible,
                                       rejected_identical=rejected_identical,
                                       constraints="typed in/out degree per node; typed self-loop "
                                                   "counts; cross-type parallel relations; no "
                                                   "duplicate same-type edge; admissible"))
    raise RuntimeError("N1: no admissible instance in %d attempts" % max_instances)


# ---------------------------------------------------------------------------
# N3 arithmetic-label scramble
# ---------------------------------------------------------------------------

def n3_arithmetic_scramble(seed: int, specimen: str = "") -> D.TypedGraph:
    rng = random.Random(instance_seed("N3", specimen, seed))
    perm = list(range(10))
    while perm == list(range(10)):
        rng.shuffle(perm)
    edges = []
    for e in canonical().edges:
        if e.type == C.GATE:
            v = C.cumulation(perm[e.src])
            edges.append(D.Edge(e.src, e.dst, e.type, "Gt-%02d" % v, v, e.disputed))
        else:
            edges.append(e)
    return D.TypedGraph(n=10, edges=tuple(edges), family="N3",
                        meta=_meta(seed=seed, specimen=specimen, permutation=perm,
                                   constraints="typed graph fixed; gate arithmetic C(pi(z)); "
                                               "dispute flag stays structural"))


# ---------------------------------------------------------------------------
# N4 random episodic baseline
# ---------------------------------------------------------------------------

def _random_typed_graph(rng: random.Random, n: int = 10, per_type: int = 10) -> List[D.Edge]:
    edges = []
    for t in TYPES:
        pairs = set()
        while len(pairs) < per_type:
            pairs.add((rng.randrange(n), rng.randrange(n)))
        for s, d in sorted(pairs):
            if t == C.GATE:
                v = C.cumulation(s)
                edges.append(D.Edge(s, d, t, "Gt-%02d" % v, v, False))
            else:
                edges.append(D.Edge(s, d, t, t))
    return edges


def n4_random_episode_graph(seed: int, specimen: str = "", max_instances: int = 100000) -> D.TypedGraph:
    """N4a, the broad random floor."""
    rng = random.Random(instance_seed("N4", specimen, seed))
    rejected = 0
    for _ in range(max_instances):
        edges = _random_typed_graph(rng)
        if admissible(10, edges):
            return D.TypedGraph(n=10, edges=tuple(edges), family="N4a",
                                meta=_meta(seed=seed, specimen=specimen, rejected_inadmissible=rejected,
                                           constraints="10 nodes; 10 edges per type; no duplicate "
                                                       "same-type edge; degree sequence free; admissible"))
        rejected += 1
    raise RuntimeError("N4: no admissible instance")


def macro_shape(n: int, edges: Sequence[D.Edge]) -> Dict[str, object]:
    out = {z: [e for e in edges if e.src == z] for z in range(n)}
    term = D.terminal_classes(n, out)
    in_term = {z for c in term for z in c}
    core = [z for z in range(n) if z not in in_term]

    def reach(srcs):
        seen, st = set(srcs), list(srcs)
        while st:
            for e in out[st.pop()]:
                if e.dst not in seen:
                    seen.add(e.dst)
                    st.append(e.dst)
        return seen

    r = reach(core) if core else set()
    return {"region_sizes": sorted(len(c) for c in term), "transient": len(core),
            "regions_reachable_from_core": all(c <= r for c in term) if core else False,
            "core_strongly_connected": bool(core) and all(set(core) <= reach([z]) for z in core)}


CANONICAL_SHAPE = None


def canonical_shape() -> Dict[str, object]:
    global CANONICAL_SHAPE
    if CANONICAL_SHAPE is None:
        CANONICAL_SHAPE = macro_shape(10, canonical().edges)
    return CANONICAL_SHAPE


def n4b_shape_matched(seed: int, specimen: str = "", max_draws: int = 5000000) -> D.TypedGraph:
    """N4a conditioned on the canonical macro-shape (region sizes, transient count,
    regions reachable from the core)."""
    target = canonical_shape()
    rng = random.Random(instance_seed("N4b", specimen, seed))
    for k in range(max_draws):
        edges = _random_typed_graph(rng)
        sh = macro_shape(10, edges)
        if (sh["region_sizes"] == target["region_sizes"] and sh["transient"] == target["transient"]
                and sh["regions_reachable_from_core"]):
            return D.TypedGraph(n=10, edges=tuple(edges), family="N4b",
                                meta=_meta(seed=seed, specimen=specimen, rejected_draws=k,
                                           core_strongly_connected=sh["core_strongly_connected"],
                                           constraints="N4a generator conditioned on region sizes "
                                                       "{2,2}, 6 transient, regions reachable from core"))
    raise RuntimeError("N4b: no instance in %d draws" % max_draws)


def census(samples: int = 2000, seed: int = 0) -> Dict[str, object]:
    """Archive: how often unrestricted random generation (N4 without the admissibility
    filter) fails to support episodes."""
    rng = random.Random(seed)
    no_terminal = all_terminal = ok = 0
    for _ in range(samples):
        edges = _random_typed_graph(rng)
        out = {z: [e for e in edges if e.src == z] for z in range(10)}
        term = D.terminal_classes(10, out)
        in_term = {z for c in term for z in c}
        if not term:
            no_terminal += 1
        elif len(in_term) == 10:
            all_terminal += 1
        else:
            ok += 1
    return {"samples": samples, "admissible": ok, "no_proper_terminal_scc": no_terminal,
            "no_transient_node": all_terminal}


# ---------------------------------------------------------------------------
# Family
# ---------------------------------------------------------------------------

n4a_random = n4_random_episode_graph

N2_PRIMARY_BASES = (8, 12, 64)
N2_SECONDARY_BASES = (46,)

NULL_PREREGISTRATION = {
    "hierarchy": ["N4a random floor", "N4b episodic macroarchitecture", "N1 typed local structure",
                  "canonical specific wiring"],
    "n2_roles": {"8": "broad, architecture-changing", "12": "broad, architecture-changing",
                 "64": "architecture-matched (primary)", "46": "secondary sensitivity only"},
    "interpretation_rules": [
        "canonical > N4a but ~ N4b: the advantage belongs to the episodic macroarchitecture.",
        "canonical > N4b: the specific arrangement does work beyond the coarse architecture.",
        "N4b > N4a: the macroarchitecture has computational significance of its own.",
        "canonical > N1: the specific typed wiring matters beyond typed degrees.",
        "decimal > 8 and 12 but ~ 64: an architectural-family effect, not decimal specificity.",
        "decimal > 8, 12 and 64: stronger evidence for a specifically decimal realisation.",
        "all bases similar: evidence for the generalised rule family.",
        "D2 x N2 cells are descriptive only: gate values C(z) grow with the base, so D2 "
        "conflates base with gate clock speed (D2 truncation at the 1260 cap: base 8 about "
        "7-11%, base 12 about 50%, base 64 about 48%). Decimal-specificity claims use D0, D1 "
        "and D3; laws and cap stay identical on every graph.",
    ],
}


def family(seed: int, specimen: str = "") -> Dict[str, D.TypedGraph]:
    """All primary interfaces for one (specimen, seed) cell of Stage II."""
    fam = {"canonical": canonical(), "N1": n1_degree_matched(seed, specimen)}
    for b in N2_PRIMARY_BASES:
        fam["N2-b%d" % b] = n2_base(b)
    fam["N3"] = n3_arithmetic_scramble(seed, specimen)
    fam["N4a"] = n4_random_episode_graph(seed, specimen)
    fam["N4b"] = n4b_shape_matched(seed, specimen)
    return fam


def null_family_hash() -> str:
    return D._sha({"version": NULL_VERSION, "preregistration": NULL_PREREGISTRATION,
                   "invariants": list(NULL_LAYER_INVARIANTS)})


if __name__ == "__main__":
    print(NULL_VERSION, "on", D.DYNAMICS_VERSION)
    for b in (8, 10, 12, 64):
        print("base %2d time-systems: %s" % (b, time_systems(b)))
    fam = family(seed=1)
    for k, g in fam.items():
        c = D.D0Uniform(g)
        m = dict(g.meta)
        print("%-9s n=%-2d digest %s  terminal %s  transient %d  rejections %s"
              % (k, g.n, g.digest()[:12], [sorted(x) for x in c.terminal], len(c.transient),
                 m.get("rejected_inadmissible", "-")))
    print("census of unrestricted random typed graphs:", census())
    print("canonical macro-shape:", canonical_shape())
    print("null pre-registration seal:", null_family_hash())
