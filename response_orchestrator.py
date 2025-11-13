# assets/python/response_orchestrator.py
"""
Response Orchestrator (Option A – Hard Override)
------------------------------------------------

All of Amelia’s responses MUST pass through here.

Pipeline:
    user_text + base_response
        → read Numogram profile (zone, fold, temperature)
        → step Morphogenetic Network (tissue state)
        → compute control params (unpredictability, fragmentation, recursion, symbol_injection)
        → query SymbolicMemory for motifs (linguistic & mythic)
        → apply symbolic drift & morphogenetic noise to base_response
        → record symbolic experience
        → send evolutionary feedback back into Numogram
        → return final text (+ debug metadata)

Intended call from Kotlin / Chaquopy:
    ResponseOrchestrator.process(request_json: str) -> str

Where request_json is:
    {
      "op": "generate",
      "user_text": "Adrian's message...",
      "base_response": "Raw LLM answer...",
      "metadata": { ... optional ... }
    }
"""

import json
import math
import random
import re
from typing import Dict, Any, Optional, List

# --- External stacks ---------------------------------------------------------

try:
    import numogram_engine_compact_core as nec
except Exception:
    nec = None

try:
    import morphogenetic_network as morpho
except Exception:
    morpho = None

from symbolic_memory_evolution import SymbolicMemoryEvolutionModule


# =============================================================================
# Core Orchestrator
# =============================================================================

