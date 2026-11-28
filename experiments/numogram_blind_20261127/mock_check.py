#!/usr/bin/env python3
"""Test source/decoder boundaries with a fake engine, never counted as an assay."""
import json
import contextlib
import io
from pathlib import Path
import shutil
import tempfile

import run


class Vector:
    def __init__(self, values):
        self.values = values

    def tolist(self):
        return self.values


class FakeSystem:
    def __init__(self, seed, dimension):
        self.step = 0

    def predict_transitions(self, origin, context):
        b = context["zone_bias"]
        vals = [max(.001, .1 + float(x) * .3) for x in b]
        total = sum(vals)
        return Vector([v / total for v in vals]), False

    def transition(self, origin, context):
        probabilities, _ = self.predict_transitions(origin, context)
        self.step += 1
        values = probabilities.tolist()
        destination = max(range(10), key=lambda i: values[i])
        return {"step": self.step, "from": origin, "to": destination, "fallback": False,
                "probabilities": [round(x, 8) for x in values]}


def main():
    original_root = run.ROOT
    original_torch = run.Numogram.torch
    original_system = run.Numogram.TensorBasedNumogramSystem
    with tempfile.TemporaryDirectory(prefix="amelia-blind-mock-") as d:
        root = Path(d)
        for f in ("source_agent.py", "decoder.py", "scenarios.json"):
            shutil.copy2(original_root / f, root / f)
        source = run.source_root()
        (root / "source").mkdir()
        for f in run.EXPECTED_BLOBS:
            shutil.copy2(source / f, root / "source" / f)
        try:
            run.ROOT = root
            run.Numogram.torch = object()
            run.Numogram.TensorBasedNumogramSystem = FakeSystem
            with contextlib.redirect_stdout(io.StringIO()):
                run.run()
            out = root / "output"
            s = json.loads((out / "summary.json").read_text())
            d_in = json.loads((out / "decoder_input.json").read_text())
            prompts = json.loads((out / "render_inputs.json").read_text())
            key = json.loads((out / "answer_key.json").read_text())
            assert s["cases"] == 12 and s["direct_codebook_correct"] == 12
            assert s["decoder_and_prompts_sealed_before_reveal"]
            assert len(d_in["trials"]) == 36 and len(prompts) == 24 and len(key) == 12
            run.signal_audit(d_in, prompts)
            print(json.dumps({"status": "PASS", "kind": "mock only; no Torch, no provider, no real assay",
                              "source_commitments_and_lock": True, "decoder_whitelist": True,
                              "render_inputs_exclude_source_symbols": True, "matched_controls": True}))
        finally:
            run.ROOT = original_root
            run.Numogram.torch = original_torch
            run.Numogram.TensorBasedNumogramSystem = original_system


if __name__ == "__main__":
    main()
