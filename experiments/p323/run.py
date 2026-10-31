#!/usr/bin/env python3
"""P3.23 — Independent-Signal Relational Transduction."""
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
WINDOWS=16
SIGNAL_LEN=24
RELEASE_STEPS=16
LINEAGE_BASE=3270000
REWIRE_BASE=3276000
TEST_BASE=3277000
REWIRES=24
DRAWS=50000
COMPONENTS=("S","C","G","SS","SC","SG","CS","CC","CG","GS","GC","GG")
OPS=("S","C","G")

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def op(name,z):
    if name=="S": return syzygy_of(z)
    if name=="C": return current_of(z)
    if name=="G": return gate_of(z)
    raise ValueError(name)

def load_beacon():
    path=os.path.join(ROOT,"experiments","p323","results","BEACON.json")
    with open(path,encoding="utf-8") as h: data=json.load(h)
    if data.get("schema")!="amelia-p323-drand-default-v1": raise AssertionError("wrong beacon schema")
    seal=open(os.path.join(ROOT,"experiments","p323","SEALED_REGISTRATION_SHA.txt"),encoding="utf-8").read().strip()
    if data.get("sealed_registration_sha")!=seal: raise AssertionError("registration SHA mismatch")
    rounds=data.get("rounds",[])
    if len(rounds)!=WINDOWS: raise AssertionError("requires 16 beacon windows")
    for i,r in enumerate(rounds):
        a=list(map(int,r["real_zones"])); b=list(map(int,r["shuffled_zones"]))
        if len(a)!=SIGNAL_LEN or len(b)!=SIGNAL_LEN: raise AssertionError("signal length")
        if any(x<0 or x>9 for x in a+b): raise AssertionError("zone range")
        if sorted(a)!=sorted(b): raise AssertionError("shuffle multiset mismatch")
        if i and int(r["round"])!=int(rounds[i-1]["round"])+1: raise AssertionError("non-consecutive rounds")
        local=hashlib.sha256(bytes.fromhex(r["signature"])).hexdigest()
        if local!=r["randomness"] or local!=r["local_randomness_sha256"]: raise AssertionError("randomness digest mismatch")
    return data

def develop_rows(gates=None):
    rows=[]
    canonical_gates=p317.FULL_NUMOGRAM_GATES if gates is None else gates
    permeability=p317.original_gate_permeability(canonical_gates)
    for i in range(N):
        seed=LINEAGE_BASE+i
        dev,_=p317.make_tapes(seed)
        p=DynamicNumogramProcess(gates=gates,current_zone=seed%10)
        p317.run_dynamic_tape(p,dev)
        p317.shock_process(p,seed,permeability)
        rows.append({"seed":seed,"dev":dev,"base":p})
    return rows

def relation_profile(path):
    if len(path)!=RELEASE_STEPS+1: raise AssertionError("release path length")
    vals=[]
    for name in OPS:
        hits=sum(1 for i in range(RELEASE_STEPS) if path[i+1]==op(name,path[i]))
        vals.append(hits/RELEASE_STEPS)
    for a in OPS:
        for b in OPS:
            hits=0
            for i in range(RELEASE_STEPS-1):
                m=op(a,path[i]); t=op(b,m)
                if path[i+1]==m and path[i+2]==t: hits+=1
            vals.append(hits/(RELEASE_STEPS-1))
    if len(vals)!=12: raise AssertionError("relation profile width")
    return vals

def encounter(base,signal):
    p=copy.deepcopy(base)
    for x in signal: p.step(int(x))
    p.current_zone=4
    path=[4]
    for _ in range(RELEASE_STEPS):
        path.append(int(p.step(None)["to_zone"]))
    return relation_profile(path),path

def mean_vec(vectors):
    return [statistics.mean(v[j] for v in vectors) for j in range(len(vectors[0]))]

def sqdist(a,b):
    return sum((x-y)**2 for x,y in zip(a,b))

