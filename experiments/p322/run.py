#!/usr/bin/env python3
"""P3.22 — Relational Analogy Completion."""
from __future__ import annotations

import argparse, copy, gzip, hashlib, importlib.util, json, math, os, random, statistics, sys
from collections import defaultdict

ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
if ROOT not in sys.path: sys.path.insert(0,ROOT)
P316=os.path.join(ROOT,"experiments","p316")
if P316 not in sys.path: sys.path.insert(0,P316)

from DynamicNumogram import DynamicNumogramProcess, IntegratedMemorySystem
from FullNumogram import syzygy_of, current_of, gate_of

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(mod); return mod

p317=load("p317_frozen",os.path.join(ROOT,"experiments","p317","run.py"))

N=96
LINEAGE_BASE=3250000
REWIRE_BASE=3256000
TEST_BASE=3257000
DRAWS=50000
REWIRES=24
FAMILIES=("SC","CS","SG","GS")
CONDITIONS=("CONGRUENT","SHUFFLED","QUERY_ONLY")

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def load_trials():
    path=os.path.join(ROOT,"experiments","p322","TRIALS.json")
    with open(path,encoding="utf-8") as h: payload=json.load(h)
    trials=payload["trials"]
    if len(trials)!=32: raise AssertionError("P3.22 requires 32 frozen trials")
    return trials

def op(name,z):
    if name=="S":return syzygy_of(z)
    if name=="C":return current_of(z)
    if name=="G":return gate_of(z)
    raise ValueError(name)

def validate_trials(trials):
    for t in trials:
        a=int(t["demo_source"]); b=int(t["query_source"])
        dm=op(t["first"],a); dt=op(t["second"],dm)
        qm=op(t["first"],b); qt=op(t["second"],qm)
        if (dm,dt,qm,qt)!=(t["demo_mid"],t["demo_terminal"],t["query_mid"],t["query_terminal"]):
            raise AssertionError("trial operator mismatch {}".format(t["trial_id"]))
        if len({a,dm,dt})!=3 or len({b,qm,qt})!=3:
            raise AssertionError("trial contains degenerate relation")
        if qt in {a,dm,dt,b}:
            raise AssertionError("query terminal leaked into demonstration/query source")
    if [t["family"] for t in trials].count("SC")!=8:raise AssertionError("SC count")
    for fam in FAMILIES:
        if sum(1 for t in trials if t["family"]==fam)!=8:raise AssertionError("family count")

def develop_rows(gates=None):
    rows=[]
    permeability=p317.original_gate_permeability(p317.FULL_NUMOGRAM_GATES if gates is None else gates)
    for i in range(N):
        seed=LINEAGE_BASE+i
        dev,_=p317.make_tapes(seed)
        p=DynamicNumogramProcess(gates=gates,current_zone=seed%10)
        p317.run_dynamic_tape(p,dev)
        p317.shock_process(p,seed,permeability)
        rows.append({"seed":seed,"dev":dev,"base":p})
    return rows

def run_trial(base,t,condition):
    p=copy.deepcopy(base)
    a=int(t["demo_source"]); dm=int(t["demo_mid"]); dt=int(t["demo_terminal"]); b=int(t["query_source"])
    qm=int(t["query_mid"]); qt=int(t["query_terminal"])
    if condition=="CONGRUENT":
        seq=[a,dm,dt]*4
        for x in seq:p.step(x)
    elif condition=="SHUFFLED":
        seq=[a,dt,dm]*4
        for x in seq:p.step(x)
    elif condition=="QUERY_ONLY":
        for _ in range(12):p.step(None)
    else:raise ValueError(condition)
    p.current_zone=b
    x1=p.step(None); x2=p.step(None)
    path=[int(x1["to_zone"]),int(x2["to_zone"])]
    return {
      "exact":path==[qm,qt],
      "intermediate_hit":path[0]==qm,
      "terminal_hit":path[1]==qt,
      "path":path,
    }

def signflip(diffs,seed,one_sided=True):
    if not diffs:return 1.0
    obs=statistics.mean(diffs); rng=random.Random(seed); ge=0
    for _ in range(DRAWS):
        m=statistics.mean(d*(1 if rng.random()<.5 else -1) for d in diffs)
        cond=(m>=obs-1e-15) if one_sided else (abs(m)>=abs(obs)-1e-15)
        if cond:ge+=1
    return (ge+1)/(DRAWS+1)

