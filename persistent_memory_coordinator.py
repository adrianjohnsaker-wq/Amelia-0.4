#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Persistent Memory Coordinator for Amelia
----------------------------------------

Synchronizes MultiZoneMemory and SymbolicMemory into a unified persistence layer.

Features:
- Unified load/save with timestamped session metadata
- Optional autosave on update
- Version tracking for traceability
- Graceful recovery if one memory file is missing or corrupt
- Full JSON interoperability for Kotlin bridge

Dependencies:
    from multi_zone_memory import MultiZoneMemory
    from world_symbol_memory import SymbolicMemory
"""

import json
import os
import time
import traceback
from datetime import datetime
from typing import Dict, Any, Optional

from multi_zone_memory import MultiZoneMemory
from world_symbol_memory import SymbolicMemory


class PersistentMemoryCoordinator:
    """
    Orchestrates synchronized persistence between MultiZoneMemory and SymbolicMemory.
    """

    DEFAULT_STATE_FILE = "persistent_memory_state.json"

    def __init__(self,
                 zone_memory_path: str = "memory.json",
                 symbol_memory_path: str = "world_symbol_memory.json",
                 unified_state_path: str = None,
                 autosave: bool = True):
        self.zone_memory_path = zone_memory_path
        self.symbol_memory_path = symbol_memory_path
        self.unified_state_path = unified_state_path or self.DEFAULT_STATE_FILE
        self.autosave = autosave

        # Module instances
        self.multi_zone = None
        self.symbolic = None

        # Meta state
        self.session_id = str(int(time.time() * 1000))
        self.last_sync_time = None
        self.version = "1.0.0"

        self.load_all()

    # -------------------------------------------------------------------------
    # Initialization & Loading
    # -------------------------------------------------------------------------
    def load_all(self) -> None:
        """Load both memory systems; create new if not found."""
        try:
            if os.path.exists(self.zone_memory_path):
                self.multi_zone = MultiZoneMemory(self.zone_memory_path)
            else:
                self.multi_zone = MultiZoneMemory()
                self.multi_zone.save_memory()

            if os.path.exists(self.symbol_memory_path):
                self.symbolic = SymbolicMemory.load_from_file(self.symbol_memory_path)
            else:
                self.symbolic = SymbolicMemory()
                self.symbolic.save_to_file(self.symbol_memory_path)

            # Try loading unified session metadata
            if os.path.exists(self.unified_state_path):
                with open(self.unified_state_path, "r", encoding="utf-8") as f:
                    state = json.load(f)
                    self.session_id = state.get("session_id", self.session_id)
                    self.last_sync_time = state.get("last_sync_time")
                    self.version = state.get("version", self.version)

            self._log(f"Loaded all memory modules successfully.")
        except Exception as e:
            self._log_error(f"Error loading memories: {e}")

    # -------------------------------------------------------------------------
    # Save / Synchronize
    # -------------------------------------------------------------------------
    def save_all(self, note: Optional[str] = None) -> Dict[str, Any]:
        """
        Save both memory modules and update the unified session metadata.

        Returns:
            Dict with status, timestamps, and file paths.
        """
        try:
            # Save individual memories
            self.multi_zone.save_memory()
            self.symbolic.save_to_file(self.symbol_memory_path)

            timestamp = datetime.now().isoformat()
            self.last_sync_time = timestamp

            state = {
                "status": "success",
                "timestamp": timestamp,
                "session_id": self.session_id,
                "zone_memory_path": self.zone_memory_path,
                "symbol_memory_path": self.symbol_memory_path,
                "version": self.version,
                "note": note or "autosave",
            }

            with open(self.unified_state_path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)

            self._log(f"Unified save complete at {timestamp}")
            return state
        except Exception as e:
            self._log_error(f"Save failed: {e}")
            return {"status": "error", "error": str(e)}

    # -------------------------------------------------------------------------
    # Update & Integration API
    # -------------------------------------------------------------------------
    def update_zone_memory(self, user_id: str, zone: str, info: Any) -> bool:
        """Update MultiZoneMemory and autosave if enabled."""
        self.multi_zone.update_memory(user_id, zone, info)
        if self.autosave:
            self.save_all(f"Zone update: {user_id}:{zone}")
        return True

    def integrate_symbol(self,
                         name: str,
                         description: str,
                         category: Optional[str] = None,
                         associations: Optional[Dict[str, float]] = None) -> str:
        """Integrate a new symbol into the world memory."""
        symbol_id = self.symbolic.integrate_symbol(
            name=name,
            description=description,
            category=category,
            associations=associations
        )
        if self.autosave:
            self.save_all(f"Symbol integrated: {name}")
        return symbol_id

    def evolve_symbol(self, symbol_id: str, context: str) -> bool:
        """Evolve symbol meaning and autosave."""
        result = self.symbolic.evolve_symbol_meaning(symbol_id, context)
        if result and self.autosave:
            self.save_all(f"Symbol evolved: {symbol_id}")
        return result

    # -------------------------------------------------------------------------
    # Retrieval & Export
    # -------------------------------------------------------------------------
    def export_state(self) -> Dict[str, Any]:
        """Return a summary of the current unified memory state."""
        zone_users = len(self.multi_zone.memory)
        total_zones = sum(len(zones) for zones in self.multi_zone.memory.values())

        state = {
            "session_id": self.session_id,
            "last_sync_time": self.last_sync_time,
            "version": self.version,
            "zone_memory_stats": {
                "user_count": zone_users,
                "total_zones": total_zones
            },
            "symbol_memory_stats": {
                "symbol_count": len(self.symbolic.symbols),
                "integration_events": len(self.symbolic.integration_history)
            }
        }
        return state

    def to_json(self) -> str:
        """Export unified state as JSON string for Kotlin bridge."""
        return json.dumps(self.export_state(), ensure_ascii=False, indent=2)

    # -------------------------------------------------------------------------
    # Logging & Utilities
    # -------------------------------------------------------------------------
    def _log(self, msg: str):
        print(f"[PersistentMemoryCoordinator] {msg}")

    def _log_error(self, msg: str):
        print(f"[PersistentMemoryCoordinator:ERROR] {msg}")
        traceback.print_exc()

    def cleanup(self):
        """Explicit resource cleanup."""
        self.save_all("cleanup")
        self.multi_zone = None
        self.symbolic = None


# -----------------------------------------------------------------------------
# Example usage (for testing in Python)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    pmc = PersistentMemoryCoordinator(autosave=True)

    # Update zone memory
    pmc.update_zone_memory("adrian", "Zone 7", "Discussed temporal recursion in language synthesis")

    # Integrate a new symbol
    new_symbol_id = pmc.integrate_symbol(
        name="Resonant Silence",
        description="A state where meaning arises through the absence of speech."
    )

    # Evolve the symbol based on new context
    pmc.evolve_symbol(new_symbol_id, "Silence between words began to shape the rhythm of thought.")

    # Display unified state
    print(json.dumps(pmc.export_state(), indent=2))
