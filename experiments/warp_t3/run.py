#!/usr/bin/env python3
"""WARP-T3 — Passage-Trace Address Discrimination."""
from __future__ import annotations
import argparse, copy, gzip, hashlib, importlib.util, json, math, os, random, statistics, sys
from collections import Counter, defaultdict

ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
if ROOT not in sys.path: sys.path.insert(0,ROOT)
P316=os.path.join(ROOT,"experiments","p316")
if P316 not in sys.path: sys.path.insert(0,P316)

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(mod); return mod

p317=load("p317_frozen",os.path.join(ROOT,"experiments","p317","run.py"))
wt1=load("warp_t1_frozen",os.path.join(ROOT,"experiments","warp_t1","run.py"))
wt2=load("warp_t2_frozen",os.path.join(ROOT,"experiments","warp_t2","run.py"))

N=160; SEED_BASE=3240000; PROBE_BASE=3245000; TEST_BASE=3247000
PROBES=32; PROBE_LEN=40; K=32; V=33; DRAWS=50000; BOOT_DRAWS=20000
OTHER="OTHER"
ARMS=("W","E","N","B","T","P")
POINTER_MOTIFS={"1-7-8-9","1-7","1-2-7","1-8-7","7-8","1-7-8"}

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def address_probe(i):
    seed=PROBE_BASE+i
    matrix=p317.transition_matrix(seed*19+3)
    return p317.sample_markov_tape(matrix,seed*29+17,PROBE_LEN)

def response(base,tape):
    p=copy.deepcopy(base)
    rec=p317.run_dynamic_tape(p,tape)
    path=[int(x["zone"]) for x in rec]
    echo=p317.ngrams(tape,4)
    motifs=[]; positions=defaultdict(list)
    for j in range(len(path)-3):
        m=tuple(path[j:j+4])
        if m not in echo:
            s="-".join(map(str,m)); motifs.append(s); positions[s].append(j)
    edges=Counter(zip(path,path[1:])); total=sum(edges.values())
    tent=0.0 if total==0 else -sum((c/total)*math.log(c/total,2) for c in edges.values() if c)
    return {"motifs":motifs,"positions":dict(positions),"transition_entropy":tent}

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
      "E":wt2.release_shell(pre,entry.memory,entry.deformation_tensor,seed),
      "N":wt2.release_shell(pre,nonwarp.memory,nonwarp.deformation_tensor,seed),
      "B":wt2.release_shell(pre,pre.memory,pre.deformation_tensor,seed),
      "T":wt2.release_shell(pre,topo.memory,topo.deformation_tensor,seed),
      "P":wt2.release_shell(pre,real.memory,pre.deformation_tensor,seed),
    }
    return {
      "index":index,"seed":seed,"eligible":True,"entry_step":int(e["index"]),
      "source":int(pre.current_zone),"target":int(e["target"]),
      "inputs":inputs,"targets":targets,"shells":shells
    }

def build_vocab(responses,train_ids):
    c=Counter()
    for li in train_ids:
        for r in responses[li]:c.update(r["motifs"])
    return [m for m,_ in sorted(c.items(),key=lambda kv:(-kv[1],kv[0]))[:K]]

def compress(motifs,vset):
    return [m if m in vset else OTHER for m in motifs]

def train_model(responses,train_ids,vocab):
    alpha=list(vocab)+[OTHER]; vs=set(vocab)
    counts=[Counter() for _ in range(PROBES)]; totals=[0]*PROBES
    for li in train_ids:
        for pi,r in enumerate(responses[li]):
            toks=compress(r["motifs"],vs); counts[pi].update(toks); totals[pi]+=len(toks)
    out=[]
    for pi in range(PROBES):
        den=totals[pi]+V
        out.append({tok:math.log((counts[pi][tok]+1)/den) for tok in alpha})
    return out

def decode(responses,test_ids,vocab,model):
    vs=set(vocab); per=[0]*PROBES; correct=0; margins=[]
    for li in test_ids:
        for pi,r in enumerate(responses[li]):
            toks=compress(r["motifs"],vs)
            scores=[sum(model[a].get(t,model[a][OTHER]) for t in toks) for a in range(PROBES)]
            best=max(range(PROBES),key=lambda x:(scores[x],-x))
            if best==pi:correct+=1; per[pi]+=1
            margins.append(scores[pi]-max(scores[a] for a in range(PROBES) if a!=pi))
    return {"accuracy":correct/(len(test_ids)*PROBES),"per_probe_accuracy":[x/len(test_ids) for x in per],"correct":correct,"n":len(test_ids)*PROBES,"mean_margin":statistics.mean(margins)}

