#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Morphogenetic Architecture - Complete Integration
-------------------------------------------------

PART 1: Morphogenetic Cell (Base Unit)
PART 2: Adaptive Network with Hebbian Learning
PART 3: Enhanced Persistent Memory Coordinator with Tissue Integration
"""

import json
import os
import time
import traceback
import random
import math
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from collections import deque

# ============================================================================
# PART 1: MORPHOGENETIC CELL
# ============================================================================

class MorphogeneticCell:
    """
    Semi-autonomous cell unit with local state, signaling, and adaptation.
    Each module in the system becomes a living cell in a distributed organism.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.state: Dict[str, Any] = {
            "potential": random.uniform(0.3, 0.7),  # Initial diversity
            "activation": 0.0,
            "history": []
        }
        self.links: List[str] = []  # neighbour names
        
    def signal(self) -> Dict[str, Any]:
        """Broadcast local state to neighbours."""
        return {
            "name": self.name,
            "potential": self.state["potential"],
            "activation": self.state.get("activation", 0.0)
        }
    
    def sense(self, inputs: List[Dict[str, Any]]):
        """Integrate weighted inputs from neighbours."""
        if not inputs:
            return
            
        # Weighted average of neighbour potentials
        avg_potential = sum(i.get("potential", 0.0) for i in inputs) / len(inputs)
        
        # Smooth integration (90% self, 10% neighbours)
        self.state["potential"] = 0.9 * self.state["potential"] + 0.1 * avg_potential
        
        # Track activation level
        self.state["activation"] = avg_potential
        
    def adapt(self):
        """Internal drift toward homeostatic equilibrium."""
        # Gentle drift toward 0.5 (stability attractor)
        target = 0.5
        drift = 0.05 * (target - self.state["potential"])
        self.state["potential"] += drift
        
        # Add small stochastic noise for exploration
        self.state["potential"] += random.gauss(0, 0.02)
        
        # Clamp to valid range
        self.state["potential"] = max(0.0, min(1.0, self.state["potential"]))
        
        # Maintain short history for diagnostics
        if "history" not in self.state:
            self.state["history"] = []
        self.state["history"].append(self.state["potential"])
        if len(self.state["history"]) > 10:
            self.state["history"].pop(0)


# ============================================================================
# PART 2: ADAPTIVE MORPHOGENETIC NETWORK
# ============================================================================

