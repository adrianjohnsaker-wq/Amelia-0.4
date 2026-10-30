#!/usr/bin/env python3
"""P3.19 hysteretic competence deconfounding assay."""
from __future__ import annotations

import argparse, copy, hashlib, importlib.util, json, math, os, random, statistics, sys
from typing import Dict, List, Sequence, Tuple

REPO_ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
if REPO_ROOT not in sys.path: sys.path.insert(0,REPO_ROOT)
P316=os.path.join(REPO_ROOT,"experiments","p316")
if P316 not in sys.path: sys.path.insert(0,P316)
from DynamicNumogram import DynamicNumogramProcess, IntegratedMemorySystem, MemoryReadout

P317_PATH=os.path.join(REPO_ROOT,"experiments","p317","run.py")
spec=importlib.util.spec_from_file_location("p317_frozen",P317_PATH)
p317=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(p317)

N=240
SEED_BASE=3190000
DONOR_SEED=3194000
PERM_SEED=3195000
PERM_DRAWS=50000
CLAMPS=(0.05,0.20,0.40,0.60,0.80,0.95)
ARMS=("FULL_OWN","BLANK","PFM_ONLY","DONOR_PFM")+tuple("H{:02d}".format(int(v*100)) for v in CLAMPS)

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

class ClampMemory(IntegratedMemorySystem):
    def __init__(self,value:float):
        super().__init__(); self.value=float(value); self.hysteresis_tension=self.value
    def append(self,event):
        # Bookkeeping is deliberately not retained: the clamp arm contains no episodic
        # content or strain, only the scalar hysteresis supplied to the Governor.
        self.events=[]
        self.zone_strain_history=[0.0]*10
        self.hysteresis_tension=self.value
    def read_memory_bias(self):
        self.events=[]; self.zone_strain_history=[0.0]*10; self.hysteresis_tension=self.value
        return MemoryReadout([0.0]*10,round(self.value,4),0,0,0.95)

def exact_upper_sign_p(wins,losses):
    n=wins+losses
    if n==0:return 1.0
    return sum(math.comb(n,k) for k in range(wins,n+1))/float(2**n)

def paired_test(a:Sequence[bool],b:Sequence[bool]):
    w=sum(1 for x,y in zip(a,b) if x and not y)
    l=sum(1 for x,y in zip(a,b) if y and not x)
    return {"left_only":w,"right_only":l,"discordant":w+l,"p_upper":exact_upper_sign_p(w,l)}

def score(records):
    hits=[]
    for i in range(len(records)-3):
        chunk=records[i:i+4]
        path=tuple(int(x["zone"]) for x in chunk)
        if path==(1,2,3,6) and int(chunk[-1]["top_activation"])==0:
            hits.append(i)
    return {"present":bool(hits),"count":len(hits),"first":min(hits) if hits else None}

def ranks(vals):
    order=sorted(range(len(vals)),key=lambda i:vals[i])
    out=[0.0]*len(vals); i=0
    while i<len(order):
        j=i
        while j+1<len(order) and vals[order[j+1]]==vals[order[i]]: j+=1
        r=(i+j+2)/2.0
        for k in range(i,j+1): out[order[k]]=r
        i=j+1
    return out

def spearman(x,y):
    rx,ry=ranks(x),ranks(y)
    mx,my=statistics.mean(rx),statistics.mean(ry)
    num=sum((a-mx)*(b-my) for a,b in zip(rx,ry))
    den=math.sqrt(sum((a-mx)**2 for a in rx)*sum((b-my)**2 for b in ry))
    return num/den if den else 0.0

def trend_p(counts):
    observed=spearman(list(CLAMPS),list(counts))
    rng=random.Random(PERM_SEED); ge=0
    base=list(counts)
    for _ in range(PERM_DRAWS):
        perm=list(base); rng.shuffle(perm)
        if spearman(list(CLAMPS),perm)>=observed-1e-15: ge+=1
    return observed,(ge+1)/(PERM_DRAWS+1)

def build_rows():
    donor=p317.fixed_derangement(N,DONOR_SEED)
    rows=[]
    permeability=p317.original_gate_permeability(p317.FULL_NUMOGRAM_GATES)
    for i in range(N):
        seed=SEED_BASE+i
        dev,post=p317.make_tapes(seed)
        proc=DynamicNumogramProcess(current_zone=seed%10)
        p317.run_dynamic_tape(proc,dev)
        shocked=copy.deepcopy(proc); p317.shock_process(shocked,seed,permeability)
        rows.append({"seed":seed,"dev":dev,"post":post,"shocked":shocked})
    return rows,donor

