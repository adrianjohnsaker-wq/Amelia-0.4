"""P3.7 tensor Numogram substrate.

P3.6 was the first runtime to import Torch and commit seeded transitions.
P3.6.1 fixed unconditional reinitialization and uncaught facade exceptions.

P3.7 adds a sealed, non-mutating matched-condition fork: FULL,
ABLATED_TRANSITION, ABLATED_MAGNETISM, ABLATED_BOTH, and NEUTRAL_RESET,
run from one captured pre-state, none of them touching the live system.

Two channels carry state across committed transitions here:
transition_tensor (updated by update_transition_tensor) and zone_magnetism
(updated by update_zone_magnetism). zone_tensors never changes after
construction, so it is not part of what any of these conditions vary.

Condition definitions:
  FULL                predicts using the LIVE transition_tensor and LIVE
                       zone_magnetism -- i.e. exactly what a real transition
                       would use right now.
  ABLATED_TRANSITION  predicts using the CONSTRUCTION-TIME (unlearned)
                       transition_tensor, but the LIVE zone_magnetism.
                       Isolates transition_tensor's learned contribution.
  ABLATED_MAGNETISM   predicts using the LIVE transition_tensor, but the
                       CONSTRUCTION-TIME (unlearned) zone_magnetism.
                       Isolates zone_magnetism's learned contribution.
  ABLATED_BOTH        predicts using CONSTRUCTION-TIME values for both.
                       Matches the single combined "memory channel" P2
                       used; kept as the bridge to that precedent and as a
                       built-in consistency check against NEUTRAL_RESET.
  NEUTRAL_RESET        predicts using a freshly constructed system with the
                       same seed and dimension -- "begin from the neutral
                       field" per the original P1 definition.

A note on what that consistency check actually means here, precisely:
since zone_tensors is immutable after construction and there is no OTHER
per-instance state besides the two channels above, ABLATED_BOTH and
NEUTRAL_RESET are mathematically forced to compute the identical
PROBABILITY DISTRIBUTION -- same T0, same M0, same zone_tensors, same
origin/context. That equality is checked directly and does hold. Their
SAMPLED destinations are a different matter: each branch draws from its
own independently-derived generator (see _branch_seed below), precisely
so no branch's outcome can be inferred from another's, so two independent
draws from an identical distribution landing on different zones is
expected, not a bug -- the invariant check below compares probabilities
only, not the sampled `to` value, and an earlier draft of this file that
compared both was caught failing exactly this way before being fixed.

Non-mutation, made explicit rather than assumed: predict_transitions no
longer mutates self._last_fallback_triggered (it returns the fallback flag
instead), and every fork branch samples using its OWN generator, derived
deterministically from the capsule digest -- never self._torch_generator.
Reusing the live generator for a "read-only" branch would silently advance
its internal stream, which would be a real mutation (it would change what
every subsequent COMMITTED transition draws) even though transition_tensor,
zone_magnetism, evolution_step, and transition_history stayed untouched.
The capsule result reports a generator-fingerprint comparison so this
invariant is checked on every run, not just asserted in a comment.

Persistence remains off unless a later, separate stage enables it.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
from typing import Any, Dict, List, Optional, Sequence, Tuple

try:
    import torch
except ImportError:  # P3.5A deliberately reaches this condition only if imported.
    torch = None


ZONE_COUNT = 10


class MinimalBaseNumogram:
    """Minimal non-persistent base topology used by the tensor layer."""

    TRANSITION_MATRIX = tuple(
        tuple(1.0 if destination in ((source + 1) % ZONE_COUNT, ZONE_COUNT - 1 - source) else 0.08
              for destination in range(ZONE_COUNT))
        for source in range(ZONE_COUNT)
    )
    ZONE_DATA = {
        index: {"zone": index, "syzygy": ZONE_COUNT - 1 - index}
        for index in range(ZONE_COUNT)
    }

    def __init__(self, storage_dir: Optional[str] = None, enable_persistence: bool = False):
        self.storage_dir = storage_dir
        self.enable_persistence = bool(enable_persistence)
        self.user_memory: Dict[str, Any] = {}

    def save_user_memory(self) -> bool:
        if not self.enable_persistence or not self.storage_dir:
            return False
        import os

        os.makedirs(self.storage_dir, exist_ok=True)
        path = os.path.join(self.storage_dir, "numogram_user_memory.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(self.user_memory, handle, ensure_ascii=False, sort_keys=True)
        return True


def _generator_fingerprint(generator) -> str:
    """SHA-256 over a generator's current internal state, without drawing
    from it. Works against both real torch.Generator (get_state() returns
    a ByteTensor) and the shim's Generator (same shape, loosely)."""
    state_tensor = generator.get_state()
    raw_bytes = bytes(int(v) for v in state_tensor.tolist())
    return hashlib.sha256(raw_bytes).hexdigest()


