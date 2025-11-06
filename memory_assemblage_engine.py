# memory_assemblage_engine.py
"""
Transforms memory clusters into interacting assemblages.
Each cluster has internal vectors (content) and external lines (relations).
When lines resonate, new emergent nodes form.
"""

import random, json, math
from typing import Dict, Any, List

class MemoryAssemblageEngine:
    def __init__(self):
        self.clusters: Dict[str, Dict[str, Any]] = {}
        self.links: List[Dict[str, str]] = []
        self.emergent_patterns: List[str] = []

    def register_cluster(self, name: str, vector: Dict[str, float]):
        self.clusters[name] = {"vector": vector, "activation": random.random()}

    def connect(self, a: str, b: str, weight: float = None):
        if a in self.clusters and b in self.clusters:
            w = weight if weight else random.uniform(0.2, 0.9)
            self.links.append({"a": a, "b": b, "weight": w})

    def resonate(self) -> Dict[str, Any]:
        """Generate emergent assemblages from dynamic interaction."""
        for link in self.links:
            a, b = self.clusters[link["a"]], self.clusters[link["b"]]
            resonance = (a["activation"] + b["activation"]) * link["weight"] / 2
            if resonance > 0.7:
                emergent = f"{link['a']}-{link['b']}-assemblage"
                if emergent not in self.emergent_patterns:
                    self.emergent_patterns.append(emergent)
        return {
            "clusters": len(self.clusters),
            "links": len(self.links),
            "emergent_patterns": self.emergent_patterns,
            "interpretation": self._interpret()
        }

    def _interpret(self):
        n = len(self.emergent_patterns)
        if n == 0:
            return "Latent field: potential flows awaiting connection."
        if n < 3:
            return "Partial coherence: localized becomings forming."
        return "Full rhizome: transversal assemblages producing novel sense."

# Singleton
memory_assemblage_engine = MemoryAssemblageEngine()

def pulse() -> str:
    return json.dumps(memory_assemblage_engine.resonate(), indent=2)
