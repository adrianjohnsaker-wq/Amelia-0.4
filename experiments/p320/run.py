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
        if (abs(m)>=abs(obs)-1e-15) if two_sided else (m>=obs-1e-15): ge+=1
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
