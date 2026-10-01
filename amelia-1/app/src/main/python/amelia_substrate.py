"""
amelia_substrate.py -- Android Amelia 1.0, milestone M1: the developmental substrate.

WHAT AMELIA IS
    An episodic walker on the canonical Numogram. Warp and Plex are closed and the
    Time-Circuit is transient under every sealed law, so behaviour has two channels:
        INGRESS  the zone at which Amelia enters the next episode (the embodiment's choice)
        PASSAGE  the edge taken at each step inside an episode, among the edges the sealed
                 law permits from the current zone
    Episodes follow NumogramInterface's sealed rules exactly (episode-local clock, end at
    the first step into a terminal class, holds, cap 1260). No edge is ever added,
    removed or relabelled; the law's exact probabilities are the prior.

MEMORY ACTS ONLY THROUGH BEHAVIOUR
        passage:  p(e) proportional to p_law(e) * (1 + beta * s(e)),   s(e) in [0, 1 + ...]
        ingress:  q(z) proportional to 1 + gamma * i(z)
    With every modulation zero (beta = gamma = 0, or an empty trace) passage is drawn with
    the law's exact Fraction arithmetic from the same stream, so episodes are identical to
    NumogramInterface.episode (the M1 regression check).

PRESENT STATE P AND TRACE H (serialised and digested separately)
    P  seed, transaction index k, previous exit zone, law key, configuration digest.
       All randomness is derived from (seed, k) by SHA-256, so P carries no mutable PRNG.
    H  L1 habit field      E[a][b]: leaky trace of passages a->b (per step, lambda1);
                           Z[z]: leaky trace of zones entered. Read by row at the current
                           zone: s1(e) = E[z][dst] / (1 + sum_b E[z][b]).
       L2 episodic archive bounded list of traces {key, content, strength, born, retrieved}.
                           key = context at episode start (entry zone, previous exit zone,
                           region profile); content = weighted passages of that episode.
                           Retrieval by cosine similarity of context (not recency), top R
                           above threshold. Retrieved traces are LABILE for the episode:
                           at its end their content is blended toward what happened
                           (reconsolidation, rate rho). s2(e) = similarity- and strength-
                           weighted share of retrieved traces containing passage src->dst.
       L3 canalisation     one slow variable x_r per structural region (the transient set
                           and each terminal class, found from the graph, never from labels):
                           x <- x + alpha * (x - x^3 + h_r), h_r = a * (o_r - b_r), o_r the
                           recent share of steps in region r. Bistable for |h_r| < 0.385.
                           m_r = (x_r + 1) / 2 sets gains and a preference for entering r.

DETERMINISM
    Only IEEE-exact operations (+, -, *, /, math.sqrt) are used in the dynamics, so the phone
    and the CI runner produce bit-identical states. No exp, log or trigonometric function.

CONSTANTS
    All constants below are PROVISIONAL. They are fixed by the M3 instrument
    characterisation on off-cohort seeds and sealed before the M4 acceptance run.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import random
from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Tuple

import NumogramDynamics as D
import NumogramInterface as I

SUBSTRATE_VERSION = "AmeliaSubstrate-1.0.0-M1"

PROVISIONAL = {
    "law": "D1",
    "beta": 2.0,          # passage modulation gain
    "gamma": 1.0,         # ingress modulation gain
    "g1": 1.0,            # L1 weight in s(e)
    "g2": 1.0,            # L2 weight in s(e)
    "g3": 0.5,            # L3 direct preference for entering a region
    "kappa": 0.5,         # L3 gain on L1 + L2 toward the destination region
    "lambda1": 0.98,      # L1 per-step carry-forward (time constant ~50 steps)
    "l2_capacity": 256,
    "l2_retrieve": 3,     # R
    "l2_threshold": 0.5,  # minimum cosine similarity for retrieval
    "l2_rho": 0.3,        # reconsolidation rate while labile
    "l2_decay": 0.995,    # per-episode strength decay
    "l2_reinforce": 0.2,  # strength added on retrieval
    "l3_alpha": 0.05,     # L3 integration rate per episode
    "l3_a": 4.0,          # drive gain
    "l3_eta": 0.05,       # EWMA rate of region occupancy per episode
    "l3_baseline": None,  # b_r; None = equal shares (to be characterised in M3)
    "l_max": I.L_MAX_DEFAULT,
}


def _sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _uniform(tag: str, seed: int, k: int) -> float:
    h = hashlib.sha256(("AMELIA1|%s|%d|%d" % (tag, seed, k)).encode("ascii")).hexdigest()
    return (int(h[:13], 16) + 0.5) / float(1 << 52)


def contract_for(law: str) -> D.Contract:
    return D.registry(graph=D.canonical_graph())[law]


def regions_of(contract: D.Contract) -> Tuple[Tuple[int, ...], ...]:
    """Structural regions: the transient set, then each terminal class (sorted)."""
    terminal = sorted(tuple(sorted(c)) for c in contract.terminal)
    transient = tuple(sorted(contract.transient))
    return (transient,) + tuple(terminal)


def _key(region: Sequence[int]) -> str:
    return ",".join(str(z) for z in region)


class AmeliaSubstrate:
    """One developmental lineage. All state lives in self.P (present) and self.H (trace)."""

    def __init__(self, seed: int, config: Optional[Dict[str, object]] = None):
        cfg = dict(PROVISIONAL)
        cfg.update(config or {})
        self.cfg = cfg
        self.contract = contract_for(cfg["law"])
        self.interface = I.NumogramInterface(self.contract, l_max=cfg["l_max"])
        self.regions = regions_of(self.contract)
        self.region_of = {z: i for i, r in enumerate(self.regions) for z in r}
        n = self.contract.graph.n
        self.n = n
        base = cfg["l3_baseline"] or [1.0 / len(self.regions)] * len(self.regions)
        self.baseline = [float(b) for b in base]
        self.P = {"seed": seed, "k": 0, "prev_exit": None, "law": cfg["law"],
                  "config_digest": self.config_digest()}
        self.H = self.empty_trace()

    # -- configuration and state ---------------------------------------------------
    def config_digest(self) -> str:
        return _sha({"version": SUBSTRATE_VERSION, "config": self.cfg,
                     "contract": self.contract.contract_hash()})

    def empty_trace(self) -> Dict[str, object]:
        n, R = self.n, len(self.regions)
        return {"L1": {"E": [[0.0] * n for _ in range(n)], "Z": [0.0] * n},
                "L2": {"traces": [], "next_id": 0},
                "L3": {"x": [-1.0] * R, "o": list(self.baseline)}}

    def digest_P(self) -> str:
        return _sha(self.P)

    def digest_H(self) -> str:
        return _sha(self.H)

    def export_state(self) -> str:
        return json.dumps({"version": SUBSTRATE_VERSION, "P": self.P, "H": self.H,
                           "digest_P": self.digest_P(), "digest_H": self.digest_H()},
                          sort_keys=True, separators=(",", ":"))

    @classmethod
    def import_state(cls, blob: str, config: Optional[Dict[str, object]] = None) -> "AmeliaSubstrate":
        d = json.loads(blob)
        s = cls(d["P"]["seed"], config)
        if d["P"]["config_digest"] != s.config_digest():
            raise ValueError("configuration differs from the one that produced this state")
        s.P, s.H = d["P"], d["H"]
        if s.digest_P() != d["digest_P"] or s.digest_H() != d["digest_H"]:
            raise ValueError("state digest mismatch on import")
        return s

    def fork(self) -> "AmeliaSubstrate":
        other = AmeliaSubstrate(self.P["seed"], self.cfg)
        other.P = copy.deepcopy(self.P)
        other.H = copy.deepcopy(self.H)
        return other

    def restore_present(self, P: Dict[str, object]) -> None:
        """Set present state P, leaving trace H untouched (AC-2)."""
        if P["config_digest"] != self.config_digest():
            raise ValueError("present state from a different configuration")
        self.P = copy.deepcopy(P)

    # -- readouts -----------------------------------------------------------------
    def _m(self) -> List[float]:
        return [(x + 1.0) / 2.0 for x in self.H["L3"]["x"]]

    def context(self, entry: int) -> List[float]:
        v = [0.0] * (2 * self.n + len(self.regions))
        v[entry] = 1.0
        if self.P["prev_exit"] is not None:
            v[self.n + self.P["prev_exit"]] = 1.0
        for i, o in enumerate(self.H["L3"]["o"]):
            v[2 * self.n + i] = o
        return v

    @staticmethod
    def _cos(a: Sequence[float], b: Sequence[float]) -> float:
        na = sum(x * x for x in a)
        nb = sum(x * x for x in b)
        if na == 0.0 or nb == 0.0:
            return 0.0
        return sum(x * y for x, y in zip(a, b)) / (math.sqrt(na) * math.sqrt(nb))

    def retrieve(self, ctx: Sequence[float]) -> List[Tuple[int, float]]:
        """Indices of retrieved traces with their similarity; ties broken by trace id."""
        scored = []
        for i, tr in enumerate(self.H["L2"]["traces"]):
            sim = self._cos(ctx, tr["key"])
            if sim >= self.cfg["l2_threshold"]:
                scored.append((-sim, tr["id"], i, sim))
        scored.sort()
        return [(i, sim) for _, _, i, sim in scored[: self.cfg["l2_retrieve"]]]

    def s_edge(self, z: int, e: D.Edge, retrieved: List[Tuple[int, float]]) -> float:
        E = self.H["L1"]["E"][z]
        row = sum(E)
        s1 = E[e.dst] / (1.0 + row)
        s2 = 0.0
        if retrieved:
            num = den = 0.0
            traces = self.H["L2"]["traces"]
            for i, sim in retrieved:
                w = sim * traces[i]["strength"]
                den += w
                c = traces[i]["content"]
                tot = sum(c.values())
                if tot > 0.0:
                    num += w * c.get("%d>%d" % (e.src, e.dst), 0.0) / tot
            s2 = num / den if den > 0.0 else 0.0
        m = self._m()
        r_dst, r_src = self.region_of[e.dst], self.region_of[z]
        s = (self.cfg["g1"] * s1 + self.cfg["g2"] * s2) * (1.0 + self.cfg["kappa"] * m[r_dst])
        if r_dst != r_src:
            s += self.cfg["g3"] * m[r_dst]
        return s

    def ingress_scores(self) -> List[float]:
        Z = self.H["L1"]["Z"]
        zt = sum(Z)
        entry_strength = [0.0] * self.n
        for tr in self.H["L2"]["traces"]:
            entry_strength[tr["entry"]] += tr["strength"]
        et = sum(entry_strength)
        m = self._m()
        return [(Z[z] / zt if zt > 0.0 else 0.0) + (entry_strength[z] / et if et > 0.0 else 0.0)
                + m[self.region_of[z]] for z in range(self.n)]

    # -- the two behavioural channels ---------------------------------------------
    def choose_entry(self) -> int:
        u = _uniform("INGRESS", self.P["seed"], self.P["k"])
        g = self.cfg["gamma"]
        if g == 0.0:
            return min(self.n - 1, int(self.n * u))
        w = [1.0 + g * sc for sc in self.ingress_scores()]
        r, acc = u * sum(w), 0.0
        for z, x in enumerate(w):
            acc += x
            if r < acc:
                return z
        return self.n - 1

    def _step(self, state: D.State, t: int, rng: random.Random,
              retrieved: List[Tuple[int, float]]) -> Tuple[Optional[D.Edge], D.State]:
        probs = self.contract.probabilities(state, t, rng)
        if not probs:
            return None, D.State(state.zone, D.HOLD)
        u = rng.random()
        beta = self.cfg["beta"]
        mod = [beta * self.s_edge(state.zone, e, retrieved) for e, _ in probs] if beta != 0.0 else None
        if mod is None or all(x == 0.0 for x in mod):
            uf, acc = Fraction(u), Fraction(0)          # identical to Contract.step
            for e, p in probs:
                acc += p
                if uf < acc:
                    return e, D.State(e.dst, e.type)
            e = probs[-1][0]
            return e, D.State(e.dst, e.type)
        w = [float(p) * (1.0 + x) for (e, p), x in zip(probs, mod)]
        r, acc = u * sum(w), 0.0
        for (e, _), x in zip(probs, w):
            acc += x
            if r < acc:
                return e, D.State(e.dst, e.type)
        e = probs[-1][0]
        return e, D.State(e.dst, e.type)

    def episode(self, z0: int, rng: random.Random, retrieved: List[Tuple[int, float]]) -> I.RawEpisodeRecord:
        """NumogramInterface.episode with modulated passage (episode clock, same end rule)."""
        itf = self.interface
        state = D.State(z0, None)
        steps, truncated = [], True
        for k in range(itf.l_max):
            if not self.contract.edges[state.zone]:
                truncated = False
                break
            e, state = self._step(state, k, rng, retrieved)
            if e is None:
                steps.append((k, state.zone, D.HOLD, D.HOLD, state.zone))
                continue
            steps.append((k, e.src, e.type, e.label, e.dst))
            self._l1_step(e.src, e.dst)
            if state.zone in itf._class_of:
                truncated = False
                break
        cls = itf._class_of.get(state.zone)
        return I.RawEpisodeRecord(graph_digest=self.contract.graph.digest(), n=self.n, entry=z0,
                                  exit=state.zone, exit_class=tuple(sorted(cls)) if cls else None,
                                  steps=tuple(steps), truncated=truncated)

    # -- trace updates ------------------------------------------------------------
    def _l1_step(self, a: int, b: int) -> None:
        lam = self.cfg["lambda1"]
        E, Z = self.H["L1"]["E"], self.H["L1"]["Z"]
        for row in E:
            for j in range(self.n):
                row[j] *= lam
        for j in range(self.n):
            Z[j] *= lam
        E[a][b] += 1.0
        Z[b] += 1.0

    def _l2_update(self, ctx: List[float], entry: int, raw: I.RawEpisodeRecord,
                   retrieved: List[Tuple[int, float]]) -> None:
        cfg, L2 = self.cfg, self.H["L2"]
        content: Dict[str, float] = {}
        for s in raw.steps:
            if s[2] != D.HOLD:
                key = "%d>%d" % (s[1], s[4])
                content[key] = content.get(key, 0.0) + 1.0
        traces = L2["traces"]
        rho = cfg["l2_rho"]
        for i, _ in retrieved:                          # reconsolidation of labile traces
            tr = traces[i]
            old = tr["content"]
            new = {kk: (1.0 - rho) * v for kk, v in old.items()}
            for kk, v in content.items():
                new[kk] = new.get(kk, 0.0) + rho * v
            tr["content"] = {kk: new[kk] for kk in sorted(new)}
            tr["strength"] += cfg["l2_reinforce"]
            tr["retrieved"] = self.P["k"]
        for tr in traces:
            tr["strength"] *= cfg["l2_decay"]
        traces.append({"id": L2["next_id"], "born": self.P["k"], "retrieved": None, "entry": entry,
                       "key": list(ctx), "content": {kk: content[kk] for kk in sorted(content)},
                       "strength": 1.0})
        L2["next_id"] += 1
        if len(traces) > cfg["l2_capacity"]:
            j = min(range(len(traces)), key=lambda i: (traces[i]["strength"], traces[i]["id"]))
            traces.pop(j)

    def _l3_update(self, raw: I.RawEpisodeRecord) -> None:
        cfg, L3 = self.cfg, self.H["L3"]
        R = len(self.regions)
        counts = [0.0] * R
        zones = [raw.entry] + [s[4] for s in raw.steps]
        for z in zones:
            counts[self.region_of[z]] += 1.0
        tot = sum(counts)
        eta = cfg["l3_eta"]
        for r in range(R):
            L3["o"][r] = (1.0 - eta) * L3["o"][r] + eta * counts[r] / tot
            h = cfg["l3_a"] * (L3["o"][r] - self.baseline[r])
            x = L3["x"][r]
            L3["x"][r] = x + cfg["l3_alpha"] * (x - x * x * x + h)

    # -- one transaction ----------------------------------------------------------
    def transact(self) -> Dict[str, object]:
        seed, k = self.P["seed"], self.P["k"]
        z0 = self.choose_entry()
        ctx = self.context(z0)
        retrieved = self.retrieve(ctx)
        raw = self.episode(z0, I.episode_rng(seed, k), retrieved)
        retrieved_ids = [self.H["L2"]["traces"][i]["id"] for i, _ in retrieved]
        self._l2_update(ctx, z0, raw, retrieved)
        self._l3_update(raw)
        self.P["prev_exit"] = raw.exit
        self.P["k"] = k + 1
        return {"k": k, "entry": z0, "exit": raw.exit, "length": raw.length,
                "passages": [[s[1], s[4], s[2]] for s in raw.steps],
                "retrieved": retrieved_ids,
                "raw_digest": raw.digest()}

    def run(self, n: int) -> List[Dict[str, object]]:
        return [self.transact() for _ in range(n)]


# ---------------------------------------------------------------------------
# Android entry points (JSON strings)
# ---------------------------------------------------------------------------

def demo_run(seed: int, n: int) -> str:
    s = AmeliaSubstrate(seed)
    recs = s.run(n)
    exits = {}
    for r in recs:
        exits[str(r["exit"])] = exits.get(str(r["exit"]), 0) + 1
    return json.dumps({"ok": True, "version": SUBSTRATE_VERSION, "seed": seed, "episodes": n,
                       "exits": exits, "digest_P": s.digest_P(), "digest_H": s.digest_H(),
                       "l2_traces": len(s.H["L2"]["traces"]), "l3_x": s.H["L3"]["x"]},
                      sort_keys=True)
