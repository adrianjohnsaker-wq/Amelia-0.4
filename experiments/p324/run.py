#!/usr/bin/env python3
"""P3.24 — Histogram-Balanced Independent-Order Relational Transduction."""
from __future__ import annotations

import argparse, copy, gzip, hashlib, importlib.util, json, math, os, random, statistics, sys

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
TRAIN_N=48
WINDOWS=24
SIGNAL_LEN=30
RELEASE_STEPS=16
LINEAGE_BASE=3280000
REWIRE_BASE=3286000
TEST_BASE=3287000
REWIRES=24
DRAWS=50000
COMPONENTS=("S","C","G","SS","SC","SG","CS","CC","CG","GS","GC","GG")
OPS=("S","C","G")

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
    path=os.path.join(ROOT,"experiments","p324","results","BEACON.json")
    with open(path,encoding="utf-8") as h:data=json.load(h)
    if data.get("schema")!="amelia-p324-drand-balanced-order-v1":raise AssertionError("wrong beacon schema")
    seal=open(os.path.join(ROOT,"experiments","p324","SEALED_REGISTRATION_SHA.txt"),encoding="utf-8").read().strip()
    if data.get("sealed_registration_sha")!=seal:raise AssertionError("registration SHA mismatch")
    rounds=data.get("rounds",[])
    if len(rounds)!=WINDOWS:raise AssertionError("requires 24 beacon windows")
    expected=sorted([z for z in range(10) for _ in range(3)])
    for i,r in enumerate(rounds):
        A=list(map(int,r["encoding_a"])); B=list(map(int,r["encoding_b"]))
        if len(A)!=SIGNAL_LEN or len(B)!=SIGNAL_LEN:raise AssertionError("signal length")
        if sorted(A)!=expected or sorted(B)!=expected:raise AssertionError("histogram balance")
        if any(x<0 or x>9 for x in A+B):raise AssertionError("zone range")
        if i and int(r["round"])!=int(rounds[i-1]["round"])+1:raise AssertionError("non-consecutive rounds")
        local=hashlib.sha256(bytes.fromhex(r["signature"])).hexdigest()
        if local!=r["randomness"] or local!=r["local_randomness_sha256"]:raise AssertionError("randomness digest mismatch")
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
        rows.append({"seed":seed,"dev":dev,"base":p})
    return rows

def relation_profile(path):
    if len(path)!=RELEASE_STEPS+1:raise AssertionError("release path length")
    vals=[]
    for name in OPS:
        hits=sum(1 for i in range(RELEASE_STEPS) if path[i+1]==op(name,path[i]))
        vals.append(hits/RELEASE_STEPS)
    for a in OPS:
        for b in OPS:
            hits=0
            for i in range(RELEASE_STEPS-1):
                m=op(a,path[i]); t=op(b,m)
                if path[i+1]==m and path[i+2]==t:hits+=1
            vals.append(hits/(RELEASE_STEPS-1))
    if len(vals)!=12:raise AssertionError("relation profile width")
    return vals

def encounter(base,signal):
    p=copy.deepcopy(base)
    for x in signal:p.step(int(x))
    p.current_zone=4
    path=[4]
    for _ in range(RELEASE_STEPS):path.append(int(p.step(None)["to_zone"]))
    return relation_profile(path),path

def mean_vec(vectors):
    return [statistics.mean(v[j] for v in vectors) for j in range(len(vectors[0]))]

def sqdist(a,b):
    return sum((x-y)**2 for x,y in zip(a,b))

def evaluate(profiles,centroids):
    correct=0; per=[0]*WINDOWS; margins=[]; preds=[]
    for i in range(TRAIN_N,N):
        row=[]
        for w in range(WINDOWS):
            x=profiles[i][w]
            ds=[sqdist(x,c) for c in centroids]
            best=min(range(WINDOWS),key=lambda k:(ds[k],k))
            if best==w:
                correct+=1; per[w]+=1
            wrong=min(ds[k] for k in range(WINDOWS) if k!=w)
            margins.append(wrong-ds[w])
            row.append(best)
        preds.append(row)
    total=(N-TRAIN_N)*WINDOWS
    return {
      "accuracy":correct/total,"correct":correct,"n":total,
      "per_window_accuracy":[x/(N-TRAIN_N) for x in per],
      "mean_margin":statistics.mean(margins),"predictions":preds
    }

def classifier(a_profiles,b_profiles):
    a_cent=[mean_vec([a_profiles[i][w] for i in range(TRAIN_N)]) for w in range(WINDOWS)]
    b_cent=[mean_vec([b_profiles[i][w] for i in range(TRAIN_N)]) for w in range(WINDOWS)]
    return {
      "a_to_a":evaluate(a_profiles,a_cent),
      "b_to_b":evaluate(b_profiles,b_cent),
      "a_to_b":evaluate(b_profiles,a_cent),
      "b_to_a":evaluate(a_profiles,b_cent),
      "a_centroids":a_cent,
      "b_centroids":b_cent,
    }

