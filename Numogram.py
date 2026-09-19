"""Deferred P3.6 tensor Numogram substrate.

P3.5A packages and syntax-checks this module without importing it: the P3.5A
probe intentionally carries no Torch dependency.  When P3.6 installs the
declared Android Torch wheel, this module provides a deterministic, explicitly
seeded Numogram system for initialize -> status -> transition testing.
"""
from __future__ import annotations

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
        self._torch_generator = torch.Generator(device="cpu")
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


def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def initialize_system(seed: int = 0, dimension: int = 3):
    global _SYSTEM
    _SYSTEM = TensorBasedNumogramSystem(seed=int(seed), dimension=int(dimension))
    return _canonical({"status": "initialized", "system": _SYSTEM.status()})


def get_status():
    if _SYSTEM is None:
        return _canonical({"status": "uninitialized"})
    return _canonical({"status": "ready", "system": _SYSTEM.status()})


def transition(current_zone: int, context_json: str = "{}"):
    if _SYSTEM is None:
        raise RuntimeError("initialize_system must be called before transition")
    try:
        context = json.loads(context_json) if context_json else {}
    except Exception as error:
        raise ValueError("context_json must be a JSON object") from error
    if not isinstance(context, dict):
        raise ValueError("context_json must encode a JSON object")
    return _canonical({"status": "transitioned", "event": _SYSTEM.transition(current_zone, context), "system": _SYSTEM.status()})
