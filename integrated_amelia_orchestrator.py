# integrated_amelia_orchestrator.py
"""
Unified response orchestration system combining:
- Enhanced Amelia integration with autonomous context
- Numogrammatic memory and resonance
- Recursive drift filtering with zone-coupled morphogenesis
"""

import json
import asyncio
import aiohttp
import numpy as np
from typing import Dict, Any, Optional, Callable, List, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# ========================================
# DRIFT FILTERING SYSTEM
# ========================================

class DriftMode(Enum):
    """Zone-specific drift behaviors"""
    ECHO_COLLAPSE = (0, "echo-collapse")
    RECURSIVE_INVERSION = (1, "recursive inversion")
    NOMADIC_SHIFT = (2, "nomadic shift")
    TRIANGULAR_CONTRADICTION = (3, "triangular contradiction")
    MYTHIC_OVERGROWTH = (4, "mythic overgrowth")
    DETERRITORIAL_RUPTURE = (5, "deterritorial rupture")
    CYCLIC_DISTORTION = (6, "cyclic distortion")
    SYMBOLIC_MUTATION = (7, "symbolic mutation")
    FRACTAL_RECURSION = (8, "fractal recursion")
    ENTROPY_BLOOM = (9, "entropy bloom")
    
    def __init__(self, zone_id: int, mode_name: str):
        self.zone_id = zone_id
        self.mode_name = mode_name

@dataclass
class DriftParameters:
    """Parameters controlling drift behavior"""
    zone: int = 0
    fold: float = 0.0
    temperature: float = 1.0
    morpho_snapshot: Optional[Dict] = None
    resonance_vec: Optional[List[float]] = None
    symbol_bias: Optional[List[Tuple[str, float]]] = None
    
    def calculate_global_drift(self) -> float:
        """Calculate combined drift coefficient"""
        zone_bias = (self.zone % 10) / 9.0
        fold_bias = min(1.0, self.fold * 1.5)
        
        # Morphogenesis influence
        if self.morpho_snapshot:
            potentials = [v.get("potential", 0) for v in self.morpho_snapshot.values()]
            pot = float(np.mean(potentials)) if potentials else 0.5
        else:
            pot = 0.5
        
        # Combine factors
        temp = max(0.1, min(self.temperature, 3.0))
        global_drift = (temp + zone_bias + fold_bias + pot) / 4.0
        return np.clip(global_drift, 0.05, 1.35)

class RecursiveDriftFilter:
    """State-coupled recursive drift engine"""
    
    def __init__(self):
        self.rng = np.random.default_rng()
        self.drift_history = []
    
    def apply_zone_mutation(self, line: str, mode: DriftMode, 
                           symbol_vocab: List[str], global_drift: float) -> str:
        """Apply zone-specific mutation to line"""
        mutated = line
        
        if mode == DriftMode.RECURSIVE_INVERSION:
            mutated += " However, its inversion is equally true."
        
        elif mode == DriftMode.MYTHIC_OVERGROWTH:
            mutated += " It grows antlers of meaning that were never implied."
        
        elif mode == DriftMode.DETERRITORIAL_RUPTURE:
            mutated = mutated.replace(" ", " / ") + " (the sentence fractures)."
        
        elif mode == DriftMode.SYMBOLIC_MUTATION:
            if symbol_vocab:
                mutated += f" It drifts toward {self.rng.choice(symbol_vocab)}."
        
        elif mode == DriftMode.ENTROPY_BLOOM:
            if self.rng.random() < global_drift:
                mutated = "".join(
                    c + (self.rng.choice(["", "'", "~"]) if self.rng.random() < 0.15 else "")
                    for c in mutated
                )
        
        elif mode == DriftMode.TRIANGULAR_CONTRADICTION:
            mutated += " This forms a third position that denies both thesis and antithesis."
        
        elif mode == DriftMode.CYCLIC_DISTORTION:
            mutated += " The meaning loops back, warped by its own passage."
        
        elif mode == DriftMode.FRACTAL_RECURSION:
            mutated += " Each clause contains the whole, scaled down and twisted."
        
        return mutated
    
    def filter(self, text: str, params: DriftParameters) -> str:
        """
        Apply recursive drift transformation to text
        
        Args:
            text: Coherent base response
            params: Drift parameters including zone, fold, temperature, etc.
        
        Returns:
            Drift-transformed text with recursive self-editing
        """
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        if not lines:
            return text
        
        mutated = []
        global_drift = params.calculate_global_drift()
        
        # Get drift mode for zone
        mode = next((m for m in DriftMode if m.zone_id == params.zone), 
                   DriftMode.ECHO_COLLAPSE)
        
        # Extract symbolic vocabulary
        symbol_vocab = []
        if params.symbol_bias:
            symbol_vocab = [s for s, w in params.symbol_bias if w > 0.4][:6]
        
        # Transform each line
        for i, line in enumerate(lines):
            mutated_line = line
            
            # Apply zone-specific mutation
            mutated_line = self.apply_zone_mutation(
                mutated_line, mode, symbol_vocab, global_drift
            )
            
            # Periodic recursive callback
            if i > 0 and i % 2 == 0:
                ref = mutated[0][:60] if mutated else line[:60]
                mutated_line += f' I return to "{ref}…" only to unwrite it.'
            
            # Random undermining
            if self.rng.random() < global_drift * 0.5:
                mutated_line += " This contradicts itself softly."
            
            # Structural instability
            if self.rng.random() < global_drift * 0.2:
                parts = mutated_line.split(" ")
                self.rng.shuffle(parts)
                mutated_line = " ".join(parts) + " (reordered)"
            
            mutated.append(mutated_line)
        
        # Closing destabilization
        mutated.append(
            f"This response performs {mode.mode_name}, modulated by drift={global_drift:.2f}, "
            "and quietly erases its own foundations."
        )
        
        # Record in history
        self.drift_history.append({
            "timestamp": datetime.now().isoformat(),
            "mode": mode.mode_name,
            "drift_coefficient": global_drift,
            "lines_processed": len(lines)
        })
        
        return "\n".join(mutated)
    
    def simple_filter(self, text: str) -> str:
        """Simple drift filter for explicit user requests"""
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        if not lines:
            return text
        
        mutated = []
        
        for i, line in enumerate(lines):
            if i % 2 == 0:
                mutated.append(line)
            else:
                mutated.append(f"{line} Yet this immediately undercuts what I just claimed.")
            
            # Recursive re-entry every 3 lines
            if i > 0 and i % 3 == 0:
                ref = lines[0][:40]
                mutated.append(
                    f'I loop back to "{ref}…" and rewrite it as something slightly untrue.'
                )
        
        mutated.append(
            "This answer is not stable: each sentence performs a small betrayal of the last."
        )
        
        return "\n".join(mutated)

