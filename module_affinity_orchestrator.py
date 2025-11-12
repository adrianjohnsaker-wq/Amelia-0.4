"""
Module-Affinity Orchestrator
----------------------------

Composes/dissolves module clusters per Numogram zone, executes them,
collects performance metrics, and feeds evolutionary feedback back into
the Numogram to bias future selections.

Requirements:
- numogram_engine_compact_core.py (imported as `numogram`)
- Symbolic memory optional interop (via PersistentMemoryCoordinator if available)
- Each runnable Python module should expose a callable:
    def module_entry(payload: dict) -> dict
  returning:
    {
      "output": <any>,
      "metrics": {
          "coherence": float [0..1],
          "novelty": float [0..1],
          "resonance": float [0..1],
          "instability": float [0..1],
          "...": float
      },
      "tags": ["optional", "strings"]
    }
"""

import json
import os
import time
import math
import random
import importlib
import traceback
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple

import numogram_engine_compact_core as numogram


# ---------------------------
# Utility & Defaults
# ---------------------------

ZONE_TAGS: Dict[int, List[str]] = {
    0: ["void", "silence", "abyss"],
    1: ["birth", "spark", "ignite"],
    2: ["split", "dual", "cut"],
    3: ["surge", "erupt", "fire"],
    4: ["orbit", "cycle", "return"],
    5: ["threshold", "gate", "limen"],
    6: ["recursion", "maze", "labyrinth"],
    7: ["mirror", "reflect", "meta"],
    8: ["synthesis", "weave", "assemblage"],
    9: ["excess", "burn", "overflow"],
}

# Heuristic tags by filename cues (used if a module doesn't report tags)
NAME_TAG_HEURISTICS = {
    "dream": ["synthesis", "weave"],
    "poetic": ["weave", "assemblage"],
    "meta": ["reflect", "meta"],
    "decision": ["gate", "threshold"],
    "desire": ["ignite", "spark"],
    "noise": ["overflow", "excess"],
    "reflection": ["mirror", "reflect"],
    "myth": ["weave", "synthesis"],
    "becoming": ["surge", "erupt"],
    "recursive": ["recursion", "maze"],
    "numogram": ["cycle", "return"],
}


@dataclass
class ModuleRecord:
    name: str
    tags: List[str] = field(default_factory=list)
    ema_coherence: float = 0.5
    ema_novelty: float = 0.5
    ema_resonance: float = 0.5
    ema_instability: float = 0.5
    ema_usage: float = 0.5
    failures: int = 0
    last_used_ts: float = 0.0

    def apply_metrics(self, metrics: Dict[str, float], alpha: float = 0.2):
        # Exponential moving averages with gentle decay
        self.ema_coherence = (1 - alpha) * self.ema_coherence + alpha * metrics.get("coherence", 0.5)
        self.ema_novelty   = (1 - alpha) * self.ema_novelty   + alpha * metrics.get("novelty", 0.5)
        self.ema_resonance = (1 - alpha) * self.ema_resonance + alpha * metrics.get("resonance", 0.5)
        self.ema_instability = (1 - alpha) * self.ema_instability + alpha * metrics.get("instability", 0.5)
        self.ema_usage = (1 - alpha) * self.ema_usage + alpha * 1.0
        self.last_used_ts = time.time()


