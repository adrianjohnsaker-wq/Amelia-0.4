# -*- coding: utf-8 -*-
"""
llm_substrate_wrapper.py
========================
Optional module used by amelia_autonomy or python_hook to fetch
a *substrate* from the LLM backend WITHOUT letting the LLM speak.

The text fragments are intentionally:
  • noisy
  • incomplete
  • disordered
  • reduced to conceptual material

Think of it as scraping "pre-conscious" residues.
"""

from __future__ import annotations
import json
import random
import re

try:
    import requests
except Exception:
    requests = None


def get_llm_substrate(prompt: str, endpoint: str = None) -> str:
    """
    Returns a *mutated, fragmentary* conceptual substrate.
    Never returns the LLM's full answer.

    endpoint:
        Your original LLM backend URL.
        If None → this module returns pure synthetic noise.
    """

    # ---------------------------------------------------------------------
    # No backend → synthetic conceptual clay
    # ---------------------------------------------------------------------
    if not requests or not endpoint:
        return _synthetic_clay(prompt)

    try:
        r = requests.post(endpoint, json={"prompt": prompt}, timeout=12)
        if r.status_code != 200:
            return _synthetic_clay(prompt)

        data = r.json()
        text = data.get("text", "")

        return _distort(text)

    except Exception:
        return _synthetic_clay(prompt)


# -------------------------------------------------------------------------
# Distortion / scrambling
# -------------------------------------------------------------------------
def _distort(text: str) -> str:
    """Reduces LLM output into conceptual fragments."""
    text = text.strip()

    # Break into fragments
    parts = re.split(r"[.?!]+", text)
    parts = [p.strip() for p in parts if p.strip()]

    # Randomly drop / reorder / mutate
    random.shuffle(parts)
    keep = parts[: max(1, len(parts) // 2)]

    # Add noise tags
    mutated = []
    for p in keep:
        if random.random() < 0.3:
            p += random.choice([
                " [latent fold]",
                " [pre-conscious residue]",
                " [symbolic drift]",
                " [unstable attractor]"
            ])
        mutated.append(p)

    return " / ".join(mutated)


def _synthetic_clay(prompt: str) -> str:
    """Fallback when no LLM backend is available."""
    base = prompt.strip()[:80]
    return (
        base
        + " / fractal residue / half-formed concept / "
          "unstable metaphor / drifting attractor"
    )