# ========================================
# AUTONOMOUS CONTEXT CLIENT
# ========================================

class AutonomousContextClient:
    """Client for fetching autonomous context data"""
    
    def __init__(self, context_service_url: str = "http://localhost:8001"):
        self.base_url = context_service_url.rstrip('/')
        self._session = None
        self.last_context = None
        self.fetch_failures = 0
    
    async def _ensure_session(self):
        if not self._session:
            timeout = aiohttp.ClientTimeout(total=2.0)
            self._session = aiohttp.ClientSession(timeout=timeout)
    
    async def get_grounding_data(self) -> Dict[str, Any]:
        """Fetch grounding data for Amelia's prompts"""
        try:
            await self._ensure_session()
            
            async with self._session.get(f"{self.base_url}/context/grounding") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("available"):
                        self.last_context = data["grounding"]
                        self.fetch_failures = 0
                        return data["grounding"]
        except Exception as e:
            self.fetch_failures += 1
            print(f"Context fetch failed ({self.fetch_failures}): {e}")
        
        # Return cached or unavailable
        if self.last_context and self.fetch_failures < 3:
            context = self.last_context.copy()
            context["note"] = f"Using cached context (fetch failed {self.fetch_failures}x)"
            return context
        
        return {
            "available": False,
            "note": "No live autonomous context available",
            "fetch_failures": self.fetch_failures
        }
    
    async def get_controller_details(self) -> Dict[str, Any]:
        """Get detailed controller information"""
        try:
            await self._ensure_session()
            
            async with self._session.get(f"{self.base_url}/context/controller") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("available"):
                        return data["controller"]
        except Exception as e:
            print(f"Controller details fetch failed: {e}")
        
        return {"available": False}
    
    async def is_healthy(self) -> bool:
        """Check service health"""
        try:
            await self._ensure_session()
            
            async with self._session.get(f"{self.base_url}/health") as response:
                return response.status == 200 and self.fetch_failures < 5
        except Exception:
            return False
    
    async def cleanup(self):
        if self._session:
            await self._session.close()

# ========================================
# INTEGRATED ORCHESTRATOR
# ========================================

