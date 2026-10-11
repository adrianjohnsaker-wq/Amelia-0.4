"""Build preparation: no edits to the accepted dynamics; seal extracted assets."""
import hashlib,json,shutil,sys
from pathlib import Path
root=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'runtime'))
from android_session import reference_result
from drift_core import canonical_json,verify_canonical
verify_canonical()
(root/'runtime/device_reference.json').write_text(canonical_json(reference_result()))
files={p.relative_to(root/'runtime').as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
       for p in sorted((root/'runtime').rglob('*')) if p.is_file() and '__pycache__' not in p.parts
       and p.name!='runtime_manifest.json'}
manifest={'files':files,'digest':hashlib.sha256(canonical_json(files).encode('ascii')).hexdigest()}
(root/'runtime/runtime_manifest.json').write_text(canonical_json(manifest))
target=root/'app/src/main/assets/g1_runtime'
if target.exists():shutil.rmtree(target)
target.mkdir(parents=True)
for name in list(files)+['runtime_manifest.json']:
 dst=target/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/'runtime'/name,dst)
print('G1 runtime sealed:',manifest['digest'])
