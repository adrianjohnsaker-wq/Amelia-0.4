#!/usr/bin/env python3
"""P3.21 — Repertoire-Controlled Communication Efficacy."""
from __future__ import annotations
import argparse, copy, gzip, hashlib, importlib.util, json, math, os, random, statistics, sys
from collections import Counter, defaultdict

ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
if ROOT not in sys.path: sys.path.insert(0,ROOT)
P316=os.path.join(ROOT,"experiments","p316")
if P316 not in sys.path: sys.path.insert(0,P316)
from DynamicNumogram import DynamicNumogramProcess, IntegratedMemorySystem

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(mod); return mod

p317=load("p317_frozen",os.path.join(ROOT,"experiments","p317","run.py"))

N=96; TRAIN_N=48; TEST_N=48
LINEAGE_BASE=3230000; PROBE_BASE=3235000; REWIRE_BASE=3236000
TEST_BASE=3237000; BOOT_BASE=3238000
PROBES=64; PROBE_LEN=40; K=32; V=33
REWIRES=32; DRAWS=50000; BOOT_DRAWS=20000
OTHER="OTHER"

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def probe(i):
    seed=PROBE_BASE+i
    matrix=p317.transition_matrix(seed*17+7)
    return p317.sample_markov_tape(matrix,seed*31+11,PROBE_LEN)

def response_dynamic(base,tape):
    p=copy.deepcopy(base)
    rec=p317.run_dynamic_tape(p,tape)
    path=[int(x["zone"]) for x in rec]
    echo=p317.ngrams(tape,4)
    occ=[]; pos=defaultdict(list)
    for i in range(len(path)-3):
        m=tuple(path[i:i+4])
        if m not in echo:
            s="-".join(map(str,m)); occ.append(s); pos[s].append(i)
    edges=Counter((a,b) for a,b in zip(path,path[1:]))
    total=sum(edges.values())
    tent=0.0 if total==0 else -sum((c/total)*math.log(c/total,2) for c in edges.values() if c)
    return {"motifs":occ,"positions":dict(pos),"transition_entropy":tent}

def develop_canonical():
    rows=[]; permeability=p317.original_gate_permeability(p317.FULL_NUMOGRAM_GATES)
    for i in range(N):
        seed=LINEAGE_BASE+i
        dev,_=p317.make_tapes(seed)
        p=DynamicNumogramProcess(current_zone=seed%10)
        p317.run_dynamic_tape(p,dev)
        s=copy.deepcopy(p); p317.shock_process(s,seed,permeability)
        rows.append({"seed":seed,"dev":dev,"full":s})
    return rows

def controller_responses(bases,probes):
    return [[response_dynamic(bases[i],t) for t in probes] for i in range(N)]

def build_vocab(responses):
    c=Counter()
    for li in range(TRAIN_N):
        for r in responses[li]: c.update(r["motifs"])
    ranked=sorted(c.items(),key=lambda kv:(-kv[1],kv[0]))
    return [m for m,_ in ranked[:K]]

def compress(motifs,vocab_set):
    return [m if m in vocab_set else OTHER for m in motifs]

def train_model(responses,vocab):
    vs=set(vocab); alphabet=list(vocab)+[OTHER]
    counts=[[Counter() for _ in range(PROBES)]][0]
    totals=[0]*PROBES
    for li in range(TRAIN_N):
        for pi,r in enumerate(responses[li]):
            toks=compress(r["motifs"],vs); counts[pi].update(toks); totals[pi]+=len(toks)
    logp=[]
    for pi in range(PROBES):
        denom=totals[pi]+V
        logp.append({tok:math.log((counts[pi][tok]+1)/denom) for tok in alphabet})
    return logp

def decode(responses,vocab,model):
    vs=set(vocab)
    correct=0; margins=[]; per_correct=[0]*PROBES
    preds=[]
    for li in range(TRAIN_N,N):
        line=[]
        for pi,r in enumerate(responses[li]):
            toks=compress(r["motifs"],vs)
            scores=[]
            for cand in range(PROBES):
                scores.append(sum(model[cand].get(tok,model[cand][OTHER]) for tok in toks))
            best=max(range(PROBES),key=lambda x:(scores[x],-x))
            if best==pi:
                correct+=1; per_correct[pi]+=1
            wrong=max(scores[j] for j in range(PROBES) if j!=pi)
            margins.append(scores[pi]-wrong)
            line.append(best)
        preds.append(line)
    return {
      "correct":correct,"n":TEST_N*PROBES,"accuracy":correct/(TEST_N*PROBES),
      "per_probe_accuracy":[x/TEST_N for x in per_correct],
      "mean_margin":statistics.mean(margins),"predictions":preds
    }

