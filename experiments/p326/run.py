#!/usr/bin/env python3
"""P3.26 sealed graph-field assay."""
from __future__ import annotations
import copy,gzip,hashlib,importlib.util,json,math,os,random,statistics,sys
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
P316=ROOT/"experiments/p316"; P317=ROOT/"experiments/p317"; P326=ROOT/"experiments/p326"
for p in (ROOT,P316,P317,P326): sys.path.insert(0,str(p))
from DynamicNumogram import DynamicNumogramProcess
from atlas import CreateOnlyAtlas,verify
from graph_field import packet_from_randomness
from runner import run_encounters

N=96; LBASE=3260000; R=24; RBASE=3263000; CALLS=24; RELEASE=24; SHUFFLE_SEED=3264000
BOOT_SEED=3267000; BOOT_DRAWS=5000

def load_p317():
    spec=importlib.util.spec_from_file_location("p317_frozen",P317/"run.py")
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def load_beacon():
    d=json.loads((P326/"results/BEACON.json").read_text())
    seal=(P326/"SEALED_REGISTRATION_SHA.txt").read_text().strip()
    if d.get("schema")!="amelia-p326-drand-field-v1" or d.get("sealed_registration_sha")!=seal: raise ValueError("beacon/registration mismatch")
    if len(d.get("rounds",[]))!=CALLS: raise ValueError("requires 24 beacon records")
    packets=[]
    for i,row in enumerate(d["rounds"]):
        if int(row["packet_index"])!=i or (i and int(row["round"])!=int(d["rounds"][i-1]["round"])+1): raise ValueError("packet order invalid")
        rand=str(row["randomness"]).lower()
        if hashlib.sha256(bytes.fromhex(row["signature"])).hexdigest()!=rand: raise ValueError("randomness digest mismatch")
        packet=packet_from_randomness(rand,i)
        if any(abs(a-float(b))>2e-15 for a,b in zip(packet,row["field"])): raise ValueError("packet mapping mismatch")
        if abs(sum(packet))>1e-12 or abs(math.sqrt(sum(x*x for x in packet))-1)>1e-12: raise ValueError("packet normalization mismatch")
        packets.append(packet)
    return d,packets

def boot(values,seed):
    rng=random.Random(seed); n=len(values)
    if not n:return [None,None,None]
    means=[]
    for _ in range(BOOT_DRAWS): means.append(statistics.mean(values[rng.randrange(n)] for _ in range(n)))
    means.sort()
    return [statistics.mean(values),means[int(.025*(BOOT_DRAWS-1))],means[int(.975*(BOOT_DRAWS-1))]]

def route_features(rec):
    v=[0.0]*100
    for t in rec["withdrawal_transitions"]: v[int(t["from_zone"])*10+int(t["to_zone"])]+=1
    return [x/24 for x in v]

def motif_set(rec):
    t=rec["graph_field"]["transition"]
    path=[int(t["from_zone"]),int(t["to_zone"])]
    path.extend(int(x["to_zone"]) for x in rec["withdrawal_transitions"])
    out=set()
    for n in range(2,6):
        out.update(tuple(path[i:i+n]) for i in range(len(path)-n+1))
    return out

