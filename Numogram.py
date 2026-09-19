"""P3.6.1 tensor Numogram substrate.

P3.5A packaged and syntax-checked this module without importing it. P3.6
was the first runtime to import Torch, initialize the tensor field, and
commit one seeded transition -- confirmed on-device.

P3.6.1 is a hygiene revision to the module-level facade only. Nothing in
TensorBasedNumogramSystem or MinimalBaseNumogram changes.

Two fixes:

1. initialize_system() previously had no guard at all: every call
   unconditionally replaced _SYSTEM, silently discarding any accumulated
   evolution_step/transition_history from a prior process attachment.
   Python's module state is process-wide and can outlive the Activity that
   first created it, so a bare "require uninitialized" would only make the
   discarding visible, not prevent it. Instead: a second initialize_system
   call is checked against a canonical digest of (seed, dimension). If it
   matches what's already running, the call reattaches without touching
   _SYSTEM -- no reset, no data loss. If it doesn't match, the call is
   rejected outright and _SYSTEM is still left untouched. Either way,
   nothing is silently overwritten.

2. initialize_system() and transition() could previously raise uncaught
   across the Chaquopy boundary (get_status/get_runtime_info could not --
   nothing in them raises). Both now catch their own exceptions and return
   a structured {"status": "error", ...} string instead, matching
   get_status/get_runtime_info's existing behaviour. This also means a
   failure partway through a call sequence no longer discards whatever
   already succeeded before it, since the caller keeps getting a valid
   JSON string back at every step rather than an exception unwinding the
   whole sequence.

Persistence remains off unless a later, separate stage enables it.
"""
from __future__ import annotations

import hashlib
import json
import math
import random
from typing import Any, Dict, List, Optional, Sequence

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
        """Persistence is opt-in and remains disabled in the Android probe line."""
        if not self.enable_persistence or not self.storage_dir:
            return False
        import os

        os.makedirs(self.storage_dir, exist_ok=True)
        path = os.path.join(self.storage_dir, "numogram_user_memory.json")
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(self.user_memory, handle, ensure_ascii=False, sort_keys=True)
        return True


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
        # The default CPU generator is supported by the Android Torch 1.8.1
        # wheel and is deliberately independent of Python's random stream.
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

    def predict_transitions(self, current_zone: int, context_data: Optional[Dict[str, Any]] = None):
        origin = self._require_zone(current_zone)
        tensor_strength = self.zone_tensors[origin].mean(dim=0).mean()
        scores = self.transition_tensor[origin].clone()
        scores = scores + self.zone_magnetism[origin] + tensor_strength
        scores = scores + self._context_bias(context_data)
        scores = torch.clamp(scores, min=0.0)
        total = float(scores.sum().item())
        if total <= 0.0 or not math.isfinite(total):
            self._last_fallback_triggered = True
            return torch.full((ZONE_COUNT,), 1.0 / ZONE_COUNT, dtype=torch.float32)
        self._last_fallback_triggered = False
        return scores / scores.sum()

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
        probabilities = self.predict_transitions(origin, context_data)
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


def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _config_digest(seed: int, dimension: int) -> str:
    # Covers exactly the parameters initialize_system actually exposes.
    # If a future revision exposes learning_rate as a caller-supplied
    # parameter too, it needs to be folded into this payload, or a
    # reattachment could silently accept a configuration that differs in
    # a way this digest can't see.
    payload = json.dumps({"seed": int(seed), "dimension": int(dimension)}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def get_runtime_info():
    """Return the sealed, read-only Torch runtime identity for P3.6."""
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
    """
    Exact-once initialization with digest-matched reattachment.

    - No existing system: construct one, record its config digest.
    - Existing system, same (seed, dimension): reattach, state unchanged.
    - Existing system, different (seed, dimension): rejected, state
      unchanged -- this is what keeps it exact-once rather than a reset.
    """
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
                "status": "error",
                "error_type": "RuntimeError",
                "message": "initialize_system must be called before transition",
            })
        try:
            context = json.loads(context_json) if context_json else {}
        except Exception:
            return _canonical({
                "status": "error",
                "error_type": "ValueError",
                "message": "context_json must be a JSON object",
            })
        if not isinstance(context, dict):
            return _canonical({
                "status": "error",
                "error_type": "ValueError",
                "message": "context_json must encode a JSON object",
            })
        event = _SYSTEM.transition(current_zone, context)
        return _canonical({"status": "transitioned", "event": event, "system": _SYSTEM.status()})
    except Exception as error:
        return _canonical({"status": "error", "error_type": type(error).__name__, "message": str(error)})
