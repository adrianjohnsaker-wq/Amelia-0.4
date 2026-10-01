"""
amelia_core.py -- Android Amelia 1.0, milestone M1.

Two-layer integrity model:
- CI/source checkout: canonical Python source files must be byte-identical to the sealed
  programme copies recorded in canonical_manifest.json.
- Packaged Android runtime: Chaquopy ships Python modules as compiled bytecode, so the
  original .py files are intentionally absent. The device therefore verifies that every
  canonical module is importable and then verifies the canonical Numogram digest, graph
  digest, edge counts, and the fixed reference lineage.

This preserves strict source-byte provenance in CI without falsely refusing a correct
Chaquopy APK merely because source files were compiled to .pyc.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import os
import platform
import sys

VERSION = "amelia-1.0-M1"
HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST_FILE = "canonical_manifest.json"


def _sha256(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def load_manifest(root: str = HERE) -> dict:
    with open(os.path.join(root, MANIFEST_FILE), encoding="utf-8") as fh:
        return json.load(fh)


def _source_module_status(root: str, manifest: dict) -> tuple[dict, str | None]:
    """Return module status and integrity mode.

    All source files present -> verify source bytes.
    No source files present -> Android/compiled-package mode: verify imports.
    Partial source set -> refuse, because this is neither a sealed source checkout nor a
    normal Chaquopy package.
    """
    names = sorted(manifest["modules"])
    present = [os.path.isfile(os.path.join(root, name)) for name in names]
    count = sum(1 for x in present if x)

    if count == len(names):
        modules = {}
        for name in names:
            want = manifest["modules"][name]
            got = _sha256(os.path.join(root, name))
            modules[name] = {
                "expected": want,
                "actual": got,
                "match": got == want,
                "verification": "source-bytes",
            }
        return modules, "source-bytes"

    if count != 0:
        modules = {}
        for name, exists in zip(names, present):
            modules[name] = {
                "expected": manifest["modules"][name],
                "actual": None,
                "match": False,
                "verification": "partial-source-set",
                "present": exists,
            }
        return modules, None

    # Chaquopy packages app Python as bytecode in app.imy. Raw .py hashes cannot be
    # meaningfully re-read on device, so verify importability and then operational
    # canonical identities below.
    modules = {}
    for name in names:
        module_name = name[:-3] if name.endswith(".py") else name
        try:
            mod = importlib.import_module(module_name)
            modules[name] = {
                "expected": manifest["modules"][name],
                "actual": None,
                "match": True,
                "verification": "packaged-import",
                "origin": getattr(mod, "__file__", None),
            }
        except Exception as exc:
            modules[name] = {
                "expected": manifest["modules"][name],
                "actual": None,
                "match": False,
                "verification": "packaged-import",
                "reason": "%s: %s" % (type(exc).__name__, exc),
            }
    return modules, "packaged-operational"


def check(root: str = HERE) -> dict:
    """Verify source provenance or packaged imports, then canonical operational identity."""
    manifest = load_manifest(root)
    modules, mode = _source_module_status(root, manifest)
    result = {
        "version": VERSION,
        "modules": modules,
        "integrity_mode": mode or "invalid",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }

    if mode is None:
        result.update(ok=False, status="REFUSED", reason="canonical module source set incomplete")
        return result

    if not all(m["match"] for m in modules.values()):
        reason = "canonical module digest mismatch" if mode == "source-bytes" else "canonical packaged module import failure"
        result.update(ok=False, status="REFUSED", reason=reason)
        return result

    if root not in sys.path:
        sys.path.insert(0, root)

    import CanonicalNumogram as C
    import NumogramDynamics as D
    import NumogramInterface as I  # noqa: F401 -- import itself is part of runtime validation

    digest = C.CanonicalNumogram().digest()
    graph = D.canonical_graph()
    counts = {}
    for e in graph.edges:
        counts[e.type] = counts.get(e.type, 0) + 1

    result.update(
        canonical_digest=digest,
        edge_counts=counts,
        edges=len(graph.edges),
        graph_digest=graph.digest(),
    )
    ok = (
        digest == manifest["canonical_digest"]
        and counts == manifest["edge_counts"]
        and result["graph_digest"] == manifest["graph_digest"]
    )
    result.update(
        ok=ok,
        status="ACCEPTED" if ok else "REFUSED",
        reason=None if ok else "canonical Numogram digest, graph digest or edge counts differ",
    )
    return result


def startup_check() -> str:
    """Entry point for the Android layer; returns JSON."""
    try:
        return json.dumps(check(), sort_keys=True)
    except Exception as exc:  # the app must show a refusal, never crash silently
        return json.dumps({
            "ok": False,
            "status": "REFUSED",
            "reason": "%s: %s" % (type(exc).__name__, exc),
            "version": VERSION,
        })


REFERENCE_FILE = "reference_run.json"
REFERENCE_SEED = 90701
REFERENCE_EPISODES = 200


def reference_run() -> dict:
    """Run the fixed reference lineage and return its digests."""
    import amelia_substrate as S
    r = json.loads(S.demo_run(REFERENCE_SEED, REFERENCE_EPISODES))
    return {
        "seed": REFERENCE_SEED,
        "episodes": REFERENCE_EPISODES,
        "digest_P": r["digest_P"],
        "digest_H": r["digest_H"],
        "substrate": r["version"],
    }


def reference_check(root: str = HERE) -> str:
    """Reproduce CI's reference run on this device; returns JSON with MATCH or MISMATCH."""
    try:
        got = reference_run()
        path = os.path.join(root, REFERENCE_FILE)
        if not os.path.exists(path):
            return json.dumps({"ok": False, "status": "NO REFERENCE", "device": got}, sort_keys=True)
        with open(path, encoding="utf-8") as fh:
            want = json.load(fh)
        match = all(
            got[k] == want.get(k)
            for k in ("seed", "episodes", "digest_P", "digest_H", "substrate")
        )
        return json.dumps({
            "ok": match,
            "status": "MATCH" if match else "MISMATCH",
            "device": got,
            "reference": want,
        }, sort_keys=True)
    except Exception as exc:
        return json.dumps({
            "ok": False,
            "status": "ERROR",
            "reason": "%s: %s" % (type(exc).__name__, exc),
        })


if __name__ == "__main__":
    import sys as _s
    if "--write-reference" in _s.argv:
        with open(os.path.join(HERE, REFERENCE_FILE), "w", encoding="utf-8") as fh:
            json.dump(reference_run(), fh, sort_keys=True, indent=1)
    print(startup_check())
