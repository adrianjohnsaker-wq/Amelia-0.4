"""
meta_introspection_index.py
─────────────────────────────────────────────────────────────────────────────
Builds and queries a live introspection index of Python modules/classes/
functions/methods. Also keeps a small runtime object registry for stateful
diagnostics from Kotlin via Chaquopy.

Designed to be lightweight, zero-dep (stdlib only), and JSON-friendly.

Public API (all return JSON-serializable dicts/lists):
- initialize(config: dict | None) -> dict
- build_index(modules: list[str] | None = None, paths: list[str] | None = None) -> dict
- refresh() -> dict
- query_by_name(name: str) -> dict
- query_by_concept(concept: str) -> dict
- search(text: str, limit: int = 50) -> dict
- stats() -> dict
- register_runtime(name: str, state: dict) -> dict
- get_runtime(name: str) -> dict
- list_runtime() -> dict
- diagnostics() -> dict

Notes
- If you pass `paths`, they’ll be appended to sys.path for discovery.
- If you pass `modules`, they’ll be imported eagerly and indexed.
- Concept queries are heuristic: tokenizes names/docs and fuzzy-matches.
"""

from __future__ import annotations
import sys
import os
import pkgutil
import importlib
import inspect
import time
import json
import traceback
from typing import Any, Dict, List, Optional, Tuple

# ────────────────────────────────────────────────────────────────────────────
# Internals / globals
# ────────────────────────────────────────────────────────────────────────────

_START_TS = time.time()

_INDEX: Dict[str, Any] = {
    "built_at": None,
    "modules": {},        # mod -> {"objects":[...], "ok":bool, "error":str|None}
    "classes": {},        # fqname -> entry
    "functions": {},      # fqname -> entry
    "concept_map": {},    # concept -> [fqnames]
}

_RUNTIME_REGISTRY: Dict[str, Dict[str, Any]] = {}  # name -> {"state":..., "ts":...}

_DEFAULT_EXCLUDES = {
    "pip", "setuptools", "distutils", "pkg_resources",
    "ensurepip", "test", "idlelib", "tkinter",
    "_distutils_hack", "numpy.f2py", "site-packages.tests",
}

# Simple tokenizer for concept detection
def _tokens(s: str) -> List[str]:
    out = []
    acc = []
    for ch in s:
        if ch.isalnum():
            acc.append(ch.lower())
        else:
            if acc:
                out.append("".join(acc))
                acc = []
    if acc:
        out.append("".join(acc))
    return out

def _fq(mod: str, name: str) -> str:
    return f"{mod}.{name}" if mod else name

def _safe_sig(obj) -> str:
    try:
        return str(inspect.signature(obj))
    except Exception:
        return "(?)"

def _doc(obj) -> str:
    try:
        d = inspect.getdoc(obj) or ""
        return d[:2000]  # trim
    except Exception:
        return ""

def _record_module(mod_name: str, ok: bool, error: Optional[str] = None):
    _INDEX["modules"].setdefault(mod_name, {"objects": [], "ok": True, "error": None})
    _INDEX["modules"][mod_name]["ok"] = ok
    _INDEX["modules"][mod_name]["error"] = error

def _add_object(mod_name: str, kind: str, name: str, entry: Dict[str, Any]):
    _INDEX["modules"].setdefault(mod_name, {"objects": [], "ok": True, "error": None})
    _INDEX["modules"][mod_name]["objects"].append({"kind": kind, "fqname": entry["fqname"]})
    if kind == "class":
        _INDEX["classes"][entry["fqname"]] = entry
    elif kind == "function":
        _INDEX["functions"][entry["fqname"]] = entry

def _index_class(mod_name: str, cls) -> None:
    fqname = _fq(mod_name, cls.__name__)
    entry = {
        "fqname": fqname,
        "module": mod_name,
        "name": cls.__name__,
        "kind": "class",
        "bases": [b.__name__ for b in getattr(cls, "__bases__", [])],
        "doc": _doc(cls),
        "methods": [],
        "attrs": [],
    }
    for m_name, m_obj in inspect.getmembers(cls):
        if m_name.startswith("__") and m_name.endswith("__"):
            continue
        if inspect.isfunction(m_obj) or inspect.ismethod(m_obj):
            entry["methods"].append({
                "name": m_name,
                "signature": _safe_sig(m_obj),
                "doc": (_doc(m_obj)[:600] if _doc(m_obj) else ""),
            })
        else:
            entry["attrs"].append(m_name)
    _add_object(mod_name, "class", cls.__name__, entry)