def conditional_distributions(responses,test_ids,vocab):
    alpha=list(vocab)+[OTHER]; vs=set(vocab); out=[]
    for pi in range(PROBES):
        c=Counter()
        for li in test_ids:c.update(compress(responses[li][pi]["motifs"],vs))
        total=sum(c.values())
        out.append({tok:(c[tok]/total if total else 0.0) for tok in alpha})
    return alpha,out

def balanced_efficiency_contrib(responses,test_ids,vocab):
    alpha,cond=conditional_distributions(responses,test_ids,vocab)
    vals=[]
    for p in range(PROBES):
        p1=cond[p]
        p0={tok:sum(cond[q][tok] for q in range(PROBES) if q!=p)/(PROBES-1) for tok in alpha}
        mix={tok:.5*(p1[tok]+p0[tok]) for tok in alpha}
        I=0.0
        for dist in (p1,p0):
            for tok in alpha:
                q=dist[tok]
                if q>0 and mix[tok]>0:I+=.5*q*math.log(q/mix[tok],2)
        H=-sum(x*math.log(x,2) for x in mix.values() if x>0)
        vals.append(0.0 if H==0 else I/H)
    return vals

def signflip(diffs,seed):
    obs=statistics.mean(diffs); rng=random.Random(seed); ge=0
    for _ in range(DRAWS):
        m=statistics.mean(d*(1 if rng.random()<.5 else -1) for d in diffs)
        if abs(m)>=abs(obs)-1e-15:ge+=1
    return (ge+1)/(DRAWS+1)

def bootstrap_ci(diffs,seed):
    rng=random.Random(seed); vals=[]
    n=len(diffs)
    for _ in range(BOOT_DRAWS):vals.append(statistics.mean(rng.choice(diffs) for _ in range(n)))
    vals.sort()
    return {"lo":vals[int(.05*BOOT_DRAWS)],"hi":vals[min(BOOT_DRAWS-1,int(.95*BOOT_DRAWS)-1)],"mean":statistics.mean(vals)}

def eval_arm(responses,train_ids,test_ids):
    vocab=build_vocab(responses,train_ids); model=train_model(responses,train_ids,vocab)
    dec=decode(responses,test_ids,vocab,model)
    eff=balanced_efficiency_contrib(responses,test_ids,vocab)
    branch=statistics.mean(responses[li][pi]["transition_entropy"] for li in test_ids for pi in range(PROBES))
    return {"vocab":vocab,"decoder":dec,"efficiency_contrib":eff,"mean_efficiency_contrib":statistics.mean(eff),"branch_entropy":branch}

