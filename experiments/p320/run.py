#!/usr/bin/env python3
"""P3.20 — Developmental Accessibility Geometry."""
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
from DynamicNumogram import DynamicNumogramProcess, IntegratedMemorySystem

P317_PATH=os.path.join(ROOT,"experiments","p317","run.py")
spec=importlib.util.spec_from_file_location("p317_frozen",P317_PATH)
p317=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(p317)

N=96
LINEAGE_BASE=3210000
DONOR_SEED=3214000
PROBE_BASE=3215000
REWIRE_BASE=3216000
PERM_BASE=3217000
DRAWS=50000
PROBE_COUNT=48
PROBE_LEN=32
HALF=24
REWIRE_COUNT=24
GEOM_KEYS=("non_echo_breadth","motif_entropy","edge_breadth","probe_divergence")
ARMS=("FULL_OWN","BLANK","DONOR_PFM","FRESH","STATIC_CANONICAL")

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def make_probe(i:int)->List[int]:
    seed=PROBE_BASE+i
    matrix=p317.transition_matrix(seed*17+5)
    return p317.sample_markov_tape(matrix,seed*31+9,PROBE_LEN)

def response_from_records(records,probe):
    path=[int(r["zone"]) for r in records]
    echo=p317.ngrams(probe,4)
    positions=defaultdict(list)
    all4=[]
    for i in range(len(path)-3):
        motif=tuple(path[i:i+4]); all4.append(motif)
        if motif not in echo: positions[motif].append(i)
    edges={(path[i],path[i+1]) for i in range(len(path)-1)}
    return {
      "path":path,
      "non_echo_positions":{"-".join(map(str,k)):v for k,v in positions.items()},
      "non_echo_occurrences":["-".join(map(str,m)) for m in all4 if m not in echo],
      "edges":[list(x) for x in sorted(edges)],
      "warp_capture":bool(path and path[-1] in (3,6)),
    }

def run_dynamic_probe(base,probe):
    p=copy.deepcopy(base)
    rec=p317.run_dynamic_tape(p,probe)
    return response_from_records(rec,probe)

def run_static_probe(current_zone,probe):
    rec=p317.run_static_tape(current_zone,probe)
    return response_from_records(rec,probe)

def entropy_counts(counter):
    total=sum(counter.values())
    if not total:return 0.0
    return -sum((c/total)*math.log(c/total,2) for c in counter.values() if c)

def divergence(responses):
    n=len(responses)
    if n<2:return 0.0
    total_pairs=n*(n-1)/2
    disagree=0.0
    for pos in range(PROBE_LEN):
        c=Counter(r["path"][pos] for r in responses)
        same=sum(v*(v-1)/2 for v in c.values())
        disagree += (total_pairs-same)/total_pairs
    return disagree/PROBE_LEN

def aggregate_geometry(responses):
    motifs=Counter()
    edges=set()
    for r in responses:
        motifs.update(r["non_echo_occurrences"])
        edges.update(tuple(e) for e in r["edges"])
    return {
      "non_echo_breadth":float(len(motifs)),
      "motif_entropy":entropy_counts(motifs),
      "edge_breadth":float(len(edges)),
      "probe_divergence":divergence(responses),
      "warp_capture_fraction":sum(1 for r in responses if r["warp_capture"])/len(responses),
      "motif_set":set(motifs.keys()),
    }

def split_geometry(responses):
    return {
      "all":aggregate_geometry(responses),
      "A":aggregate_geometry(responses[:HALF]),
      "B":aggregate_geometry(responses[HALF:]),
    }

def signflip_p(diffs,seed,two_sided=False):
    if not diffs:return 1.0
    obs=statistics.mean(diffs)
    rng=random.Random(seed); ge=0
    for _ in range(DRAWS):
        m=statistics.mean(d*(1 if rng.random()<.5 else -1) for d in diffs)
        condition = abs(m)>=abs(obs)-1e-15 if two_sided else m>=obs-1e-15
        if condition: ge+=1
    return (ge+1)/(DRAWS+1)

