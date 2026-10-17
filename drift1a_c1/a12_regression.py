"""Fail-closed A12 identity check against the sealed A7–A10 ledger and A11 record."""
import argparse
import gzip
import json
import zipfile
from pathlib import Path
from drift1a_c1.common import cj,publish,sha
from drift1a_c1.engine import frozen_files
from drift1a_c1.metrics import PRIMARY_KEYS,VERSION
from drift1a_c1.remeasure import SOURCE_SHA256

def check(archive, simulation, output):
    baseline=json.loads(Path("drift1a_c1/evidence/validation-status-A11.json").read_text())
    sim=Path(simulation);archive=Path(archive)
    checks={}
    try:
        current=frozen_files()
        # Charter draft 0.4 was explicitly approved after A11. It is frozen
        # at genesis, but cannot truthfully equal the older A11 charter digest.
        exceptions={"claude/DRIFT1A_C1_CHARTER_draft.md"}
        changes={p:{"A11":v,"current":current.get(p)} for p,v in baseline["measurement_files"].items()
                 if current.get(p)!=v}
        checks["frozen_files_except_approved_charter"]=not(set(changes)-exceptions)
        checks["charter_exception_explicit"]=set(changes).issubset(exceptions)
        checks["measurement_version"]=VERSION==baseline["measurement_version"]
        checks["source_archive_sha256"]=sha(archive.read_bytes())==SOURCE_SHA256
        if not checks["source_archive_sha256"]:
            raise ValueError("source archive digest mismatch")
        with zipfile.ZipFile(archive) as z:
            for w in baseline["reports"]:
                source=json.loads(z.read(f"c1-simulation/reports/{w}/report.json"))
                actual=json.loads((sim/"reports"/w/"report.json").read_text())
                # A11 independently established that source arm measurements
                # are identical, including all 29 primary values per arm.
                checks[f"{w}_all_arm_measurements"]=all(
                    actual["arms"][a]==source["arms"][a] for a in source["arms"])
                checks[f"{w}_29_primary_values"]=all(
                    all(actual["arms"][a].get(k)==source["arms"][a].get(k)
                        for k in PRIMARY_KEYS) for a in source["arms"])
                expected=baseline["reports"][w]
                checks[f"{w}_records_digest"]=actual["records_digest"]==expected["records_digest"]
                checks[f"{w}_F_N"]=(actual["flags"]["F"],actual["flags"]["N"])==(expected["F"],expected["N"])
                checks[f"{w}_leave_one_out"]=all(
                    actual["leave_one_out_flags"][a]["F"]==v["F"] and
                    actual["leave_one_out_flags"][a]["N_compared"]==v["N_compared"]
                    for a,v in expected["leave_one_out"].items())
                renderer=Path("drift1a_c1/reports.py")
                checks[f"{w}_renderer_json"]=actual["renderer_sha256"]==sha(renderer.read_bytes())
                md=(sim/"reports"/w/"report.md").read_text()
                checks[f"{w}_renderer_markdown"]=actual["renderer_sha256"] in md
    except Exception as exc:
        checks["execution_error"]=False
        error=str(exc)
    else:
        error=None
    result={"status":"PASS" if all(checks.values()) else "FAIL",
            "measurement_version":VERSION,"approved_charter_change":changes.get("claude/DRIFT1A_C1_CHARTER_draft.md"),
            "checks":checks,"error":error}
    publish(Path(output),cj(result))
    print(json.dumps(result,indent=2),flush=True)
    if result["status"]!="PASS":raise SystemExit(1)
    return result

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--archive",required=True);p.add_argument("--simulation",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args();check(a.archive,a.simulation,a.output)
