#!/usr/bin/env python3
"""WARP-T4 — Portable Trace and Relational Entry."""
from __future__ import annotations

import argparse, copy, gzip, hashlib, importlib.util, json, math, os, random, statistics, sys

ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
if ROOT not in sys.path: sys.path.insert(0,ROOT)
P316=os.path.join(ROOT,"experiments","p316")
if P316 not in sys.path: sys.path.insert(0,P316)

from FullNumogram import syzygy_of, current_of, gate_of

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(mod); return mod

p317=load("p317_frozen",os.path.join(ROOT,"experiments","p317","run.py"))
wt1=load("warp_t1_frozen",os.path.join(ROOT,"experiments","warp_t1","run.py"))
wt2=load("warp_t2_frozen",os.path.join(ROOT,"experiments","warp_t2","run.py"))

N=160
SEED_BASE=3260000
PERM_BASE=3267000
BOOT_BASE=3268000
DRAWS=50000
BOOT_DRAWS=20000
FAMILIES=("SC","CS","SG","GS")
ARMS=("W","P","N","B","E","T")
CONDITIONS=("CONGRUENT","SHUFFLED","QUERY_ONLY")
POINTER_TRIPLETS={"1-2-7","1-8-7","1-7-8"}

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def load_trials():
    with open(os.path.join(ROOT,"experiments","warp_t4","TRIALS.json"),encoding="utf-8") as h:
        payload=json.load(h)
    trials=payload["trials"]
    if len(trials)!=32:raise AssertionError("WARP-T4 requires 32 trials")
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
            raise AssertionError("trial mismatch")
        if qt in {a,dm,dt,b}:raise AssertionError("query terminal leaked")
    for fam in FAMILIES:
        if sum(1 for t in trials if t["family"]==fam)!=8:raise AssertionError("family count")

def make_lineage(index):
    seed=SEED_BASE+index
    e=wt1.first_entry(seed)
    if e is None or len(e["remaining"])<4:return {"index":index,"seed":seed,"eligible":False}
    inputs=[int(e["input"])]+[int(x) for x in e["remaining"][:4]]
    real,targets=wt2.passage_real(e["pre"],inputs[0],e["target"],inputs[1:])
    entry=wt2.passage_forced(e["pre"],inputs,targets,True)
    topo=wt2.passage_forced(e["pre"],inputs,targets,False)
    try:
        nonwarp=wt2.passage_nonwarp(e["pre"],inputs)
    except Exception:
        return {"index":index,"seed":seed,"eligible":False}
    pre=e["pre"]
    shells={
      "W":wt2.release_shell(pre,real.memory,real.deformation_tensor,seed),
      "P":wt2.release_shell(pre,real.memory,pre.deformation_tensor,seed),
      "N":wt2.release_shell(pre,nonwarp.memory,nonwarp.deformation_tensor,seed),
      "B":wt2.release_shell(pre,pre.memory,pre.deformation_tensor,seed),
      "E":wt2.release_shell(pre,entry.memory,entry.deformation_tensor,seed),
      "T":wt2.release_shell(pre,topo.memory,topo.deformation_tensor,seed),
    }
    return {
      "index":index,"seed":seed,"eligible":True,
      "entry_step":int(e["index"]),"source":int(pre.current_zone),"target":int(e["target"]),
      "passage_inputs":inputs,"passage_targets":targets,"shells":shells
    }

def run_trial(base,t,condition):
    p=copy.deepcopy(base)
    a=int(t["demo_source"]); dm=int(t["demo_mid"]); dt=int(t["demo_terminal"]); b=int(t["query_source"])
    qm=int(t["query_mid"]); qt=int(t["query_terminal"])
    if condition=="CONGRUENT":
        for x in [a,dm,dt]*4:p.step(x)
    elif condition=="SHUFFLED":
        for x in [a,dt,dm]*4:p.step(x)
    elif condition=="QUERY_ONLY":
        for _ in range(12):p.step(None)
    else:raise ValueError(condition)
    p.current_zone=b
    x1=p.step(None); x2=p.step(None)
    path=[int(x1["to_zone"]),int(x2["to_zone"])]
    return {"exact":path==[qm,qt],"path":path}