def evaluate_controller(name,bases,trials,raw):
    success={c:[[False]*N for _ in trials] for c in CONDITIONS}
    paths={c:[[None]*N for _ in trials] for c in CONDITIONS}
    for ti,t in enumerate(trials):
        for li,base in enumerate(bases):
            for c in CONDITIONS:
                r=run_trial(base,t,c)
                success[c][ti][li]=bool(r["exact"]); paths[c][ti][li]=r["path"]
                raw.write(json.dumps({
                  "controller":name,"trial_id":int(t["trial_id"]),"family":t["family"],
                  "lineage":"P322-{:03d}".format(li),"condition":c,
                  "exact":r["exact"],"intermediate_hit":r["intermediate_hit"],
                  "terminal_hit":r["terminal_hit"],"path":r["path"]
                },sort_keys=True,separators=(",",":"))+"\n")
    rows=[]
    for ti,t in enumerate(trials):
        rates={c:sum(success[c][ti])/N for c in CONDITIONS}
        rows.append({
          "trial_id":int(t["trial_id"]),"family":t["family"],
          "congruent":rates["CONGRUENT"],"shuffled":rates["SHUFFLED"],"query_only":rates["QUERY_ONLY"],
          "lift":rates["CONGRUENT"]-rates["SHUFFLED"],
          "query_gain":rates["CONGRUENT"]-rates["QUERY_ONLY"],
        })
    family={}
    for fam in FAMILIES:
        rr=[x for x in rows if x["family"]==fam]
        family[fam]={
          "congruent":statistics.mean(x["congruent"] for x in rr),
          "shuffled":statistics.mean(x["shuffled"] for x in rr),
          "query_only":statistics.mean(x["query_only"] for x in rr),
          "lift":statistics.mean(x["lift"] for x in rr),
        }
    return {
      "name":name,"trials":rows,"family":family,
      "mean_congruent":statistics.mean(x["congruent"] for x in rows),
      "mean_shuffled":statistics.mean(x["shuffled"] for x in rows),
      "mean_query_only":statistics.mean(x["query_only"] for x in rows),
      "mean_lift":statistics.mean(x["lift"] for x in rows),
      "mean_query_gain":statistics.mean(x["query_gain"] for x in rows),
      "_success":success,"_paths":paths
    }

def compact(ev):
    return {k:v for k,v in ev.items() if not k.startswith("_")}

def atlas(full,trials):
    out=[]
    succ=full["_success"]["CONGRUENT"]; paths=full["_paths"]["CONGRUENT"]
    for ti,t in enumerate(trials):
        lineages=[]
        for li in range(N):
            if succ[ti][li]:
                lineages.append({"lineage":"P322-{:03d}".format(li),"path":paths[ti][li]})
        out.append({
          **t,
          "congruent_completion":full["trials"][ti]["congruent"],
          "shuffled_completion":full["trials"][ti]["shuffled"],
          "query_only_completion":full["trials"][ti]["query_only"],
          "lineages":lineages
        })
    return out