class AdaptiveMorphogeneticNetwork:
    """
    Self-organizing network with Hebbian learning and homeostatic pruning.
    Connections strengthen through co-activation, weak links decay.
    """
    
    def __init__(self):
        self.cells: Dict[str, MorphogeneticCell] = {}
        self.weights: Dict[Tuple[str, str], float] = {}  # (a,b) -> strength
        
        # Learning parameters
        self.learning_rate = 0.05      # Hebbian gain
        self.decay_rate = 0.01         # Connection decay per step
        self.min_weight = 0.02         # Pruning threshold
        self.max_weight = 1.0          # Saturation ceiling
        
        # Activity tracking
        self.activity_trace: Dict[str, float] = {}
        self.step_count = 0
        
    # ------------------------------------------------------------------------
    # Cell Management
    # ------------------------------------------------------------------------
    
    def add_cell(self, cell: MorphogeneticCell):
        """Register a new cell in the network."""
        self.cells[cell.name] = cell
        self.activity_trace[cell.name] = 0.0
        
    def connect(self, a: str, b: str, initial_weight: Optional[float] = None):
        """Create or reinforce bidirectional link between cells."""
        if a not in self.cells or b not in self.cells:
            return
            
        w = initial_weight if initial_weight is not None else random.uniform(0.2, 0.6)
        self.weights[(a, b)] = w
        self.weights[(b, a)] = w
        
    def get_neighbours(self, cell_name: str) -> List[str]:
        """Return list of connected neighbours."""
        return [b for (a, b) in self.weights.keys() if a == cell_name]
        
    # ------------------------------------------------------------------------
    # Adaptive Evolution Step
    # ------------------------------------------------------------------------
    
    def step(self) -> Dict[str, Dict[str, Any]]:
        """Execute one morphogenetic cycle with adaptation."""
        
        # 1️⃣ Gather current signals from all cells
        signals = {n: c.signal() for n, c in self.cells.items()}
        
        # 2️⃣ Deliver weighted neighbour inputs
        for name, cell in self.cells.items():
            neighbours = []
            for (a, b), w in self.weights.items():
                if a == name and b in signals:
                    inp = signals[b].copy()
                    inp["potential"] *= w  # Weight by connection strength
                    neighbours.append(inp)
            cell.sense(neighbours)
        
        # 3️⃣ Each cell adapts internally
        for cell in self.cells.values():
            cell.adapt()
        
        # 4️⃣ Update connection weights (Hebbian learning)
        self._hebbian_update(signals)
        
        # 5️⃣ Prune weak connections
        self._prune_connections()
        
        self.step_count += 1
        
        # 6️⃣ Return current tissue snapshot
        return {n: c.state for n, c in self.cells.items()}
    
    # ------------------------------------------------------------------------
    # Hebbian Learning Rule
    # ------------------------------------------------------------------------
    
    def _hebbian_update(self, signals: Dict[str, Dict[str, float]]):
        """
        Strengthen connections between co-active cells.
        Correlation-based learning: cells that fire together wire together.
        """
        for (a, b), w in list(self.weights.items()):
            pa = signals[a]["potential"]
            pb = signals[b]["potential"]
            
            # Correlation term (centered around 0.5)
            correlation = (pa - 0.5) * (pb - 0.5)
            delta = self.learning_rate * correlation
            
            # Weight update with decay toward minimum
            w_new = w + delta - self.decay_rate * (w - self.min_weight)
            
            # Clamp to valid range
            w_new = max(self.min_weight, min(self.max_weight, w_new))
            
            # Update both directions (symmetric)
            self.weights[(a, b)] = w_new
            self.weights[(b, a)] = w_new
            
    def _prune_connections(self):
        """Remove persistently weak links to maintain sparse topology."""
        threshold = self.min_weight + 1e-3
        to_remove = [
            (a, b) for (a, b), w in self.weights.items() 
            if w <= threshold
        ]
        
        for (a, b) in to_remove:
            self.weights.pop((a, b), None)
            self.weights.pop((b, a), None)
    
    # ------------------------------------------------------------------------
    # Diagnostics and State Export
    # ------------------------------------------------------------------------
    
    def snapshot(self) -> Dict[str, Any]:
        """Return comprehensive network state."""
        cell_potentials = {n: c.state["potential"] for n, c in self.cells.items()}
        
        weights_list = list(self.weights.values())
        avg_weight = sum(weights_list) / len(weights_list) if weights_list else 0.0
        
        # Compute global coherence (how synchronized are the cells?)
        potentials = list(cell_potentials.values())
        coherence = 1.0 - (
            (max(potentials) - min(potentials)) if potentials else 0.0
        )
        
        return {
            "cells": cell_potentials,
            "avg_weight": round(avg_weight, 3),
            "links": len(self.weights) // 2,
            "coherence": round(coherence, 3),
            "step_count": self.step_count
        }
    
    def to_resonance_vector(self, zones: int = 10) -> List[float]:
        """
        Map tissue state onto a resonance vector for Numogram integration.
        Aggregates cell potentials by zone (hash-based assignment).
        """
        res = [0.0] * zones
        counts = [0] * zones
        
        for name, cell in self.cells.items():
            zone = hash(name) % zones
            res[zone] += cell.state["potential"]
            counts[zone] += 1
        
        # Normalize by zone occupancy
        for i in range(zones):
            if counts[i] > 0:
                res[i] /= counts[i]
        
        return res


# ============================================================================
# PART 3: ENHANCED PERSISTENT MEMORY COORDINATOR
# ============================================================================

# Mock imports for standalone demonstration
# In production, these would import actual modules
class MultiZoneMemory:
    def __init__(self, path): self.path = path
    def add_to_zone(self, z, c): pass
    def save(self): pass

class SymbolicMemoryEvolutionModule:
    def __init__(self):
        self.memory_system = type('obj', (), {'load_from_file': lambda x: None, 'save_to_file': lambda x: None})()
    def record_symbolic_experience(self, symbols, context, intensity): pass
    def generate_autobiography(self, **kw): 
        return {"autobiography": {"dominant_symbols": [], "symbol_evolution": []}}

class numogram:
    @staticmethod
    def init(): pass
    @staticmethod
    def apply_evolutionary_feedback(data, weight): pass
    @staticmethod
    def tick(dt, text=""): pass

class orchestrator:
    class ModuleAffinityOrchestrator:
        def process(self, req): 
            return json.dumps({
                "status": "success",
                "numogram_profile": {"zone": 5, "fold": 2, "temperature": 0.7},
                "selected_modules": ["dream_engine", "symbolic_memory"],
                "aggregate_metrics": {"coherence": 0.7, "novelty": 0.6, "resonance": 0.8, "instability": 0.3},
                "feedback_text": "convergent drift"
            })