def classifier(real_profiles, shuffled_profiles):
    # profiles[lineage][window][component]
    centroids=[]
    sh_centroids=[]
    for w in range(WINDOWS):
        centroids.append(mean_vec([real_profiles[i][w] for i in range(TRAIN_N)]))
        sh_centroids.append(mean_vec([shuffled_profiles[i][w] for i in range(TRAIN_N)]))

    def evaluate(profiles, cents):
        correct=0; per=[0]*WINDOWS; margins=[]; preds=[]
        for i in range(TRAIN_N,N):
            row=[]
            for w in range(WINDOWS):
                x=profiles[i][w]
                ds=[sqdist(x,c) for c in cents]
                best=min(range(WINDOWS),key=lambda k:(ds[k],k))
                if best==w:
                    correct+=1; per[w]+=1
                wrong=min(ds[k] for k in range(WINDOWS) if k!=w)
                margins.append(wrong-ds[w])
                row.append(best)
            preds.append(row)
        total=(N-TRAIN_N)*WINDOWS
        return {
          "accuracy":correct/total,
          "correct":correct,
          "n":total,
          "per_window_accuracy":[x/(N-TRAIN_N) for x in per],
          "mean_margin":statistics.mean(margins),
          "predictions":preds,
        }

    rr=evaluate(real_profiles,centroids)
    rs=evaluate(shuffled_profiles,centroids)
    ss=evaluate(shuffled_profiles,sh_centroids)
    return rr,rs,ss,centroids,sh_centroids

def signflip(diffs,seed,one_sided=True):
    obs=statistics.mean(diffs); rng=random.Random(seed); ge=0
    for _ in range(DRAWS):
        m=statistics.mean(d*(1 if rng.random()<.5 else -1) for d in diffs)
        if (m>=obs-1e-15) if one_sided else (abs(m)>=abs(obs)-1e-15): ge+=1
    return (ge+1)/(DRAWS+1)

def multivar(real_means,shuf_means,seed):
    ds=[[a-b for a,b in zip(real_means[w],shuf_means[w])] for w in range(WINDOWS)]
    sds=[]
    for j in range(12):
        col=[d[j] for d in ds]
        sd=statistics.stdev(col) if len(col)>1 else 0.0
        sds.append(sd if sd>1e-12 else 0.0)
    def stat(signs=None):
        total=0.0
        for j,sd in enumerate(sds):
            if sd<=0: continue
            vals=[d[j]*(1 if signs is None else signs[i]) for i,d in enumerate(ds)]
            total+=(statistics.mean(vals)/sd)**2
        return total
    obs=stat(); rng=random.Random(seed); ge=0
    for _ in range(DRAWS):
        signs=[1 if rng.random()<.5 else -1 for _ in range(WINDOWS)]
        if stat(signs)>=obs-1e-15: ge+=1
    component_mean={COMPONENTS[j]:statistics.mean(d[j] for d in ds) for j in range(12)}
    return {"T":obs,"p":(ge+1)/(DRAWS+1),"component_mean_differences":component_mean}

def exact_binom_upper(n,k,p):
    # stable recurrence; p=1/16 and n=768 are safe in float.
    pmf=(1-p)**n
    vals=[pmf]
    for j in range(n):
        pmf=pmf*((n-j)/(j+1))*(p/(1-p))
        vals.append(pmf)
    return min(1.0,sum(vals[k:]))

def test_means(profiles):
    return [mean_vec([profiles[i][w] for i in range(TRAIN_N,N)]) for w in range(WINDOWS)]

def evaluate_controller(name,bases,beacon,raw,keep_paths=False):
    real_profiles=[[None]*WINDOWS for _ in range(N)]
    shuf_profiles=[[None]*WINDOWS for _ in range(N)]
    paths={"REAL":[[None]*WINDOWS for _ in range(N)],"SHUFFLED":[[None]*WINDOWS for _ in range(N)]} if keep_paths else None

    for i,base in enumerate(bases):
        for w,r in enumerate(beacon["rounds"]):
            for cond,key,store in (("REAL","real_zones",real_profiles),("SHUFFLED","shuffled_zones",shuf_profiles)):
                prof,path=encounter(base,r[key])
                store[i][w]=prof
                if keep_paths: paths[cond][i][w]=path
                raw.write(json.dumps({
                  "controller":name,"lineage":"P323-{:03d}".format(i),"window":w,
                  "round":int(r["round"]),"condition":cond,
                  "profile":prof,"path":path
                },sort_keys=True,separators=(",",":"))+"\n")

    rr,rs,ss,cents,shc=classifier(real_profiles,shuf_profiles)
    return {
      "name":name,
      "real_to_real":rr,
      "real_to_shuffled":rs,
      "shuffled_to_shuffled":ss,
      "real_centroids":cents,
      "shuffled_centroids":shc,
      "real_test_means":test_means(real_profiles),
      "shuffled_test_means":test_means(shuf_profiles),
      "_real_profiles":real_profiles,
      "_shuffled_profiles":shuf_profiles,
      "_paths":paths
    }