def holm(raw):
    ordered=sorted(raw.items(),key=lambda kv:(kv[1],kv[0])); m=len(ordered)
    out={}; running=0.0
    for i,(k,p) in enumerate(ordered):
        running=max(running,min(1.0,(m-i)*p)); out[k]=running
    return out

def signflip(diffs,seed,two_sided=True):
    if not diffs:return 1.0
    obs=statistics.mean(diffs); rng=random.Random(seed); ge=0
    for _ in range(DRAWS):
        m=statistics.mean(d*(1 if rng.random()<.5 else -1) for d in diffs)
        cond=abs(m)>=abs(obs)-1e-15 if two_sided else m>=obs-1e-15
        if cond:ge+=1
    return (ge+1)/(DRAWS+1)

def multivar(left,right,seed,component_base):
    ds=[[left[i][fam]-right[i][fam] for fam in FAMILIES] for i in range(len(left))]
    sds=[]
    for j in range(4):
        col=[d[j] for d in ds]
        sd=statistics.stdev(col) if len(col)>1 else 0.0
        sds.append(sd if sd>1e-12 else 0.0)
    def stat(signs=None):
        total=0.0
        for j,sd in enumerate(sds):
            if sd<=0:continue
            vals=[d[j]*(1 if signs is None else signs[i]) for i,d in enumerate(ds)]
            total+=(statistics.mean(vals)/sd)**2
        return total
    obs=stat(); rng=random.Random(seed); ge=0
    for _ in range(DRAWS):
        signs=[1 if rng.random()<.5 else -1 for _ in ds]
        if stat(signs)>=obs-1e-15:ge+=1
    comp={}; raw={}
    for j,fam in enumerate(FAMILIES):
        diffs=[d[j] for d in ds]; p=signflip(diffs,component_base+j,True)
        comp[fam]={"mean_difference":statistics.mean(diffs),"p_two_sided":p}; raw[fam]=p
    adj=holm(raw)
    for fam in comp:comp[fam]["holm_p"]=adj[fam]
    return {"T":obs,"p":(ge+1)/(DRAWS+1),"components":comp}

def bootstrap_ci(diffs,seed):
    rng=random.Random(seed); vals=[]; n=len(diffs)
    for _ in range(BOOT_DRAWS):
        vals.append(statistics.mean(rng.choice(diffs) for _ in range(n)))
    vals.sort()
    return {"lo":vals[int(.05*BOOT_DRAWS)],"hi":vals[min(BOOT_DRAWS-1,int(.95*BOOT_DRAWS)-1)],"mean":statistics.mean(vals)}

def profile_arm(lineages,arm,trials,raw):
    profiles=[]; raw_rates=[]
    by_family={fam:[i for i,t in enumerate(trials) if t["family"]==fam] for fam in FAMILIES}
    for row in lineages:
        li=row["index"]; base=row["shells"][arm]
        exact={c:[False]*len(trials) for c in CONDITIONS}; paths={c:[None]*len(trials) for c in CONDITIONS}
        for ti,t in enumerate(trials):
            for cond in CONDITIONS:
                r=run_trial(base,t,cond); exact[cond][ti]=bool(r["exact"]); paths[cond][ti]=r["path"]
                raw.write(json.dumps({"arm":arm,"lineage":"WT4-{:03d}".format(li),"trial_id":ti,"family":t["family"],"condition":cond,"exact":r["exact"],"path":r["path"]},sort_keys=True,separators=(",",":"))+"\n")
        prof={}; rates={}
        for fam,idxs in by_family.items():
            cg=statistics.mean(1.0 if exact["CONGRUENT"][i] else 0.0 for i in idxs)
            sh=statistics.mean(1.0 if exact["SHUFFLED"][i] else 0.0 for i in idxs)
            qo=statistics.mean(1.0 if exact["QUERY_ONLY"][i] else 0.0 for i in idxs)
            prof[fam]=cg-sh
            rates[fam]={"congruent":cg,"shuffled":sh,"query_only":qo,"lift":cg-sh}
        profiles.append(prof); raw_rates.append({"lineage":li,"rates":rates,"exact":exact,"paths":paths})
    return profiles,raw_rates