def signflip(diffs,seed):
    obs=statistics.mean(diffs); rng=random.Random(seed); ge=0
    for _ in range(DRAWS):
        m=statistics.mean(d*(1 if rng.random()<.5 else -1) for d in diffs)
        if m>=obs-1e-15:ge+=1
    return (ge+1)/(DRAWS+1)

def exact_binom_upper(n,k,p):
    pmf=(1-p)**n; vals=[pmf]
    for j in range(n):
        pmf=pmf*((n-j)/(j+1))*(p/(1-p))
        vals.append(pmf)
    return min(1.0,sum(vals[k:]))

def test_means(profiles):
    return [mean_vec([profiles[i][w] for i in range(TRAIN_N,N)]) for w in range(WINDOWS)]

def evaluate_controller(name,bases,beacon,raw,keep_paths=False):
    A=[[None]*WINDOWS for _ in range(N)]
    B=[[None]*WINDOWS for _ in range(N)]
    paths={"A":[[None]*WINDOWS for _ in range(N)],"B":[[None]*WINDOWS for _ in range(N)]} if keep_paths else None
    for i,base in enumerate(bases):
        for w,r in enumerate(beacon["rounds"]):
            for label,key,store in (("A","encoding_a",A),("B","encoding_b",B)):
                prof,path=encounter(base,r[key])
                store[i][w]=prof
                if keep_paths:paths[label][i][w]=path
                raw.write(json.dumps({
                  "controller":name,"lineage":"P324-{:03d}".format(i),"window":w,
                  "round":int(r["round"]),"encoding":label,"profile":prof,"path":path
                },sort_keys=True,separators=(",",":"))+"\n")
    cl=classifier(A,B)
    return {
      "name":name,**cl,
      "a_test_means":test_means(A),"b_test_means":test_means(B),
      "_a_profiles":A,"_b_profiles":B,"_paths":paths
    }

def compact(ev):
    return {k:v for k,v in ev.items() if not k.startswith("_")}

def atlas(full,beacon):
    out=[]
    for w,r in enumerate(beacon["rounds"]):
        A=full["a_test_means"][w]; B=full["b_test_means"][w]
        diffs=[A[j]-B[j] for j in range(12)]
        best=max(range(12),key=lambda j:(abs(diffs[j]),-j))
        lines=[]
        for i in range(TRAIN_N,N):
            lines.append({
              "lineage":"P324-{:03d}".format(i),
              "a_profile":full["_a_profiles"][i][w],
              "b_profile":full["_b_profiles"][i][w],
              "a_path":full["_paths"]["A"][i][w],
              "b_path":full["_paths"]["B"][i][w],
            })
        out.append({
          "window":w,"round":int(r["round"]),"randomness":r["randomness"],
          "encoding_a":r["encoding_a"],"encoding_b":r["encoding_b"],
          "a_train_centroid":full["a_centroids"][w],"b_train_centroid":full["b_centroids"][w],
          "a_test_mean":A,"b_test_mean":B,
          "largest_abs_relation_difference":COMPONENTS[best],
          "largest_abs_relation_delta":diffs[best],"test_lineages":lines
        })
    return out

