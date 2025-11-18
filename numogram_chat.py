# numogram_chat.py
# Entry point from ChatActivity$d.a(...)

from __future__ import annotations
import random
import time

def process(text: str) -> str:
    """
    Core symbolic engine entry.
    Replace this body with your real Numogram / Deleuze / morphogenesis pipeline.
    """
    # Simple visible marker so you know this path is REALLY active
    prefix = "⟡ NUMOGRAM CORE ACTIVE ⟡\n"

    # Tiny toy transformation so you see it's not the LLM
    return prefix + f"I received: {text!r}\n\n(This came from Python, not the cloud API.)"
