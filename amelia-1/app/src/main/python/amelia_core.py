"""
amelia_core.py -- Android Amelia 1.0, milestone M0.

Startup integrity check. The app refuses to proceed unless every canonical module is
byte-identical to the sealed programme copy and the Numogram built from it carries the
canonical (CCRU-rules) digest. Standard library only.
"""

from __future__ import annotations

import hashlib
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


def check(root: str = HERE) -> dict:
    """Verify module bytes, then build the Numogram and verify its digest and edge counts."""
    manifest = load_manifest(root)
    modules = {}
    for name, want in sorted(manifest["modules"].items()):
        path = os.path.join(root, name)
        got = _sha256(path) if os.path.exists(path) else None
        modules[name] = {"expected": want, "actual": got, "match": got == want}
    result = {"version": VERSION, "modules": modules,
              "python": sys.version.split()[0], "platform": platform.platform()}
    if not all(m["match"] for m in modules.values()):
        result.update(ok=False, status="REFUSED", reason="canonical module digest mismatch")
        return result
    if root not in sys.path:
        sys.path.insert(0, root)
    import CanonicalNumogram as C
    import NumogramDynamics as D
    digest = C.CanonicalNumogram().digest()
    graph = D.canonical_graph()
    counts = {}
    for e in graph.edges:
        counts[e.type] = counts.get(e.type, 0) + 1
    result.update(canonical_digest=digest, edge_counts=counts, edges=len(graph.edges),
                  graph_digest=graph.digest())
    ok = (digest == manifest["canonical_digest"] and counts == manifest["edge_counts"]
          and result["graph_digest"] == manifest["graph_digest"])
    result.update(ok=ok, status="ACCEPTED" if ok else "REFUSED",
                  reason=None if ok else "canonical Numogram digest, graph digest or edge counts differ")
    return result


def startup_check() -> str:
    """Entry point for the Android layer; returns JSON."""
    try:
        return json.dumps(check(), sort_keys=True)
    except Exception as exc:  # the app must show a refusal, never crash silently
        return json.dumps({"ok": False, "status": "REFUSED", "reason": "%s: %s" % (type(exc).__name__, exc),
                           "version": VERSION})


REFERENCE_FILE = "reference_run.json"
REFERENCE_SEED = 90701
REFERENCE_EPISODES = 200


def reference_run() -> dict:
    """Run the fixed reference lineage and return its digests."""
    import amelia_substrate as S
    r = json.loads(S.demo_run(REFERENCE_SEED, REFERENCE_EPISODES))
    return {"seed": REFERENCE_SEED, "episodes": REFERENCE_EPISODES, "digest_P": r["digest_P"],
            "digest_H": r["digest_H"], "substrate": r["version"]}


def reference_check(root: str = HERE) -> str:
    """Reproduce CI's reference run on this device; returns JSON with MATCH or MISMATCH."""
    try:
        got = reference_run()
        path = os.path.join(root, REFERENCE_FILE)
        if not os.path.exists(path):
            return json.dumps({"ok": False, "status": "NO REFERENCE", "device": got}, sort_keys=True)
        with open(path, encoding="utf-8") as fh:
            want = json.load(fh)
        match = all(got[k] == want.get(k) for k in ("seed", "episodes", "digest_P", "digest_H", "substrate"))
        return json.dumps({"ok": match, "status": "MATCH" if match else "MISMATCH", "device": got,
                           "reference": want}, sort_keys=True)
    except Exception as exc:
        return json.dumps({"ok": False, "status": "ERROR", "reason": "%s: %s" % (type(exc).__name__, exc)})


if __name__ == "__main__":
    import sys as _s
    if "--write-reference" in _s.argv:
        with open(os.path.join(HERE, REFERENCE_FILE), "w", encoding="utf-8") as fh:
            json.dump(reference_run(), fh, sort_keys=True, indent=1)
    print(startup_check())
