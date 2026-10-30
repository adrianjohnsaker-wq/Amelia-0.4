"""Bounded experimental Warp developmental sedimentation operator for P3.18.

This is not a canonical Amelia modification. It changes only PFM inscription for
a limited number of developmental events touching Warp zones {3,6}. It does not
change topology, gate selection, phase velocity, tick count, or dwell rules.
"""
from __future__ import annotations

from typing import Dict, object as _object  # type: ignore

from DynamicNumogram import IntegratedMemorySystem


class WarpDevelopmentMemory(IntegratedMemorySystem):
    def __init__(self, gain: float = 1.5, event_budget: int = 8) -> None:
        super().__init__()
        self.warp_gain = float(gain)
        self.warp_event_budget = int(event_budget)
        self.warp_gain_used = 0
        self.warp_gain_enabled = True
        self.warp_gain_log = []

    def append(self, event: Dict[str, object]) -> None:
        transformed = dict(event)
        source = int(transformed.get("fromZone", transformed.get("targetZone", -1)))
        target = int(transformed.get("targetZone", -1))
        touches_warp = source in (3, 6) or target in (3, 6)

        applied = False
        original_flux = float(transformed.get("fluxDelta", 0.0))
        if (
            self.warp_gain_enabled
            and touches_warp
            and self.warp_gain_used < self.warp_event_budget
        ):
            transformed["fluxDelta"] = min(0.18, original_flux * self.warp_gain)
            self.warp_gain_used += 1
            applied = True

        self.warp_gain_log.append({
            "blockIndex": int(transformed.get("blockIndex", len(self.warp_gain_log) + 1)),
            "fromZone": source,
            "targetZone": target,
            "touchesWarp": touches_warp,
            "gainApplied": applied,
            "originalFluxDelta": original_flux,
            "storedFluxDelta": float(transformed.get("fluxDelta", 0.0)),
            "gainUseIndex": self.warp_gain_used if applied else None,
        })
        super().append(transformed)

    def disable_warp_gain(self) -> None:
        self.warp_gain_enabled = False


def install_warp_development_gain(process, gain: float = 1.5, event_budget: int = 8):
    memory = WarpDevelopmentMemory(gain=gain, event_budget=event_budget)
    process.memory = memory
    return process