def main():
    out=P326/"results"; out.mkdir(parents=True,exist_ok=True)
    atlas_path=out/"ATLAS.jsonl.gz"
    if atlas_path.exists(): raise FileExistsError("create-only atlas already exists")
    beacon,packets=load_beacon(); p317=load_p317()
    canonical=p317.FULL_NUMOGRAM_GATES
    sig=p317.degree_signature(canonical); loops=p317.self_loop_count(canonical)
    rewires=[p317.rewired_gates(RBASE+i) for i in range(R)]
    for g in rewires:
        if p317.degree_signature(g)!=sig or p317.self_loop_count(g)!=loops: raise AssertionError("rewire invariant failed")
    rng=random.Random(SHUFFLE_SEED); perm=list(range(10)); rng.shuffle(perm)
    if perm==list(range(10)): perm=perm[1:]+perm[:1]
    metadata={"schema":"amelia-p326-run-metadata-v1","registration_sha":beacon["sealed_registration_sha"],
      "beacon_sha256":sha(out/"BEACON.json"),"lineage_seeds":[LBASE+i for i in range(N)],
      "rewire_seeds":[RBASE+i for i in range(R)],"relation_permutation":perm,"calls":CALLS,"release_steps":RELEASE}
    (out/"RUN_METADATA.json").write_text(json.dumps(metadata,indent=2,sort_keys=True)+"\n")
    with CreateOnlyAtlas(str(atlas_path)) as atlas:
        for i in range(N):
            seed=LBASE+i; dev,_=p317.make_tapes(seed)
            base=DynamicNumogramProcess(current_zone=seed%10)
            p317.run_dynamic_tape(base,dev)
            p317.shock_process(base,seed,p317.original_gate_permeability(base.gates))
            baseline={(a,b) for a,row in enumerate(base.transition_counts) for b,count in enumerate(row) if count>0}
            fixed=copy.deepcopy(base.gates); lid="P326-{:03d}".format(i)
            arms=[("CANONICAL_LIVE","canonical_live",base.gates),
                  ("CANONICAL_FIXED","canonical_fixed",fixed),
                  ("RELATION_SHUFFLED","relation_shuffled",base.gates),
                  ("NO_FIELD","no_field",base.gates),
                  ("PFM_FEEDBACK_MUTED","pfm_feedback_muted",base.gates)]
            for name,mode,gates in arms:
                run_encounters(base,packets,mode,name,gates,atlas,lid,RELEASE,baseline,perm)
            for j,gates in enumerate(rewires):
                name="R{:02d}".format(j)
                run_encounters(base,packets,"degree_rewired",name,gates,atlas,lid,RELEASE,baseline,perm)
    verify(str(atlas_path))
    total_records=0
    discovery=defaultdict(lambda:{"lineages":set(),"encounters":0})
    with gzip.open(atlas_path,"rt",encoding="utf-8") as f:
        for line in f:
            x=json.loads(line); total_records+=1
            name=x["controller_id"]; idx=int(x["lineage_id"].split("-")[-1])
    nofield={}
    with gzip.open(atlas_path,"rt",encoding="utf-8") as f:
        for line in f:
            x=json.loads(line)
            if x["controller_id"]=="NO_FIELD":
                nofield[(x["lineage_id"],x["encounter_index"])]=x
    ctrl=defaultdict(list)
    with gzip.open(atlas_path,"rt",encoding="utf-8") as f:
        for line in f:
            x=json.loads(line)
            name=x["controller_id"]; idx=int(x["lineage_id"].split("-")[-1])
            no=nofield[(x["lineage_id"],x["encounter_index"])]
            a=route_features(x); b=route_features(no)
            tv=.5*sum(abs(y-z) for y,z in zip(a,b))
            baseline={tuple(e) for e in x["development_transition_edges"]}
            trans={(int(t["from_zone"]),int(t["to_zone"])) for t in x["withdrawal_transitions"]}
            tr=x["graph_field"]["transition"]; trans.add((int(tr["from_zone"]),int(tr["to_zone"])))
            before=x["pre_pfm_state"]; after=x["pfm_state_after"]
            strain=sum(abs(float(z)-float(y)) for y,z in zip(before["zone_strain_history"],after["zone_strain_history"]))
            ctrl[name].append({"lineage":idx,"tv":tv,"novel":len(trans-baseline)/max(1,len(trans)),
                "hysteresis_delta":float(after["hysteresis_tension"])-float(before["hysteresis_tension"]),
                "strain_l1":strain})
            if name=="CANONICAL_LIVE" and idx<48 and int(x["encounter_index"])<12:
                for m in motif_set(x):
                    key=",".join(map(str,m)); discovery[key]["lineages"].add(idx); discovery[key]["encounters"]+=1
    expected=N*CALLS*(5+R)
    if total_records!=expected: raise ValueError("atlas record count mismatch")
    metrics={}
    for name,rows in ctrl.items():
        by=defaultdict(list)
        for row in rows: by[row["lineage"]].append(row)
        lineage_tv=[statistics.mean(r["tv"] for r in vals) for vals in by.values()]
        ci=boot(lineage_tv,BOOT_SEED+sum(map(ord,name)))
        metrics[name]={"mean_transition_TV_vs_no_field":ci[0],"lineage_bootstrap_95pct_CI":ci[1:],
          "train_mean_TV":statistics.mean(r["tv"] for r in rows if r["lineage"]<48),
          "held_out_mean_TV":statistics.mean(r["tv"] for r in rows if r["lineage"]>=48),
          "mean_novel_transition_fraction":statistics.mean(r["novel"] for r in rows),
          "mean_PFM_hysteresis_delta":statistics.mean(r["hysteresis_delta"] for r in rows),
          "mean_PFM_strain_L1_delta":statistics.mean(r["strain_l1"] for r in rows),"records":len(rows)}
    chosen={k for k,v in discovery.items() if v["encounters"]>=12 and len(v["lineages"])>=8}
    held=defaultdict(lambda:{"lineages":set(),"encounters":0})
    if chosen:
        with gzip.open(atlas_path,"rt",encoding="utf-8") as f:
            for line in f:
                x=json.loads(line); name=x["controller_id"]
                idx=int(x["lineage_id"].split("-")[-1]); call=int(x["encounter_index"])
                if idx<48 or call<12: continue
                for m in motif_set(x):
                    key=",".join(map(str,m))
                    if key in chosen:
                        held[(key,name)]["lineages"].add(idx); held[(key,name)]["encounters"]+=1
    candidates=[]
    for key in sorted(chosen,key=lambda s:tuple(map(int,s.split(",")))):
        v=discovery[key]; row={"motif":[int(x) for x in key.split(",")],
          "discovery_lineages":len(v["lineages"]),"discovery_encounters":v["encounters"],
          "held_out_by_controller":{}}
        for name in metrics:
            score=held[(key,name)]
            row["held_out_by_controller"][name]={"lineages":len(score["lineages"]),"encounters":score["encounters"]}
        candidates.append(row)
    result={"schema":"amelia-p326-exploratory-summary-v1","records":total_records,
       "controllers":metrics,"candidate_motif_count":len(candidates),"candidate_motifs":candidates,
       "atlas_head_sha256":verify(str(atlas_path)),
       "provenance":{"registration_sha256":sha(P326/"REGISTRATION.md"),
        "graph_field_sha256":sha(P326/"graph_field.py"),"runner_sha256":sha(P326/"runner.py"),
        "atlas_sha256":sha(atlas_path),"p316_sha256":sha(P316/"DynamicNumogram.py"),
        "p317_sha256":sha(P317/"run.py")}}
    (out/"SUMMARY.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    lines=["# P3.26 — Numogram Graph-Field Morphogenetic Uptake","",
      "Registered exploratory mapping. No pass/fail or ontological verdict is assigned.","",
      "## Coverage","",
      "- Verified fresh public-randomness packets: 24","- Fresh lineages: 96 (48 TRAIN, 48 HELD-OUT)",
      "- Controllers: 5 matched conditions and 24 degree-preserving field rewires",
      "- Hash-chained encounter records: {}".format(total_records),
      "- Candidate motifs meeting discovery threshold: {}".format(len(candidates)),"",
      "## Controller summaries","","| Controller | Mean transition TV from NO_FIELD | Lineage-bootstrap 95% CI | Novel transition fraction | PFM hysteresis delta |",
      "|---|---:|---:|---:|---:|"]
    for name,m in metrics.items():
        ci=m["lineage_bootstrap_95pct_CI"]
        lines.append("| {} | {:.6f} | [{:.6f}, {:.6f}] | {:.6f} | {:+.6f} |".format(
          name,m["mean_transition_TV_vs_no_field"],ci[0],ci[1],
          m["mean_novel_transition_fraction"],m["mean_PFM_hysteresis_delta"]))
    lines += ["","## Interpretation boundary","",
      "Candidate motifs were discovered in canonical-live TRAIN traces from packets 0–11 and counted unchanged in held-out lineages and packets 12–23. The archive retains all traces, including null and nonrecurring responses. Recurrence is a substrate-path observation and remains a candidate for later query-contingent discrimination.",""]
    (out/"REPORT.md").write_text("\n".join(lines))
    print(json.dumps({"records":total_records,"candidate_motifs":len(candidates),
      "controllers":metrics,"atlas_head_sha256":result["atlas_head_sha256"],
      "interpretation":"exploratory mapping; no pass/fail"},indent=2,sort_keys=True))

if __name__=="__main__": main()