def holm(raw):
    ordered=sorted(raw.items(),key=lambda kv:(kv[1],kv[0]))
    m=len(ordered); out={}; running=0.0
    for i,(k,p) in enumerate(ordered):
        running=max(running,min(1.0,(m-i)*p)); out[k]=running
    return out

def multivar(left,right,seed):
    ds=[[float(left[i][k])-float(right[i][k]) for k in GEOM_KEYS] for i in range(len(left))]
    sds=[]
    for j in range(len(GEOM_KEYS)):
        col=[d[j] for d in ds]
        sds.append(statistics.stdev(col) if len(col)>1 and statistics.stdev(col)>1e-12 else 0.0)
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
        if stat(signs)>=obs-1e-15: ge+=1
    comp={}
    raw={}
    for j,k in enumerate(GEOM_KEYS):
        diffs=[d[j] for d in ds]
        p=signflip_p(diffs,PERM_BASE+100+j,True)
        raw[k]=p
        comp[k]={"mean_difference":statistics.mean(diffs),"p_two_sided":p}
    adj=holm(raw)
    for k in comp:comp[k]["holm_p"]=adj[k]
    return {"T":obs,"p":(ge+1)/(DRAWS+1),"components":comp}

def pooled_sd(xs,ys):
    vals=list(xs)+list(ys)
    return statistics.stdev(vals) if len(vals)>1 and statistics.stdev(vals)>1e-12 else 0.0

def donor_transfer(full,blank,donor,seed):
    scales={k:pooled_sd([x[k] for x in full],[x[k] for x in blank]) for k in GEOM_KEYS}
    advantages=[]
    for f,b,d in zip(full,blank,donor):
        use=[k for k in GEOM_KEYS if scales[k]>0]
        df=math.sqrt(sum(((d[k]-f[k])/scales[k])**2 for k in use))
        db=math.sqrt(sum(((d[k]-b[k])/scales[k])**2 for k in use))
        advantages.append(db-df)
    return {"mean_advantage":statistics.mean(advantages),"p_upper":signflip_p(advantages,seed,False)}

def addressability(lineage_responses,include_details=False):
    # lineage_responses[lineage][probe]
    motif_by_probe=[defaultdict(list) for _ in range(PROBE_COUNT)]
    for li,resps in enumerate(lineage_responses):
        for pi,r in enumerate(resps):
            for motif,starts in r["non_echo_positions"].items():
                motif_by_probe[pi][motif].append((li,starts))
    prevalence=[]
    for pi in range(PROBE_COUNT):
        prevalence.append({m:len(rows)/N for m,rows in motif_by_probe[pi].items()})
    maxima=[]; details=[]
    for pi in range(PROBE_COUNT):
        candidates=[]
        for motif,rows in motif_by_probe[pi].items():
            if len(rows)<8:continue
            others=[prevalence[q].get(motif,0.0) for q in range(PROBE_COUNT) if q!=pi]
            spec=len(rows)/N-statistics.mean(others)
            if spec>0:candidates.append((spec,len(rows)/N,motif,rows))
        if candidates:
            candidates.sort(key=lambda x:(-x[0],-x[1],x[2]))
            spec,prev,motif,rows=candidates[0]; maxima.append(spec)
            if include_details:
                details.append({
                  "probe_id":pi,"motif":motif,"prevalence":prev,"specificity":spec,
                  "lineages":[{"lineage":"P320-{:03d}".format(li),"starts":starts} for li,starts in rows]
                })
        else:
            maxima.append(0.0)
            if include_details:details.append({"probe_id":pi,"motif":None,"prevalence":0.0,"specificity":0.0,"lineages":[]})
    return {"score":statistics.mean(maxima),"probe_maxima":maxima,"details":details}


def develop_canonical():
    rows=[]
    permeability=p317.original_gate_permeability(p317.FULL_NUMOGRAM_GATES)
    for i in range(N):
        seed=LINEAGE_BASE+i
        dev,_=p317.make_tapes(seed)
        p=DynamicNumogramProcess(current_zone=seed%10)
        p317.run_dynamic_tape(p,dev)
        mature=copy.deepcopy(p)
        shocked=copy.deepcopy(p)
        p317.shock_process(shocked,seed,permeability)
        rows.append({"seed":seed,"dev":dev,"mature":mature,"shocked":shocked})
    return rows

