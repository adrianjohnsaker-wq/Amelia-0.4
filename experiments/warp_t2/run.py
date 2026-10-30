#!/usr/bin/env python3
"""WARP-T2 — Portable Passage Trace."""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import importlib.util
import json
import math
import os
import random
import statistics
import sys
from collections import Counter, defaultdict
from typing import Dict, List, Sequence, Tuple

ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
if ROOT not in sys.path: sys.path.insert(0,ROOT)
P316=os.path.join(ROOT,"experiments","p316")
if P316 not in sys.path: sys.path.insert(0,P316)
from DynamicNumogram import DynamicNumogramProcess, IntegratedMemorySystem, warp_open_gates

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(mod); return mod

p317=load_module("p317_frozen",os.path.join(ROOT,"experiments","p317","run.py"))
wt1=load_module("warp_t1_frozen",os.path.join(ROOT,"experiments","warp_t1","run.py"))

N=192
SEED_BASE=3220000
PROBE_BASE=3225000
PERM_BASE=3227000
DRAWS=50000
WINDOW_KEYS=("zone_entropy","transition_entropy","distinct_zones","distinct_4grams","non_echo_breadth","warp_occupancy","bias_mag","activation_hhi","hysteresis","strain_mass")
ARMS=("PRE_ENTRY_BASELINE_TRACE","WARP_FULL_TRACE","WARP_PFM_TRACE","WARP_TENSOR_TRACE","WARP_TRACE_RESET","ENTRY_ONLY_TRACE","TOPOLOGY_ONLY_TRACE","NONWARP_FULL_TRACE")
NONWARP_ZONES=(0,1,2,4,5,7,8,9)

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def entropy_counter(c):
    n=sum(c.values())
    if not n:return 0.0
    return -sum((v/n)*math.log(v/n,2) for v in c.values() if v)

def release_probe(index,passage_inputs):
    seed=PROBE_BASE+index
    matrix=p317.transition_matrix(seed)
    forbidden=p317.ngrams(passage_inputs,4)
    for attempt in range(10000):
        tape=p317.sample_markov_tape(matrix,seed+1000000+attempt,64)
        if not (p317.ngrams(tape,4)&forbidden):return tape
    raise RuntimeError("release probe rejection exhausted")

def passage_real(pre,input_zone,target,rest4):
    p=copy.deepcopy(pre)
    outputs=[]
    outputs.append(wt1.forced_step(p,input_zone,target,"normal"))
    for sym in rest4:
        out=p.step(int(sym))
        outputs.append({"source":int(out["from_zone"]),"target":int(out["to_zone"]),"actual":int(out["to_zone"])})
    return p,[int(x["target"]) for x in outputs]

def passage_forced(pre,inputs,targets,first_normal=False):
    p=copy.deepcopy(pre)
    for j,(sym,target) in enumerate(zip(inputs,targets)):
        if first_normal and j==0:
            wt1.forced_step(p,int(sym),int(target),"normal")
        else:
            memory_before=copy.deepcopy(p.memory)
            wt1.forced_step(p,int(sym),int(target),"topology_only")
            p.memory=memory_before
    return p

def passage_nonwarp(pre,inputs):
    p=copy.deepcopy(pre)
    p.gates=warp_open_gates()
    for sym in inputs:
        wt1.forced_step(p,int(sym),None,"normal",True)
        if p.current_zone in (3,6):raise RuntimeError("matched passage entered Warp")
    return p

def release_shell(pre,slow_memory,slow_tensor,seed):
    p=copy.deepcopy(pre)
    p.gates=warp_open_gates()
    p.current_zone=NONWARP_ZONES[seed%len(NONWARP_ZONES)]
    p.zone_visit_counts=[0]*10; p.zone_visit_counts[p.current_zone]=1
    p.transition_counts=[[0]*10 for _ in range(10)]
    p.step_count=0
    p.last_trait_snapshot=None; p.last_audit=None
    p.memory=copy.deepcopy(slow_memory)
    p.deformation_tensor=list(slow_tensor)
    return p

