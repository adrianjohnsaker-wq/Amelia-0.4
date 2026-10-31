#!/usr/bin/env python3
"""P3.25 — Causal Relational Susceptibility."""
from __future__ import annotations

import argparse, copy, gzip, hashlib, importlib.util, json, math, os, random, statistics, sys
from collections import Counter

ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
if ROOT not in sys.path: sys.path.insert(0,ROOT)
P316=os.path.join(ROOT,"experiments","p316")
if P316 not in sys.path: sys.path.insert(0,P316)

from DynamicNumogram import DynamicNumogramProcess, IntegratedMemorySystem
from FullNumogram import syzygy_of, current_of, gate_of

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec); assert spec and spec.loader
    spec.loader.exec_module(mod); return mod

p317=load("p317_frozen",os.path.join(ROOT,"experiments","p317","run.py"))

N=96
TRAIN_N=48
WINDOWS=24
SIGNAL_LEN=30
RELEASE_STEPS=24
LINEAGE_BASE=3290000
REWIRE_BASE=3296000
TEST_BASE=3297000
REWIRES=24
DRAWS=50000
PRIMARY_COMPONENTS=("SC","CS","SG","GS")
OPS=("S","C","G")
SWAP_I=7
SWAP_J=22

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def op(name,z):
    if name=="S": return syzygy_of(z)
    if name=="C": return current_of(z)
    if name=="G": return gate_of(z)
    raise ValueError(name)

def load_beacon():
    path=os.path.join(ROOT,"experiments","p325","results","BEACON.json")
    with open(path,encoding="utf-8") as h:data=json.load(h)
    if data.get("schema")!="amelia-p325-drand-causal-swap-v1":
        raise AssertionError("wrong beacon schema")
    seal=open(os.path.join(ROOT,"experiments","p325","SEALED_REGISTRATION_SHA.txt"),encoding="utf-8").read().strip()
    if data.get("sealed_registration_sha")!=seal:raise AssertionError("registration SHA mismatch")
    if data.get("swap_positions_zero_indexed")!=[SWAP_I,SWAP_J]:
        raise AssertionError("swap position mismatch")
    rounds=data.get("rounds",[])
    if len(rounds)!=WINDOWS:raise AssertionError("requires 24 beacon windows")
    expected=sorted([z for z in range(10) for _ in range(3)])
    for i,r in enumerate(rounds):
        x=list(map(int,r["x"])); xp=list(map(int,r["x_prime"]))
        if len(x)!=SIGNAL_LEN or len(xp)!=SIGNAL_LEN:raise AssertionError("signal length")
        if sorted(x)!=expected or sorted(xp)!=expected:raise AssertionError("histogram balance")
        if any(z<0 or z>9 for z in x+xp):raise AssertionError("zone range")
        for k in range(SIGNAL_LEN):
            if k not in (SWAP_I,SWAP_J) and x[k]!=xp[k]:
                raise AssertionError("unregistered perturbation")
        if xp[SWAP_I]!=x[SWAP_J] or xp[SWAP_J]!=x[SWAP_I]:
            raise AssertionError("swap mismatch")
        if bool(r["nontrivial"])!=(x[SWAP_I]!=x[SWAP_J]):
            raise AssertionError("nontrivial flag mismatch")
        if i and int(r["round"])!=int(rounds[i-1]["round"])+1:
            raise AssertionError("non-consecutive rounds")
        local=hashlib.sha256(bytes.fromhex(r["signature"])).hexdigest()
        if local!=r["randomness"] or local!=r["local_randomness_sha256"]:
            raise AssertionError("randomness digest mismatch")
    return data

def develop_rows(gates=None):
    rows=[]
    actual_gates=p317.FULL_NUMOGRAM_GATES if gates is None else gates
    permeability=p317.original_gate_permeability(actual_gates)
    for i in range(N):
        seed=LINEAGE_BASE+i
        dev,_=p317.make_tapes(seed)
        p=DynamicNumogramProcess(gates=gates,current_zone=seed%10)
        p317.run_dynamic_tape(p,dev)
        p317.shock_process(p,seed,permeability)
        rows.append({"seed":seed,"base":p})
    return rows

