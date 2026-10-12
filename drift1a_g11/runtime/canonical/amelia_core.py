"""
amelia_core.py -- Android Amelia 1.0, milestone M1.1.

Startup integrity has two distinct layers which must not be conflated:

1. Exact canonical-source verification (required for ACCEPTED).  The three canonical
   modules must hash byte-for-byte to canonical_manifest.json.  In CI/desktop the bytes
   are read from ordinary files.  In the Android APK, Chaquopy keeps .py sources and the
   bytes are read through each module's import loader, i.e. from the same source object
   the interpreter loads.
2. Packaged-operational diagnostics (retained from M1).  If exact source bytes cannot be
   recovered, the code can still report whether the packaged modules import and whether
   their canonical graph identities are operationally correct.  This diagnostic path is
   intentionally NOT sufficient for startup acceptance in M1.1.

Standard library only.
"""

from __future__ import annotations

import hashlib
import importlib
import importlib.util
import json
import os
import platform
import sys

VERSION = "amelia-1.0-M1.1"
HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST_FILE = "canonical_manifest.json"


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256(path: str) -> str:
    with open(path, "rb") as fh:
        return _sha256_bytes(fh.read())


def load_manifest(root: str = HERE) -> dict:
    with open(os.path.join(root, MANIFEST_FILE), encoding="utf-8") as fh:
        return json.load(fh)


def module_bytes(name: str, root: str = HERE):
    """Return "(bytes, source)" for a canonical module source file.

    Source checkout / CI:
      read the real "root/name" file directly.

    Packaged Android runtime:
      resolve the import spec and ask its loader for "spec.origin" bytes.  M1.1 builds
      set Chaquopy "pyc.src = false", so a valid packaged origin must still be the named
      ".py" source rather than ".pyc" bytecode.

    Returns "(None, reason)" if exact source bytes cannot be established.
    """
    path = os.path.join(root, name)
    if os.path.isfile(path):
        with open(path, "rb") as fh:
            return fh.read(), "file"

    stem = name[:-3] if name.endswith(".py") else name
    if root not in sys.path:
        sys.path.insert(0, root)

    spec = importlib.util.find_spec(stem)
    if spec is None or spec.origin is None or spec.loader is None:
        return None, "module not found"

    if os.path.basename(spec.origin) != name:
        return None, "loader origin is %s, not sealed source %s" % (
            os.path.basename(spec.origin), name
        )

    get_data = getattr(spec.loader, "get_data", None)
    if get_data is None:
        return None, "loader cannot return source bytes"

    try:
        return get_data(spec.origin), "loader"
    except Exception as exc:
        return None, "%s: %s" % (type(exc).__name__, exc)


def _exact_module_status(root: str, manifest: dict) -> dict:
    modules = {}
    for name, want in sorted(manifest["modules"].items()):
        data, source = module_bytes(name, root)
        got = _sha256_bytes(data) if data is not None else None
        modules[name] = {
            "expected": want,
            "actual": got,
            "match": got == want,
            "source": source,
            "verification": "exact-source-bytes",
        }
    return modules


def packaged_operational_status(root: str = HERE) -> dict:
    """Retained M1 diagnostic; importability only, never sufficient for ACCEPTED in M1.1."""
    manifest = load_manifest(root)
    modules = {}
    if root not in sys.path:
        sys.path.insert(0, root)
    for name in sorted(manifest["modules"]):
        stem = name[:-3] if name.endswith(".py") else name
        try:
            mod = importlib.import_module(stem)
            modules[name] = {
                "match": True,
                "verification": "packaged-import",
                "origin": getattr(mod, "__file__", None),
            }
        except Exception as exc:
            modules[name] = {
                "match": False,
                "verification": "packaged-import",
                "reason": "%s: %s" % (type(exc).__name__, exc),
            }
    return modules


def _canonical_operational_identity(root: str, manifest: dict) -> dict:
    if root not in sys.path:
        sys.path.insert(0, root)

    import CanonicalNumogram as C
    import NumogramDynamics as D
    import NumogramInterface as I  # noqa: F401 -- import is part of runtime validation

    digest = C.CanonicalNumogram().digest()
    graph = D.canonical_graph()
    counts = {}
    for e in graph.edges:
        counts[e.type] = counts.get(e.type, 0) + 1

    graph_digest = graph.digest()
    ok = (
        digest == manifest["canonical_digest"]
        and counts == manifest["edge_counts"]
        and graph_digest == manifest["graph_digest"]
    )
    return {
        "ok": ok,
        "canonical_digest": digest,
        "edge_counts": counts,
        "edges": len(graph.edges),
        "graph_digest": graph_digest,
    }


def check(root: str = HERE) -> dict:
    """Require exact module bytes, then verify canonical operational identity."""
    manifest = load_manifest(root)
    modules = _exact_module_status(root, manifest)
    exact_ok = all(m["match"] for m in modules.values())

    result = {
        "version": VERSION,
        "modules": modules,
        "integrity_mode": "exact-source-bytes",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }

    if not exact_ok:
        result["packaged_operational"] = packaged_operational_status(root)
        result.update(
            ok=False,
            status="REFUSED",
            reason="canonical module digest mismatch or exact source bytes unavailable",
        )
        return result

    identity = _canonical_operational_identity(root, manifest)
    result.update({k: v for k, v in identity.items() if k != "ok"})
    result.update(
        ok=identity["ok"],
        status="ACCEPTED" if identity["ok"] else "REFUSED",
        reason=None if identity["ok"] else "canonical Numogram digest, graph digest or edge counts differ",
    )
    return result


def startup_check() -> str:
    """Entry point for the Android layer; returns JSON."""
    try:
        return json.dumps(check(), sort_keys=True)
    except Exception as exc:
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
