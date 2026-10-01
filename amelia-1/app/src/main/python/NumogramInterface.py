"""
NumogramInterface.py -- episodic embodiment <-> interface transduction
Amelia Interface Programme, Stage II preparation

WHY EPISODIC
    Under every dynamics contract the canonical Time-Circuit is transient and Warp
    and Plex are closed. The Numogram, on its own terms, is an episodic transducer.
    The interface therefore adds no edge to any graph. The embodiment supplies the
    recurrence by repeatedly launching finite episodes:

        E_t --iota--> z0 --D_k on graph N_j--> episode --epsilon--> packet --> E_{t+1}

THE SEALED RULES (Stage II primary; identical for every graph N_j)
    INGRESS   The embodiment exports a normalised scalar u in [0, 1]. The interface
              maps it by one topology-blind rule that knows only the node count n:
                  iota_n(u) = min(n - 1, floor(n * u))
              For the canonical Numogram (n = 10) this is the ten-bin quantizer.
    EPISODE   Start at z0 with no previous step, episode clock at 0. Step under the
              contract. End at the first step after which the walker is in a
              terminal strongly connected component of the STRUCTURAL graph (the
              union of all possible edges, never the edges open at time t, so a
              temporarily closed gate cannot make a node look terminal). At least
              one move is attempted. If no edge is permitted, the walker holds (time
              advances). A node with no structural out-edge ends the episode at
              once. Cap L_max = 1260 steps; a capped episode is flagged truncated.
    CLOCK     Episode-local, so that all memory lives in the embodiment.
    EGRESS    Two objects. The RawEpisodeRecord (node IDs, edges, labels) is kept for
              provenance and audit only. The ObservationPacket is the ONLY object that
              embodiments and the observer may read. Its schema is fixed and
              interface-neutral:
                  entry_position          z0 / (n - 1)
                  exit_position           z_exit / (n - 1)
                  episode_length          steps / L_max
                  edge_fraction_syzygy    syzygy steps / steps
                  edge_fraction_current   current steps / steps
                  edge_fraction_gate      gate steps / steps   (holds make these sum below 1)
                  node_coverage           distinct nodes visited / n
                  transition_recurrence   repeated (src, dst, type) moves / moves
                  truncated               0 or 1
              No node ID, node count, edge label or interface identity is in the packet.

RESIDUAL LEAKAGE (declared)
    Positions are multiples of 1 / (n - 1), and coverage of 1 / n, so a long run of
    packets reveals n statistically. The observer is blind to interface identity by
    construction; the family N_j of a packet stream is recoverable only by such
    inference, which the observer protocol must forbid.

COMPATIBILITY
    Python 3.8+ standard library only. Each episode draws from its own stream derived
    from (seed, transaction index), independent of the embodiment's randomness.
"""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple

import CanonicalNumogram as C
import NumogramDynamics as D

INTERFACE_VERSION = "NumogramInterface-1.1.0"
L_MAX_DEFAULT = 1260
CLOCK_EPISODE = "episode"
CLOCK_GLOBAL = "global"

PACKET_FIELDS = ("entry_position", "exit_position", "episode_length", "edge_fraction_syzygy",
                 "edge_fraction_current", "edge_fraction_gate", "node_coverage",
                 "transition_recurrence", "truncated")


# ---------------------------------------------------------------------------
# Records
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RawEpisodeRecord:
    """Audit only. Never passed to an embodiment or the observer."""
    graph_digest: str
    n: int
    entry: int
    exit: int
    exit_class: Optional[Tuple[int, ...]]
    steps: Tuple[Tuple[int, int, str, str, int], ...]   # (t, src, type, label, dst); holds typed 'hold'
    truncated: bool

    @property
    def length(self) -> int:
        return len(self.steps)

    def digest(self) -> str:
        return D._sha({"graph": self.graph_digest, "entry": self.entry, "exit": self.exit,
                       "steps": [list(s) for s in self.steps], "truncated": self.truncated})


@dataclass(frozen=True)
class ObservationPacket:
    entry_position: float
    exit_position: float
    episode_length: float
    edge_fraction_syzygy: float
    edge_fraction_current: float
    edge_fraction_gate: float
    node_coverage: float
    transition_recurrence: float
    truncated: int

    def as_tuple(self) -> Tuple[float, ...]:
        return tuple(getattr(self, f) for f in PACKET_FIELDS)