def build_focal_bases(rows,donor_map):
    bases={arm:[] for arm in ARMS if arm!="STATIC_CANONICAL"}
    static_zones=[]
    for i,row in enumerate(rows):
        s=row["shocked"]
        bases["FULL_OWN"].append(copy.deepcopy(s))
        b=copy.deepcopy(s); b.memory=IntegratedMemorySystem(); b.deformation_tensor=[0.1]*10
        bases["BLANK"].append(b)
        d=copy.deepcopy(s); d.memory=copy.deepcopy(rows[donor_map[i]]["shocked"].memory); d.deformation_tensor=[0.1]*10
        bases["DONOR_PFM"].append(d)
        bases["FRESH"].append(DynamicNumogramProcess(current_zone=s.current_zone))
        static_zones.append(int(s.current_zone))
    return bases,static_zones

def collect_focal(rows,probes,donor_map):
    bases,static_zones=build_focal_bases(rows,donor_map)
    responses={arm:[[] for _ in range(N)] for arm in ARMS}
    for i in range(N):
        for probe in probes:
            for arm in ("FULL_OWN","BLANK","DONOR_PFM","FRESH"):
                responses[arm][i].append(run_dynamic_probe(bases[arm][i],probe))
            responses["STATIC_CANONICAL"][i].append(run_static_probe(static_zones[i],probe))
    return responses

def lineage_geometry(responses):
    return {
      arm:[split_geometry(responses[arm][i]) for i in range(N)]
      for arm in responses
    }

def rewire_controller(controller_index,rows,probes):
    gates=p317.rewired_gates(REWIRE_BASE+controller_index)
    permeability=p317.original_gate_permeability(gates)
    all_responses=[]
    geometry=[]
    for i,row in enumerate(rows):
        seed=int(row["seed"])
        p=DynamicNumogramProcess(gates=gates,current_zone=seed%10)
        p317.run_dynamic_tape(p,row["dev"])
        p317.shock_process(p,seed,permeability)
        rr=[run_dynamic_probe(p,probe) for probe in probes]
        all_responses.append(rr)
        geometry.append(split_geometry(rr))
    addr=addressability(all_responses,False)
    means={
      half:{k:statistics.mean(g[half][k] for g in geometry) for k in GEOM_KEYS}
      for half in ("all","A","B")
    }
    return {
      "controller":controller_index,
      "seed":REWIRE_BASE+controller_index,
      "addressability_score":addr["score"],
      "geometry_means":means,
      "responses":all_responses,
    }

def write_raw(path,focal,rewire_summaries):
    with gzip.open(path,"wt",encoding="utf-8") as h:
        for arm in ARMS:
            for li in range(N):
                h.write(json.dumps({
                  "kind":"focal","arm":arm,"lineage":"P320-{:03d}".format(li),
                  "responses":focal[arm][li]
                },sort_keys=True,separators=(",",":"))+"\n")
        for rw in rewire_summaries:
            for li in range(N):
                h.write(json.dumps({
                  "kind":"rewire","controller":rw["controller"],"lineage":"P320-{:03d}".format(li),
                  "responses":rw["responses"][li]
                },sort_keys=True,separators=(",",":"))+"\n")