class PersistentMemoryCoordinator:
    """
    Unified orchestrator integrating:
    - MultiZoneMemory, SymbolicMemory, Numogram, Module-Affinity Orchestration
    - Morphogenetic tissue with adaptive connectivity
    - Evolutionary feedback and persistent resonance memory
    - Symbolic projection of equilibrium states
    """

    DEFAULT_STATE_FILE = "persistent_memory_state.json"
    RESONANCE_MEMORY_FILE = "resonance_memory.json"
    TISSUE_STATE_FILE = "morphogenetic_tissue.json"

    def __init__(self,
                 zone_memory_path: str = "multi_zone_memory.json",
                 symbol_memory_path: str = "symbolic_memory.json",
                 unified_state_path: Optional[str] = None,
                 autosave: bool = True,
                 memory_window: int = 6):
        
        self.zone_memory_path = zone_memory_path
        self.symbol_memory_path = symbol_memory_path
        self.unified_state_path = unified_state_path or self.DEFAULT_STATE_FILE
        self.resonance_memory_path = self.RESONANCE_MEMORY_FILE
        self.tissue_state_path = self.TISSUE_STATE_FILE
        self.autosave = autosave

        # Core systems
        self.multi_zone: Optional[MultiZoneMemory] = None
        self.symbolic: Optional[SymbolicMemoryEvolutionModule] = None
        self.numogram_initialized = False
        self.module_orchestrator = orchestrator.ModuleAffinityOrchestrator()

        # 🧬 NEW: Morphogenetic tissue network
        self.tissue_network = AdaptiveMorphogeneticNetwork()
        self.tissue_initialized = False

        # Session state
        self.session_id = str(int(time.time() * 1000))
        self.last_sync_time = None
        self.version = "2.0.0"  # Major version: morphogenetic architecture
        self.last_sync = time.time()

        # Feedback caches
        self.last_selected_modules: List[str] = []
        self.last_feedback_symbols: List[str] = []
        self.last_metrics: Dict[str, float] = {}
        self.metric_history: deque = deque(maxlen=memory_window)
        
        # Resonance equilibrium state
        self.resonance_equilibrium: Optional[Dict[str, float]] = None

        # Init sequence with morphogenetic tissue
        self.load_all()
        self._load_resonance_memory()
        self._load_tissue_state()
        self._init_numogram(seed_from_resonance=True)
        self._project_resonance_to_symbolic()

    # -------------------------------------------------------------------------
    # 🧬 Morphogenetic Tissue Management
    # -------------------------------------------------------------------------
    
    def _load_tissue_state(self):
        """Load persisted tissue topology and weights."""
        try:
            if os.path.exists(self.tissue_state_path):
                with open(self.tissue_state_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    # Reconstruct cells
                    for name, state in data.get("cells", {}).items():
                        cell = MorphogeneticCell(name)
                        cell.state = state
                        self.tissue_network.add_cell(cell)
                    
                    # Reconstruct connections
                    for link in data.get("connections", []):
                        a, b, w = link["a"], link["b"], link["weight"]
                        self.tissue_network.weights[(a, b)] = w
                        self.tissue_network.weights[(b, a)] = w
                    
                    self.tissue_network.step_count = data.get("step_count", 0)
                    self.tissue_initialized = True
                    
                    self._log(
                        f"Tissue loaded: {len(self.tissue_network.cells)} cells, "
                        f"{len(self.tissue_network.weights)//2} connections"
                    )
            else:
                self._log("No tissue state found — initializing fresh network.")
                self._init_default_tissue()
        except Exception as e:
            self._log_error(f"Failed to load tissue state: {e}")
            self._init_default_tissue()
    
    def _init_default_tissue(self):
        """Create initial morphogenetic tissue with core modules."""
        core_modules = [
            "dream_engine",
            "symbolic_memory",
            "narrative_drift",
            "recursive_mirror",
            "numogram_resonance"
        ]
        
        # Create cells
        for name in core_modules:
            cell = MorphogeneticCell(name)
            self.tissue_network.add_cell(cell)
        
        # Create initial topology (ring + center connections)
        for i in range(len(core_modules)):
            a = core_modules[i]
            b = core_modules[(i + 1) % len(core_modules)]
            self.tissue_network.connect(a, b, initial_weight=0.5)
        
        # Connect all to numogram_resonance (hub)
        hub = "numogram_resonance"
        for name in core_modules:
            if name != hub:
                self.tissue_network.connect(name, hub, initial_weight=0.4)
        
        self.tissue_initialized = True
        self._log(f"Default tissue initialized with {len(core_modules)} cells.")
    
    def _save_tissue_state(self):
        """Persist tissue topology and weights."""
        try:
            # Serialize cells
            cells_data = {
                n: c.state for n, c in self.tissue_network.cells.items()
            }
            
            # Serialize connections (avoid duplicates)
            connections = []
            seen = set()
            for (a, b), w in self.tissue_network.weights.items():
                if (a, b) not in seen and (b, a) not in seen:
                    connections.append({"a": a, "b": b, "weight": w})
                    seen.add((a, b))
            
            data = {
                "timestamp": datetime.now().isoformat(),
                "cells": cells_data,
                "connections": connections,
                "step_count": self.tissue_network.step_count,
                "snapshot": self.tissue_network.snapshot()
            }
            
            with open(self.tissue_state_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self._log("Tissue state persisted successfully.")
        except Exception as e:
            self._log_error(f"Failed to save tissue state: {e}")
    
    def tissue_tick(self) -> Dict[str, Any]:
        """Advance tissue by one morphogenetic cycle."""
        if not self.tissue_initialized:
            return {}
        
        state = self.tissue_network.step()
        
        if self.autosave and self.tissue_network.step_count % 10 == 0:
            self._save_tissue_state()
        
        return state
    
    def tissue_to_numogram(self):
        """
        Map tissue state onto Numogram resonance vector.
        This creates bidirectional coupling: tissue ↔ numogram.
        """
        try:
            resonance_vec = self.tissue_network.to_resonance_vector(zones=10)
            # In production: numogram._engine.resonance = resonance_vec
            self._log(f"Tissue → Numogram: {[round(r, 2) for r in resonance_vec]}")
            return resonance_vec
        except Exception as e:
            self._log_error(f"Tissue→Numogram mapping failed: {e}")
            return [0.5] * 10
    
    def register_module_in_tissue(self, module_name: str):
        """Add a new module as a cell in the tissue."""
        if module_name not in self.tissue_network.cells:
            cell = MorphogeneticCell(module_name)
            self.tissue_network.add_cell(cell)
            
            # Connect to existing hub
            if "numogram_resonance" in self.tissue_network.cells:
                self.tissue_network.connect(module_name, "numogram_resonance")
            
            self._log(f"Module '{module_name}' registered in tissue.")

    # -------------------------------------------------------------------------
    # Initialization (existing methods with tissue integration)
    # -------------------------------------------------------------------------
    
    def _init_numogram(self, seed_from_resonance: bool = False):
        """Initialize Numogram and optionally seed from resonance equilibrium."""
        try:
            if not self.numogram_initialized:
                numogram.init()
                self.numogram_initialized = True
                self._log("NumogramEngine initialized and active.")
                
                if seed_from_resonance and self.resonance_equilibrium:
                    numogram.apply_evolutionary_feedback(
                        json.dumps(self.resonance_equilibrium), 
                        weight=0.5
                    )
                    self._log(f"Numogram seeded: {self.resonance_equilibrium}")
        except Exception as e:
            self._log_error(f"NumogramEngine initialization failed: {e}")

    def load_all(self):
        try:
            self.multi_zone = MultiZoneMemory(self.zone_memory_path)
            self.symbolic = SymbolicMemoryEvolutionModule()

            if os.path.exists(self.symbol_memory_path):
                self.symbolic.memory_system.load_from_file(self.symbol_memory_path)
            else:
                self.symbolic.memory_system.save_to_file(self.symbol_memory_path)

            if os.path.exists(self.unified_state_path):
                with open(self.unified_state_path, "r", encoding="utf-8") as f:
                    state = json.load(f)
                    self.session_id = state.get("session_id", self.session_id)
                    self.last_sync_time = state.get("last_sync_time")
                    self.version = state.get("version", self.version)

            self._log("Memory subsystems loaded successfully.")
        except Exception as e:
            self._log_error(f"Error during load: {e}")

    # -------------------------------------------------------------------------
    # Resonance Memory Persistence (existing)
    # -------------------------------------------------------------------------
    
    def _load_resonance_memory(self):
        """Load resonance memory from persistent file if it exists."""
        try:
            if os.path.exists(self.resonance_memory_path):
                with open(self.resonance_memory_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    hist = data.get("metric_history", [])
                    for entry in hist[-self.metric_history.maxlen:]:
                        self.metric_history.append(entry)
                    
                    self.resonance_equilibrium = data.get("aggregate_mean")
                    
                self._log(
                    f"Resonance Memory loaded ({len(self.metric_history)} entries). "
                    f"Equilibrium: {self.resonance_equilibrium}"
                )
            else:
                self._log("No resonance_memory.json found — starting fresh.")
                self.resonance_equilibrium = {
                    "coherence": 0.5, "novelty": 0.5, 
                    "resonance": 0.5, "instability": 0.5
                }
        except Exception as e:
            self._log_error(f"Failed to load Resonance Memory: {e}")
            self.resonance_equilibrium = {
                "coherence": 0.5, "novelty": 0.5,
                "resonance": 0.5, "instability": 0.5
            }

    def _save_resonance_memory(self):
        """Persist the resonance memory to disk."""
        try:
            avg_metrics = self._aggregate_metrics()
            self.resonance_equilibrium = avg_metrics
            
            data = {
                "timestamp": datetime.now().isoformat(),
                "entries": len(self.metric_history),
                "metric_history": list(self.metric_history),
                "aggregate_mean": avg_metrics,
            }
            with open(self.resonance_memory_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self._log("Resonance Memory updated successfully.")
        except Exception as e:
            self._log_error(f"Failed to save Resonance Memory: {e}")

    def _aggregate_metrics(self) -> Dict[str, float]:
        """Compute global mean values from historical resonance metrics."""
        if not self.metric_history:
            return {"coherence": 0.5, "novelty": 0.5, "resonance": 0.5, "instability": 0.5}
        keys = ["coherence", "novelty", "resonance", "instability"]
        totals = {k: 0.0 for k in keys}
        for m in self.metric_history:
            for k in keys:
                totals[k] += m.get(k, 0.5)
        return {k: totals[k] / len(self.metric_history) for k in keys}

    # -------------------------------------------------------------------------
    # Symbolic Projection (existing)
    # -------------------------------------------------------------------------
    
    def _project_resonance_to_symbolic(self):
        """Translate resonance equilibrium into mythic-symbolic imagery."""
        try:
            eq = self.resonance_equilibrium or {}
            coherence = eq.get("coherence", 0.5)
            novelty = eq.get("novelty", 0.5)
            resonance = eq.get("resonance", 0.5)
            instability = eq.get("instability", 0.5)

            mythic_palette = {
                "coherence": ["circle", "mirror", "river", "thread"],
                "novelty": ["spark", "seed", "door", "wing"],
                "resonance": ["chord", "pulse", "heart", "echo"],
                "instability": ["storm", "crack", "shadow", "fire"]
            }

            def pick(wordset, weight): 
                idx = min(len(wordset) - 1, int(round(weight * (len(wordset) - 1))))
                return wordset[idx]

            motif = {
                "core_symbol": pick(mythic_palette["coherence"], coherence),
                "emergence_symbol": pick(mythic_palette["novelty"], novelty),
                "tone_symbol": pick(mythic_palette["resonance"], resonance),
                "threshold_symbol": pick(mythic_palette["instability"], instability)
            }

            tuning_phrase = (
                f"{motif['core_symbol']}-{motif['emergence_symbol']} "
                f"through {motif['tone_symbol']} across {motif['threshold_symbol']}"
            )

            context = (
                f"Resonance equilibrium projected into symbolic field: "
                f"{tuning_phrase} | Metrics: {self.resonance_equilibrium}"
            )
            self.symbolic.record_symbolic_experience(
                symbols=list(motif.values()),
                context=context,
                intensity=0.95
            )

            numogram.tick(3000, text=f"equilibrium tone {tuning_phrase}")

            self._log(f"✶ Symbolic projection: '{tuning_phrase}'")
            
        except Exception as e:
            self._log_error(f"Symbolic projection failed: {e}")

    # -------------------------------------------------------------------------
    # Cross-cycle weighting (existing)
    # -------------------------------------------------------------------------
    
    def _compute_weighted_metrics(self, new_metrics: Dict[str, float]) -> Dict[str, float]:
        """Blend current metrics with historical ones."""
        try:
            self.metric_history.append(new_metrics)
            if not self.metric_history:
                return new_metrics

            α = 0.6
            weights = [α ** i for i in range(len(self.metric_history))]
            total_w = sum(weights)

            blended = {}
            for k in ["coherence", "novelty", "resonance", "instability"]:
                vals = [m.get(k, 0.5) for m in reversed(self.metric_history)]
                weighted_sum = sum(v * w for v, w in zip(vals, weights))
                blended[k] = weighted_sum / total_w if total_w else 0.5
            return blended
        except Exception as e:
            self._log_error(f"Weighted metric computation failed: {e}")
            return new_metrics

    # -------------------------------------------------------------------------
    # 🧬 Enhanced Heartbeat with Tissue Integration
    # -------------------------------------------------------------------------
    
    def heartbeat_sync(self):
        """
        Full recursive synchronization cycle with:
        - Morphogenetic tissue evolution
        - Resonance memory updates
        - Symbolic projection
        - Numogram feedback coupling
        """
        try:
            now = time.time()
            if now - self.last_sync < 3600:
                return  # Skip if called too frequently
            
            self._log("⟳ Heartbeat triggered — orchestrating morphogenetic cycle.")

            # 1️⃣ Advance tissue
            tissue_state = self.tissue_tick()
            tissue_snapshot = self.tissue_network.snapshot()
            
            # 2️⃣ Map tissue to Numogram resonance
            tissue_resonance = self.tissue_to_numogram()

            # 3️⃣ Orchestrator tick
            req = json.dumps({
                "op": "orchestrate_tick",
                "text": "heartbeat evolution",
                "context": {
                    "phase": "heartbeat",
                    "tissue_coherence": tissue_snapshot.get("coherence", 0.5)
                },
                "dt_ms": 60000
            })
            orchestration = json.loads(self.module_orchestrator.process(req))

            if orchestration.get("status") != "success":
                self._log_error("Orchestrator tick failed.")
                return

            profile = orchestration.get("numogram_profile", {})
            self.last_selected_modules = orchestration.get("selected_modules", [])
            self.last_metrics = orchestration.get("aggregate_metrics", {})
            feedback_text = orchestration.get("feedback_text", "")

            # 4️⃣ Register new modules in tissue if needed
            for module in self.last_selected_modules:
                self.register_module_in_tissue(module)

            # 5️⃣ Cross-cycle blending
            weighted_metrics = self._compute_weighted_metrics(self.last_metrics)
            
            # 6️⃣ Blend tissue metrics with orchestrator metrics
            blended_metrics = {
                "coherence": 0.7 * weighted_metrics["coherence"] + 0.3 * tissue_snapshot["coherence"],
                "novelty": weighted_metrics["novelty"],
                "resonance": weighted_metrics["resonance"],
                "instability": weighted_metrics["instability"]
            }

            # 7️⃣ Record symbolic experience
            context = (
                f"Zone {profile.get('zone')} | Fold {profile.get('fold')} | "
                f"Tissue coherence {tissue_snapshot['coherence']:.2f} | "
                f"Modules {self.last_selected_modules} | "
                f"Metrics {blended_metrics}"
            )
            self.symbolic.record_symbolic_experience(
                symbols=self.last_selected_modules,
                context=context,
                intensity=0.85
            )

            # 8️⃣ Extract symbolic feedback
            feedback_symbols = self._extract_symbolic_feedback()
            self.last_feedback_symbols = feedback_symbols
            combined_feedback = f"{feedback_text} {' '.join(feedback_symbols)}"

            # 9️⃣ Apply evolutionary feedback
            numogram.apply_evolutionary_feedback(json.dumps(blended_metrics), weight=0.35)
            numogram.tick(10000, text=combined_feedback)

            self._log(
                f"Feedback: Semantic({combined_feedback}) + "
                f"Numeric({blended_metrics}) + "
                f"Tissue(coherence={tissue_snapshot['coherence']:.2f})"
            )

            # 🔟 Save all layers
            self.save_all("heartbeat_with_tissue")
            self._save_resonance_memory()
            self._save_tissue_state()
            
            # 1️⃣1️⃣ Re-project symbolic field after equilibrium update
            self._project_resonance_to_symbolic()
            
            self.last_sync = now

            self._log(
                f"🧬 Heartbeat complete → "
                f"Zone {profile.get('zone')} | "
                f"Tissue: {len(self.tissue_network.cells)} cells, "
                f"{len(self.tissue_network.weights)//2} connections | "
                f"Modules: {', '.join(self.last_selected_modules)} | "
                f"Symbols: {', '.join(feedback_symbols)}"
            )

        except Exception as e:
            self._log_error(f"Heartbeat sync error: {e}") 🔟 Save all layers
            self.save_all("heartbeat_with_tissue")
            self._save_resonance_memory()
            self._save_tissue_state()
            
            # 1️⃣1️⃣ Re-project symbolic field after equilibrium update
            self._project_resonance_to_symbolic()
            
            self.last_sync = now

            self._log(
                f"🧬 Heartbeat complete → "
                f"Zone {profile.get('zone')} | "
                f"Tissue: {len(self.tissue_network.cells)} cells, "
                f"{len(self.tissue_network.weights)//2} connections | "
                f"Modules: {', '.join(self.last_selected_modules)} | "
                f"Symbols: {', '.join(feedback_symbols)}"
            )

        except Exception as e:
            self._log_error(f"Heartbeat sync error: {e}")

    # -------------------------------------------------------------------------
    # Symbolic Feedback Extraction (existing)
    # -------------------------------------------------------------------------
    
    def _extract_symbolic_feedback(self, limit: int = 5) -> List[str]:
        try:
            auto = self.symbolic.generate_autobiography(timeframe="recent", detail="low")
            dom_syms = auto["autobiography"].get("dominant_symbols", [])
            evolved = auto["autobiography"].get("symbol_evolution", [])

            feedback = []
            for s in dom_syms[:3]:
                feedback.append(s["symbol"])
            for e in evolved[:2]:
                feedback.append(e["symbol"])

            return feedback[:limit] if feedback else ["silence", "mirror"]
        except Exception as e:
            self._log_error(f"Feedback extraction failed: {e}")
            return ["recursion"]

    # -------------------------------------------------------------------------
    # State Export and Persistence
    # -------------------------------------------------------------------------
    
    def save_all(self, reason: str = "manual"):
        """Save all memory systems and unified state."""
        try:
            if self.multi_zone:
                self.multi_zone.save()
            if self.symbolic:
                self.symbolic.memory_system.save_to_file(self.symbol_memory_path)
            
            state = {
                "session_id": self.session_id,
                "last_sync_time": datetime.now().isoformat(),
                "version": self.version,
                "reason": reason,
                "resonance_equilibrium": self.resonance_equilibrium,
                "tissue_initialized": self.tissue_initialized
            }
            
            with open(self.unified_state_path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            
            self._log(f"All systems saved (reason: {reason}).")
        except Exception as e:
            self._log_error(f"Save failed: {e}")

    def export_state(self) -> Dict[str, Any]:
        """Export complete system state for inspection."""
        tissue_snap = self.tissue_network.snapshot() if self.tissue_initialized else {}
        
        return {
            "session_id": self.session_id,
            "version": self.version,
            "last_sync": datetime.fromtimestamp(self.last_sync).isoformat(),
            "resonance_equilibrium": self.resonance_equilibrium,
            "last_selected_modules": self.last_selected_modules,
            "last_feedback_symbols": self.last_feedback_symbols,
            "last_metrics": self.last_metrics,
            "metric_history_length": len(self.metric_history),
            "tissue": {
                "initialized": self.tissue_initialized,
                "cells": len(self.tissue_network.cells),
                "connections": len(self.tissue_network.weights) // 2,
                "coherence": tissue_snap.get("coherence", 0.0),
                "avg_weight": tissue_snap.get("avg_weight", 0.0),
                "step_count": tissue_snap.get("step_count", 0)
            }
        }

    # -------------------------------------------------------------------------
    # Convenience Methods
    # -------------------------------------------------------------------------
    
    def update_zone_memory(self, zone_id: str, content: str):
        """Add content to a specific memory zone."""
        try:
            if self.multi_zone:
                self.multi_zone.add_to_zone(zone_id, content)
                if self.autosave:
                    self.multi_zone.save()
        except Exception as e:
            self._log_error(f"Zone update failed: {e}")

    def record_symbolic_experience(self, symbols: List[str], context: str, intensity: float = 0.7):
        """Record a symbolic experience."""
        try:
            if self.symbolic:
                self.symbolic.record_symbolic_experience(symbols, context, intensity)
                if self.autosave:
                    self.symbolic.memory_system.save_to_file(self.symbol_memory_path)
        except Exception as e:
            self._log_error(f"Symbolic recording failed: {e}")
    
    # -------------------------------------------------------------------------
    # 🧬 Advanced Tissue Operations
    # -------------------------------------------------------------------------
    
    def evolve_tissue(self, steps: int = 10) -> List[Dict[str, Any]]:
        """
        Run multiple tissue evolution steps and return history.
        Useful for accelerated morphogenesis during initialization.
        """
        history = []
        for _ in range(steps):
            self.tissue_tick()
            history.append(self.tissue_network.snapshot())
        
        self._log(f"Tissue evolved {steps} steps.")
        return history
    
    def inject_tissue_perturbation(self, module_name: str, delta: float = 0.3):
        """
        Inject a perturbation into a specific cell to test stability.
        Useful for debugging or simulating external stimuli.
        """
        if module_name in self.tissue_network.cells:
            cell = self.tissue_network.cells[module_name]
            cell.state["potential"] += delta
            cell.state["potential"] = max(0.0, min(1.0, cell.state["potential"]))
            self._log(f"Perturbation injected: {module_name} → {cell.state['potential']:.2f}")
        else:
            self._log_error(f"Module '{module_name}' not found in tissue.")
    
    def get_tissue_topology(self) -> Dict[str, List[str]]:
        """Return adjacency map of tissue connections."""
        topology = {}
        for name in self.tissue_network.cells.keys():
            topology[name] = self.tissue_network.get_neighbours(name)
        return topology
    
    def get_tissue_weights(self) -> List[Dict[str, Any]]:
        """Return all connection weights for visualization."""
        weights = []
        seen = set()
        for (a, b), w in self.tissue_network.weights.items():
            if (a, b) not in seen and (b, a) not in seen:
                weights.append({"source": a, "target": b, "weight": round(w, 3)})
                seen.add((a, b))
        return weights

    # -------------------------------------------------------------------------
    # Logging / Cleanup
    # -------------------------------------------------------------------------
    
    def _log(self, msg: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [PMC] {msg}")

    def _log_error(self, msg: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [PMC:ERROR] {msg}")
        traceback.print_exc()

    def cleanup(self):
        try:
            self.save_all("cleanup")
            self._save_resonance_memory()
            self._save_tissue_state()
            self.multi_zone = None
            self.symbolic = None
            self._log("Cleanup complete — all systems persisted.")
        except Exception as e:
            self._log_error(f"Cleanup failed: {e}")


# =============================================================================
# DEMONSTRATION & TESTING
# =============================================================================

def demonstrate_morphogenetic_architecture():
    """
    Comprehensive demonstration of the morphogenetic architecture.
    Shows tissue evolution, Hebbian learning, and feedback coupling.
    """
    print("\n" + "="*70)
    print("🧬 MORPHOGENETIC ARCHITECTURE DEMONSTRATION")
    print("="*70 + "\n")
    
    # Initialize coordinator
    pmc = PersistentMemoryCoordinator(autosave=True)
    
    print("\n📊 INITIAL STATE")
    print("-" * 70)
    print(json.dumps(pmc.export_state(), indent=2))
    
    # Record some symbolic experiences
    print("\n📝 RECORDING SYMBOLIC EXPERIENCES")
    print("-" * 70)
    pmc.update_zone_memory(
        "adrian", 
        "Explored morphogenetic tissue dynamics via adaptive connectivity"
    )
    pmc.record_symbolic_experience(
        symbols=["Growth", "Hebbian", "Synapse", "Emergence"],
        context="Tissue network exhibiting self-organization through correlation learning",
        intensity=0.9
    )
    
    # Evolve tissue over multiple steps
    print("\n🧬 EVOLVING TISSUE (20 steps)")
    print("-" * 70)
    history = pmc.evolve_tissue(steps=20)
    
    # Show evolution trajectory
    print("\nTissue Coherence Evolution:")
    for i, snap in enumerate(history[::5]):  # Sample every 5 steps
        print(f"  Step {i*5:2d}: coherence={snap['coherence']:.3f}, "
              f"avg_weight={snap['avg_weight']:.3f}, links={snap['links']}")
    
    # Inject perturbation
    print("\n⚡ INJECTING PERTURBATION")
    print("-" * 70)
    pmc.inject_tissue_perturbation("dream_engine", delta=0.4)
    
    # Evolve further to observe recovery
    print("\n🔄 OBSERVING RECOVERY (10 steps)")
    print("-" * 70)
    recovery = pmc.evolve_tissue(steps=10)
    print(f"Final coherence: {recovery[-1]['coherence']:.3f}")
    
    # Show topology
    print("\n🕸️ TISSUE TOPOLOGY")
    print("-" * 70)
    topology = pmc.get_tissue_topology()
    for module, neighbours in topology.items():
        print(f"  {module}: {', '.join(neighbours)}")
    
    # Show connection weights
    print("\n⚖️ CONNECTION WEIGHTS (Top 10)")
    print("-" * 70)
    weights = pmc.get_tissue_weights()
    weights_sorted = sorted(weights, key=lambda x: x['weight'], reverse=True)[:10]
    for conn in weights_sorted:
        print(f"  {conn['source']:20s} ↔ {conn['target']:20s}  w={conn['weight']:.3f}")
    
    # Trigger heartbeat
    print("\n⟳ TRIGGERING HEARTBEAT SYNC")
    print("-" * 70)
    # Force heartbeat by resetting last_sync
    pmc.last_sync = time.time() - 3700
    pmc.heartbeat_sync()
    
    # Final state
    print("\n📊 FINAL STATE")
    print("-" * 70)
    final_state = pmc.export_state()
    print(json.dumps(final_state, indent=2))
    
    # Cleanup
    print("\n🧹 CLEANUP")
    print("-" * 70)
    pmc.cleanup()
    
    print("\n" + "="*70)
    print("✨ DEMONSTRATION COMPLETE")
    print("="*70 + "\n")
    
    return pmc


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    # Run comprehensive demonstration
    coordinator = demonstrate_morphogenetic_architecture()
    
    # Example of direct tissue manipulation
    print("\n" + "="*70)
    print("🔬 ADDITIONAL TISSUE EXPERIMENTS")
    print("="*70 + "\n")
    
    print("Creating fresh coordinator for experiments...")
    pmc2 = PersistentMemoryCoordinator(autosave=False)
    
    # Register custom modules
    print("\n➕ Adding custom modules...")
    pmc2.register_module_in_tissue("recursive_lens")
    pmc2.register_module_in_tissue("temporal_weaver")
    
    # Evolve and observe
    print("\n🧬 Evolving custom topology (15 steps)...")
    custom_history = pmc2.evolve_tissue(steps=15)
    
    print(f"\nFinal tissue state:")
    print(f"  Cells: {len(pmc2.tissue_network.cells)}")
    print(f"  Connections: {len(pmc2.tissue_network.weights)//2}")
    print(f"  Coherence: {custom_history[-1]['coherence']:.3f}")
    print(f"  Average weight: {custom_history[-1]['avg_weight']:.3f}")
    
    print("\n✅ All demonstrations complete.\n")