def make_packet(raw: RawEpisodeRecord, l_max: int) -> ObservationPacket:
    n, L = raw.n, raw.length
    denom = max(1, L)
    moves = [s for s in raw.steps if s[2] != D.HOLD]
    counts = {t: sum(1 for s in moves if s[2] == t) for t in (C.SYZYGY, C.CURRENT, C.GATE)}
    visited = {raw.entry} | {s[4] for s in raw.steps}
    seen, repeats = set(), 0
    for s in moves:
        k = (s[1], s[4], s[2])
        repeats += k in seen
        seen.add(k)
    return ObservationPacket(
        entry_position=raw.entry / (n - 1),
        exit_position=raw.exit / (n - 1),
        episode_length=L / l_max,
        edge_fraction_syzygy=counts[C.SYZYGY] / denom,
        edge_fraction_current=counts[C.CURRENT] / denom,
        edge_fraction_gate=counts[C.GATE] / denom,
        node_coverage=len(visited) / n,
        transition_recurrence=repeats / max(1, len(moves)),
        truncated=int(raw.truncated),
    )


@dataclass(frozen=True)
class Transaction:
    index: int
    u: float
    embodiment_digest_before: str
    raw: RawEpisodeRecord
    packet: ObservationPacket


@dataclass(frozen=True)
class TransactionLog:
    interface_hash: str
    embodiment: str
    seed: int
    transactions: Tuple[Transaction, ...]

    def digest(self) -> str:
        return D._sha({"interface": self.interface_hash, "embodiment": self.embodiment,
                       "seed": self.seed,
                       "tx": [[t.index, repr(t.u), t.embodiment_digest_before, t.raw.digest(),
                               list(t.packet.as_tuple())] for t in self.transactions]})

    def packets(self) -> List[ObservationPacket]:
        """The observer's view: packets only."""
        return [t.packet for t in self.transactions]

    def truncation_rate(self) -> float:
        return sum(t.raw.truncated for t in self.transactions) / max(1, len(self.transactions))


# ---------------------------------------------------------------------------
# Embodiments
# ---------------------------------------------------------------------------

class Embodiment:
    """Protocol. observe() returns u in [0, 1]; update() receives the packet only."""
    name = "embodiment"

    def observe(self) -> float:
        raise NotImplementedError

    def update(self, packet: ObservationPacket) -> None:
        raise NotImplementedError

    def state_digest(self) -> str:
        raise NotImplementedError


class NullEmbodiment(Embodiment):
    """E0: memoryless; u uniform on [0, 1) from its own seeded stream; updates ignored."""
    name = "E0-null"

    def __init__(self, seed: int):
        self._rng = random.Random(seed)
        self._seed = seed

    def observe(self) -> float:
        return self._rng.random()

    def update(self, packet) -> None:
        return None

    def state_digest(self) -> str:
        return "E0:%d" % self._seed


# ---------------------------------------------------------------------------
# The interface
# ---------------------------------------------------------------------------