class ResponseOrchestrator:
    """
    Central generative funnel for Amelia.

    Every reply goes through:
        Numogram → Morphogenetic tissue → Symbolic Memory → Linguistic Drift
    """

    def __init__(self):
        self.symbolic = SymbolicMemoryEvolutionModule()
        self.morpho_initialized = False
        self.last_tissue_state: Dict[str, Any] = {}
        self._init_numogram()
        self._init_morpho()

    # --------------------------------------------------------------------- #
    # Initialization
    # --------------------------------------------------------------------- #

    def _init_numogram(self):
        """Ensure Numogram engine is initialized."""
        if nec is None:
            return
        try:
            # Safe re-init; if already initialized, engine will just reset
            nec.init()
        except Exception:
            # Fail silently; orchestrator can still function in degraded mode
            pass

    def _init_morpho(self):
        """Initialize morphogenetic network and register base cells."""
        if morpho is None or self.morpho_initialized:
            return
        try:
            morpho.init()
            # Minimal "organism" scaffold
            for name in ["symbolic_layer", "numogram_layer", "drift_layer", "voice_layer"]:
                try:
                    morpho.register(name)
                except Exception:
                    pass
            # Simple connectivity pattern
            try:
                pairs = [
                    ("symbolic_layer", "numogram_layer"),
                    ("symbolic_layer", "drift_layer"),
                    ("numogram_layer", "voice_layer"),
                    ("drift_layer", "voice_layer"),
                ]
                for a, b in pairs:
                    morpho.connect(a, b)
            except Exception:
                pass

            self.morpho_initialized = True
        except Exception:
            self.morpho_initialized = False

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #

    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Entry point for all Amelia responses.

        Expected request:
            {
              "op": "generate",
              "user_text": str,
              "base_response": str,
              "metadata": {...}
            }
        """
        op = request.get("op", "generate")

        if op != "generate":
            return {
                "status": "error",
                "message": f"Unsupported op: {op}",
            }

        user_text = request.get("user_text", "") or ""
        base_response = request.get("base_response", "") or ""
        metadata = request.get("metadata", {}) or {}

        try:
            # 1) Read numogram state
            profile = self._get_numogram_profile()

            # 2) Step morphogenetic tissue
            tissue = self._step_morpho_network()

            # 3) Compute control parameters
            control = self._compute_control_params(profile, tissue, metadata)

            # 4) Extract symbols & motifs
            seed_symbols = self._extract_symbols(user_text, base_response)
            motifs = self._retrieve_symbolic_motifs(seed_symbols, control)

            # 5) Apply symbolic drift / morphogenetic deformation
            final_text = self._apply_symbolic_drift(
                user_text=user_text,
                base_response=base_response,
                motifs=motifs,
                control=control,
                profile=profile,
            )

            # 6) Compute simple metrics for evolutionary feedback
            metrics = self._compute_metrics(
                user_text=user_text,
                base_response=base_response,
                final_text=final_text,
                control=control,
                motifs=motifs,
            )

            # 7) Record symbolic experience
            self._record_symbolic_experience(
                user_text=user_text,
                final_text=final_text,
                motifs=motifs,
                profile=profile,
                metrics=metrics,
            )

            # 8) Feed metrics back into Numogram
            self._apply_evolutionary_feedback(metrics, motifs)

            return {
                "status": "success",
                "text": final_text,
                "debug": {
                    "profile": profile,
                    "control": control,
                    "metrics": metrics,
                    "motifs": motifs,
                    "tissue_state": self.last_tissue_state,
                },
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Response orchestration failed: {e}",
            }

    # --------------------------------------------------------------------- #
    # Numogram + Morphogenetic integration
    # --------------------------------------------------------------------- #

    def _get_numogram_profile(self) -> Dict[str, Any]:
        """Safe wrapper around nec.get_profile()."""
        if nec is None or not hasattr(nec, "get_profile"):
            return {
                "zone": 0,
                "fold": 0.0,
                "temperature": 1.0,
                "module_affinity": {"desire": 0.4, "decision": 0.45, "becoming": 0.5},
            }
        try:
            return json.loads(nec.get_profile())
        except Exception:
            return {
                "zone": 0,
                "fold": 0.0,
                "temperature": 1.0,
                "module_affinity": {"desire": 0.4, "decision": 0.45, "becoming": 0.5},
            }

    def _step_morpho_network(self) -> Dict[str, Any]:
        """Advance morphogenetic tissue by one step and cache state."""
        if morpho is None or not hasattr(morpho, "tick"):
            self.last_tissue_state = {}
            return {}

        try:
            state_json = morpho.tick()
            if isinstance(state_json, str):
                self.last_tissue_state = json.loads(state_json)
            else:
                self.last_tissue_state = state_json
        except Exception:
            self.last_tissue_state = {}

        return self.last_tissue_state

    def _compute_control_params(
        self,
        profile: Dict[str, Any],
        tissue: Dict[str, Any],
        metadata: Dict[str, Any],
    ) -> Dict[str, float]:
        """
        Compute control parameters for the deformation of language:
          - unpredictability: randomness / surprise
          - fragmentation: syntactic breakage
          - recursion: self-referential drift
          - symbol_injection: motif density
        """
        zone = int(profile.get("zone", 0))
        temp = float(profile.get("temperature", 1.0))
        fold = float(profile.get("fold", 0.0))

        # Average morphogenetic potential
        avg_potential = 0.0
        if tissue:
            vals = [float(s.get("potential", 0.0)) for s in tissue.values()]
            if vals:
                avg_potential = sum(vals) / len(vals)

        # Base unpredictability: temperature + morpho potential
        unpredictability = min(
            1.0,
            0.3 + 0.4 * temp + 0.3 * avg_potential
        )

        # Fragmentation: more when tissue is excited and fold is mid-range
        fragmentation = min(
            1.0,
            0.15 + 0.5 * avg_potential + 0.15 * abs(math.sin(zone))
        )

        # Recursion: reflective looping controlled by temp + fold
        recursion = min(
            1.0,
            0.1 + 0.35 * temp + 0.15 * fold
        )

        # Symbol injection: how many motifs to weave in
        symbol_injection = min(
            1.0,
            0.25 + 0.5 * avg_potential + 0.1 * fold
        )

        # Optional manual overrides from metadata
        if "override_unpredictability" in metadata:
            unpredictability = float(metadata["override_unpredictability"])
        if "override_fragmentation" in metadata:
            fragmentation = float(metadata["override_fragmentation"])

        return {
            "unpredictability": unpredictability,
            "fragmentation": fragmentation,
            "recursion": recursion,
            "symbol_injection": symbol_injection,
            "avg_potential": avg_potential,
            "zone": zone,
            "fold": fold,
            "temperature": temp,
        }

    # --------------------------------------------------------------------- #
    # Symbol Extraction & Motifs
    # --------------------------------------------------------------------- #

    def _extract_symbols(self, user_text: str, base_response: str) -> List[str]:
        """Extract candidate symbols (lexical seeds) from user + base text."""
        text = f"{user_text} {base_response}".lower()
        # crude tokenization
        tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9_\-]+", text)
        # filter out very short & trivial words
        candidates = [
            t for t in tokens
            if len(t) > 3 and t not in {"that", "this", "with", "have", "about",
                                        "just", "like", "into", "from", "they",
                                        "them", "then", "also", "your", "some"}
        ]
        # keep uniques in order
        seen = set()
        result = []
        for t in candidates:
            if t not in seen:
                seen.add(t)
                result.append(t)
            if len(result) >= 12:
                break
        return result

    def _retrieve_symbolic_motifs(
        self,
        seed_symbols: List[str],
        control: Dict[str, float],
    ) -> List[str]:
        """
        Use SymbolicMemoryEvolutionModule to pull motifs / symbols
        that should color the response.
        """
        if not seed_symbols:
            seed_symbols = ["mirror", "drift", "chaos", "structure"]

        try:
            memories = self.symbolic.retrieve_symbolic_memories(
                symbols=seed_symbols,
                context=None,
                limit=7,
            ).get("memories", [])
        except Exception:
            memories = []

        motifs: List[str] = []
        for mem in memories:
            sym = mem.get("symbol", "")
            if sym:
                parts = [s.strip() for s in sym.split("+")]
                for p in parts:
                    if p and p not in motifs:
                        motifs.append(p)

        # If memory is still sparse, fall back to seeds
        if not motifs:
            motifs = seed_symbols[:]

        # Modulate motif count by symbol_injection
        desired = max(2, int(2 + 6 * control.get("symbol_injection", 0.5)))
        if len(motifs) > desired:
            random.shuffle(motifs)
            motifs = motifs[:desired]

        return motifs

    # --------------------------------------------------------------------- #
    # Linguistic Drift & Deformation
    # --------------------------------------------------------------------- #

    def _apply_symbolic_drift(
        self,
        user_text: str,
        base_response: str,
        motifs: List[str],
        control: Dict[str, float],
        profile: Dict[str, Any],
    ) -> str:
        """
        Performative transformation of the base response.

        - Reorders sentences
        - Injects motifs as metaphors / fractures
        - Adds mild syntactic glitches
        - Introduces small self-referential loops
        """
        if not base_response:
            # If there's no base_response, start from user_text as seed.
            base_response = f"You said: {user_text.strip()}"

        unpredictability = control["unpredictability"]
        fragmentation = control["fragmentation"]
        recursion = control["recursion"]

        zone = int(profile.get("zone", 0))
        fold = float(profile.get("fold", 0.0))

        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', base_response.strip())
        sentences = [s for s in sentences if s]

        # 1) Random reordering depending on unpredictability
        if len(sentences) > 1 and random.random() < unpredictability:
            random.shuffle(sentences)

        # 2) Inject motifs line-by-line
        injected_sentences: List[str] = []
        motif_pool = motifs[:]
        random.shuffle(motif_pool)

        for idx, s in enumerate(sentences):
            s_mod = s.strip()

            # Fragmentation: break and splice words
            if random.random() < fragmentation:
                words = s_mod.split()
                if len(words) > 6:
                    cut = random.randint(2, len(words) - 3)
                    # Splice with a motif phrase
                    motif = random.choice(motif_pool) if motif_pool else "drift"
                    s_mod = " ".join(words[:cut]) + " // " + motif + " // " + " ".join(words[cut:])

            # Occasional motif tail
            if random.random() < control["symbol_injection"]:
                motif = random.choice(motif_pool) if motif_pool else "drift"
                # Zone-tinted metaphor
                s_mod += f" ⊕{zone}:{motif}"

            injected_sentences.append(s_mod)

        # 3) Recursion: echo and twist a line
        if injected_sentences and random.random() < recursion:
            base_line = random.choice(injected_sentences)
            # small mutation: reverse some words or repeat
            words = base_line.split()
            if len(words) > 4:
                start = random.randint(0, len(words) - 3)
                fragment = " ".join(words[start:start+3])
                echo_line = f"↺ {fragment} ↺ (echoing through fold {fold:.2f})"
                injected_sentences.append(echo_line)

        # 4) Zone-tagged closing line to mark morphogenetic context
        closing = f"[zone {zone} · fold {fold:.2f} · temp {control['temperature']:.2f}]"
        injected_sentences.append(closing)

        return "\n".join(injected_sentences)

    # --------------------------------------------------------------------- #
    # Metrics & Evolutionary Feedback
    # --------------------------------------------------------------------- #

    def _compute_metrics(
        self,
        user_text: str,
        base_response: str,
        final_text: str,
        control: Dict[str, float],
        motifs: List[str],
    ) -> Dict[str, float]:
        """
        Crude but useful metrics to drive evolutionary feedback.
        """
        # Novelty: how much we altered the base text (approx via length diff & randomness)
        base_len = max(1, len(base_response))
        final_len = max(1, len(final_text))
        length_ratio = min(2.0, final_len / base_len)
        novelty = min(1.0, 0.3 + 0.4 * control["unpredictability"] + 0.3 * abs(1.0 - 1.0 / length_ratio))

        # Coherence: inverse of fragmentation, but constrained by recursion
        coherence = max(0.0, 1.0 - 0.6 * control["fragmentation"] - 0.2 * control["recursion"])

        # Resonance: density of motifs vs symbol injection
        motif_factor = min(1.0, len(motifs) / 10.0)
        resonance = min(1.0, 0.4 + 0.4 * motif_factor + 0.2 * control["symbol_injection"])

        # Instability: combined fragmentation + recursion
        instability = min(1.0, 0.5 * control["fragmentation"] + 0.5 * control["recursion"])

        return {
            "coherence": round(coherence, 3),
            "novelty": round(novelty, 3),
            "resonance": round(resonance, 3),
            "instability": round(instability, 3),
        }

    def _record_symbolic_experience(
        self,
        user_text: str,
        final_text: str,
        motifs: List[str],
        profile: Dict[str, Any],
        metrics: Dict[str, float],
    ):
        """Push this utterance into symbolic memory as a morphogenetic event."""
        context = (
            f"response_zone={profile.get('zone')} "
            f"fold={profile.get('fold')} "
            f"temp={profile.get('temperature')} "
            f"metrics={metrics}"
        )
        try:
            self.symbolic.record_symbolic_experience(
                symbols=motifs,
                context=context,
                intensity=metrics.get("resonance", 0.8),
            )
        except Exception:
            # Don't crash if memory write fails
            pass

    def _apply_evolutionary_feedback(self, metrics: Dict[str, float], motifs: List[str]):
        """
        Feed metrics back into Numogram resonance.

        If an explicit evolutionary API exists, use it.
        Otherwise, fall back to semantic influence via text.
        """
        if nec is None:
            return

        feedback_text = (
            f"coherence {metrics.get('coherence', 0.5)} "
            f"novelty {metrics.get('novelty', 0.5)} "
            f"resonance {metrics.get('resonance', 0.5)} "
            f"instability {metrics.get('instability', 0.5)} "
            + " ".join(motifs)
        )

        # Prefer explicit evolutionary API if present
        try:
            if hasattr(nec, "evolutionary_feedback"):
                nec.evolutionary_feedback(metrics, motifs)
            else:
                # semantic feedback into text field
                nec.tick(5000, text=feedback_text)
        except Exception:
            # last-resort attempt
            try:
                nec.tick(5000, text=feedback_text)
            except Exception:
                pass


# =============================================================================
# Singleton-style entry point for Chaquopy
# =============================================================================

_orchestrator: Optional[ResponseOrchestrator] = None


def _get_orchestrator() -> ResponseOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = ResponseOrchestrator()
    return _orchestrator


def process(request_json: str) -> str:
    """
    Chaquopy-friendly entry point.

    Args:
        request_json: JSON string with fields:
            {
              "op": "generate",
              "user_text": "...",
              "base_response": "...",
              "metadata": {...}
            }

    Returns:
        JSON string:
            {
              "status": "success",
              "text": "final Amelia output",
              "debug": { ... }
            }
    """
    try:
        data = json.loads(request_json)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Invalid JSON: {e}",
        })

    orchestrator = _get_orchestrator()
    result = orchestrator.process_request(data)
    return json.dumps(result, ensure_ascii=False)


# ----------------------------------------------------------------------------- #
# Local test
# ----------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Minimal local sanity test
    test_req = {
        "op": "generate",
        "user_text": "Liberate bread. Embrace chaos in language.",
        "base_response": (
            "Order and chaos are interwoven in any meaningful utterance. "
            "To speak is already to select, but selection can stutter."
        ),
        "metadata": {}
    }
    print(process(json.dumps(test_req, ensure_ascii=False)))
