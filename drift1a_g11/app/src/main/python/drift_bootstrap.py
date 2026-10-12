"""Verify and load the byte-exact G1 sources extracted from APK assets."""
import hashlib
import importlib
import json
from pathlib import Path
import sys


def load(root):
    root=Path(str(root))
    manifest=json.loads((root/'runtime_manifest.json').read_text())
    for name,want in manifest['files'].items():
        got=hashlib.sha256((root/name).read_bytes()).hexdigest()
        if got!=want:
            raise ValueError('Runtime source mismatch: '+name)
    payload=json.dumps(manifest['files'],sort_keys=True,separators=(',',':'),ensure_ascii=True)
    if hashlib.sha256(payload.encode('ascii')).hexdigest()!=manifest['digest']:
        raise ValueError('Runtime manifest mismatch')
    sys.path.insert(0,str(root))
    return importlib.import_module('android_session')