class NumogramInterface:
    def __init__(self, dynamics: D.Contract, l_max: int = L_MAX_DEFAULT, clock: str = CLOCK_EPISODE):
        if clock not in (CLOCK_EPISODE, CLOCK_GLOBAL):
            raise ValueError("clock must be 'episode' or 'global'")
        if l_max < 1:
            raise ValueError("l_max must be at least 1")
        self.dynamics = dynamics
        self.n = dynamics.graph.n
        self.l_max = l_max
        self.clock = clock
        self.closed = dynamics.terminal        # structural, never time-dependent
        self._class_of = {z: c for c in self.closed for z in c}
        self._global_t = 0

    def declaration(self) -> Dict[str, object]:
        return {
            "interface_version": INTERFACE_VERSION,
            "dynamics_contract": self.dynamics.contract_hash(),
            "ingress": "iota_n(u) = min(n - 1, floor(n * u)), u in [0, 1]",
            "episode_rule": "end at the first step after which the walker is in a terminal SCC of "
                            "the structural graph; at least one move attempted; holds when no edge "
                            "is permitted; cap l_max",
            "l_max": self.l_max, "clock": self.clock,
            "packet_schema": list(PACKET_FIELDS),
        }

    def interface_hash(self) -> str:
        return D._sha(self.declaration())

    # -- iota, episode, epsilon ------------------------------------------------------
    def iota(self, u: float) -> int:
        if not 0.0 <= u <= 1.0:
            raise ValueError("embodiment output u=%r outside [0, 1]" % (u,))
        return min(self.n - 1, int(self.n * u))

    def episode(self, z0: int, rng: random.Random) -> RawEpisodeRecord:
        state = D.State(z0, None)
        t0 = self._global_t if self.clock == CLOCK_GLOBAL else 0
        steps = []
        truncated = True
        for k in range(self.l_max):
            if not self.dynamics.edges[state.zone]:     # structural sink: nothing can happen
                truncated = False
                break
            e, state = self.dynamics.step(state, t0 + k, rng)
            if e is None:
                steps.append((k, state.zone, D.HOLD, D.HOLD, state.zone))
                continue
            steps.append((k, e.src, e.type, e.label, e.dst))
            if state.zone in self._class_of:
                truncated = False
                break
        if self.clock == CLOCK_GLOBAL:
            self._global_t += len(steps)
        cls = self._class_of.get(state.zone)
        return RawEpisodeRecord(graph_digest=self.dynamics.graph.digest(), n=self.n, entry=z0,
                                exit=state.zone, exit_class=tuple(sorted(cls)) if cls else None,
                                steps=tuple(steps), truncated=truncated)

    def epsilon(self, raw: RawEpisodeRecord) -> ObservationPacket:
        return make_packet(raw, self.l_max)

    def transact(self, u: float, rng: random.Random) -> Tuple[RawEpisodeRecord, ObservationPacket]:
        raw = self.episode(self.iota(u), rng)
        return raw, self.epsilon(raw)


def episode_rng(seed: int, index: int) -> random.Random:
    h = hashlib.sha256(("%d:%d" % (seed, index)).encode()).hexdigest()
    return random.Random(int(h[:16], 16))


def run_transactions(embodiment: Embodiment, interface: NumogramInterface,
                     n: int, seed: int) -> TransactionLog:
    """E_t -> iota -> episode -> epsilon -> E_{t+1}, n times. The embodiment sees packets only."""
    txs = []
    for k in range(n):
        before = embodiment.state_digest()
        u = embodiment.observe()
        raw, packet = interface.transact(u, episode_rng(seed, k))
        embodiment.update(packet)
        txs.append(Transaction(index=k, u=u, embodiment_digest_before=before, raw=raw, packet=packet))
    return TransactionLog(interface_hash=interface.interface_hash(), embodiment=embodiment.name,
                          seed=seed, transactions=tuple(txs))


def interfaces_for(graph: Optional[D.TypedGraph] = None, gt00: str = D.GT00_INCLUDE
                   ) -> Dict[str, NumogramInterface]:
    """One sealed interface per pre-registered law on the given graph (canonical by default)."""
    return {k: NumogramInterface(c) for k, c in D.registry(gt00, graph=graph).items()}


def primary_interfaces(gt00: str = D.GT00_INCLUDE) -> Dict[str, NumogramInterface]:
    return interfaces_for(None, gt00)


if __name__ == "__main__":
    print(INTERFACE_VERSION, "on", D.DYNAMICS_VERSION, "/", C.SPEC_VERSION)
    for k, itf in primary_interfaces().items():
        log = run_transactions(NullEmbodiment(seed=1), itf, n=2000, seed=11)
        exits: Dict[float, int] = {}
        for p in log.packets():
            exits[round(p.exit_position, 3)] = exits.get(round(p.exit_position, 3), 0) + 1
        mean_len = sum(t.raw.length for t in log.transactions) / len(log.transactions)
        print("%-4s hash %s  terminal %s  mean length %.1f  truncated %.4f  exit positions %s"
              % (k, itf.interface_hash()[:12], [sorted(c) for c in itf.closed], mean_len,
                 log.truncation_rate(), dict(sorted(exits.items()))))