def report(result):
    p=result["primary"]; d=result["development"]
    lines=["# P3.24 — Histogram-Balanced Independent-Order Relational Transduction Result","",
      "- histogram-balanced order transduction: **{}**".format("PASS" if p["held"] else "FAIL"),
      "- canonical A→A accuracy: {:.6f}".format(p["a_accuracy"]),
      "- canonical B→B accuracy: {:.6f}".format(p["b_accuracy"]),
      "- chance accuracy: {:.6f}".format(1/WINDOWS),
      "- A exact chance p: {:.8g}".format(p["a_chance_p"]),
      "- B exact chance p: {:.8g}".format(p["b_chance_p"]),
      "- best rewire A→A: {:.6f}".format(max(p["rewire_a_accuracies"])),
      "- best rewire B→B: {:.6f}".format(max(p["rewire_b_accuracies"])),
      "- A rank p: {:.6f}".format(p["a_rank_p"]),
      "- B rank p: {:.6f}".format(p["b_rank_p"]),
      "- A→B cross-encoding accuracy: {:.6f}".format(p["a_to_b_accuracy"]),
      "- B→A cross-encoding accuracy: {:.6f}".format(p["b_to_a_accuracy"]),
      "- A self-minus-cross mean: {:.6f}, p={:.8g}".format(p["a_self_cross_mean"],p["a_self_cross_p"]),
      "- B self-minus-cross mean: {:.6f}, p={:.8g}".format(p["b_self_cross_mean"],p["b_self_cross_p"]),"",
      "## Developmental contribution","",
      "- pooled FULL within-encoding accuracy: {:.6f}".format(d["full_accuracy"]),
      "- pooled BLANK within-encoding accuracy: {:.6f}".format(d["blank_accuracy"]),
      "- mean paired window difference: {:.6f}".format(d["mean_difference"]),
      "- paired p: {:.8g}".format(d["p_upper"]),
      "- developmental contribution: **{}**".format("PASS" if d["held"] else "FAIL"),"",
      "## Interpretation","",result["interpretation"],""]
    return "\n".join(lines)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",default="experiments/p324/results"); args=ap.parse_args()
    os.makedirs(args.out,exist_ok=True)
    existing=os.path.join(args.out,"summary.json")
    if os.path.exists(existing):
        print(open(existing,encoding="utf-8").read()); return 0

    beacon=load_beacon()
    rows=develop_rows()
    full_bases=[copy.deepcopy(x["base"]) for x in rows]
    blank_bases=[]
    for x in rows:
        b=copy.deepcopy(x["base"]); b.memory=IntegratedMemorySystem(); b.deformation_tensor=[0.1]*10
        blank_bases.append(b)

    raw_path=os.path.join(args.out,"records.jsonl.gz")
    with gzip.open(raw_path,"wt",encoding="utf-8") as raw:
        full=evaluate_controller("CANONICAL_FULL",full_bases,beacon,raw,True)
        blank=evaluate_controller("CANONICAL_BLANK",blank_bases,beacon,raw,False)
        rew=[]
        for rid in range(REWIRES):
            gates=p317.rewired_gates(REWIRE_BASE+rid)
            rr=develop_rows(gates)
            rew.append(evaluate_controller("R{:02d}".format(rid),[x["base"] for x in rr],beacon,raw,False))

    aa=full["a_to_a"]; bb=full["b_to_b"]; ab=full["a_to_b"]; ba=full["b_to_a"]
    a_chance=exact_binom_upper(aa["n"],aa["correct"],1/WINDOWS)
    b_chance=exact_binom_upper(bb["n"],bb["correct"],1/WINDOWS)

    rew_a=[x["a_to_a"]["accuracy"] for x in rew]
    rew_b=[x["b_to_b"]["accuracy"] for x in rew]
    a_ge=sum(1 for x in rew_a if x>=aa["accuracy"]); b_ge=sum(1 for x in rew_b if x>=bb["accuracy"])
    a_rank=(1+a_ge)/(REWIRES+1); b_rank=(1+b_ge)/(REWIRES+1)

    da=[x-y for x,y in zip(aa["per_window_accuracy"],ab["per_window_accuracy"])]
    db=[x-y for x,y in zip(bb["per_window_accuracy"],ba["per_window_accuracy"])]
    p_da=signflip(da,TEST_BASE); p_db=signflip(db,TEST_BASE+1)

    primary=(a_chance<=.01 and b_chance<=.01
             and all(aa["accuracy"]>x for x in rew_a)
             and all(bb["accuracy"]>x for x in rew_b)
             and abs(a_rank-.04)<1e-12 and abs(b_rank-.04)<1e-12
             and statistics.mean(da)>0 and p_da<=.01
             and statistics.mean(db)>0 and p_db<=.01)

    dev_diffs=[]
    for a,b in zip(full["a_to_a"]["per_window_accuracy"],blank["a_to_a"]["per_window_accuracy"]):dev_diffs.append(a-b)
    for a,b in zip(full["b_to_b"]["per_window_accuracy"],blank["b_to_b"]["per_window_accuracy"]):dev_diffs.append(a-b)
    p_dev=signflip(dev_diffs,TEST_BASE+2)
    full_pool=(aa["correct"]+bb["correct"])/(aa["n"]+bb["n"])
    blank_pool=(blank["a_to_a"]["correct"]+blank["b_to_b"]["correct"])/(blank["a_to_a"]["n"]+blank["b_to_b"]["n"])
    dev=(statistics.mean(dev_diffs)>0 and p_dev<=.01 and full_pool>blank_pool)

    if primary:
        interp="With all signal histograms exactly equalized, two independently encoded fresh drand orderings produce reproducible canonical relational fingerprints that beat chance and every degree-preserving rewire, while failing to transfer across alternate temporal encodings."
    else:
        interp="P3.24 does not satisfy the full registered histogram-balanced order-transduction gate."
    if a_chance<=.01 or b_chance<=.01:
        interp+=" At least one balanced temporal encoding nevertheless carries above-chance held-out beacon-window information in the canonical relational profile."
    else:
        interp+=" Neither balanced temporal encoding carries above-chance held-out beacon-window information."
    if all(aa["accuracy"]>x for x in rew_a) and all(bb["accuracy"]>x for x in rew_b):
        interp+=" Canonical identification exceeds every rewire for both registered encodings."
    else:
        interp+=" Canonical identification is not uniquely above all rewired controls across both encodings."
    if statistics.mean(da)>0 and p_da<=.01 and statistics.mean(db)>0 and p_db<=.01:
        interp+=" Exact order produces encoding-specific relational fingerprints beyond the common histogram."
    else:
        interp+=" The paired cross-encoding tests do not establish robust encoding-specific temporal-order fingerprints."
    if dev:
        interp+=" Mature development contributes positively to balanced-order transduction."
    else:
        interp+=" Mature development does not satisfy the registered positive contribution gate."

    at=atlas(full,beacon)
    result={
      "schema":"amelia-p324-balanced-order-transduction-v1",
      "primary":{
        "held":primary,
        "a_accuracy":aa["accuracy"],"a_correct":aa["correct"],"a_n":aa["n"],"a_chance_p":a_chance,
        "b_accuracy":bb["accuracy"],"b_correct":bb["correct"],"b_n":bb["n"],"b_chance_p":b_chance,
        "a_to_b_accuracy":ab["accuracy"],"b_to_a_accuracy":ba["accuracy"],
        "a_self_cross_mean":statistics.mean(da),"a_self_cross_p":p_da,
        "b_self_cross_mean":statistics.mean(db),"b_self_cross_p":p_db,
        "rewire_a_accuracies":rew_a,"rewire_b_accuracies":rew_b,
        "a_rank_p":a_rank,"b_rank_p":b_rank,
        "b_minus_a_accuracy":bb["accuracy"]-aa["accuracy"],
      },
      "development":{"held":dev,"full_accuracy":full_pool,"blank_accuracy":blank_pool,
        "mean_difference":statistics.mean(dev_diffs),"p_upper":p_dev},
      "canonical":compact(full),"blank":compact(blank),
      "rewires":[{"id":i,"a_accuracy":x["a_to_a"]["accuracy"],"b_accuracy":x["b_to_b"]["accuracy"],
                  "a_to_b_accuracy":x["a_to_b"]["accuracy"],"b_to_a_accuracy":x["b_to_a"]["accuracy"]} for i,x in enumerate(rew)],
      "atlas":at,"interpretation":interp,
      "beacon":{"start_round":beacon["start_round"],"end_round":beacon["rounds"][-1]["round"],
                "sealed_registration_sha":beacon["sealed_registration_sha"],
                "beacon_sha256":sha256_file("experiments/p324/results/BEACON.json")},
      "provenance":{"registration_sha256":sha256_file("experiments/p324/REGISTRATION.md"),
        "amendment_sha256":sha256_file("experiments/p324/AMENDMENT_1.md"),
        "runner_sha256":sha256_file("experiments/p324/run.py"),
        "engine_sha256":sha256_file("experiments/p316/DynamicNumogram.py"),
        "raw_sha256":sha256_file(raw_path)}
    }
    with open(existing,"w",encoding="utf-8") as h:json.dump(result,h,indent=2,sort_keys=True)
    with open(os.path.join(args.out,"ATLAS.md"),"w",encoding="utf-8") as h:
        h.write("# P3.24 — Histogram-Balanced Relation Atlas\n\n")
        for x in at:
            h.write("## Window {:02d} — drand round {}\n\n".format(x["window"],x["round"]))
            h.write("- randomness: `{}`\n".format(x["randomness"]))
            h.write("- encoding A: {}\n".format(" ".join(map(str,x["encoding_a"]))))
            h.write("- encoding B: {}\n".format(" ".join(map(str,x["encoding_b"]))))
            h.write("- largest |A-B| relation: {} ({:+.6f})\n".format(x["largest_abs_relation_difference"],x["largest_abs_relation_delta"]))
            h.write("- A TEST mean: {}\n".format(", ".join("{:.4f}".format(v) for v in x["a_test_mean"])))
            h.write("- B TEST mean: {}\n\n".format(", ".join("{:.4f}".format(v) for v in x["b_test_mean"])))
    with open(os.path.join(args.out,"REPORT.md"),"w",encoding="utf-8") as h:h.write(report(result))
    print(json.dumps({"primary":result["primary"],"development":result["development"],"beacon":result["beacon"],"interpretation":interp},indent=2,sort_keys=True))
    return 0

if __name__=="__main__":raise SystemExit(main())