class TensorBasedNumogramSystem:
    """A ten-zone tensor system with isolated Python and Torch random streams."""

    def __init__(
        self,
        base: Optional[MinimalBaseNumogram] = None,
        dimension: int = 3,
        learning_rate: float = 0.01,
        seed: int = 0,
        storage_dir: Optional[str] = None,
        enable_persistence: bool = False,
    ):
        if torch is None:
            raise RuntimeError("Torch is required to initialize TensorBasedNumogramSystem")
        if int(dimension) < 2:
            raise ValueError("dimension must be at least 2")
        self.base = base or MinimalBaseNumogram(storage_dir, enable_persistence)
        self.dimension = int(dimension)
        self.learning_rate = float(learning_rate)
        self.seed = int(seed)
        self._rng = random.Random(self.seed)
        self._torch_generator = torch.Generator()
        self._torch_generator.manual_seed(self.seed)
        self.zone_tensors = torch.rand(
            (ZONE_COUNT, self.dimension, self.dimension),
            generator=self._torch_generator,
            dtype=torch.float32,
        )
        self.transition_tensor = torch.tensor(
            self.base.TRANSITION_MATRIX,
            dtype=torch.float32,
        )
        self.zone_magnetism = self._initial_magnetism()

        # P3.7: retained baselines. These are never mutated after
        # construction -- they exist so ABLATED_* branches have something
        # concrete to fall back to, distinct from "zero".
        self._initial_transition_tensor = self.transition_tensor.clone()
        self._initial_zone_magnetism = self.zone_magnetism.clone()

        self.hyperedges = self._build_hyperedges()
        self.transition_history: List[Dict[str, Any]] = []
        self.evolution_step = 0
        self.stability_threshold = 0.01
        self._last_fallback_triggered = False

    def _initial_magnetism(self):
        rows = []
        for origin in range(ZONE_COUNT):
            row = []
            for destination in range(ZONE_COUNT):
                if (origin + destination) % 9 == 0:
                    row.append(0.2)
                elif origin == destination:
                    row.append(0.0)
                else:
                    row.append(self._rng.uniform(-0.2, 0.2))
            rows.append(row)
        return torch.tensor(rows, dtype=torch.float32)

    @staticmethod
    def _build_hyperedges():
        return [
            {"name": "Unity", "zones": (0, 1, 2)},
            {"name": "Division", "zones": (3, 4, 5)},
            {"name": "Synthesis", "zones": (6, 7, 8)},
            {"name": "Structure", "zones": (1, 4, 7)},
            {"name": "Transformation", "zones": (2, 5, 8)},
            {"name": "Diagonal", "zones": (0, 4, 9)},
            {"name": "Oscillator", "zones": (1, 6, 8)},
            {"name": "Resonator", "zones": (2, 7, 9)},
            {"name": "Horizontal", "zones": (3, 5, 7)},
        ]

    def _require_zone(self, zone: int) -> int:
        value = int(zone)
        if value < 0 or value >= ZONE_COUNT:
            raise ValueError("zone must be between 0 and 9")
        return value

    def _context_bias(self, context_data: Optional[Dict[str, Any]]):
        bias = torch.zeros(ZONE_COUNT, dtype=torch.float32)
        if not isinstance(context_data, dict):
            return bias
        supplied = context_data.get("zone_bias")
        if isinstance(supplied, Sequence) and not isinstance(supplied, (str, bytes)):
            for index, value in enumerate(supplied[:ZONE_COUNT]):
                try:
                    bias[index] = float(value)
                except (TypeError, ValueError):
                    continue
        return bias

    def predict_transitions(
        self,
        current_zone: int,
        context_data: Optional[Dict[str, Any]] = None,
        transition_tensor_override=None,
        zone_magnetism_override=None,
    ) -> Tuple[Any, bool]:
        """Pure with respect to instance state: returns (probabilities,
        fallback_triggered) rather than mutating self._last_fallback_triggered,
        so fork branches can call this freely without leaving a trace on the
        live instance. transition() is the one caller that still wants the
        old side-effecting behaviour; it now sets the attribute itself from
        the returned value, immediately below."""
        origin = self._require_zone(current_zone)
        tensor_strength = self.zone_tensors[origin].mean(dim=0).mean()

        active_transition_tensor = (
            transition_tensor_override if transition_tensor_override is not None else self.transition_tensor
        )
        active_zone_magnetism = (
            zone_magnetism_override if zone_magnetism_override is not None else self.zone_magnetism
        )

        scores = active_transition_tensor[origin].clone()
        scores = scores + active_zone_magnetism[origin] + tensor_strength
        scores = scores + self._context_bias(context_data)
        scores = torch.clamp(scores, min=0.0)
        total = float(scores.sum().item())
        if total <= 0.0 or not math.isfinite(total):
            return torch.full((ZONE_COUNT,), 1.0 / ZONE_COUNT, dtype=torch.float32), True
        return scores / scores.sum(), False

    def update_transition_tensor(self, current_zone: int, next_zone: int, intensity: float = 1.0):
        origin = self._require_zone(current_zone)
        destination = self._require_zone(next_zone)
        adjustment = max(-1.0, min(1.0, float(intensity))) * self.learning_rate
        self.transition_tensor[origin, destination] = torch.clamp(
            self.transition_tensor[origin, destination] + adjustment,
            min=0.0,
            max=1.0,
        )
        row_total = self.transition_tensor[origin].sum()
        if float(row_total.item()) > 0.0:
            self.transition_tensor[origin] = self.transition_tensor[origin] / row_total

    def update_zone_magnetism(self, current_zone: int, next_zone: int):
        origin = self._require_zone(current_zone)
        destination = self._require_zone(next_zone)
        self.zone_magnetism[origin, destination] = torch.clamp(
            self.zone_magnetism[origin, destination] + self.learning_rate,
            min=-1.0,
            max=1.0,
        )

    def activate_hyperedge(self, name: str, strength: float = 1.0):
        matching = [edge for edge in self.hyperedges if edge["name"] == name]
        if not matching:
            raise ValueError("unknown hyperedge")
        edge = matching[0]
        value = float(strength) * self.learning_rate
        for origin in edge["zones"]:
            for destination in edge["zones"]:
                if origin != destination:
                    self.zone_magnetism[origin, destination] = torch.clamp(
                        self.zone_magnetism[origin, destination] + value,
                        min=-1.0,
                        max=1.0,
                    )
        return {"name": edge["name"], "zones": list(edge["zones"])}

    def calculate_zone_distance(self, zone_a: int, zone_b: int) -> float:
        a = self._require_zone(zone_a)
        b = self._require_zone(zone_b)
        return float(torch.norm(self.zone_tensors[a] - self.zone_tensors[b]).item())

    def transition(self, current_zone: int, context_data: Optional[Dict[str, Any]] = None):
        origin = self._require_zone(current_zone)
        probabilities, fallback = self.predict_transitions(origin, context_data)
        self._last_fallback_triggered = fallback
        destination = int(torch.multinomial(probabilities, 1, generator=self._torch_generator).item())
        self.update_transition_tensor(origin, destination)
        self.update_zone_magnetism(origin, destination)
        self.evolution_step += 1
        event = {
            "step": self.evolution_step,
            "from": origin,
            "to": destination,
            "fallback": self._last_fallback_triggered,
            "probabilities": [round(float(value), 8) for value in probabilities.tolist()],
        }
        self.transition_history.append(event)
        return event

    def run_fork_branch(
        self,
        branch_name: str,
        current_zone: int,
        context_data: Optional[Dict[str, Any]],
        transition_tensor_override,
        zone_magnetism_override,
        generator,
    ) -> Dict[str, Any]:
        """The core non-mutating assay primitive. Touches nothing on self
        except reading zone_tensors/transition_tensor/zone_magnetism
        (whichever override wasn't supplied falls back to reading, never
        writing, the live values) -- no update_*, no evolution_step, no
        transition_history, no self._last_fallback_triggered, and no
        self._torch_generator. `generator` is supplied by the caller,
        already seeded independently per branch."""
        origin = self._require_zone(current_zone)
        probabilities, fallback = self.predict_transitions(
            origin,
            context_data,
            transition_tensor_override=transition_tensor_override,
            zone_magnetism_override=zone_magnetism_override,
        )
        destination = int(torch.multinomial(probabilities, 1, generator=generator).item())
        return {
            "branch": branch_name,
            "from": origin,
            "to": destination,
            "fallback": fallback,
            "probabilities": [round(float(value), 8) for value in probabilities.tolist()],
        }

    def status(self):
        return {
            "schema": "amelia-tensor-numogram-status-v1",
            "zones": ZONE_COUNT,
            "dimension": self.dimension,
            "learning_rate": self.learning_rate,
            "seed": self.seed,
            "evolution_step": self.evolution_step,
            "stability_threshold": self.stability_threshold,
            "transition_history": len(self.transition_history),
            "last_fallback_triggered": self._last_fallback_triggered,
            "persistence_enabled": self.base.enable_persistence,
        }