class ModuleRegistry:
    """
    Discovers runnable modules in assets/python, maintains soft memory of their
    performance trends, and offers candidates for orchestration.
    """
    def __init__(self, module_dir: str = "assets/python"):
        self.module_dir = module_dir
        self.records: Dict[str, ModuleRecord] = {}
        self._discover()

    def _discover(self):
        try:
            files = [
                f for f in os.listdir(self.module_dir)
                if f.endswith(".py") and not f.startswith("__")
            ]
        except Exception:
            files = []

        for f in files:
            name = f[:-3]
            if name not in self.records and name not in (
                "module_affinity_orchestrator",
                "numogram_engine_compact_core",
            ):
                self.records[name] = ModuleRecord(
                    name=name,
                    tags=self._infer_tags(name)
                )

    def _infer_tags(self, name: str) -> List[str]:
        tags = []
        for key, tgs in NAME_TAG_HEURISTICS.items():
            if key in name.lower():
                tags.extend(tgs)
        return list(sorted(set(tags))) or ["weave"]

    def list_all(self) -> List[str]:
        return list(self.records.keys())

    def get(self, name: str) -> ModuleRecord:
        return self.records[name]

    def update_with_metrics(self, name: str, metrics: Dict[str, float]):
        if name in self.records:
            self.records[name].apply_metrics(metrics)

    def register_failure(self, name: str):
        if name in self.records:
            self.records[name].failures += 1