def state_step(p,sym):
    out=p.step(int(sym))
    r=p.memory.read_memory_bias()
    acts=[float(p.zones[i]["activation"]) for i in range(10)]
    total=sum(acts)
    return {
      "zone":int(p.current_zone),
      "edge":(int(out["from_zone"]),int(out["to_zone"])),
      "bias_mag":statistics.mean(abs(float(x)) for x in r.bias_vector),
      "activation_hhi":sum((x/total)**2 for x in acts) if total else 0.0,
      "hysteresis":float(r.hysteresis_tension),
      "strain_mass":sum(float(x) for x in p.memory.zone_strain_history),
    }

def window_metrics(records,probe,start,stop):
    rs=records[start:stop]
    zones=[r["zone"] for r in rs]
    edges=Counter(r["edge"] for r in rs)
    zc=Counter(zones)
    response4=p317.ngrams(zones,4)
    input4=p317.ngrams(probe,4)
    return {
      "zone_entropy":entropy_counter(zc),
      "transition_entropy":entropy_counter(edges),
      "distinct_zones":float(len(set(zones))),
      "distinct_4grams":float(len(response4)),
      "non_echo_breadth":float(len(response4-input4)),
      "warp_occupancy":sum(1 for z in zones if z in (3,6))/len(zones),
      "bias_mag":statistics.mean(r["bias_mag"] for r in rs),
      "activation_hhi":statistics.mean(r["activation_hhi"] for r in rs),
      "hysteresis":statistics.mean(r["hysteresis"] for r in rs),
      "strain_mass":statistics.mean(r["strain_mass"] for r in rs),
    }

def run_release(p,probe):
    records=[state_step(p,s) for s in probe]
    return {
      "early":window_metrics(records,probe,0,32),
      "late":window_metrics(records,probe,32,64),
      "path":[r["zone"] for r in records],
    }

def signflip_p(diffs,seed,two_sided=False):
    if not diffs:return 1.0
    obs=statistics.mean(diffs); rng=random.Random(seed); ge=0
    for _ in range(DRAWS):
        m=statistics.mean(d*(1 if rng.random()<.5 else -1) for d in diffs)
        condition=abs(m)>=abs(obs)-1e-15 if two_sided else m>=obs-1e-15
        if condition:ge+=1
    return (ge+1)/(DRAWS+1)

def holm(raw):
    ordered=sorted(raw.items(),key=lambda kv:(kv[1],kv[0])); m=len(ordered); out={}; running=0.0
    for i,(k,p) in enumerate(ordered):
        running=max(running,min(1.0,(m-i)*p)); out[k]=running
    return out

def multivar(left,right,seed,component_seed):
    ds=[[float(left[i][k])-float(right[i][k]) for k in WINDOW_KEYS] for i in range(len(left))]
    sds=[]
    for j in range(len(WINDOW_KEYS)):
        col=[d[j] for d in ds]
        sd=statistics.stdev(col) if len(col)>1 else 0.0
        sds.append(sd if sd>1e-12 else 0.0)
    def stat(signs=None):
        t=0.0
        for j,sd in enumerate(sds):
            if sd<=0:continue
            vals=[d[j]*(1 if signs is None else signs[i]) for i,d in enumerate(ds)]
            t+=(statistics.mean(vals)/sd)**2
        return t
    obs=stat(); rng=random.Random(seed); ge=0
    for _ in range(DRAWS):
        signs=[1 if rng.random()<.5 else -1 for _ in ds]
        if stat(signs)>=obs-1e-15:ge+=1
    comp={}; raw={}
    for j,k in enumerate(WINDOW_KEYS):
        diffs=[d[j] for d in ds]; p=signflip_p(diffs,component_seed+j,True)
        comp[k]={"mean_difference":statistics.mean(diffs),"p_two_sided":p}; raw[k]=p
    adj=holm(raw)
    for k in comp:comp[k]["holm_p"]=adj[k]
    return {"T":obs,"p":(ge+1)/(DRAWS+1),"components":comp}

def pooled_sd(xs,ys):
    vals=list(xs)+list(ys)
    sd=statistics.stdev(vals) if len(vals)>1 else 0.0
    return sd if sd>1e-12 else 0.0