def conditional_token_distributions(responses,vocab,lineage_indices):
    vs=set(vocab); alpha=list(vocab)+[OTHER]
    probs=[]
    for pi in range(PROBES):
        c=Counter()
        for li in lineage_indices:c.update(compress(responses[li][pi]["motifs"],vs))
        total=sum(c.values())
        if total==0: probs.append({tok:0.0 for tok in alpha})
        else: probs.append({tok:c[tok]/total for tok in alpha})
    return alpha,probs

def information_efficiency(responses,vocab,lineage_indices):
    alpha,cond=conditional_token_distributions(responses,vocab,lineage_indices)
    pr={tok:sum(cond[a][tok] for a in range(PROBES))/PROBES for tok in alpha}
    I=0.0
    for a in range(PROBES):
        for tok in alpha:
            q=cond[a][tok]
            if q>0 and pr[tok]>0:I+=(1/PROBES)*q*math.log(q/pr[tok],2)
    H=-sum(x*math.log(x,2) for x in pr.values() if x>0)
    return {"I":I,"H":H,"E":0.0 if H==0 else I/H}

def exact_binom_upper(n,k,p):
    if k<=0:return 1.0
    pmf=(1-p)**n; vals=[pmf]
    for j in range(0,n):
        pmf=pmf*((n-j)/(j+1))*(p/(1-p)); vals.append(pmf)
    return min(1.0,sum(vals[k:]))

def signflip(diffs,seed,two_sided=True):
    obs=statistics.mean(diffs); rng=random.Random(seed); ge=0
    for _ in range(DRAWS):
        m=statistics.mean(d*(1 if rng.random()<.5 else -1) for d in diffs)
        if (abs(m)>=abs(obs)-1e-15) if two_sided else (m>=obs-1e-15): ge+=1
    return (ge+1)/(DRAWS+1)

def branch_entropy(responses):
    return statistics.mean(responses[li][pi]["transition_entropy"] for li in range(TRAIN_N,N) for pi in range(PROBES))

def eval_controller(name,bases,probes,raw_handle):
    responses=controller_responses(bases,probes)
    vocab=build_vocab(responses); model=train_model(responses,vocab)
    dec=decode(responses,vocab,model)
    info=information_efficiency(responses,vocab,range(TRAIN_N,N))
    bent=branch_entropy(responses)
    for li in range(N):
        raw_handle.write(json.dumps({"controller":name,"lineage":li,"responses":responses[li]},sort_keys=True,separators=(",",":"))+"\n")
    return {"name":name,"vocab":vocab,"decoder":dec,"info":info,"branch_entropy":bent},responses

def canonical_atlas(responses,vocab):
    rows=[]; vset=set(vocab)
    for pi in range(PROBES):
        candidates=[]
        for motif in vocab:
            tr_present=sum(1 for li in range(TRAIN_N) if motif in responses[li][pi]["positions"])
            te_present=sum(1 for li in range(TRAIN_N,N) if motif in responses[li][pi]["positions"])
            te_abs=TEST_N-te_present
            other_present=0; other_abs=0
            for q in range(PROBES):
                if q==pi:continue
                for li in range(TRAIN_N,N):
                    if motif in responses[li][q]["positions"]:other_present+=1
                    else:other_abs+=1
            odds_p=(te_present+.5)/(te_abs+.5)
            odds_o=(other_present+.5)/(other_abs+.5)
            lo=math.log(odds_p/odds_o)
            candidates.append((lo,te_present/TEST_N,motif,tr_present,te_present))
        candidates.sort(key=lambda x:(-x[0],-x[1],x[2]))
        lo,tep,motif,trp,tep_n=candidates[0]
        contributors=[]
        for li in range(TRAIN_N,N):
            starts=responses[li][pi]["positions"].get(motif,[])
            if starts:contributors.append({"lineage":"P321-{:03d}".format(li),"starts":starts})
        rows.append({"probe_id":pi,"motif":motif,"train_prevalence":trp/TRAIN_N,"test_prevalence":tep_n/TEST_N,"log_odds":lo,"lineages":contributors})
    return rows