def make_arm(base,arm,donor_mem=None):
    p=copy.deepcopy(base)
    if arm=="FULL_OWN": return p
    p.deformation_tensor=[0.1]*10
    if arm=="BLANK": p.memory=IntegratedMemorySystem()
    elif arm=="PFM_ONLY": p.memory=copy.deepcopy(base.memory)
    elif arm=="DONOR_PFM": p.memory=copy.deepcopy(donor_mem)
    elif arm.startswith("H"):
        value=int(arm[1:])/100.0; p.memory=ClampMemory(value)
    else: raise ValueError(arm)
    return p

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",default="experiments/p319/results"); args=ap.parse_args()
    os.makedirs(args.out,exist_ok=True)
    existing=os.path.join(args.out,"summary.json")
    if os.path.exists(existing):
        print(open(existing,encoding="utf-8").read()); return 0

    rows,donor=build_rows()
    results={arm:[] for arm in ARMS}
    for i,row in enumerate(rows):
        for arm in ARMS:
            dm=rows[donor[i]]["shocked"].memory if arm=="DONOR_PFM" else None
            p=make_arm(row["shocked"],arm,dm)
            rec=p317.run_dynamic_tape(p,row["post"])
            s=score(rec)
            s["final_hysteresis"]=float(p.memory.hysteresis_tension)
            s["post_warp_occupancy"]=sum(1 for x in rec if int(x["zone"]) in (3,6))/len(rec)
            results[arm].append(s)

    pres={arm:[bool(x["present"]) for x in results[arm]] for arm in ARMS}
    counts={arm:sum(pres[arm]) for arm in ARMS}
    full=paired_test(pres["FULL_OWN"],pres["BLANK"])
    pfm=paired_test(pres["PFM_ONLY"],pres["BLANK"])
    donor_t=paired_test(pres["DONOR_PFM"],pres["BLANK"])
    replication=(full["p_upper"]<=.01 and pfm["p_upper"]<=.01 and donor_t["p_upper"]<=.01
                 and counts["PFM_ONLY"]>=.75*counts["FULL_OWN"]
                 and counts["DONOR_PFM"]>=.75*counts["FULL_OWN"])

    clamp_arms=tuple("H{:02d}".format(int(v*100)) for v in CLAMPS)
    clamp_counts=[counts[a] for a in clamp_arms]
    highlow=paired_test(pres["H95"],pres["H05"])
    rho,tp=trend_p(clamp_counts)
    hysteresis=(highlow["p_upper"]<=.01 and rho>=.80 and tp<=.01 and counts["H95"]>=.75*counts["PFM_ONLY"])

    interp=("HYSTERETIC CAUSATION SUPPORTED." if hysteresis else
            "HYSTERETIC CAUSATION NOT SUPPORTED under the hysteresis-free trajectory endpoint.")
    if replication: interp+=" The broader transferable PFM competence effect replicates."
    else: interp+=" The broader transferable PFM competence effect does not satisfy its replication gate."

    summary={
      "schema":"amelia-p319-hysteretic-competence-v1",
      "endpoint":{"path":[1,2,3,6],"top_activation":0,"hysteresis_condition":None},
      "counts":counts,
      "primary_hysteresis":{"held":hysteresis,"H95_vs_H05":highlow,"clamp_counts":dict(zip(clamp_arms,clamp_counts)),"spearman_rho":rho,"trend_p":tp},
      "pfm_replication":{"held":replication,"full_vs_blank":full,"pfm_vs_blank":pfm,"donor_vs_blank":donor_t},
      "results":results,
      "interpretation":interp,
      "provenance":{
        "registration_sha256":sha256_file("experiments/p319/REGISTRATION.md"),
        "runner_sha256":sha256_file("experiments/p319/run.py"),
        "dynamic_engine_sha256":sha256_file("experiments/p316/DynamicNumogram.py"),
        "p317_runner_sha256":sha256_file("experiments/p317/run.py")
      }
    }
    with open(existing,"w",encoding="utf-8") as f: json.dump(summary,f,indent=2,sort_keys=True)
    report=[
      "# P3.19 — Hysteretic Competence Deconfounding Result","",
      "- hysteretic causation gate: **{}**".format("PASS" if hysteresis else "FAIL"),
      "- transferable PFM replication gate: **{}**".format("PASS" if replication else "FAIL"),
      "- FULL_OWN: {}/{}".format(counts["FULL_OWN"],N),
      "- BLANK: {}/{}".format(counts["BLANK"],N),
      "- PFM_ONLY: {}/{}".format(counts["PFM_ONLY"],N),
      "- DONOR_PFM: {}/{}".format(counts["DONOR_PFM"],N),
      "- H05/H20/H40/H60/H80/H95: {}".format(clamp_counts),
      "- H95 > H05 paired p: {:.8g}".format(highlow["p_upper"]),
      "- clamp-dose Spearman rho: {:.6f}".format(rho),
      "- monotonic-trend permutation p: {:.8g}".format(tp),"",
      "## Interpretation","",interp,"",
      "The primary endpoint is the path 1→2→3→6 ending with top-activation zone 0; H-state is not part of the endpoint.",""
    ]
    with open(os.path.join(args.out,"REPORT.md"),"w",encoding="utf-8") as f:f.write("\n".join(report))
    print(json.dumps({k:summary[k] for k in ("counts","primary_hysteresis","pfm_replication","interpretation")},indent=2,sort_keys=True))
    return 0

if __name__=="__main__": raise SystemExit(main())