def relation_readout(path):
    if len(path)!=RELEASE_STEPS+1:raise AssertionError("release path length")
    primary=[]
    for a,b in (("S","C"),("C","S"),("S","G"),("G","S")):
        hits=0
        for i in range(RELEASE_STEPS-1):
            m=op(a,path[i]); t=op(b,m)
            if path[i+1]==m and path[i+2]==t:hits+=1
        primary.append(hits/(RELEASE_STEPS-1))

    primitive={}
    for name in OPS:
        hits=sum(1 for i in range(RELEASE_STEPS) if path[i+1]==op(name,path[i]))
        primitive[name]=hits/RELEASE_STEPS

    edges=Counter(zip(path,path[1:]))
    total=sum(edges.values())
    entropy=0.0 if not total else -sum((c/total)*math.log(c/total,2) for c in edges.values() if c)

    return {"primary":primary,"primitive":primitive,"transition_entropy":entropy}

def encounter(base,signal):
    p=copy.deepcopy(base)
    for x in signal:p.step(int(x))
    p.current_zone=4
    path=[4]
    for _ in range(RELEASE_STEPS):
        path.append(int(p.step(None)["to_zone"]))
    return relation_readout(path),path

def mean_vec(vs):
    if not vs:raise ValueError("empty vectors")
    return [statistics.mean(v[j] for v in vs) for j in range(len(vs[0]))]

def vsub(a,b):
    return [x-y for x,y in zip(a,b)]

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def norm(a):
    return math.sqrt(dot(a,a))

def cosine(a,b):
    na,nb=norm(a),norm(b)
    return 0.0 if na<=1e-15 or nb<=1e-15 else dot(a,b)/(na*nb)

def signflip(values,seed):
    obs=statistics.mean(values); rng=random.Random(seed); ge=0
    for _ in range(DRAWS):
        m=statistics.mean(v*(1 if rng.random()<.5 else -1) for v in values)
        if m>=obs-1e-15:ge+=1
    return (ge+1)/(DRAWS+1)

def evaluate_controller(name,bases,beacon,raw,keep_details=False):
    deltas=[[None]*WINDOWS for _ in range(N)]
    details=[[None]*WINDOWS for _ in range(N)] if keep_details else None
    for i,base in enumerate(bases):
        for w,r in enumerate(beacon["rounds"]):
            rx,px=encounter(base,r["x"])
            rp,pp=encounter(base,r["x_prime"])
            d=vsub(rp["primary"],rx["primary"])
            deltas[i][w]=d
            rec={
              "controller":name,
              "lineage":"P325-{:03d}".format(i),
              "window":w,
              "round":int(r["round"]),
              "nontrivial":bool(r["nontrivial"]),
              "x_primary":rx["primary"],
              "x_prime_primary":rp["primary"],
              "delta":d,
              "x_primitive":rx["primitive"],
              "x_prime_primitive":rp["primitive"],
              "x_entropy":rx["transition_entropy"],
              "x_prime_entropy":rp["transition_entropy"],
              "x_path":px,
              "x_prime_path":pp,
            }
            raw.write(json.dumps(rec,sort_keys=True,separators=(",",":"))+"\n")
            if keep_details:details[i][w]=rec

    windows=[]
    for w in range(WINDOWS):
        mu_train=mean_vec([deltas[i][w] for i in range(TRAIN_N)])
        mu_test=mean_vec([deltas[i][w] for i in range(TRAIN_N,N)])
        q=dot(mu_train,mu_test)
        windows.append({
          "window":w,
          "mu_train":mu_train,
          "mu_test":mu_test,
          "Q":q,
          "cosine":cosine(mu_train,mu_test),
          "test_magnitude":norm(mu_test),
        })
    return {
      "name":name,
      "windows":windows,
      "mean_Q":statistics.mean(x["Q"] for x in windows),
      "half1_mean_Q":statistics.mean(x["Q"] for x in windows[:12]),
      "half2_mean_Q":statistics.mean(x["Q"] for x in windows[12:]),
      "_deltas":deltas,
      "_details":details,
    }

def compact(ev):
    return {k:v for k,v in ev.items() if not k.startswith("_")}