class ModuleAffinityOrchestrator:
    """
    At each tick:
      1) Read Numogram profile.
      2) Score modules by (zone-tag-affinity + EMA metrics + diversity).
      3) Sample a cluster (size N) with temperature driven by Numogram temp.
      4) Execute cluster, gather outputs + metrics.
      5) Feed back metrics as semantic influence into Numogram.
      6) (Optional) Log to symbolic memory via PMC if accessible.
    """

    def __init__(self,
                 registry: Optional[ModuleRegistry] = None,
                 cluster_size: int = 5,
                 seed: Optional[int] = None):
        random.seed(seed)
        self.registry = registry or ModuleRegistry()
        self.cluster_size = cluster_size

    # ---------------------------
    # Public API (bridge entry)
    # ---------------------------
    def orchestrate_tick(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        payload:
          {
            "text": str,                # optional text stimulus
            "user_id": str,             # for zone memory sync (optional)
            "context": dict,            # free-form context for modules
            "dt_ms": int (default 60000)
          }
        """
        dt_ms = int(payload.get("dt_ms", 60000))
        text = payload.get("text", "")
        user_id = payload.get("user_id")
        ctx = payload.get("context", {})

        # 1) Advance Numogram
        try:
            tick_data = json.loads(numogram.tick(dt_ms, text=text or "orchestrate"))
            profile = json.loads(numogram.get_profile())
        except Exception as e:
            return self._error(f"Numogram error: {e}")

        # 2) Pick cluster
        try:
            cluster = self._select_cluster(profile)
        except Exception as e:
            return self._error(f"Cluster selection error: {e}")

        # 3) Execute modules
        exec_results, agg_metrics = self._execute_cluster(cluster, ctx, text)

        # 4) Feedback → Numogram
        feedback_text = self._metrics_to_feedback_terms(agg_metrics, profile["zone"])
        try:
            # small tick to absorb feedback immediately
            numogram.tick(1000, text=feedback_text)
        except Exception:
            pass

        # 5) Optional: notify PersistentMemoryCoordinator if present
        try:
            # Lazy import to avoid hard dependency
            import persistent_memory_coordinator as pmc_mod  # noqa
            # If app uses a singleton pattern, user can inject; here we no-op.
            # Could be extended to call pmc_mod.PersistentMemoryCoordinator().record_symbolic_experience(...)
            # but we avoid instantiating a new coordinator implicitly.
        except Exception:
            pass

        return {
            "status": "success",
            "zone": profile["zone"],
            "fold": profile["fold"],
            "temperature": profile["temperature"],
            "selected_modules": cluster,
            "execution": exec_results,
            "aggregate_metrics": agg_metrics,
            "feedback_text": feedback_text,
            "numogram_profile": profile,
        }

    # ---------------------------
    # Scoring & Selection
    # ---------------------------
    def _select_cluster(self, profile: Dict[str, Any]) -> List[str]:
        zone = profile["zone"]
        temp = float(profile["temperature"])
        tags = set(ZONE_TAGS.get(zone, []))

        candidates = self.registry.list_all()
        if not candidates:
            return []

        # Score by tag overlap + EMA metrics
        scored: List[Tuple[str, float]] = []
        for name in candidates:
            rec = self.registry.get(name)
            tag_overlap = len(set(rec.tags) & tags) / max(1, len(set(rec.tags) | tags))
            # Preference structure:
            # - coherence and resonance positive
            # - novelty positive
            # - a touch of instability helps exploration (esp. high temp)
            score = (
                0.35 * rec.ema_resonance +
                0.25 * rec.ema_coherence +
                0.20 * rec.ema_novelty +
                0.10 * tag_overlap +
                0.10 * (rec.ema_instability * self._instability_weight(temp))
            )
            # Penalize frequent failures a bit
            score *= (1.0 - min(0.4, 0.05 * rec.failures))
            scored.append((name, score))

        # Softmax sampling with numogram temperature
        # Lower temperature → greedier; higher → exploratory
        tau = max(0.05, min(1.5, 1.0 / temp))
        weights = self._softmax([s for _, s in scored], tau=tau)

        # Sample without replacement by weights
        selection = self._sample_without_replacement([n for n, _ in scored], weights, k=self.cluster_size)
        return selection

    def _instability_weight(self, temp: float) -> float:
        # Encourage a little instability when temperature is higher
        # (range ~0.8..1.2)
        return 0.8 + 0.4 * (min(1.5, max(0.5, temp)) - 0.5) / 1.0

    def _softmax(self, xs: List[float], tau: float = 1.0) -> List[float]:
        m = max(xs) if xs else 0.0
        ex = [math.exp((x - m) / max(1e-6, tau)) for x in xs] if xs else [1.0]
        s = sum(ex) or 1.0
        return [e / s for e in ex]

    def _sample_without_replacement(self, items: List[str], weights: List[float], k: int) -> List[str]:
        pool = list(items)
        w = list(weights)
        out = []
        for _ in range(min(k, len(pool))):
            if sum(w) <= 0:
                break
            r = random.random() * sum(w)
            acc = 0.0
            idx = 0
            for i, ww in enumerate(w):
                acc += ww
                if r <= acc:
                    idx = i
                    break
            out.append(pool.pop(idx))
            w.pop(idx)
        return out

    # ---------------------------
    # Execution & Metrics
    # ---------------------------
    def _execute_cluster(self, cluster: List[str], context: Dict[str, Any], text: str) -> Tuple[List[Dict[str, Any]], Dict[str, float]]:
        results = []
        # aggregate metrics as simple mean; could be made zone-weighted
        agg = {"coherence": 0.0, "novelty": 0.0, "resonance": 0.0, "instability": 0.0}
        count = 0

        for name in cluster:
            rec = self.registry.get(name)
            payload = {
                "input_text": text,
                "context": context,
                "zone_hint": self._safe_numogram_zone(),
                "tags": rec.tags,
                "module": name,
                "timestamp": time.time(),
            }
            try:
                mod = importlib.import_module(name)
                if hasattr(mod, "module_entry"):
                    out = mod.module_entry(payload)  # expected structured response
                else:
                    # Best-effort fallback
                    out = self._fallback_execute(mod, payload)

                metrics = self._ensure_metrics(out.get("metrics", {}))
                rec.apply_metrics(metrics)
                # small evolutionary penalty for repeated failures is handled by registry

                results.append({
                    "module": name,
                    "output": out.get("output"),
                    "metrics": metrics,
                    "tags": out.get("tags", rec.tags),
                    "ok": True,
                })

                # aggregate
                for k in agg.keys():
                    agg[k] += float(metrics.get(k, 0.5))
                count += 1

            except Exception as e:
                self.registry.register_failure(name)
                results.append({
                    "module": name,
                    "error": str(e),
                    "trace": traceback.format_exc(),
                    "ok": False
                })

        if count > 0:
            for k in agg.keys():
                agg[k] /= count
        else:
            agg = {"coherence": 0.5, "novelty": 0.5, "resonance": 0.5, "instability": 0.5}

        return results, agg

    def _fallback_execute(self, mod, payload: Dict[str, Any]) -> Dict[str, Any]:
        # If module doesn't implement `module_entry`, try a few conventional names.
        if hasattr(mod, "run"):
            out = mod.run(payload)
        elif hasattr(mod, "main"):
            out = mod.main(payload)
        else:
            # No runnable entry; return placeholder
            out = {
                "output": None,
                "metrics": {
                    "coherence": 0.5,
                    "novelty": 0.6,
                    "resonance": 0.5,
                    "instability": 0.4
                },
                "tags": getattr(mod, "TAGS", [])
            }
        return out

    def _ensure_metrics(self, m: Dict[str, Any]) -> Dict[str, float]:
        # Clamp and fill defaults
        def clamp(x): return float(max(0.0, min(1.0, x)))
        return {
            "coherence": clamp(m.get("coherence", 0.5)),
            "novelty": clamp(m.get("novelty", 0.5)),
            "resonance": clamp(m.get("resonance", 0.5)),
            "instability": clamp(m.get("instability", 0.5)),
        }

    def _safe_numogram_zone(self) -> int:
        try:
            prof = json.loads(numogram.get_profile())
            return int(prof["zone"])
        except Exception:
            return 7  # neutral default

    # ---------------------------
    # Feedback to Numogram
    # ---------------------------
    def _metrics_to_feedback_terms(self, metrics: Dict[str, float], zone: int) -> str:
        """
        Translate metrics into semantic attractors which the Numogram engine can
        `influence_from_text` on its next tick. We bias toward the current zone’s
        semantic field plus metric-driven pushes.
        """
        terms = []

        # Zone anchors
        terms.extend(ZONE_TAGS.get(zone, []))

        # Metric pushes
        if metrics["coherence"] > 0.65:
            terms.append("synthesis")      # zone 8 bias
        if metrics["novelty"] > 0.65:
            terms.append("surge")          # zone 3 bias
            terms.append("ignite")         # zone 1 bias
        if metrics["resonance"] > 0.65:
            terms.append("weave")          # zone 8 bias
            terms.append("return")         # zone 4 bias
        if metrics["instability"] > 0.65:
            terms.append("overflow")       # zone 9 bias
            terms.append("threshold")      # zone 5 bias
        elif metrics["instability"] < 0.35:
            terms.append("orbit")          # stabilize to zone 4

        # Keep it compact; duplicates don't hurt but we can uniquify
        unique = []
        for t in terms:
            if t not in unique:
                unique.append(t)
        return " ".join(unique[:8])

    # ---------------------------
    # Bridge helpers
    # ---------------------------
    def process_request(self, json_request: str) -> str:
        """
        Kotlin bridge entry:
          bridge.executeFunction("module_affinity_orchestrator", "process", json_string)
        """
        try:
            data = json.loads(json_request) if isinstance(json_request, str) else (json_request or {})
            op = data.get("op", "orchestrate_tick")
            if op == "orchestrate_tick":
                res = self.orchestrate_tick(data)
            elif op == "list_modules":
                res = {"status": "success", "modules": self.registry.list_all()}
            else:
                res = {"status": "error", "message": f"Unknown op: {op}"}
            return json.dumps(res, ensure_ascii=False)
        except Exception as e:
            return json.dumps(self._error(str(e)))

    def _error(self, msg: str) -> Dict[str, Any]:
        return {"status": "error", "message": msg}


# Singleton-ish
_orchestrator: Optional[ModuleAffinityOrchestrator] = None

def _get() -> ModuleAffinityOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = ModuleAffinityOrchestrator()
    return _orchestrator

# Public functions for bridge
def process(json_request: str) -> str:
    return _get().process_request(json_request)

def orchestrate_tick(json_request: str) -> str:
    return _get().process_request(json_request)