_SYSTEM: Optional[TensorBasedNumogramSystem] = None
_INIT_DIGEST: Optional[str] = None
_LAST_FORK: Optional[Dict[str, Any]] = None

_FORK_BRANCHES = ("FULL", "ABLATED_TRANSITION", "ABLATED_MAGNETISM", "ABLATED_BOTH", "NEUTRAL_RESET")


def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest_of(value) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _config_digest(seed: int, dimension: int) -> str:
    payload = json.dumps({"seed": int(seed), "dimension": int(dimension)}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _branch_seed(capsule_digest: str, branch_name: str) -> int:
    digest_hex = hashlib.sha256(f"{capsule_digest}:{branch_name}".encode("utf-8")).hexdigest()
    return int(digest_hex[:8], 16)


def get_runtime_info():
    if torch is None:
        return _canonical(
            {
                "schema": "amelia-p3.6-torch-runtime-v1",
                "status": "torch_unavailable",
                "torch_version": None,
                "zone_count": ZONE_COUNT,
                "persistence_default": False,
            }
        )
    return _canonical(
        {
            "schema": "amelia-p3.6-torch-runtime-v1",
            "status": "torch_ready",
            "torch_version": str(torch.__version__),
            "zone_count": ZONE_COUNT,
            "persistence_default": False,
        }
    )


def initialize_system(seed: int = 0, dimension: int = 3):
    global _SYSTEM, _INIT_DIGEST
    try:
        seed = int(seed)
        dimension = int(dimension)
        attempted_digest = _config_digest(seed, dimension)

        if _SYSTEM is not None:
            if attempted_digest == _INIT_DIGEST:
                return _canonical({
                    "status": "already_initialized",
                    "init_digest": _INIT_DIGEST,
                    "attempted_init_digest": attempted_digest,
                    "state_unchanged": True,
                    "system": _SYSTEM.status(),
                })
            return _canonical({
                "status": "error",
                "error_type": "ConfigMismatch",
                "message": "system already initialized with a different (seed, dimension)",
                "init_digest": _INIT_DIGEST,
                "attempted_init_digest": attempted_digest,
            })

        system = TensorBasedNumogramSystem(seed=seed, dimension=dimension)
        _SYSTEM = system
        _INIT_DIGEST = attempted_digest
        return _canonical({"status": "initialized", "init_digest": _INIT_DIGEST, "system": _SYSTEM.status()})
    except Exception as error:
        return _canonical({"status": "error", "error_type": type(error).__name__, "message": str(error)})


def get_status():
    if _SYSTEM is None:
        return _canonical({"status": "uninitialized"})
    return _canonical({"status": "ready", "init_digest": _INIT_DIGEST, "system": _SYSTEM.status()})


def transition(current_zone: int, context_json: str = "{}"):
    try:
        if _SYSTEM is None:
            return _canonical({
                "status": "error", "error_type": "RuntimeError",
                "message": "initialize_system must be called before transition",
            })
        try:
            context = json.loads(context_json) if context_json else {}
        except Exception:
            return _canonical({"status": "error", "error_type": "ValueError", "message": "context_json must be a JSON object"})
        if not isinstance(context, dict):
            return _canonical({"status": "error", "error_type": "ValueError", "message": "context_json must encode a JSON object"})
        event = _SYSTEM.transition(current_zone, context)
        return _canonical({"status": "transitioned", "event": event, "system": _SYSTEM.status()})
    except Exception as error:
        return _canonical({"status": "error", "error_type": type(error).__name__, "message": str(error)})


def _run_fork_branches(
    system: TensorBasedNumogramSystem,
    origin: int,
    context: Dict[str, Any],
    capsule_digest: str,
    t_live,
    m_live,
    t0,
    m0,
) -> Dict[str, Dict[str, Any]]:
    """Runs the four in-instance branches (everything except NEUTRAL_RESET,
    which needs its own throwaway system) and returns them keyed by name.

    t_live/m_live and t0/m0 are ALWAYS supplied explicitly by the caller --
    there is deliberately no "None means fall back to system's own current
    live values" behaviour here. At seal time (run_fork) t_live/m_live are
    the just-captured snapshot of system's own state, so that fallback
    would happen to be correct; at replay time (verify_last_fork) system is
    a fresh throwaway instance whose OWN live values are just its baseline,
    not the capsule's recorded snapshot, so that same fallback would be
    silently wrong for any capsule sealed after evolution_step 0. Threading
    both explicitly through one shared function removes that failure mode
    instead of relying on every call site remembering to override it."""
    results = {}

    full_generator = torch.Generator()
    full_generator.manual_seed(_branch_seed(capsule_digest, "FULL"))
    results["FULL"] = system.run_fork_branch("FULL", origin, context, t_live, m_live, full_generator)

    ablated_transition_generator = torch.Generator()
    ablated_transition_generator.manual_seed(_branch_seed(capsule_digest, "ABLATED_TRANSITION"))
    results["ABLATED_TRANSITION"] = system.run_fork_branch(
        "ABLATED_TRANSITION", origin, context, t0, m_live, ablated_transition_generator
    )

    ablated_magnetism_generator = torch.Generator()
    ablated_magnetism_generator.manual_seed(_branch_seed(capsule_digest, "ABLATED_MAGNETISM"))
    results["ABLATED_MAGNETISM"] = system.run_fork_branch(
        "ABLATED_MAGNETISM", origin, context, t_live, m0, ablated_magnetism_generator
    )

    ablated_both_generator = torch.Generator()
    ablated_both_generator.manual_seed(_branch_seed(capsule_digest, "ABLATED_BOTH"))
    results["ABLATED_BOTH"] = system.run_fork_branch(
        "ABLATED_BOTH", origin, context, t0, m0, ablated_both_generator
    )

    return results


def run_fork(current_zone: int, context_json: str = "{}"):
    """Seals the current (transition_tensor, zone_magnetism) pair plus the
    origin and context, then runs all five conditions against that sealed
    capsule. Nothing here mutates _SYSTEM: no update_transition_tensor, no
    update_zone_magnetism, no evolution_step, no transition_history, no
    self._torch_generator draw. Verified below, not just asserted."""
    global _LAST_FORK
    try:
        if _SYSTEM is None:
            return _canonical({"status": "error", "error_type": "RuntimeError", "message": "initialize_system must be called before run_fork"})

        try:
            context = json.loads(context_json) if context_json else {}
        except Exception:
            return _canonical({"status": "error", "error_type": "ValueError", "message": "context_json must be a JSON object"})
        if not isinstance(context, dict):
            return _canonical({"status": "error", "error_type": "ValueError", "message": "context_json must encode a JSON object"})

        origin = _SYSTEM._require_zone(current_zone)

        # Snapshot BEFORE any branch runs. These are what get sealed into
        # the capsule and what the post-run comparison checks against.
        pre_transition_tensor = _SYSTEM.transition_tensor.clone()
        pre_zone_magnetism = _SYSTEM.zone_magnetism.clone()
        pre_evolution_step = _SYSTEM.evolution_step
        pre_history_len = len(_SYSTEM.transition_history)
        pre_generator_fingerprint = _generator_fingerprint(_SYSTEM._torch_generator)

        t0 = _SYSTEM._initial_transition_tensor
        m0 = _SYSTEM._initial_zone_magnetism

        capsule_payload = {
            "seed": _SYSTEM.seed,
            "dimension": _SYSTEM.dimension,
            "origin": origin,
            "context": context,
            "transition_tensor": pre_transition_tensor.tolist(),
            "zone_magnetism": pre_zone_magnetism.tolist(),
            "evolution_step": pre_evolution_step,
            "transition_history_len": pre_history_len,
        }
        capsule_digest = _digest_of(capsule_payload)

        branch_results = _run_fork_branches(
            _SYSTEM, origin, context, capsule_digest,
            pre_transition_tensor, pre_zone_magnetism, t0, m0,
        )

        # NEUTRAL_RESET: a throwaway instance, same seed/dimension. Never
        # touches _SYSTEM at all; discarded once this call returns.
        neutral_system = TensorBasedNumogramSystem(seed=_SYSTEM.seed, dimension=_SYSTEM.dimension)
        neutral_generator = torch.Generator()
        neutral_generator.manual_seed(_branch_seed(capsule_digest, "NEUTRAL_RESET"))
        branch_results["NEUTRAL_RESET"] = neutral_system.run_fork_branch(
            "NEUTRAL_RESET", origin, context, None, None, neutral_generator
        )

        # Post-run invariant checks -- computed, not assumed.
        post_transition_tensor = _SYSTEM.transition_tensor
        post_zone_magnetism = _SYSTEM.zone_magnetism
        post_generator_fingerprint = _generator_fingerprint(_SYSTEM._torch_generator)

        live_state_unchanged = (
            post_transition_tensor.tolist() == pre_transition_tensor.tolist()
            and post_zone_magnetism.tolist() == pre_zone_magnetism.tolist()
            and _SYSTEM.evolution_step == pre_evolution_step
            and len(_SYSTEM.transition_history) == pre_history_len
        )
        generator_state_unchanged = post_generator_fingerprint == pre_generator_fingerprint

        # Deliberately compares probabilities only, not `to`. ABLATED_BOTH
        # and NEUTRAL_RESET are mathematically forced to compute the exact
        # same probability DISTRIBUTION (same T0, same M0, same immutable
        # zone_tensors, same origin/context) -- confirmed empirically here,
        # not just claimed. But each branch samples from that distribution
        # using its own independently-derived generator, precisely so that
        # one branch's draw can never be inferred from another's; two
        # independent draws from an identical distribution are not
        # expected to land on the same zone, and requiring that would be
        # checking the wrong thing.
        ablated_both_matches_neutral_reset = (
            branch_results["ABLATED_BOTH"]["probabilities"] == branch_results["NEUTRAL_RESET"]["probabilities"]
        )

        capsule = {
            "status": "forked",
            "capsule_digest": capsule_digest,
            "seed": _SYSTEM.seed,
            "dimension": _SYSTEM.dimension,
            "origin": origin,
            "context": context,
            "pre_transition_tensor": capsule_payload["transition_tensor"],
            "pre_zone_magnetism": capsule_payload["zone_magnetism"],
            "pre_evolution_step": pre_evolution_step,
            "pre_history_len": pre_history_len,
            "branches": branch_results,
            "invariants": {
                "live_state_unchanged": live_state_unchanged,
                "generator_state_unchanged": generator_state_unchanged,
                "ablated_both_matches_neutral_reset": ablated_both_matches_neutral_reset,
            },
        }

        _LAST_FORK = capsule
        return _canonical(capsule)
    except Exception as error:
        return _canonical({"status": "error", "error_type": type(error).__name__, "message": str(error)})


def verify_last_fork():
    """Re-derives the branches from the last sealed capsule's recorded
    pre-state and confirms they match exactly -- a separate call, so this
    checks replay across time, not just internal consistency at seal time."""
    try:
        if _LAST_FORK is None:
            return _canonical({"status": "error", "error_type": "RuntimeError", "message": "run_fork must be called before verify_last_fork"})
        if torch is None:
            return _canonical({"status": "error", "error_type": "RuntimeError", "message": "Torch is required to verify a fork"})

        capsule = _LAST_FORK
        seed = capsule["seed"]
        dimension = capsule["dimension"]
        origin = capsule["origin"]
        context = capsule["context"]
        capsule_digest = capsule["capsule_digest"]

        pre_transition_tensor = torch.tensor(capsule["pre_transition_tensor"], dtype=torch.float32)
        pre_zone_magnetism = torch.tensor(capsule["pre_zone_magnetism"], dtype=torch.float32)

        # A throwaway system purely to supply zone_tensors (immutable, seed-
        # derived) and the run_fork_branch method; its own transition_tensor/
        # zone_magnetism are ignored in favour of the capsule's recorded
        # pre-state for the FULL/ABLATED_* branches below.
        replay_system = TensorBasedNumogramSystem(seed=seed, dimension=dimension)
        t0 = replay_system._initial_transition_tensor
        m0 = replay_system._initial_zone_magnetism

        # t_live/m_live here are the CAPSULE's recorded snapshot (correct
        # for any evolution_step the capsule was sealed at); t0/m0 are
        # replay_system's own construction-time baseline, which by
        # determinism must equal the original system's baseline for the
        # same seed regardless of how many transitions it had committed
        # before sealing. One call, no per-branch overwrite needed.
        replayed = _run_fork_branches(
            replay_system, origin, context, capsule_digest,
            pre_transition_tensor, pre_zone_magnetism, t0, m0,
        )

        neutral_system = TensorBasedNumogramSystem(seed=seed, dimension=dimension)
        neutral_generator = torch.Generator()
        neutral_generator.manual_seed(_branch_seed(capsule_digest, "NEUTRAL_RESET"))
        replayed["NEUTRAL_RESET"] = neutral_system.run_fork_branch(
            "NEUTRAL_RESET", origin, context, None, None, neutral_generator
        )

        mismatches = []
        for branch in _FORK_BRANCHES:
            original = capsule["branches"].get(branch)
            reproduced = replayed.get(branch)
            if original is None or reproduced is None:
                mismatches.append(branch)
                continue
            if original["to"] != reproduced["to"] or original["probabilities"] != reproduced["probabilities"]:
                mismatches.append(branch)

        return _canonical({
            "status": "verified" if not mismatches else "mismatch",
            "capsule_digest": capsule_digest,
            "branches_checked": list(_FORK_BRANCHES),
            "mismatched_branches": mismatches,
        })
    except Exception as error:
        return _canonical({"status": "error", "error_type": type(error).__name__, "message": str(error)})