def carriage(full,reset,carrier,seed):
    scales={k:pooled_sd([x[k] for x in full],[x[k] for x in reset]) for k in WINDOW_KEYS}
    advantages=[]
    for f,r,c in zip(full,reset,carrier):
        use=[k for k in WINDOW_KEYS if scales[k]>0]
        dc=math.sqrt(sum(((c[k]-f[k])/scales[k])**2 for k in use))
        dr=math.sqrt(sum(((r[k]-f[k])/scales[k])**2 for k in use))
        advantages.append(dr-dc)
    return {"mean_advantage":statistics.mean(advantages),"p_upper":signflip_p(advantages,seed,False)}

def motif_atlas(rows):
    counts=defaultdict(list)
    for row in rows:
        if not row["eligible"]:continue
        path=row["arms"]["WARP_FULL_TRACE"]["path"]
        probe=row["probe"]
        echo=p317.ngrams(probe,4)
        seen=defaultdict(list)
        for i in range(len(path)-3):
            m=tuple(path[i:i+4])
            if m not in echo:seen[m].append(i)
        for m,starts in seen.items():counts[m].append((row["lineage"],starts))
    ranked=sorted(counts.items(),key=lambda kv:(-len(kv[1]),kv[0]))[:30]
    return [{"motif":"-".join(map(str,m)),"lineage_count":len(xs),"lineages":[{"lineage":li,"starts":st} for li,st in xs]} for m,xs in ranked]


def build_lineage(index):
    seed=SEED_BASE+index
    e=wt1.first_entry(seed)
    if e is None or len(e["remaining"])<4:
        return {"lineage":"WT2-{:03d}".format(index),"seed":seed,"eligible":False}
    inputs=[int(e["input"])]+[int(x) for x in e["remaining"][:4]]
    real,targets=passage_real(e["pre"],inputs[0],e["target"],inputs[1:])
    entry=passage_forced(e["pre"],inputs,targets,True)
    topo=passage_forced(e["pre"],inputs,targets,False)
    matched=None
    try:
        matched=passage_nonwarp(e["pre"],inputs)
    except Exception:
        matched=None

    probe=release_probe(index,inputs)
    pre=e["pre"]
    blank=IntegratedMemorySystem()
    baseline_tensor=list(pre.deformation_tensor)
    arms={}

    slow_specs={
      "PRE_ENTRY_BASELINE_TRACE":(pre.memory,baseline_tensor),
      "WARP_FULL_TRACE":(real.memory,real.deformation_tensor),
      "WARP_PFM_TRACE":(real.memory,baseline_tensor),
      "WARP_TENSOR_TRACE":(pre.memory,real.deformation_tensor),
      "WARP_TRACE_RESET":(blank,[0.1]*10),
      "ENTRY_ONLY_TRACE":(entry.memory,entry.deformation_tensor),
      "TOPOLOGY_ONLY_TRACE":(topo.memory,topo.deformation_tensor),
    }
    if matched is not None:
        slow_specs["NONWARP_FULL_TRACE"]=(matched.memory,matched.deformation_tensor)

    for arm,(mem,tensor) in slow_specs.items():
        shell=release_shell(pre,mem,tensor,seed)
        arms[arm]=run_release(shell,probe)

    return {
      "lineage":"WT2-{:03d}".format(index),
      "seed":seed,
      "eligible":True,
      "matched_eligible":matched is not None,
      "entry_step":int(e["index"]),
      "entry_source":int(pre.current_zone),
      "entry_target":int(e["target"]),
      "passage_inputs":inputs,
      "passage_targets":targets,
      "probe":probe,
      "arms":arms,
    }

def select(rows,arm_a,arm_b,window="late",matched=False):
    eligible=[r for r in rows if r["eligible"] and (not matched or r["matched_eligible"]) and arm_a in r["arms"] and arm_b in r["arms"]]
    return eligible,[r["arms"][arm_a][window] for r in eligible],[r["arms"][arm_b][window] for r in eligible]