def compact(ev):
    return {k:v for k,v in ev.items() if not k.startswith("_")}

def atlas(full,beacon):
    out=[]
    paths=full["_paths"]
    for w,r in enumerate(beacon["rounds"]):
        real=full["real_test_means"][w]; shuf=full["shuffled_test_means"][w]
        diffs=[a-b for a,b in zip(real,shuf)]
        best=max(range(12),key=lambda j:(diffs[j],-j))
        lineage_rows=[]
        for i in range(TRAIN_N,N):
            lineage_rows.append({
              "lineage":"P323-{:03d}".format(i),
              "real_profile":full["_real_profiles"][i][w],
              "shuffled_profile":full["_shuffled_profiles"][i][w],
              "real_path":paths["REAL"][i][w],
              "shuffled_path":paths["SHUFFLED"][i][w]
            })
        out.append({
          "window":w,"round":int(r["round"]),"randomness":r["randomness"],
          "real_zones":r["real_zones"],"shuffled_zones":r["shuffled_zones"],
          "train_centroid":full["real_centroids"][w],
          "real_test_mean":real,"shuffled_test_mean":shuf,
          "most_elevated_relation":COMPONENTS[best],"most_elevated_delta":diffs[best],
          "test_lineages":lineage_rows
        })
    return out

def report(result):
    p=result["primary"]; d=result["development"]
    lines=["# P3.23 — Independent-Signal Relational Transduction Result","",
      "- independent-signal relational transduction: **{}**".format("PASS" if p["held"] else "FAIL"),
      "- canonical REAL→REAL accuracy: {:.6f}".format(p["canonical_accuracy"]),
      "- chance accuracy: 0.062500",
      "- exact chance p: {:.8g}".format(p["chance_p"]),
      "- best rewire REAL→REAL accuracy: {:.6f}".format(max(p["rewire_accuracies"])),
      "- rewire rank p: {:.6f}".format(p["rank_p"]),
      "- canonical REAL→SHUFFLED accuracy: {:.6f}".format(p["real_to_shuffled_accuracy"]),
      "- temporal-order paired p: {:.8g}".format(p["temporal_order_p"]),
      "- REAL-vs-SHUFFLED relational-profile multivariate p: {:.8g}".format(p["profile_multivariate"]["p"]),"",
      "## Developmental contribution","",
      "- FULL REAL→REAL accuracy: {:.6f}".format(d["full_accuracy"]),
      "- BLANK REAL→REAL accuracy: {:.6f}".format(d["blank_accuracy"]),
      "- paired per-window p: {:.8g}".format(d["p_upper"]),
      "- developmental contribution: **{}**".format("PASS" if d["held"] else "FAIL"),"",
      "## Interpretation","",result["interpretation"],""]
    return "\n".join(lines)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",default="experiments/p323/results"); args=ap.parse_args()
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

    rr=full["real_to_real"]; rs=full["real_to_shuffled"]
    chance_p=exact_binom_upper(rr["n"],rr["correct"],1/WINDOWS)
    temporal_diffs=[a-b for a,b in zip(rr["per_window_accuracy"],rs["per_window_accuracy"])]
    temporal_p=signflip(temporal_diffs,TEST_BASE,True)
    multi=multivar(full["real_test_means"],full["shuffled_test_means"],TEST_BASE+1)

    rew_acc=[x["real_to_real"]["accuracy"] for x in rew]
    ge=sum(1 for x in rew_acc if x>=rr["accuracy"])
    rank_p=(1+ge)/(REWIRES+1)
    primary=(chance_p<=.01 and all(rr["accuracy"]>x for x in rew_acc)
             and abs(rank_p-.04)<1e-12 and statistics.mean(temporal_diffs)>0
             and temporal_p<=.01 and multi["p"]<=.01)

    dev_diffs=[a-b for a,b in zip(full["real_to_real"]["per_window_accuracy"],blank["real_to_real"]["per_window_accuracy"])]
    dev_p=signflip(dev_diffs,TEST_BASE+2,True)
    dev=(statistics.mean(dev_diffs)>0 and dev_p<=.01
         and full["real_to_real"]["accuracy"]>blank["real_to_real"]["accuracy"])

    if primary:
        interp="Fresh independently generated drand signals are reproducibly transduced into signal-specific canonical relational profiles, with stronger held-out signal identity than all degree-preserving rewires and a loss of the original fingerprint under temporal permutation."
    else:
        interp="P3.23 does not satisfy the full registered independent-signal relational-transduction gate."
    if rr["accuracy"]>1/WINDOWS and chance_p<=.01:
        interp+=" The canonical relation basis nevertheless carries held-out information about which fresh external signal was presented."
    else:
        interp+=" The canonical relation basis does not significantly identify the fresh external signal above chance."
    if all(rr["accuracy"]>x for x in rew_acc):
        interp+=" Canonical held-out signal identification exceeds every degree-preserving rewire."
    else:
        interp+=" Canonical held-out signal identification is not uniquely above the rewired controls."
    if temporal_p<=.01 and statistics.mean(temporal_diffs)>0 and multi["p"]<=.01:
        interp+=" The exact temporal order contributes to the relational fingerprint beyond the preserved symbol multiset."
    else:
        interp+=" The registered temporal-order controls do not establish an order-specific relational fingerprint."
    if dev:
        interp+=" Mature development contributes positively to relational transduction."
    else:
        interp+=" Mature development does not satisfy the registered positive contribution gate."

    at=atlas(full,beacon)
    result={
      "schema":"amelia-p323-independent-relational-transduction-v1",
      "primary":{"held":primary,"canonical_accuracy":rr["accuracy"],"canonical_correct":rr["correct"],"n":rr["n"],
        "chance_p":chance_p,"real_to_shuffled_accuracy":rs["accuracy"],
        "shuffled_self_accuracy":full["shuffled_to_shuffled"]["accuracy"],
        "temporal_order_mean_difference":statistics.mean(temporal_diffs),"temporal_order_p":temporal_p,
        "profile_multivariate":multi,"rewire_accuracies":rew_acc,"rank_p":rank_p},
      "development":{"held":dev,"full_accuracy":full["real_to_real"]["accuracy"],
        "blank_accuracy":blank["real_to_real"]["accuracy"],"mean_difference":statistics.mean(dev_diffs),"p_upper":dev_p},
      "canonical":compact(full),"blank":compact(blank),
      "rewires":[{"id":i,"real_to_real_accuracy":x["real_to_real"]["accuracy"],
                  "real_to_shuffled_accuracy":x["real_to_shuffled"]["accuracy"],
                  "shuffled_self_accuracy":x["shuffled_to_shuffled"]["accuracy"]} for i,x in enumerate(rew)],
      "atlas":at,"interpretation":interp,
      "beacon":{"start_round":beacon["start_round"],"end_round":beacon["rounds"][-1]["round"],
                "sealed_registration_sha":beacon["sealed_registration_sha"],
                "beacon_sha256":sha256_file("experiments/p323/results/BEACON.json")},
      "provenance":{"registration_sha256":sha256_file("experiments/p323/REGISTRATION.md"),
        "amendment_sha256":sha256_file("experiments/p323/AMENDMENT_1.md"),
        "runner_sha256":sha256_file("experiments/p323/run.py"),
        "engine_sha256":sha256_file("experiments/p316/DynamicNumogram.py"),
        "raw_sha256":sha256_file(raw_path)}
    }

    with open(existing,"w",encoding="utf-8") as h: json.dump(result,h,indent=2,sort_keys=True)
    with open(os.path.join(args.out,"ATLAS.md"),"w",encoding="utf-8") as h:
        h.write("# P3.23 — Independent-Signal Relation Atlas\n\n")
        for x in at:
            h.write("## Window {:02d} — drand round {}\n\n".format(x["window"],x["round"]))
            h.write("- randomness: `{}`\n".format(x["randomness"]))
            h.write("- REAL signal: {}\n".format(" ".join(map(str,x["real_zones"]))))
            h.write("- SHUFFLED: {}\n".format(" ".join(map(str,x["shuffled_zones"]))))
            h.write("- most elevated relation vs shuffled: {} ({:+.6f})\n".format(x["most_elevated_relation"],x["most_elevated_delta"]))
            h.write("- REAL TEST mean: {}\n".format(", ".join("{:.4f}".format(v) for v in x["real_test_mean"])))
            h.write("- SHUFFLED TEST mean: {}\n\n".format(", ".join("{:.4f}".format(v) for v in x["shuffled_test_mean"])))
    with open(os.path.join(args.out,"REPORT.md"),"w",encoding="utf-8") as h: h.write(report(result))
    print(json.dumps({"primary":result["primary"],"development":result["development"],"beacon":result["beacon"],"interpretation":interp},indent=2,sort_keys=True))
    return 0

if __name__=="__main__": raise SystemExit(main())