def report(result):
    p=result["primary"]; s=result["structural"]; d=result["development"]
    lines=["# P3.22 — Relational Analogy Completion Result","",
      "- history-sensitive relational generalization: **{}**".format("PASS" if p["held"] else "FAIL"),
      "- canonical mean congruent completion: {:.6f}".format(p["canonical_congruent"]),
      "- canonical mean shuffled completion: {:.6f}".format(p["canonical_shuffled"]),
      "- canonical mean analogical lift: {:.6f}".format(p["canonical_lift"]),
      "- congruent > shuffled p: {:.8g}".format(p["lift_p"]),
      "- congruent > query-only p: {:.8g}".format(p["query_gain_p"]),
      "- canonical lift rank p vs 24 rewires: {:.6f}".format(p["rank_p"]),"",
      "## Family lifts",""]
    for fam,v in p["family_lifts"].items():lines.append("- {}: {:.6f}".format(fam,v))
    lines += ["","## Structural compositionality","",
      "- structural compositionality: **{}**".format("PASS" if s["held"] else "FAIL"),
      "- canonical query-only exact completion: {:.6f}".format(s["canonical_query_only"]),
      "- best rewire query-only exact completion: {:.6f}".format(max(s["rewire_query_only"])),
      "- rank p: {:.6f}".format(s["rank_p"]),"",
      "## Development/PFM contribution","",
      "- FULL mean lift: {:.6f}".format(d["full_lift"]),
      "- BLANK mean lift: {:.6f}".format(d["blank_lift"]),
      "- FULL > BLANK p: {:.8g}".format(d["p_upper"]),
      "- developmental contribution: **{}**".format("PASS" if d["held"] else "FAIL"),"",
      "## Interpretation","",result["interpretation"],""]
    return "\n".join(lines)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",default="experiments/p322/results"); args=ap.parse_args()
    os.makedirs(args.out,exist_ok=True)
    existing=os.path.join(args.out,"summary.json")
    if os.path.exists(existing):
        print(open(existing,encoding="utf-8").read()); return 0
    trials=load_trials(); validate_trials(trials)

    rows=develop_rows()
    full_bases=[copy.deepcopy(x["base"]) for x in rows]
    blank_bases=[]
    for x in rows:
        b=copy.deepcopy(x["base"]); b.memory=IntegratedMemorySystem(); b.deformation_tensor=[0.1]*10
        blank_bases.append(b)

    raw_path=os.path.join(args.out,"records.jsonl.gz")
    with gzip.open(raw_path,"wt",encoding="utf-8") as raw:
        full=evaluate_controller("CANONICAL_FULL",full_bases,trials,raw)
        blank=evaluate_controller("CANONICAL_BLANK",blank_bases,trials,raw)
        rew=[]
        for rid in range(REWIRES):
            gates=p317.rewired_gates(REWIRE_BASE+rid)
            rr=develop_rows(gates)
            bases=[x["base"] for x in rr]
            rew.append(evaluate_controller("R{:02d}".format(rid),bases,trials,raw))

    lift_diffs=[x["lift"] for x in full["trials"]]
    q_diffs=[x["query_gain"] for x in full["trials"]]
    p_lift=signflip(lift_diffs,TEST_BASE,True)
    p_query=signflip(q_diffs,TEST_BASE+1,True)
    family_lifts={fam:full["family"][fam]["lift"] for fam in FAMILIES}
    rew_lifts=[x["mean_lift"] for x in rew]
    ge=sum(1 for x in rew_lifts if x>=full["mean_lift"])
    rank_p=(1+ge)/(REWIRES+1)
    primary=(full["mean_lift"]>0 and p_lift<=.01 and all(v>0 for v in family_lifts.values())
             and all(full["mean_lift"]>x for x in rew_lifts) and abs(rank_p-.04)<1e-12
             and full["mean_query_gain"]>0 and p_query<=.01)

    rew_q=[x["mean_query_only"] for x in rew]
    geq=sum(1 for x in rew_q if x>=full["mean_query_only"])
    rank_q=(1+geq)/(REWIRES+1)
    structural=all(full["mean_query_only"]>x for x in rew_q) and abs(rank_q-.04)<1e-12

    dev_diffs=[a["lift"]-b["lift"] for a,b in zip(full["trials"],blank["trials"])]
    p_dev=signflip(dev_diffs,TEST_BASE+2,True)
    dev=statistics.mean(dev_diffs)>0 and p_dev<=.01

    if primary:
        interp="The historically evolving canonical Numogram generalizes demonstrated composed relations to unseen query sources more strongly than shuffled demonstrations and all degree-preserving rewires."
    else:
        interp="P3.22 does not satisfy the registered history-sensitive relational-generalization gate."
    if structural:interp+=" Independently, the canonical process shows privileged autonomous access to its own composed relations without demonstration."
    else:interp+=" The canonical process does not uniquely dominate rewires on query-only composed-relation completion."
    if dev:interp+=" Mature developmental state contributes positively to analogical lift."
    else:interp+=" Mature developmental state does not satisfy the registered positive contribution gate for analogical lift."

    at=atlas(full,trials)
    result={
      "schema":"amelia-p322-relational-analogy-v1",
      "primary":{"held":primary,"canonical_congruent":full["mean_congruent"],"canonical_shuffled":full["mean_shuffled"],
        "canonical_lift":full["mean_lift"],"canonical_query_gain":full["mean_query_gain"],"lift_p":p_lift,"query_gain_p":p_query,
        "family_lifts":family_lifts,"rewire_lifts":rew_lifts,"rank_p":rank_p},
      "structural":{"held":structural,"canonical_query_only":full["mean_query_only"],"rewire_query_only":rew_q,"rank_p":rank_q},
      "development":{"held":dev,"full_lift":full["mean_lift"],"blank_lift":blank["mean_lift"],"mean_difference":statistics.mean(dev_diffs),"p_upper":p_dev},
      "canonical":compact(full),"blank":compact(blank),
      "rewires":[compact(x) for x in rew],
      "atlas":at,"interpretation":interp,
      "provenance":{"registration_sha256":sha256_file("experiments/p322/REGISTRATION.md"),
        "amendment_sha256":sha256_file("experiments/p322/AMENDMENT_1.md"),
        "trials_sha256":sha256_file("experiments/p322/TRIALS.json"),
        "runner_sha256":sha256_file("experiments/p322/run.py"),
        "engine_sha256":sha256_file("experiments/p316/DynamicNumogram.py"),
        "raw_sha256":sha256_file(raw_path)}
    }
    with open(existing,"w",encoding="utf-8") as h:json.dump(result,h,indent=2,sort_keys=True)
    with open(os.path.join(args.out,"ATLAS.md"),"w",encoding="utf-8") as h:
        h.write("# P3.22 — Relational Analogy Atlas\n\n")
        for x in at:
            h.write("## Trial {:02d} — {}\n\n".format(x["trial_id"],x["family"]))
            h.write("- demonstration: {}→{}→{}\n".format(x["demo_source"],x["demo_mid"],x["demo_terminal"]))
            h.write("- unseen query: {}→{}→{}\n".format(x["query_source"],x["query_mid"],x["query_terminal"]))
            h.write("- congruent/shuffled/query-only: {:.4f} / {:.4f} / {:.4f}\n".format(x["congruent_completion"],x["shuffled_completion"],x["query_only_completion"]))
            h.write("- completing lineages: {}\n\n".format(", ".join(z["lineage"] for z in x["lineages"]) if x["lineages"] else "none"))
    with open(os.path.join(args.out,"REPORT.md"),"w",encoding="utf-8") as h:h.write(report(result))
    print(json.dumps({"primary":result["primary"],"structural":result["structural"],"development":result["development"],"interpretation":interp},indent=2,sort_keys=True))
    return 0

if __name__=="__main__":raise SystemExit(main())