def report(result):
    p=result["portable"]; beyond=result["passage_beyond_entry"]; carr=result["carriage"]; valid=result["topology_validity"]
    lines=[
      "# WARP-T2 — Portable Passage Trace Result","",
      "- eligible natural-entry lineages: {}/{}".format(result["eligible_lineages"],N),
      "- eligible matched-nonWarp lineages: {}".format(result["matched_lineages"]),
      "- portable Warp-passage transformation: **{}**".format("PASS" if p["held"] else "FAIL"),
      "- passage contributes beyond entry: **{}**".format("PASS" if beyond["held"] else "FAIL"),
      "- PFM carriage: **{}**".format("PASS" if carr["pfm"]["held"] else "FAIL"),
      "- tensor carriage: **{}**".format("PASS" if carr["tensor"]["held"] else "FAIL"),
      "- topology-only validity: **{}**".format("PASS" if valid["valid"] else "FAIL / INTERPRETATION INVALIDATED"),"",
      "## Portable comparison","",
      "- WARP_FULL vs NONWARP_FULL late multivariate p: {:.8g}".format(p["warp_vs_nonwarp"]["p"]),
      "- WARP_FULL vs PRE_ENTRY_BASELINE late multivariate p: {:.8g}".format(p["warp_vs_baseline"]["p"]),"",
      "## Passage beyond entry","",
      "- WARP_FULL vs ENTRY_ONLY late multivariate p: {:.8g}".format(beyond["multivariate"]["p"]),"",
      "## Carriage","",
      "- PFM closeness advantage: {:.8f}, p={:.8g}".format(carr["pfm"]["mean_advantage"],carr["pfm"]["p_upper"]),
      "- tensor closeness advantage: {:.8f}, p={:.8g}".format(carr["tensor"]["mean_advantage"],carr["tensor"]["p_upper"]),"",
      "## Interpretation","",result["interpretation"],""
    ]
    return "\n".join(lines)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",default="experiments/warp_t2/results"); args=ap.parse_args()
    os.makedirs(args.out,exist_ok=True)
    existing=os.path.join(args.out,"summary.json")
    if os.path.exists(existing):
        print(open(existing,encoding="utf-8").read()); return 0

    rows=[build_lineage(i) for i in range(N)]
    eligible=sum(1 for r in rows if r["eligible"])
    matched=sum(1 for r in rows if r["eligible"] and r["matched_eligible"])

    # Primary: Warp trace versus matched non-Warp trace on matched-eligible lineages.
    r_m,wf_l,nw_l=select(rows,"WARP_FULL_TRACE","NONWARP_FULL_TRACE","late",True)
    mv_nonwarp=multivar(wf_l,nw_l,PERM_BASE,PERM_BASE+100)
    _,wf_e,nw_e=select(rows,"WARP_FULL_TRACE","NONWARP_FULL_TRACE","early",True)

    # Necessity of incremental passage trace relative to pre-entry mature slow state.
    r_b,wf_b,base_b=select(rows,"WARP_FULL_TRACE","PRE_ENTRY_BASELINE_TRACE","late",False)
    mv_base=multivar(wf_b,base_b,PERM_BASE+1,PERM_BASE+120)

    surviving=[k for k,v in mv_nonwarp["components"].items()
               if v["holm_p"]<=.05 and
               statistics.mean(a[k]-b[k] for a,b in zip(wf_e,nw_e))*v["mean_difference"]>0]
    portable_pre=(mv_nonwarp["p"]<=.01 and bool(surviving) and mv_base["p"]<=.01)

    # Passage beyond the entry event.
    _,wf_entry,entry_l=select(rows,"WARP_FULL_TRACE","ENTRY_ONLY_TRACE","late",False)
    mv_entry=multivar(wf_entry,entry_l,PERM_BASE+2,PERM_BASE+140)
    beyond_survivors=[k for k,v in mv_entry["components"].items() if v["holm_p"]<=.05]
    beyond=mv_entry["p"]<=.01 and bool(beyond_survivors)

    # Topology-only passage must leave no portable slow trace beyond pre-entry baseline.
    _,top_l,base_t=select(rows,"TOPOLOGY_ONLY_TRACE","PRE_ENTRY_BASELINE_TRACE","late",False)
    mv_top=multivar(top_l,base_t,PERM_BASE+3,PERM_BASE+160)
    invalid_top=(mv_top["p"]<=.01 or any(v["holm_p"]<=.05 for v in mv_top["components"].values()))

    # Incremental PFM/tensor carriers.
    _,full_c,base_c=select(rows,"WARP_FULL_TRACE","PRE_ENTRY_BASELINE_TRACE","late",False)
    _,_,pfm_c=select(rows,"WARP_FULL_TRACE","WARP_PFM_TRACE","late",False)
    _,_,tensor_c=select(rows,"WARP_FULL_TRACE","WARP_TENSOR_TRACE","late",False)
    pfm_car=carriage(full_c,base_c,pfm_c,PERM_BASE+200)
    tensor_car=carriage(full_c,base_c,tensor_c,PERM_BASE+201)
    pfm_car["held"]=pfm_car["mean_advantage"]>0 and pfm_car["p_upper"]<=.01
    tensor_car["held"]=tensor_car["mean_advantage"]>0 and tensor_car["p_upper"]<=.01

    portable=portable_pre and not invalid_top

    if portable:
        interp="A finite canonical 3::6 passage leaves a downstream transformation that survives common-state release under nonterminal Warp-open dynamics."
    else:
        interp="WARP-T2 does not establish a portable Warp-passage transformation under the registered common-state release assay."
    if beyond: interp+=" The finite passage contributes beyond the entry event alone."
    else: interp+=" The finite passage was not shown to add a late effect beyond the entry event alone."
    if pfm_car["held"]: interp+=" Incremental PFM carries a significant share of the portable response geometry."
    if tensor_car["held"]: interp+=" Incremental tensor deformation carries a significant share of the portable response geometry."
    if invalid_top: interp+=" The topology-only validity control changed downstream response, so the portable interpretation is invalidated."

    atlas=motif_atlas(rows)
    result={
      "schema":"amelia-warp-t2-v1",
      "eligible_lineages":eligible,
      "matched_lineages":matched,
      "portable":{"held":portable,"pre_validity_held":portable_pre,"surviving_components":surviving,"warp_vs_nonwarp":mv_nonwarp,"warp_vs_baseline":mv_base},
      "passage_beyond_entry":{"held":beyond,"surviving_components":beyond_survivors,"multivariate":mv_entry},
      "carriage":{"pfm":pfm_car,"tensor":tensor_car},
      "topology_validity":{"valid":not invalid_top,"multivariate":mv_top},
      "atlas":atlas,
      "interpretation":interp,
      "provenance":{
        "registration_sha256":sha256_file("experiments/warp_t2/REGISTRATION.md"),
        "amendment1_sha256":sha256_file("experiments/warp_t2/AMENDMENT_1.md"),
        "amendment2_sha256":sha256_file("experiments/warp_t2/AMENDMENT_2.md"),
        "amendment3_sha256":sha256_file("experiments/warp_t2/AMENDMENT_3.md"),
        "runner_sha256":sha256_file("experiments/warp_t2/run.py"),
        "engine_sha256":sha256_file("experiments/p316/DynamicNumogram.py")
      }
    }
    with open(existing,"w",encoding="utf-8") as h:json.dump(result,h,indent=2,sort_keys=True)
    with gzip.open(os.path.join(args.out,"lineages.jsonl.gz"),"wt",encoding="utf-8") as h:
        for row in rows:h.write(json.dumps(row,sort_keys=True,separators=(",",":"))+"\n")
    with open(os.path.join(args.out,"ATLAS.md"),"w",encoding="utf-8") as h:
        h.write("# WARP-T2 — Post-release Non-echo Motif Atlas\n\n")
        for x in atlas:
            h.write("- {}: {} lineages\n".format(x["motif"],x["lineage_count"]))
    with open(os.path.join(args.out,"REPORT.md"),"w",encoding="utf-8") as h:h.write(report(result))
    print(json.dumps({k:result[k] for k in ("eligible_lineages","matched_lineages","portable","passage_beyond_entry","carriage","topology_validity","interpretation")},indent=2,sort_keys=True))
    return 0

if __name__=="__main__": raise SystemExit(main())
