"""A12 audit: fail closed and publish four explicit evidence sections."""
import argparse
import json
import zipfile
from pathlib import Path
from drift1a_c1.common import cj, publish, sha
from drift1a_c1.engine import frozen_files
from drift1a_c1.metrics import PRIMARY_KEYS, VERSION
from drift1a_c1.remeasure import SOURCE_SHA256

EXPECTED_FLAGS={"2026-W41":(0,[]),"2026-W42":(2,["self_loops_9","outcome_mm_lag_6"])}
EXPECTED_LOO={"C":2,"R01":11,"R02":4,"R03":14,"R04":9,"R05":3,"R06":8,"R07":2,"R08":5}

def audit(archive, simulation, output):
    out=Path(output)
    record={"frozen_files":{"files":{},"matches":False},
            "measurements":{"weeks":{},"differences":[],"matches":False},
            "renderer":{"weeks":{},"matches":False},
            "overall_verdict":{"status":"FAIL","errors":[]}}
    try:
        baseline=json.loads(Path("drift1a_c1/evidence/validation-status-A11.json").read_text())
        current=frozen_files()
        old=baseline["measurement_files"]
        exception=json.loads(Path("drift1a_c1/evidence/A12-baseline-exception.json").read_text())
        charter="claude/DRIFT1A_C1_CHARTER_draft.md"
        assert exception["scope"]["exception"]=="charter only"
        assert exception["charter"]["path"]==charter
        assert exception["charter"]["A11_sha256"]=="418b8722176eef032bcc4f54e491678592105b9a84b5156455a332f28ba168c5"
        assert exception["charter"]["approved_sha256"]=="f18cce34cef1812c5d1a91e0f6138a027b32605e0d36cfe8fead34c085833c71"
        assert exception["approval"]["date"]=="2026-10-17"
        assert exception["failed_audit"]["run_id"]==39059931955
        assert exception["failed_audit"]["artifact_id"]==12111771861
        for name in sorted(set(current)|set(old)):
            prior=old.get(name);now=current.get(name)
            expected=exception["charter"]["approved_sha256"] if name==charter else prior
            record["frozen_files"]["files"][name]={"A11_sha256":prior,"current_sha256":now,"required_sha256":expected,"match":prior is not None and now==expected,"exception_applies":name==charter}
        record["frozen_files"]["matches"]=bool(record["frozen_files"]["files"]) and all(x["match"] for x in record["frozen_files"]["files"].values())
        record["frozen_files"]["exception_record"]="drift1a_c1/evidence/A12-baseline-exception.json"
        record["frozen_files"]["note"]="Charter must equal approved draft 0.4 hash; every other frozen file must equal its A11 hash."
        if not record["frozen_files"]["matches"]:
            record["overall_verdict"]["errors"].append("Frozen-file hash outside strict approved baseline")
        if VERSION!=baseline["measurement_version"]:
            record["overall_verdict"]["errors"].append("Measurement version differs")
        archive=Path(archive)
        if sha(archive.read_bytes())!=SOURCE_SHA256:
            raise ValueError("A11 source archive SHA-256 mismatch")
        sim=Path(simulation)
        with zipfile.ZipFile(archive) as z:
            for w,entry in sorted(baseline["reports"].items()):
                source=json.loads(z.read(f"c1-simulation/reports/{w}/report.json"))
                actual=json.loads((sim/"reports"/w/"report.json").read_text())
                diffs=[]
                for arm in sorted(source["arms"]):
                    if arm not in actual["arms"]:
                        diffs.append({"arm":arm,"statistic":"arm_missing","expected":"present","actual":"absent"})
                        continue
                    # Compare the full nested arm measurement tree, not just
                    # top-level declared statistics.
                    def walk(a,b,path):
                        if isinstance(a,dict) and isinstance(b,dict):
                            for key in sorted(set(a)|set(b)):
                                if key not in a or key not in b:diffs.append({"arm":arm,"statistic":path+"."+key,"expected":a.get(key),"actual":b.get(key)})
                                else:walk(a[key],b[key],path+"."+key)
                        elif a!=b:
                            diffs.append({"arm":arm,"statistic":path,"expected":a,"actual":b})
                    walk(source["arms"][arm],actual["arms"][arm],"measurements")
                if len(PRIMARY_KEYS)!=29:
                    diffs.append({"statistic":"declared_statistics_count","expected":29,"actual":len(PRIMARY_KEYS)})
                if actual["records_digest"]!=entry["records_digest"]:
                    diffs.append({"statistic":"records_digest","expected":entry["records_digest"],"actual":actual["records_digest"]})
                for key,expected in [("F",entry["F"]),("N",entry["N"])]:
                    if actual["flags"].get(key)!=expected:diffs.append({"statistic":key,"expected":expected,"actual":actual["flags"].get(key)})
                for arm,expected in entry["leave_one_out"].items():
                    observed=actual["leave_one_out_flags"].get(arm)
                    if observed!=expected:diffs.append({"arm":arm,"statistic":"leave_one_out","expected":expected,"actual":observed})
                for arm,expected in (EXPECTED_LOO if w=="2026-W42" else {}).items():
                    got=actual["leave_one_out_flags"].get(arm,{}).get("F")
                    if got!=expected:diffs.append({"arm":arm,"statistic":"explicit_A11_LOO","expected":expected,"actual":got})
                expected_f,expected_keys=EXPECTED_FLAGS[w]
                if actual["flags"].get("F")!=expected_f:diffs.append({"statistic":"explicit_A11_F","expected":expected_f,"actual":actual["flags"].get("F")})
                # The flags table contains the declared comparison rows; confirm
                # the two named W42 departures rather than relying only on F.
                if expected_keys:
                    named={key for key,row in actual["references"].items() if row["strict_outside"]}
                    if named!=set(expected_keys):
                        diffs.append({"statistic":"flagged_statistic_names","expected":expected_keys,"actual":sorted(named)})
                record["measurements"]["weeks"][w]={"arms_compared":len(source["arms"]),"declared_statistics":len(PRIMARY_KEYS),"differences":diffs,"match":not diffs}
                record["measurements"]["differences"].extend([dict(week=w,**d) for d in diffs])
                printed=(sim/"reports"/w/"report.md").read_text()
                current_sha=sha(Path("drift1a_c1/reports.py").read_bytes())
                reported=actual.get("renderer_sha256")
                ok=reported==current_sha and current_sha in printed
                record["renderer"]["weeks"][w]={"report_sha256":reported,"validated_source_sha256":current_sha,"printed_in_markdown":current_sha in printed,"match":ok}
        record["measurements"]["matches"]=all(v["match"] for v in record["measurements"]["weeks"].values()) and bool(record["measurements"]["weeks"])
        record["renderer"]["matches"]=all(v["match"] for v in record["renderer"]["weeks"].values()) and bool(record["renderer"]["weeks"])
    except Exception as exc:
        record["overall_verdict"]["errors"].append(f"{type(exc).__name__}: {exc}")
    for section in ("frozen_files","measurements","renderer"):
        if not record[section]["matches"]:
            record["overall_verdict"]["errors"].append(section+" failed")
    record["overall_verdict"]["status"]="PASS" if not record["overall_verdict"]["errors"] else "FAIL"
    publish(out,cj(record))
    print(json.dumps(record,indent=2),flush=True)
    if record["overall_verdict"]["status"]!="PASS":raise SystemExit(1)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--archive",required=True);p.add_argument("--simulation",required=True);p.add_argument("--output",required=True)
    a=p.parse_args();audit(a.archive,a.simulation,a.output)