def _index_function(mod_name: str, fn) -> None:
    fqname = _fq(mod_name, fn.__name__)
    entry = {
        "fqname": fqname,
        "module": mod_name,
        "name": fn.__name__,
        "kind": "function",
        "signature": _safe_sig(fn),
        "doc": _doc(fn),
    }
    _add_object(mod_name, "function", fn.__name__, entry)

def _maybe_index_module(mod_name: str):
    try:
        mod = importlib.import_module(mod_name)
        _record_module(mod_name, ok=True)
    except Exception as e:
        _record_module(mod_name, ok=False, error=f"import error: {e}")
        return

    try:
        for name, obj in inspect.getmembers(mod):
            if inspect.isclass(obj) and getattr(obj, "__module__", mod_name).startswith(mod_name):
                _index_class(mod_name, obj)
            elif inspect.isfunction(obj) and getattr(obj, "__module__", mod_name).startswith(mod_name):
                _index_function(mod_name, obj)
    except Exception as e:
        _record_module(mod_name, ok=False, error=f"scan error: {e}")

def _build_concepts():
    concept_map = {}
    def add(key: str, fq: str):
        concept_map.setdefault(key, []).append(fq)

    # scan functions
    for fq, e in _INDEX["functions"].items():
        toks = set(_tokens(e["name"]) + _tokens(e.get("doc", "")))
        for t in toks:
            if len(t) >= 4:
                add(t, fq)

    # scan classes and their methods
    for fq, e in _INDEX["classes"].items():
        toks = set(_tokens(e["name"]) + _tokens(e.get("doc", "")))
        for m in e.get("methods", []):
            toks.update(_tokens(m["name"]))
            toks.update(_tokens(m.get("doc", "")))
        for t in toks:
            if len(t) >= 4:
                add(t, fq)

    _INDEX["concept_map"] = concept_map

# ────────────────────────────────────────────────────────────────────────────
# Public API
# ────────────────────────────────────────────────────────────────────────────