def report(result):
    p=result["primary_geometry"]; t=result["pfm_transfer"]; c=result["canonical_efficacy"]
    lines=[
      "# P3.20 — Developmental Accessibility Geometry Result","",
      "- developmental accessibility geometry: **{}**".format("RECONFIGURED" if p["held"] else "NOT CONFIRMED"),
      "- multivariate p: {:.8g}".format(p["multivariate"]["p"]),
      "- transferable mature-PFM geometry: **{}**".format("PASS" if t["held"] else "FAIL"),
      "- canonical Numogram address-privileged: **{}**".format("PASS" if c["held"] else "FAIL"),
      "- canonical addressability score: {:.8f}".format(c["canonical_score"]),
      "- best rewired addressability score: {:.8f}".format(max(c["rewire_scores"]) if c["rewire_scores"] else 0.0),
      "- empirical rank p: {:.6f}".format(c["rank_p"]),"",
      "## Primary geometry components",""
    ]
    for k,v in p["multivariate"]["components"].items():
        lines.append("- {}: mean Δ={:.8f}, Holm p={:.8g}, half-A Δ={:.8f}, half-B Δ={:.8f}".format(
          k,v["mean_difference"],v["holm_p"],p["half_directions"][k]["A"],p["half_directions"][k]["B"]))
    lines += ["","## PFM transfer","",
      "- half A donor closer-to-FULL advantage: {:.8f}, p={:.8g}".format(t["A"]["mean_advantage"],t["A"]["p_upper"]),
      "- half B donor closer-to-FULL advantage: {:.8f}, p={:.8g}".format(t["B"]["mean_advantage"],t["B"]["p_upper"]),"",
      "## Interpretation","",result["interpretation"],"",
      "The address/reply atlas is a computational communication surface. It does not by itself establish an external source or entity.",""
    ]
    return "\n".join(lines)