def atlas_w(lineages,rates,trials):
    out=[]; pointer_hits=set()
    for ti,t in enumerate(trials):
        successes=[]
        for row,rr in zip(lineages,rates):
            if rr["exact"]["CONGRUENT"][ti]:
                seq="{}-{}-{}".format(t["query_source"],t["query_mid"],t["query_terminal"])
                if seq in POINTER_TRIPLETS:pointer_hits.add(seq)
                successes.append({"lineage":"WT4-{:03d}".format(row["index"]),"path":rr["paths"]["CONGRUENT"][ti]})
        out.append({**t,"successful_lineages":successes})
    return out,sorted(pointer_hits)

def report(result):
    p=result["primary"]; be=result["passage_beyond_entry"]; pfm=result["pfm_sufficiency"]; val=result["topology_validity"]
    lines=["# WARP-T4 — Portable Trace and Relational Entry Result","",
      "- eligible lineages: {}/{}".format(result["eligible"],N),
      "- portable Warp trace changes relational entry: **{}**".format("PASS" if p["held"] else "FAIL"),
      "- W vs N multivariate p: {:.8g}".format(p["multivariate"]["p"]),
      "- passage beyond entry: **{}**".format("PASS" if be["held"] else "FAIL"),
      "- W vs E multivariate p: {:.8g}".format(be["multivariate"]["p"]),
      "- PFM sufficiency: **{}**".format("PASS" if pfm["held"] else "FAIL"),
      "- topology-only validity: **{}**".format("PASS" if val["valid"] else "FAIL"),"",
      "## W vs N family differences",""]
    for fam,v in p["multivariate"]["components"].items():
        lines.append("- {}: mean Δ={:.6f}, Holm p={:.8g}".format(fam,v["mean_difference"],v["holm_p"]))
    lines += ["","## PFM equivalence",""]
    for fam,v in pfm["families"].items():
        lines.append("- {}: 90% CI [{:.6f}, {:.6f}]".format(fam,v["lo"],v["hi"]))
    lines += ["","## Interpretation","",result["interpretation"],""]
    return "\n".join(lines)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",default="experiments/warp_t4/results"); args=ap.parse_args()
    os.makedirs(args.out,exist_ok=True)
    existing=os.path.join(args.out,"summary.json")
    if os.path.exists(existing):
        print(open(existing,encoding="utf-8").read()); return 0

    trials=load_trials(); validate_trials(trials)
    all_rows=[make_lineage(i) for i in range(N)]
    lineages=[x for x in all_rows if x["eligible"]]
    if len(lineages)<80:
        result={"schema":"amelia-warp-t4-v1","eligible":len(lineages),"valid":False,"interpretation":"Fewer than 80 eligible lineages; primary claim not evaluated."}
        with open(existing,"w") as h:json.dump(result,h,indent=2,sort_keys=True)
        with open(os.path.join(args.out,"REPORT.md"),"w") as h:h.write("# WARP-T4 Result\n\nInsufficient eligible lineages: {}/160.\n".format(len(lineages)))
        print(json.dumps(result,indent=2)); return 0

    profiles={}; rates={}
    raw_path=os.path.join(args.out,"records.jsonl.gz")
    with gzip.open(raw_path,"wt",encoding="utf-8") as raw:
        for arm in ARMS:
            profiles[arm],rates[arm]=profile_arm(lineages,arm,trials,raw)

    wn=multivar(profiles["W"],profiles["N"],PERM_BASE,3267100)
    wb=multivar(profiles["W"],profiles["B"],PERM_BASE+10,3267110)
    we=multivar(profiles["W"],profiles["E"],PERM_BASE+1,3267120)
    tb=multivar(profiles["T"],profiles["B"],PERM_BASE+2,3267130)

    shared=[fam for fam in FAMILIES if wn["components"][fam]["holm_p"]<=.05 and wb["components"][fam]["holm_p"]<=.05]
    valid=not (tb["p"]<=.01 or any(v["holm_p"]<=.05 for v in tb["components"].values()))
    primary=wn["p"]<=.01 and bool(shared) and valid
    beyond=we["p"]<=.01 and any(v["holm_p"]<=.05 for v in we["components"].values())

    cis={}; pfm=True
    for j,fam in enumerate(FAMILIES):
        diffs=[profiles["P"][i][fam]-profiles["W"][i][fam] for i in range(len(lineages))]
        ci=bootstrap_ci(diffs,BOOT_BASE+j); cis[fam]=ci
        if not (ci["lo"]>-.05 and ci["hi"]<.05):pfm=False

    if primary:
        interp="The portable Warp-passage trace changes the relation-specific priming profile after common-state release relative to matched non-Warp passage."
    else:
        interp="WARP-T4 does not satisfy the registered claim that the portable Warp trace changes which composed Numogrammatic relations the released process can enter."
    if beyond:interp+=" Passage beyond entry contributes to the relational-profile difference."
    else:interp+=" Passage beyond entry does not satisfy its registered relational-profile gate."
    if pfm:interp+=" The incremental PFM trace is sufficient within the registered ±0.05 family-profile margins."
    else:interp+=" PFM-only equivalence to the full Warp relational profile is not established."
    if not valid:interp+=" The topology-only validity control failed, invalidating the portable-trace interpretation."

    at,pointer=atlas_w(lineages,rates["W"],trials)
    result={
      "schema":"amelia-warp-t4-v1","eligible":len(lineages),"valid":valid,
      "primary":{"held":primary,"shared_significant_families":shared,"multivariate":wn,"W_vs_B":wb},
      "passage_beyond_entry":{"held":beyond,"multivariate":we},
      "pfm_sufficiency":{"held":pfm,"families":cis},
      "topology_validity":{"valid":valid,"multivariate":tb},
      "arm_family_means":{arm:{fam:statistics.mean(x[fam] for x in profiles[arm]) for fam in FAMILIES} for arm in ARMS},
      "atlas":at,"pointer_hits":pointer,"interpretation":interp,
      "provenance":{"registration_sha256":sha256_file("experiments/warp_t4/REGISTRATION.md"),
        "amendment_sha256":sha256_file("experiments/warp_t4/AMENDMENT_1.md"),
        "trials_sha256":sha256_file("experiments/warp_t4/TRIALS.json"),
        "runner_sha256":sha256_file("experiments/warp_t4/run.py"),
        "raw_sha256":sha256_file(raw_path)}
    }
    with open(existing,"w") as h:json.dump(result,h,indent=2,sort_keys=True)
    with open(os.path.join(args.out,"ATLAS.md"),"w") as h:
        h.write("# WARP-T4 — Relational Entry Atlas\n\n")
        h.write("Pointer-catalogue exact triplet hits: {}\n\n".format(", ".join(pointer) if pointer else "none"))
        for x in at:
            h.write("## Trial {:02d} — {}\n\n".format(x["trial_id"],x["family"]))
            h.write("- demonstration: {}→{}→{}\n".format(x["demo_source"],x["demo_mid"],x["demo_terminal"]))
            h.write("- unseen query: {}→{}→{}\n".format(x["query_source"],x["query_mid"],x["query_terminal"]))
            h.write("- successful W lineages: {}\n\n".format(", ".join(z["lineage"] for z in x["successful_lineages"]) if x["successful_lineages"] else "none"))
    with open(os.path.join(args.out,"REPORT.md"),"w") as h:h.write(report(result))
    print(json.dumps({k:result[k] for k in ("eligible","primary","passage_beyond_entry","pfm_sufficiency","topology_validity","arm_family_means","pointer_hits","interpretation")},indent=2,sort_keys=True))
    return 0

if __name__=="__main__":raise SystemExit(main())