def bootstrap_eff_diff(full_resp,full_vocab,blank_resp,blank_vocab):
    rng=random.Random(BOOT_BASE); diffs=[]
    test_ids=list(range(TRAIN_N,N))
    for _ in range(BOOT_DRAWS):
        sample=[rng.choice(test_ids) for _ in test_ids]
        ef=information_efficiency(full_resp,full_vocab,sample)["E"]
        eb=information_efficiency(blank_resp,blank_vocab,sample)["E"]
        diffs.append(ef-eb)
    diffs.sort()
    lo=diffs[int(.005*BOOT_DRAWS)]
    hi=diffs[min(BOOT_DRAWS-1,int(.995*BOOT_DRAWS)-1)]
    return {"lo":lo,"hi":hi,"mean":statistics.mean(diffs)}

def report(result):
    c=result["canonical"]; dev=result["development"]
    lines=["# P3.21 — Repertoire-Controlled Communication Efficacy Result","",
      "- canonical communication privilege: **{}**".format("PASS" if c["held"] else "FAIL"),
      "- canonical held-out accuracy: {:.6f}".format(c["accuracy"]),
      "- best rewire accuracy: {:.6f}".format(max(c["rewire_accuracies"])),
      "- canonical information efficiency: {:.6f}".format(c["efficiency"]),
      "- best rewire information efficiency: {:.6f}".format(max(c["rewire_efficiencies"])),
      "- canonical mean TEST transition entropy: {:.6f}".format(c["branch_entropy"]),
      "- exact chance p: {:.8g}".format(c["chance_p"]),"",
      "## Branching-matched controls","",
      "- matched rewire IDs: {}".format(", ".join(str(x) for x in c["branching_matched_ids"])),
      "- canonical exceeds all matched on both metrics: {}".format(c["beats_branch_matched"]),"",
      "## Developmental contribution","",
      "- FULL accuracy: {:.6f}".format(dev["full_accuracy"]),
      "- BLANK accuracy: {:.6f}".format(dev["blank_accuracy"]),
      "- per-probe paired p: {:.8g}".format(dev["accuracy_p"]),
      "- FULL efficiency: {:.6f}".format(dev["full_efficiency"]),
      "- BLANK efficiency: {:.6f}".format(dev["blank_efficiency"]),
      "- bootstrap 99% CI FULL-BLANK efficiency: [{:.6f}, {:.6f}]".format(dev["efficiency_bootstrap"]["lo"],dev["efficiency_bootstrap"]["hi"]),
      "- developmental communication contribution: **{}**".format("PASS" if dev["held"] else "FAIL"),"",
      "## Interpretation","",result["interpretation"],"",
      "This is a computational address/reply assay. It does not establish an external source or entity.",""]
    return "\n".join(lines)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",default="experiments/p321/results"); args=ap.parse_args()
    os.makedirs(args.out,exist_ok=True)
    existing=os.path.join(args.out,"summary.json")
    if os.path.exists(existing):
        print(open(existing,encoding="utf-8").read()); return 0

    probes=[probe(i) for i in range(PROBES)]
    rows=develop_canonical()
    raw_path=os.path.join(args.out,"responses.jsonl.gz")
    with gzip.open(raw_path,"wt",encoding="utf-8") as raw:
        full_bases=[copy.deepcopy(r["full"]) for r in rows]
        full_eval,full_resp=eval_controller("CANONICAL_FULL",full_bases,probes,raw)

        blank_bases=[]
        for r in rows:
            b=copy.deepcopy(r["full"]); b.memory=IntegratedMemorySystem(); b.deformation_tensor=[0.1]*10; blank_bases.append(b)
        blank_eval,blank_resp=eval_controller("CANONICAL_BLANK",blank_bases,probes,raw)

        revals=[]
        for rid in range(REWIRES):
            gates=p317.rewired_gates(REWIRE_BASE+rid)
            permeability=p317.original_gate_permeability(gates)
            bases=[]
            for i,r in enumerate(rows):
                p=DynamicNumogramProcess(gates=gates,current_zone=r["seed"]%10)
                p317.run_dynamic_tape(p,r["dev"]); p317.shock_process(p,r["seed"],permeability); bases.append(p)
            ev,_=eval_controller("R{:02d}".format(rid),bases,probes,raw)
            revals.append(ev)

    rew_acc=[x["decoder"]["accuracy"] for x in revals]
    rew_eff=[x["info"]["E"] for x in revals]
    rank_acc=(1+sum(1 for x in rew_acc if x>=full_eval["decoder"]["accuracy"]))/(REWIRES+1)
    rank_eff=(1+sum(1 for x in rew_eff if x>=full_eval["info"]["E"]))/(REWIRES+1)
    nearest=sorted(range(REWIRES),key=lambda i:(abs(revals[i]["branch_entropy"]-full_eval["branch_entropy"]),i))[:8]
    beats_match=all(full_eval["decoder"]["accuracy"]>rew_acc[i] and full_eval["info"]["E"]>rew_eff[i] for i in nearest)
    chance_p=exact_binom_upper(full_eval["decoder"]["n"],full_eval["decoder"]["correct"],1/PROBES)
    canonical_held=(all(full_eval["decoder"]["accuracy"]>x for x in rew_acc) and
                    all(full_eval["info"]["E"]>x for x in rew_eff) and beats_match and chance_p<=.01)

    diffs=[a-b for a,b in zip(full_eval["decoder"]["per_probe_accuracy"],blank_eval["decoder"]["per_probe_accuracy"])]
    acc_p=signflip(diffs,TEST_BASE,True)
    boot=bootstrap_eff_diff(full_resp,full_eval["vocab"],blank_resp,blank_eval["vocab"])
    boot_excludes=boot["lo"]>0 or boot["hi"]<0
    dev_held=acc_p<=.01 and boot_excludes

    atlas=canonical_atlas(full_resp,full_eval["vocab"])
    if canonical_held:
        interp="After equalizing reply vocabulary capacity and normalizing by reply entropy, the canonical Numogram carries more held-out probe identity than all 32 degree-preserving rewires."
    else:
        interp="The canonical Numogram does not satisfy the registered repertoire-controlled communication-privilege gate."
    if dev_held:interp+=" Development itself changes held-out communication discrimination relative to the matched blank state."
    else:interp+=" Development does not satisfy the registered communication-discrimination contribution gate."

    result={
      "schema":"amelia-p321-communication-efficacy-v1",
      "canonical":{
        "held":canonical_held,
        "accuracy":full_eval["decoder"]["accuracy"],"correct":full_eval["decoder"]["correct"],
        "efficiency":full_eval["info"]["E"],"mutual_information":full_eval["info"]["I"],"reply_entropy":full_eval["info"]["H"],
        "branch_entropy":full_eval["branch_entropy"],"chance_p":chance_p,
        "rewire_accuracies":rew_acc,"rewire_efficiencies":rew_eff,
        "rewire_branch_entropies":[x["branch_entropy"] for x in revals],
        "accuracy_rank_p":rank_acc,"efficiency_rank_p":rank_eff,
        "branching_matched_ids":nearest,"beats_branch_matched":beats_match
      },
      "development":{
        "held":dev_held,"full_accuracy":full_eval["decoder"]["accuracy"],"blank_accuracy":blank_eval["decoder"]["accuracy"],
        "accuracy_mean_difference":statistics.mean(diffs),"accuracy_p":acc_p,
        "full_efficiency":full_eval["info"]["E"],"blank_efficiency":blank_eval["info"]["E"],
        "efficiency_bootstrap":boot
      },
      "canonical_vocab":full_eval["vocab"],
      "atlas":atlas,
      "rewires":[{"id":i,"accuracy":x["decoder"]["accuracy"],"efficiency":x["info"]["E"],"branch_entropy":x["branch_entropy"]} for i,x in enumerate(revals)],
      "interpretation":interp,
      "provenance":{
        "registration_sha256":sha256_file("experiments/p321/REGISTRATION.md"),
        "amendment_sha256":sha256_file("experiments/p321/AMENDMENT_1.md"),
        "runner_sha256":sha256_file("experiments/p321/run.py"),
        "engine_sha256":sha256_file("experiments/p316/DynamicNumogram.py"),
        "raw_sha256":sha256_file(raw_path)
      }
    }
    with open(existing,"w",encoding="utf-8") as h:json.dump(result,h,indent=2,sort_keys=True)
    with open(os.path.join(args.out,"ATLAS.md"),"w",encoding="utf-8") as h:
        h.write("# P3.21 — Held-out Canonical Address / Reply Atlas\n\n")
        for x in atlas:
            h.write("## Probe {:02d}\n\n- motif: {}\n- TRAIN prevalence: {:.4f}\n- TEST prevalence: {:.4f}\n- TEST log-odds: {:.6f}\n".format(x["probe_id"],x["motif"],x["train_prevalence"],x["test_prevalence"],x["log_odds"]))
            for z in x["lineages"]:h.write("- {}: {}\n".format(z["lineage"],", ".join(map(str,z["starts"]))))
            h.write("\n")
    with open(os.path.join(args.out,"REPORT.md"),"w",encoding="utf-8") as h:h.write(report(result))
    print(json.dumps({"canonical":result["canonical"],"development":result["development"],"interpretation":interp},indent=2,sort_keys=True))
    return 0

if __name__=="__main__":raise SystemExit(main())