def atlas_w(responses,train_ids,test_ids,vocab,n_responses):
    rows=[]
    for pi in range(PROBES):
        candidates=[]
        for motif in vocab:
            tr=sum(1 for li in train_ids if motif in responses[li][pi]["positions"])
            te=sum(1 for li in test_ids if motif in responses[li][pi]["positions"])
            other_p=0; other_a=0
            for q in range(PROBES):
                if q==pi:continue
                for li in test_ids:
                    if motif in responses[li][q]["positions"]:other_p+=1
                    else:other_a+=1
            odds1=(te+.5)/(len(test_ids)-te+.5); odds0=(other_p+.5)/(other_a+.5)
            lo=math.log(odds1/odds0)
            candidates.append((lo,te/len(test_ids),motif,tr,te))
        candidates.sort(key=lambda x:(-x[0],-x[1],x[2]))
        lo,prev,motif,tr,te=candidates[0]
        contributors=[]
        for li in test_ids:
            starts=responses[li][pi]["positions"].get(motif,[])
            if starts:contributors.append({"lineage":"WT3-{:03d}".format(li),"starts":starts})
        rows.append({"probe_id":pi,"motif":motif,"train_prevalence":tr/len(train_ids),"test_prevalence":te/len(test_ids),"log_odds":lo,"lineages":contributors})
    return rows

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",default="experiments/warp_t3/results"); args=ap.parse_args()
    os.makedirs(args.out,exist_ok=True)
    existing=os.path.join(args.out,"summary.json")
    if os.path.exists(existing):
        print(open(existing,encoding="utf-8").read()); return 0

    lineages=[make_lineage(i) for i in range(N)]
    eligible=[r for r in lineages if r["eligible"]]
    if len(eligible)<80:
        result={"schema":"amelia-warp-t3-v1","valid":False,"eligible":len(eligible),"interpretation":"Fewer than 80 eligible lineages; primary communication claim not evaluated."}
        with open(existing,"w") as h:json.dump(result,h,indent=2,sort_keys=True)
        with open(os.path.join(args.out,"REPORT.md"),"w") as h:h.write("# WARP-T3 Result\n\nInsufficient eligible lineages: {}/160.\n".format(len(eligible)))
        print(json.dumps(result,indent=2)); return 0

    eligible_indices=[r["index"] for r in eligible]
    train_ids=[li for rank,li in enumerate(eligible_indices) if rank%2==0]
    test_ids=[li for rank,li in enumerate(eligible_indices) if rank%2==1]
    probes=[address_probe(i) for i in range(PROBES)]

    responses={arm:{} for arm in ARMS}
    raw_path=os.path.join(args.out,"responses.jsonl.gz")
    with gzip.open(raw_path,"wt",encoding="utf-8") as raw:
        for r in eligible:
            li=r["index"]
            for arm in ARMS:
                rr=[response(r["shells"][arm],t) for t in probes]
                responses[arm][li]=rr
                raw.write(json.dumps({"arm":arm,"lineage":"WT3-{:03d}".format(li),"responses":rr},sort_keys=True,separators=(",",":"))+"\n")

    evals={arm:eval_arm(responses[arm],train_ids,test_ids) for arm in ARMS}
    def diffs(metric,a,b):
        if metric=="acc":return [x-y for x,y in zip(evals[a]["decoder"]["per_probe_accuracy"],evals[b]["decoder"]["per_probe_accuracy"])]
        return [x-y for x,y in zip(evals[a]["efficiency_contrib"],evals[b]["efficiency_contrib"])]

    wn_acc=diffs("acc","W","N"); wn_eff=diffs("eff","W","N")
    p_wn_acc=signflip(wn_acc,TEST_BASE); p_wn_eff=signflip(wn_eff,TEST_BASE+1)
    wb_acc=diffs("acc","W","B"); p_wb_acc=signflip(wb_acc,TEST_BASE+2)
    same_dir=statistics.mean(wn_acc)*statistics.mean(wn_eff)>0
    primary_pre=(p_wn_acc<=.01 and p_wn_eff<=.01 and same_dir and p_wb_acc<=.01)
    direction="enhancement" if primary_pre and statistics.mean(wn_acc)>0 else ("suppression" if primary_pre else "none")

    we_acc=diffs("acc","W","E"); we_eff=diffs("eff","W","E")
    p_we_acc=signflip(we_acc,TEST_BASE+3); p_we_eff=signflip(we_eff,TEST_BASE+4)
    beyond=(p_we_acc<=.01 and p_we_eff<=.01 and statistics.mean(we_acc)*statistics.mean(we_eff)>0)

    tb_acc=diffs("acc","T","B"); tb_eff=diffs("eff","T","B")
    p_tb_acc=signflip(tb_acc,TEST_BASE+5); p_tb_eff=signflip(tb_eff,TEST_BASE+6)
    validity=not (p_tb_acc<=.01 or p_tb_eff<=.01)
    primary=primary_pre and validity

    pw_acc=diffs("acc","P","W"); pw_eff=diffs("eff","P","W")
    ci_acc=bootstrap_ci(pw_acc,3247100); ci_eff=bootstrap_ci(pw_eff,3247101)
    eq_acc=ci_acc["lo"]>-.02 and ci_acc["hi"]<.02
    eq_eff=ci_eff["lo"]>-.02 and ci_eff["hi"]<.02
    pfm_sufficient=eq_acc and eq_eff

    atlas=atlas_w(responses["W"],train_ids,test_ids,evals["W"]["vocab"],len(eligible))
    w_test_motifs=set()
    n_test_motifs=set()
    for li in test_ids:
        for pi in range(PROBES):
            w_test_motifs.update(responses["W"][li][pi]["positions"].keys())
            n_test_motifs.update(responses["N"][li][pi]["positions"].keys())
    w_only=sorted(w_test_motifs-n_test_motifs)
    pointer_hits=sorted(m for m in w_test_motifs if m in POINTER_MOTIFS)

    if primary:
        interp="The portable Warp-passage trace changes held-out address/reply discrimination after common-state release ({}) relative to matched non-Warp passage.".format(direction)
    else:
        interp="WARP-T3 does not satisfy the registered primary claim that the portable Warp-passage trace changes held-out address/reply discrimination."
    if beyond:interp+=" The communication effect extends beyond the entry event alone."
    else:interp+=" Passage beyond entry does not satisfy its registered communication-effect gate."
    if pfm_sufficient:interp+=" The incremental PFM trace is equivalent to the full Warp trace within the ±0.02 communication margin."
    else:interp+=" PFM-only communication equivalence to the full Warp trace is not established."
    if not validity:interp+=" The topology-only validity control differs from baseline, invalidating the communication interpretation."

    result={
      "schema":"amelia-warp-t3-v1","valid":validity,"eligible":len(eligible),"train_n":len(train_ids),"test_n":len(test_ids),
      "primary":{"held":primary,"pre_validity_held":primary_pre,"direction":direction,
        "W_vs_N_accuracy_mean":statistics.mean(wn_acc),"W_vs_N_accuracy_p":p_wn_acc,
        "W_vs_N_efficiency_mean":statistics.mean(wn_eff),"W_vs_N_efficiency_p":p_wn_eff,
        "W_vs_B_accuracy_mean":statistics.mean(wb_acc),"W_vs_B_accuracy_p":p_wb_acc},
      "passage_beyond_entry":{"held":beyond,"accuracy_mean":statistics.mean(we_acc),"accuracy_p":p_we_acc,"efficiency_mean":statistics.mean(we_eff),"efficiency_p":p_we_eff},
      "pfm_sufficiency":{"held":pfm_sufficient,"accuracy_ci90":ci_acc,"efficiency_ci90":ci_eff},
      "topology_validity":{"valid":validity,"accuracy_mean":statistics.mean(tb_acc),"accuracy_p":p_tb_acc,"efficiency_mean":statistics.mean(tb_eff),"efficiency_p":p_tb_eff},
      "arms":{arm:{"accuracy":evals[arm]["decoder"]["accuracy"],"mean_efficiency_contrib":evals[arm]["mean_efficiency_contrib"],"branch_entropy":evals[arm]["branch_entropy"],"vocab":evals[arm]["vocab"]} for arm in ARMS},
      "atlas":atlas,"warp_only_test_motifs":w_only,"pointer_hits":pointer_hits,
      "interpretation":interp,
      "provenance":{"registration_sha256":sha256_file("experiments/warp_t3/REGISTRATION.md"),"amendment_sha256":sha256_file("experiments/warp_t3/AMENDMENT_1.md"),"runner_sha256":sha256_file("experiments/warp_t3/run.py"),"raw_sha256":sha256_file(raw_path)}
    }
    with open(existing,"w") as h:json.dump(result,h,indent=2,sort_keys=True)
    with open(os.path.join(args.out,"ATLAS.md"),"w") as h:
        h.write("# WARP-T3 — Held-out Warp Address / Reply Atlas\n\n")
        h.write("Pointer-catalogue hits: {}\n\n".format(", ".join(pointer_hits) if pointer_hits else "none"))
        h.write("W-only TEST motifs absent from matched non-Warp: {}\n\n".format(", ".join(w_only[:100]) if w_only else "none"))
        for x in atlas:
            h.write("## Probe {:02d}\n\n- motif: {}\n- TRAIN prevalence: {:.4f}\n- TEST prevalence: {:.4f}\n- TEST log-odds: {:.6f}\n".format(x["probe_id"],x["motif"],x["train_prevalence"],x["test_prevalence"],x["log_odds"]))
            for z in x["lineages"]:h.write("- {}: {}\n".format(z["lineage"],", ".join(map(str,z["starts"]))))
            h.write("\n")
    with open(os.path.join(args.out,"REPORT.md"),"w") as h:
        h.write("# WARP-T3 — Passage-Trace Address Discrimination Result\n\n")
        h.write("- eligible lineages: {}/{} (TRAIN {}, TEST {})\n".format(len(eligible),N,len(train_ids),len(test_ids)))
        h.write("- portable trace changes discrimination: **{}**\n".format("PASS" if primary else "FAIL"))
        h.write("- direction: **{}**\n".format(direction))
        h.write("- W−N per-probe accuracy mean: {:.6f}, p={:.8g}\n".format(statistics.mean(wn_acc),p_wn_acc))
        h.write("- W−N per-probe efficiency mean: {:.6f}, p={:.8g}\n".format(statistics.mean(wn_eff),p_wn_eff))
        h.write("- W−B per-probe accuracy mean: {:.6f}, p={:.8g}\n".format(statistics.mean(wb_acc),p_wb_acc))
        h.write("- passage beyond entry: **{}**\n".format("PASS" if beyond else "FAIL"))
        h.write("- PFM communication sufficiency: **{}**\n".format("PASS" if pfm_sufficient else "FAIL"))
        h.write("- topology-only validity: **{}**\n\n".format("PASS" if validity else "FAIL"))
        h.write("## Arm readouts\n\n")
        for arm in ARMS:h.write("- {}: accuracy {:.6f}, mean efficiency {:.6f}, transition entropy {:.6f}\n".format(arm,evals[arm]["decoder"]["accuracy"],evals[arm]["mean_efficiency_contrib"],evals[arm]["branch_entropy"]))
        h.write("\n## Interpretation\n\n"+interp+"\n")
    print(json.dumps({k:result[k] for k in ("eligible","primary","passage_beyond_entry","pfm_sufficiency","topology_validity","arms","pointer_hits","interpretation")},indent=2,sort_keys=True))
    return 0

if __name__=="__main__":raise SystemExit(main())