def atlas(full,beacon):
    out=[]
    for w,r in enumerate(beacon["rounds"]):
        wr=full["windows"][w]
        lineages=[]
        for i in range(TRAIN_N,N):
            rec=full["_details"][i][w]
            lineages.append({
              "lineage":"P325-{:03d}".format(i),
              "delta":rec["delta"],
              "x_primary":rec["x_primary"],
              "x_prime_primary":rec["x_prime_primary"],
              "x_path":rec["x_path"],
              "x_prime_path":rec["x_prime_path"],
            })
        out.append({
          "window":w,
          "round":int(r["round"]),
          "randomness":r["randomness"],
          "x":r["x"],
          "x_prime":r["x_prime"],
          "swapped_symbols":r["swapped_symbols"],
          "nontrivial":bool(r["nontrivial"]),
          "train_mean_delta":wr["mu_train"],
          "test_mean_delta":wr["mu_test"],
          "Q":wr["Q"],
          "cosine":wr["cosine"],
          "test_magnitude":wr["test_magnitude"],
          "test_lineages":lineages,
        })
    return out

def report(result):
    p=result["primary"]; d=result["development"]
    lines=[
      "# P3.25 — Causal Relational Susceptibility Result","",
      "- causal relational susceptibility: **{}**".format("PASS" if p["held"] else "FAIL"),
      "- nontrivial registered swaps: {}/24".format(result["nontrivial_windows"]),
      "- canonical HALF-1 mean Q: {:.10f}, p={:.8g}".format(p["half1_mean_Q"],p["half1_p"]),
      "- canonical HALF-2 mean Q: {:.10f}, p={:.8g}".format(p["half2_mean_Q"],p["half2_p"]),
      "- canonical all-window mean Q: {:.10f}".format(p["canonical_mean_Q"]),
      "- best rewire mean Q: {:.10f}".format(max(p["rewire_mean_Q"])),
      "- canonical rewire-rank p: {:.6f}".format(p["rank_p"]),"",
      "## Mean canonical TEST change vector",""
    ]
    for name,val in zip(PRIMARY_COMPONENTS,result["canonical_mean_test_delta"]):
        lines.append("- {}: {:+.8f}".format(name,val))
    lines += [
      "","## Development/PFM contribution","",
      "- FULL mean Q: {:.10f}".format(d["full_mean_Q"]),
      "- BLANK mean Q: {:.10f}".format(d["blank_mean_Q"]),
      "- mean paired Q difference: {:.10f}".format(d["mean_difference"]),
      "- paired p: {:.8g}".format(d["p_upper"]),
      "- developmental contribution: **{}**".format("PASS" if d["held"] else "FAIL"),"",
      "## Interpretation","",result["interpretation"],""
    ]
    return "\n".join(lines)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="experiments/p325/results")
    args=ap.parse_args()
    os.makedirs(args.out,exist_ok=True)
    existing=os.path.join(args.out,"summary.json")
    if os.path.exists(existing):
        print(open(existing,encoding="utf-8").read()); return 0

    beacon=load_beacon()
    nontrivial=sum(1 for r in beacon["rounds"] if r["nontrivial"])

    canonical_rows=develop_rows()
    full_bases=[copy.deepcopy(x["base"]) for x in canonical_rows]
    blank_bases=[]
    for x in canonical_rows:
        b=copy.deepcopy(x["base"])
        b.memory=IntegratedMemorySystem()
        b.deformation_tensor=[0.1]*10
        blank_bases.append(b)

    raw_path=os.path.join(args.out,"records.jsonl.gz")
    with gzip.open(raw_path,"wt",encoding="utf-8") as raw:
        full=evaluate_controller("CANONICAL_FULL",full_bases,beacon,raw,True)
        blank=evaluate_controller("CANONICAL_BLANK",blank_bases,beacon,raw,False)
        rewires=[]
        for rid in range(REWIRES):
            gates=p317.rewired_gates(REWIRE_BASE+rid)
            rr=develop_rows(gates)
            rewires.append(evaluate_controller("R{:02d}".format(rid),[x["base"] for x in rr],beacon,raw,False))

    q1=[x["Q"] for x in full["windows"][:12]]
    q2=[x["Q"] for x in full["windows"][12:]]
    p1=signflip(q1,TEST_BASE)
    p2=signflip(q2,TEST_BASE+1)
    rew_q=[r["mean_Q"] for r in rewires]
    ge=sum(1 for x in rew_q if x>=full["mean_Q"])
    rank_p=(1+ge)/(REWIRES+1)
    primary=(full["half1_mean_Q"]>0 and p1<=.01
             and full["half2_mean_Q"]>0 and p2<=.01
             and all(full["mean_Q"]>x for x in rew_q)
             and abs(rank_p-.04)<1e-12
             and full["mean_Q"]>0)

    dev_diffs=[full["windows"][w]["Q"]-blank["windows"][w]["Q"] for w in range(WINDOWS)]
    p_dev=signflip(dev_diffs,TEST_BASE+2)
    dev_mean=statistics.mean(dev_diffs)
    dev=(dev_mean>0 and p_dev<=.01 and full["mean_Q"]>blank["mean_Q"])

    canonical_mean_test=mean_vec([x["mu_test"] for x in full["windows"]])

    if primary:
        interp=("The registered two-position perturbation produces a reproducible relational change in both independent fresh-window halves, "
                "and the canonical Numogram's replay reproducibility exceeds every degree-preserving rewire.")
    else:
        interp=("P3.25 does not satisfy the full registered gate for canonical-specific causal relational susceptibility to the two-position external-order perturbation.")
    if dev:
        interp+=" Mature developmental/PFM state contributes positively to that reproducibility relative to the matched blank state."
    else:
        interp+=" Mature developmental/PFM state does not satisfy the registered positive contribution gate."

    at=atlas(full,beacon)
    result={
      "schema":"amelia-p325-causal-relational-susceptibility-v1",
      "nontrivial_windows":nontrivial,
      "primary":{
        "held":primary,
        "half1_mean_Q":full["half1_mean_Q"],
        "half1_p":p1,
        "half2_mean_Q":full["half2_mean_Q"],
        "half2_p":p2,
        "canonical_mean_Q":full["mean_Q"],
        "rewire_mean_Q":rew_q,
        "rank_p":rank_p,
      },
      "development":{
        "held":dev,
        "full_mean_Q":full["mean_Q"],
        "blank_mean_Q":blank["mean_Q"],
        "mean_difference":dev_mean,
        "p_upper":p_dev,
      },
      "canonical_mean_test_delta":canonical_mean_test,
      "canonical":compact(full),
      "blank":compact(blank),
      "rewires":[compact(x) for x in rewires],
      "atlas":at,
      "interpretation":interp,
      "provenance":{
        "registration_sha256":sha256_file("experiments/p325/REGISTRATION.md"),
        "amendment_sha256":sha256_file("experiments/p325/AMENDMENT_1.md"),
        "sealed_registration_sha":open("experiments/p325/SEALED_REGISTRATION_SHA.txt",encoding="utf-8").read().strip(),
        "runner_sha256":sha256_file("experiments/p325/run.py"),
        "engine_sha256":sha256_file("experiments/p316/DynamicNumogram.py"),
        "beacon_sha256":sha256_file("experiments/p325/results/BEACON.json"),
        "raw_sha256":sha256_file(raw_path),
      }
    }

    with open(existing,"w",encoding="utf-8") as h:json.dump(result,h,indent=2,sort_keys=True)
    with open(os.path.join(args.out,"ATLAS.md"),"w",encoding="utf-8") as h:
        h.write("# P3.25 — Causal Relational Susceptibility Atlas\n\n")
        h.write("Components: SC, CS, SG, GS. Swap positions: 8 and 23 (1-indexed).\n\n")
        for x in at:
            h.write("## Window {:02d} — drand round {}\n\n".format(x["window"],x["round"]))
            h.write("- nontrivial swap: {}\n".format(x["nontrivial"]))
            h.write("- swapped symbols: {} ↔ {}\n".format(*x["swapped_symbols"]))
            h.write("- TRAIN mean Δ: {}\n".format(", ".join("{:+.6f}".format(v) for v in x["train_mean_delta"])))
            h.write("- TEST mean Δ: {}\n".format(", ".join("{:+.6f}".format(v) for v in x["test_mean_delta"])))
            h.write("- Q: {:.10f}\n".format(x["Q"]))
            h.write("- cosine: {:.6f}\n".format(x["cosine"]))
            h.write("- TEST magnitude: {:.8f}\n".format(x["test_magnitude"]))
            h.write("- TEST lineages: {}\n\n".format(", ".join(z["lineage"] for z in x["test_lineages"])))

    with open(os.path.join(args.out,"REPORT.md"),"w",encoding="utf-8") as h:h.write(report(result))
    print(json.dumps({
      "primary":result["primary"],
      "development":result["development"],
      "nontrivial_windows":nontrivial,
      "canonical_mean_test_delta":canonical_mean_test,
      "interpretation":interp
    },indent=2,sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