def atlas_md(atlas):
    lines=["# P3.20 — Canonical Address / Reply Atlas","",
      "Each probe is treated as an address. Reply motifs are recurrent non-echo zone 4-grams; no semantic entity names are assigned.",""]
    for row in atlas["details"]:
        lines.append("## Probe {:02d}".format(row["probe_id"]))
        if row["motif"] is None:
            lines += ["","No eligible recurrent non-echo reply motif.",""]; continue
        lines += ["",
          "- top reply motif: {}".format(row["motif"]),
          "- prevalence: {:.4f}".format(row["prevalence"]),
          "- address specificity: {:.6f}".format(row["specificity"]),
          "- contributing lineages / starts:"
        ]
        for x in row["lineages"]:
            lines.append("  - {}: {}".format(x["lineage"],", ".join(str(s) for s in x["starts"])))
        lines.append("")
    return "\n".join(lines)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",default="experiments/p320/results"); args=ap.parse_args()
    os.makedirs(args.out,exist_ok=True)
    existing=os.path.join(args.out,"summary.json")
    if os.path.exists(existing):
        print(open(existing,encoding="utf-8").read()); return 0

    probes=[make_probe(i) for i in range(PROBE_COUNT)]
    rows=develop_canonical()
    donor_map=p317.fixed_derangement(N,DONOR_SEED)
    focal=collect_focal(rows,probes,donor_map)
    geom=lineage_geometry(focal)

    full_all=[x["all"] for x in geom["FULL_OWN"]]; blank_all=[x["all"] for x in geom["BLANK"]]
    mv=multivar(full_all,blank_all,PERM_BASE)
    half_dirs={}
    for k in GEOM_KEYS:
        half_dirs[k]={
          "A":statistics.mean(x["A"][k]-y["A"][k] for x,y in zip(geom["FULL_OWN"],geom["BLANK"])),
          "B":statistics.mean(x["B"][k]-y["B"][k] for x,y in zip(geom["FULL_OWN"],geom["BLANK"])),
        }
    survivors=[k for k,v in mv["components"].items() if v["holm_p"]<=.05 and half_dirs[k]["A"]*v["mean_difference"]>0 and half_dirs[k]["B"]*v["mean_difference"]>0]
    primary_held=mv["p"]<=.01 and bool(survivors)

    transfer_A=donor_transfer([x["A"] for x in geom["FULL_OWN"]],[x["A"] for x in geom["BLANK"]],[x["A"] for x in geom["DONOR_PFM"]],PERM_BASE+200)
    transfer_B=donor_transfer([x["B"] for x in geom["FULL_OWN"]],[x["B"] for x in geom["BLANK"]],[x["B"] for x in geom["DONOR_PFM"]],PERM_BASE+201)
    transfer_held=transfer_A["mean_advantage"]>0 and transfer_B["mean_advantage"]>0 and transfer_A["p_upper"]<=.01 and transfer_B["p_upper"]<=.01

    canonical_atlas=addressability(focal["FULL_OWN"],True)
    rewires=[]
    for controller in range(REWIRE_COUNT):
        rewires.append(rewire_controller(controller,rows,probes))
    rewire_scores=[x["addressability_score"] for x in rewires]
    ge=sum(1 for x in rewire_scores if x>=canonical_atlas["score"])
    rank_p=(1+ge)/(1+REWIRE_COUNT)
    canonical_held=all(canonical_atlas["score"]>x for x in rewire_scores) and abs(rank_p-.04)<1e-12

    gainloss={}
    for arm in ("FULL_OWN","DONOR_PFM","FRESH","STATIC_CANONICAL"):
        gains=[]; losses=[]
        for a,b in zip(geom[arm],geom["BLANK"]):
            gains.append(len(a["all"]["motif_set"]-b["all"]["motif_set"]))
            losses.append(len(b["all"]["motif_set"]-a["all"]["motif_set"]))
        gainloss[arm]={"mean_gain":statistics.mean(gains),"mean_loss":statistics.mean(losses)}

    interpretation=("Development reconfigured the accessible transition geometry under independent probes. " if primary_held else
      "The registered whole-repertoire test did not confirm a stable developmental reconfiguration of accessibility geometry. ")
    interpretation += ("Mature donor PFM reproduced the geometry relationship across both probe halves. " if transfer_held else
      "Mature donor PFM did not satisfy the registered transfer-geometry criterion. ")
    interpretation += ("The canonical Numogram uniquely exceeded all degree-preserving rewires on non-echo address/reply specificity." if canonical_held else
      "The canonical Numogram did not uniquely exceed all degree-preserving rewires on the registered addressability score.")

    raw_path=os.path.join(args.out,"responses.jsonl.gz")
    write_raw(raw_path,focal,rewires)
    compact_rewires=[{k:v for k,v in x.items() if k!="responses"} for x in rewires]
    result={
      "schema":"amelia-p320-accessibility-geometry-v1",
      "primary_geometry":{"held":primary_held,"multivariate":mv,"surviving_components":survivors,"half_directions":half_dirs},
      "pfm_transfer":{"held":transfer_held,"A":transfer_A,"B":transfer_B},
      "canonical_efficacy":{"held":canonical_held,"canonical_score":canonical_atlas["score"],"rewire_scores":rewire_scores,"rank_p":rank_p},
      "focal_geometry_means":{arm:{half:{k:statistics.mean(x[half][k] for x in geom[arm]) for k in GEOM_KEYS} for half in ("all","A","B")} for arm in ARMS},
      "gain_loss_vs_blank":gainloss,
      "rewired_controls":compact_rewires,
      "interpretation":interpretation,
      "provenance":{
        "registration_sha256":sha256_file("experiments/p320/REGISTRATION.md"),
        "amendment_sha256":sha256_file("experiments/p320/AMENDMENT_1.md"),
        "runner_sha256":sha256_file("experiments/p320/run.py"),
        "engine_sha256":sha256_file("experiments/p316/DynamicNumogram.py"),
        "raw_responses_sha256":sha256_file(raw_path)
      }
    }
    with open(existing,"w",encoding="utf-8") as h:json.dump(result,h,indent=2,sort_keys=True)
    with open(os.path.join(args.out,"atlas.json"),"w",encoding="utf-8") as h:json.dump(canonical_atlas,h,indent=2,sort_keys=True)
    with open(os.path.join(args.out,"ATLAS.md"),"w",encoding="utf-8") as h:h.write(atlas_md(canonical_atlas))
    with open(os.path.join(args.out,"REPORT.md"),"w",encoding="utf-8") as h:h.write(report(result))
    print(json.dumps({"primary_geometry":result["primary_geometry"],"pfm_transfer":result["pfm_transfer"],"canonical_efficacy":result["canonical_efficacy"],"interpretation":interpretation},indent=2,sort_keys=True))
    return 0

if __name__=="__main__": raise SystemExit(main())