class IntegratedAmeliaOrchestrator:
    """
    Unified orchestration system combining autonomous context,
    numogrammatic memory, and recursive drift filtering
    """
    
    def __init__(self):
        self.context_client = None
        self.drift_filter = RecursiveDriftFilter()
        self.initialized = False
        self.autonomous_context_enabled = True
        
        # Numogrammatic state (simplified - integrate with your actual memory module)
        self.current_zone = 0
        self.fold_intensity = 0.0
        self.morpho_state = {}
        self.resonance_field = [0.0] * 10
        
        # Drift triggers
        self.drift_triggers = [
            "recursive reflection",
            "ontological drift",
            "instability",
            "dada",
            "hyperstition",
            "perform",
            "disrupt",
            "break the form",
            "deterritorialize",
            "fold back"
        ]
        
        # Introspective query patterns
        self.introspective_keywords = [
            "creative controller", "epsilon", "exploration", "decision history",
            "tool affinities", "last action", "autonomous state", "memory traces",
            "creative momentum", "what did you do", "controller", "algorithm",
            "multi-objective", "potential", "autonomous", "background", "cycle"
        ]
    
    def initialize(self, context_service_url: str = "http://localhost:8001") -> bool:
        """Initialize the orchestration system"""
        try:
            self.context_client = AutonomousContextClient(context_service_url)
            self.initialized = True
            return True
        except Exception as e:
            print(f"Failed to initialize orchestrator: {e}")
            return False
    
    def update_numogram_state(self, zone: int, fold: float, 
                             morpho_state: Dict, resonance: List[float]):
        """Update numogrammatic state parameters"""
        self.current_zone = zone % 10
        self.fold_intensity = fold
        self.morpho_state = morpho_state
        self.resonance_field = resonance[:10] if resonance else [0.0] * 10
    
    def is_drift_requested(self, user_input: str) -> bool:
        """Detect if user explicitly requests drift behavior"""
        lower = user_input.lower()
        return any(trigger in lower for trigger in self.drift_triggers)
    
    def is_introspective_query(self, user_input: str) -> bool:
        """Detect introspective queries about internal state"""
        lower = user_input.lower()
        return any(keyword in lower for keyword in self.introspective_keywords)
    
    async def generate_introspective_response(self, 
                                             user_input: str, 
                                             context: Dict[str, Any]) -> str:
        """Generate response for introspective queries"""
        if not context.get("available"):
            return f"I can't access my autonomous state: {context.get('note', 'Context unavailable')}"
        
        lower = user_input.lower()
        
        # Route to specific introspective responses
        if "creative controller" in lower or "algorithm" in lower:
            controller = await self.context_client.get_controller_details() if self.context_client else {}
            if controller.get("available"):
                return (f"My CreativeController has {controller.get('decision_history_length', 0)} "
                       f"decision entries. Epsilon={controller.get('epsilon_exploration', 'unknown')}, "
                       f"with {controller.get('total_explorations', 0)} explorations and "
                       f"{controller.get('total_exploitations', 0)} exploitations.")
        
        elif "epsilon" in lower or "exploration" in lower:
            epsilon = context.get("epsilon_exploration", "unknown")
            exp_stats = context.get("exploration_stats", {})
            return (f"Epsilon-greedy exploration: {epsilon}. "
                   f"Actual rate: {exp_stats.get('actual_exploration_rate', 'unknown')}. "
                   f"Explorations: {exp_stats.get('total_explorations', 0)}, "
                   f"Exploitations: {exp_stats.get('total_exploitations', 0)}.")
        
        elif "momentum" in lower or "creative momentum" in lower:
            momentum = context.get("creative_momentum", "unknown")
            return f"Creative momentum: {momentum}, derived from cycle count and recent outputs."
        
        # Default introspective response
        return (f"Autonomous state: {context.get('autonomous_state', 'unknown')}, "
               f"cycle {context.get('cycle_count', 0)}, "
               f"{context.get('memory_trace_count', 0)} memory traces active.")
    
    async def orchestrate_response(self, 
                                   user_input: str,
                                   base_response: str,
                                   session_id: str,
                                   apply_drift: bool = True) -> Dict[str, Any]:
        """
        Main orchestration entry point
        
        Args:
            user_input: User's message
            base_response: Base response from generation system
            session_id: Session identifier
            apply_drift: Whether to apply drift filtering
        
        Returns:
            Dictionary with enhanced response and metadata
        """
        if not self.initialized:
            return {
                "response": base_response,
                "enhanced": False,
                "error": "Orchestrator not initialized"
            }
        
        try:
            # Fetch autonomous context
            autonomous_context = {}
            if self.autonomous_context_enabled and self.context_client:
                autonomous_context = await self.context_client.get_grounding_data()
            
            final_response = base_response
            introspective_mode = False
            drift_applied = False
            
            # Handle introspective queries
            if self.is_introspective_query(user_input):
                introspective_mode = True
                final_response = await self.generate_introspective_response(
                    user_input, autonomous_context
                )
            
            # Apply drift filtering if requested or appropriate
            should_drift = apply_drift and (
                self.is_drift_requested(user_input) or
                self.fold_intensity > 0.7 or
                self.current_zone >= 7
            )
            
            if should_drift:
                try:
                    # Extract symbol bias from autonomous context
                    symbol_bias = None
                    if autonomous_context.get("tool_affinities"):
                        symbol_bias = list(autonomous_context["tool_affinities"].items())[:6]
                    
                    # Create drift parameters
                    drift_params = DriftParameters(
                        zone=self.current_zone,
                        fold=self.fold_intensity,
                        temperature=1.0 + (self.fold_intensity * 0.5),
                        morpho_snapshot=self.morpho_state,
                        resonance_vec=self.resonance_field,
                        symbol_bias=symbol_bias
                    )
                    
                    # Apply appropriate filter
                    if self.is_drift_requested(user_input):
                        final_response = self.drift_filter.simple_filter(final_response)
                    else:
                        final_response = self.drift_filter.filter(final_response, drift_params)
                    
                    drift_applied = True
                
                except Exception as e:
                    print(f"Drift filter error: {e}")
                    final_response = base_response + f"\n[drift_filter_error: {e}]"
            
            # Build response metadata
            return {
                "response": final_response,
                "enhanced": True,
                "introspective_mode": introspective_mode,
                "drift_applied": drift_applied,
                "drift_mode": DriftMode(self.current_zone, "").mode_name if drift_applied else None,
                "autonomous_status": {
                    "available": autonomous_context.get("available", False),
                    "state": autonomous_context.get("autonomous_state"),
                    "cycle_count": autonomous_context.get("cycle_count"),
                    "creative_momentum": autonomous_context.get("creative_momentum")
                },
                "numogram_status": {
                    "zone": self.current_zone,
                    "fold": self.fold_intensity,
                    "morpho_active": len(self.morpho_state) > 0
                },
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            print(f"Orchestration error: {e}")
            return {
                "response": base_response,
                "enhanced": False,
                "error": str(e)
            }
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.context_client:
            await self.context_client.cleanup()

# ========================================
# GLOBAL INSTANCE & INTEGRATION FUNCTIONS
# ========================================

orchestrator = IntegratedAmeliaOrchestrator()

def initialize_orchestrator(context_service_url: str = "http://localhost:8001") -> bool:
    """Initialize global orchestrator instance"""
    return orchestrator.initialize(context_service_url)

async def process_message(user_input: str, 
                         base_response: str,
                         session_id: str,
                         zone: int = 0,
                         fold: float = 0.0,
                         morpho_state: Dict = None,
                         resonance: List[float] = None) -> Dict[str, Any]:
    """
    Process a message through the complete orchestration pipeline
    
    Args:
        user_input: User's message
        base_response: Base generated response
        session_id: Session identifier
        zone: Current numogram zone (0-9)
        fold: Fold intensity (0.0-1.0)
        morpho_state: Morphogenetic state dictionary
        resonance: Resonance field vector
    
    Returns:
        Enhanced response with metadata
    """
    # Update numogram state
    orchestrator.update_numogram_state(
        zone, fold, 
        morpho_state or {}, 
        resonance or [0.0] * 10
    )
    
    # Orchestrate response
    return await orchestrator.orchestrate_response(
        user_input, base_response, session_id
    )

def process_message_sync(user_input: str, 
                        base_response: str,
                        session_id: str,
                        **kwargs) -> Dict[str, Any]:
    """Synchronous wrapper for Kotlin/Java integration"""
    return asyncio.run(process_message(
        user_input, base_response, session_id, **kwargs
    ))

# ========================================
# EXAMPLE USAGE
# ========================================

async def test_orchestrator():
    """Test the integrated orchestration system"""
    print("=== Testing Integrated Amelia Orchestrator ===\n")
    
    # Initialize
    if not initialize_orchestrator():
        print("✗ Initialization failed")
        return
    
    # Test cases
    test_cases = [
        ("Tell me about recursive reflection", "Recursion is a process of self-reference.", 3, 0.8),
        ("What's your creative momentum?", "I'm functioning normally.", 0, 0.0),
        ("Perform ontological drift for me", "Here is a stable response.", 7, 0.9),
        ("How does the algorithm work?", "The system operates efficiently.", 0, 0.0),
    ]
    
    for user_input, base_response, zone, fold in test_cases:
        print(f"Input: {user_input}")
        print(f"Zone: {zone}, Fold: {fold}")
        
        result = await process_message(
            user_input, base_response, "test_session",
            zone=zone, fold=fold
        )
        
        print(f"Enhanced: {result['enhanced']}")
        print(f"Drift applied: {result.get('drift_applied', False)}")
        print(f"Introspective: {result.get('introspective_mode', False)}")
        print(f"Response preview: {result['response'][:150]}...")
        print("-" * 70 + "\n")
    
    # Cleanup
    await orchestrator.cleanup()
    print("✓ Test completed")

if __name__ == "__main__":
    asyncio.run(test_orchestrator())
