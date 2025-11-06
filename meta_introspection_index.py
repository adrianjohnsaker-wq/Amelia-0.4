# meta_introspection_index.py
import inspect, pkgutil, importlib, json

_index = {}

def build_index():
    for mod_info in pkgutil.iter_modules():
        try:
            mod = importlib.import_module(mod_info.name)
            for name, obj in inspect.getmembers(mod):
                if inspect.isclass(obj) or inspect.isfunction(obj):
                    _index[name.lower()] = {
                        "module": mod_info.name,
                        "type": "class" if inspect.isclass(obj) else "function"
                    }
        except Exception:
            continue
    return _index

def query_concept(concept: str):
    key = concept.lower()
    return {k: v for k, v in _index.items() if key in k}