def initialize(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Optionally pass:
      {"paths": ["/data/user/0/…/files/python_modules"], "modules": ["meta_autonomy_engine", "numogram_core"]}
    """
    try:
        if config:
            for p in config.get("paths", []) or []:
                if p and p not in sys.path:
                    sys.path.insert(0, p)
        mods = (config or {}).get("modules", [])
        if mods:
            build_index(modules=mods)
        else:
            _INDEX["built_at"] = time.time()
        return {"ok": True, "built_at": _INDEX["built_at"], "modules": list(_INDEX["modules"].keys())}
    except Exception as e:
        return {"ok": False, "error": str(e), "trace": traceback.format_exc()}

def build_index(modules: Optional[List[str]] = None,
                paths: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Build (or rebuild) the index from provided modules and optionally search paths.
    If modules is None, we conservatively walk already-imported modules.
    """
    try:
        # reset
        _INDEX["built_at"] = time.time()
        _INDEX["modules"].clear()
        _INDEX["classes"].clear()
        _INDEX["functions"].clear()
        _INDEX["concept_map"].clear()

        if paths:
            for p in paths:
                if p and p not in sys.path:
                    sys.path.insert(0, p)

        scanned: List[str] = []

        if modules:
            for m in modules:
                if not m: continue
                _maybe_index_module(m)
                scanned.append(m)
        else:
            # conservative: index only already-imported app modules (avoid stdlib spam)
            for mname in list(sys.modules.keys()):
                if not mname or mname.startswith(("sys", "importlib", "types", "builtins")):
                    continue
                if any(mname.startswith(ex) for ex in _DEFAULT_EXCLUDES):
                    continue
                try:
                    _maybe_index_module(mname)
                    scanned.append(mname)
                except Exception:
                    pass

        _build_concepts()
        return {
            "ok": True,
            "built_at": _INDEX["built_at"],
            "scanned": scanned,
            "counts": {
                "modules": len(_INDEX["modules"]),
                "classes": len(_INDEX["classes"]),
                "functions": len(_INDEX["functions"]),
                "concepts": len(_INDEX["concept_map"]),
            },
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "trace": traceback.format_exc()}

def refresh() -> Dict[str, Any]:
    """Rebuild using whatever was scanned last time (already-imported modules)."""
    return build_index(modules=None, paths=None)

def query_by_name(name: str) -> Dict[str, Any]:
    """Find classes/functions whose FQ name or simple name contains the substring."""
    try:
        q = name.lower()
        hits_f = [e for fq, e in _INDEX["functions"].items()
                  if q in fq.lower() or q in e["name"].lower()]
        hits_c = [e for fq, e in _INDEX["classes"].items()
                  if q in fq.lower() or q in e["name"].lower()]
        return {
            "ok": True,
            "query": name,
            "functions": hits_f[:200],
            "classes": hits_c[:200],
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}

def query_by_concept(concept: str) -> Dict[str, Any]:
    """Heuristic concept map lookup (token-based)."""
    try:
        key = concept.lower().strip()
        cands = _INDEX["concept_map"].get(key)
        # Soft fallback: prefix/similar keys
        if not cands:
            similar = [k for k in _INDEX["concept_map"].keys() if key in k]
            cands = []
            for s in similar:
                cands.extend(_INDEX["concept_map"].get(s, []))
        details = []
        for fq in cands or []:
            if fq in _INDEX["functions"]:
                details.append(_INDEX["functions"][fq])
            elif fq in _INDEX["classes"]:
                details.append(_INDEX["classes"][fq])
        return {"ok": True, "concept": concept, "results": details[:200]}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def search(text: str, limit: int = 50) -> Dict[str, Any]:
    """Full-text-ish search across names and docs."""
    q = text.lower()
    fun = []
    cla = []
    for e in _INDEX["functions"].values():
        if q in e["name"].lower() or q in e.get("doc", "").lower() or q in e["fqname"].lower():
            fun.append(e)
    for e in _INDEX["classes"].values():
        if q in e["name"].lower() or q in e.get("doc", "").lower() or q in e["fqname"].lower():
            cla.append(e)
    return {"ok": True, "query": text, "functions": fun[:limit], "classes": cla[:limit]}

def stats() -> Dict[str, Any]:
    return {
        "ok": True,
        "built_at": _INDEX["built_at"],
        "uptime_sec": round(time.time() - _START_TS, 3),
        "counts": {
            "modules": len(_INDEX["modules"]),
            "classes": len(_INDEX["classes"]),
            "functions": len(_INDEX["functions"]),
            "concepts": len(_INDEX["concept_map"]),
            "runtime": len(_RUNTIME_REGISTRY),
        },
        "modules_with_errors": {m: d for m, d in _INDEX["modules"].items() if not d.get("ok", True)},
    }

def register_runtime(name: str, state: Dict[str, Any]) -> Dict[str, Any]:
    _RUNTIME_REGISTRY[name] = {"state": state, "ts": time.time()}
    return {"ok": True, "name": name, "stored": True}

def get_runtime(name: str) -> Dict[str, Any]:
    if name in _RUNTIME_REGISTRY:
        return {"ok": True, "name": name, **_RUNTIME_REGISTRY[name]}
    return {"ok": False, "error": f"not found: {name}"}

def list_runtime() -> Dict[str, Any]:
    return {"ok": True, "names": list(_RUNTIME_REGISTRY.keys())}

def diagnostics() -> Dict[str, Any]:
    return {
        "ok": True,
        "stats": stats(),
        "sample": {
            "some_function": next(iter(_INDEX["functions"].values()), None),
            "some_class": next(iter(_INDEX["classes"].values()), None),
        },
    }

# Convenience: Chaquopy-friendly single entry to JSON-string
def call(method: str, *args, **kwargs) -> str:
    api = {
        "initialize": initialize,
        "build_index": build_index,
        "refresh": refresh,
        "query_by_name": query_by_name,
        "query_by_concept": query_by_concept,
        "search": search,
        "stats": stats,
        "register_runtime": register_runtime,
        "get_runtime": get_runtime,
        "list_runtime": list_runtime,
        "diagnostics": diagnostics,
    }
    fn = api.get(method)
    if not fn:
        return json.dumps({"ok": False, "error": f"unknown method: {method}"})
    try:
        res = fn(*args, **kwargs)
        return json.dumps(res)
    except Exception as e:
        return json.dumps({"ok": False, "error": str(e), "trace": traceback.format_exc()})
