#!/usr/bin/env python3
"""WARP-T1 — first natural Warp-entry transformation decomposition."""
from __future__ import annotations
import argparse, copy, hashlib, importlib.util, json, math, os, random, statistics, sys
from typing import Dict, List, Sequence, Tuple

ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
if ROOT not in sys.path: sys.path.insert(0,ROOT)
P316=os.path.join(ROOT,"experiments","p316")
if P316 not in sys.path: sys.path.insert(0,P316)
from DynamicNumogram import DynamicNumogramProcess, evolve_trait_step

P317_PATH=os.path.join(ROOT,"experiments","p317","run.py")
spec=importlib.util.spec_from_file_location("p317_frozen",P317_PATH)
p317=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(p317)

N=240; SEED_BASE=3200000; DRAWS=50000; PERM_SEED=3204000
OFFSETS=(0,1,2,4,8,16,32)
COMPONENTS=("hysteresis","strain_mass","strain_entropy","bias_mag","tensor_norm","governor_tension","activation_hhi","warp_activation_diff","warp_phase_coherence")

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def entropy(vals):
    xs=[max(0.0,float(x)) for x in vals]; s=sum(xs)
    if s<=0:return 0.0
    return -sum((x/s)*math.log(x/s,2) for x in xs if x>0)

def metrics(p):
    r=p.memory.read_memory_bias()
    acts=[float(p.zones[i]["activation"]) for i in range(10)]
    asum=sum(acts); hhi=sum((x/asum)**2 for x in acts) if asum else 0.0
    a3,a6=float(p.zones[3]["activation"]),float(p.zones[6]["activation"])
    ph3,ph6=float(p.zones[3]["phaseAngle"]),float(p.zones[6]["phaseAngle"])
    return {
      "hysteresis":float(r.hysteresis_tension),
      "strain_mass":sum(float(x) for x in p.memory.zone_strain_history),
      "strain_entropy":entropy(p.memory.zone_strain_history),
      "bias_mag":statistics.mean(abs(float(x)) for x in r.bias_vector),
      "tensor_norm":math.sqrt(sum(float(x)**2 for x in p.deformation_tensor)),
      "governor_tension":float(p.governor.telemetry()["deformationFieldTension"]),
      "activation_hhi":hhi,
      "warp_activation_diff":abs(a3-a6),
      "warp_phase_coherence":(1.0+math.cos(ph3-ph6))/2.0,
    }

def prepare(p,input_zone):
    p.step_count+=1
    gov=p.governor.telemetry(); mem=p.memory.read_memory_bias()
    bias=list(mem.bias_vector) if p.pfm_feedback else [0.0]*10
    p.last_trait_snapshot=evolve_trait_step(p.zones,p.gates,float(gov["momentumDampingFactor"]),float(gov["advisoryWeight"]),bias,False)
    p.last_audit=p.governor.audit(p.zones,mem.hysteresis_tension,False)
    source=p.current_zone
    opts=[g for g in p.gates if bool(g["isOpen"]) and int(g["source"])==source]
    scored=[]
    for g in opts:
        t=int(g["target"]); z=p.zones[t]
        score=float(g["flux"])*(1.0-float(g["resistance"]))+bias[t]*.4+float(z["activation"])*.2+math.cos(float(z["phaseAngle"]))*.1+(0.35 if input_zone is not None and t==int(input_zone) else 0.0)
        scored.append((score,t,g))
    scored.sort(key=lambda x:x[0],reverse=True)
    return source,scored,bias,mem

def finalize(p,input_zone,source,target,bias,mem,mode="normal"):
    tz,sz=p.zones[target],p.zones[source]
    flux=round(max(.005,min(.18,abs(float(tz["activation"])-float(sz["activation"]))*.12+.025)),6)
    coh=round(max(.05,min(1.0,(1.0+math.cos(float(tz["phaseAngle"])-float(sz["phaseAngle"])))/2.0)),6)
    store_flux,store_coh=flux,coh
    if mode=="topology_only":
        store_flux=0.0; store_coh=float(mem.mean_phase_coherence)
    p.memory.append({"blockIndex":p.step_count,"depth":p.step_count,"targetZone":target,"fluxDelta":store_flux,"phaseCoherence":store_coh,"strainRelaxation":.025,"eventDigest":"warp-t1:{}:{}:{}:{}".format(p.step_count,source,target,mode),"timestamp":p.step_count,"kind":"STEP","fromZone":source,"inputZone":input_zone})
    actual=source if mode=="inscription_only" else target
    p.current_zone=actual; p.zone_visit_counts[actual]+=1; p.transition_counts[source][actual]+=1
    for i in range(10):
        z=p.zones[i]; p.deformation_tensor[i]=p.deformation_tensor[i]*.95+(float(z["deformationStress"])+bias[i])*.05
    return {"source":source,"target":target,"actual":actual,"flux":flux,"coherence":coh}

def forced_step(p,input_zone,target=None,mode="normal",nonwarp=False):
    source,scored,bias,mem=prepare(p,input_zone)
    if target is None:
        choices=[x for x in scored if (x[1] not in (3,6) if nonwarp else True)]
        if not choices: raise RuntimeError("no eligible target")
        target=choices[0][1]
    return finalize(p,input_zone,source,int(target),bias,mem,mode)

def open_warp_after_entry(p):
    i36=next(i for i,g in enumerate(p.gates) if int(g["source"])==3 and int(g["target"])==6)
    i41=next(i for i,g in enumerate(p.gates) if int(g["source"])==4 and int(g["target"])==1)
    p.gates[i36]["target"]=1; p.gates[i41]["target"]=6

def first_entry(seed):
    dev,post=p317.make_tapes(seed); tape=dev+post
    p=DynamicNumogramProcess(current_zone=seed%10)
    for idx,sym in enumerate(tape):
        before=copy.deepcopy(p); source=p.current_zone
        out=p.step(int(sym)); target=int(out["to_zone"])
        if source not in (3,6) and target in (3,6):
            # matched alternative must exist under exact pre-entry state
            probe=copy.deepcopy(before); s,sc,b,m=prepare(probe,int(sym))
            if not any(t not in (3,6) for _,t,_ in sc): return None
            return {"index":idx,"input":int(sym),"target":target,"pre":before,"remaining":tape[idx+1:idx+33]}
    return None

def run_clone(pre,input_zone,target,remaining,kind):
    p=copy.deepcopy(pre); base=metrics(p)
    if kind=="real":
        forced_step(p,input_zone,target,"normal")
    elif kind=="topology":
        forced_step(p,input_zone,target,"topology_only")
    elif kind=="inscription":
        forced_step(p,input_zone,target,"inscription_only")
    elif kind=="matched":
        forced_step(p,input_zone,None,"normal",True)
    elif kind=="open":
        forced_step(p,input_zone,target,"normal"); open_warp_after_entry(p)
    else: raise ValueError(kind)
    snap={0:metrics(p)}; zones=[p.current_zone]
    for k,sym in enumerate(remaining,1):
        p.step(int(sym)); zones.append(p.current_zone)
        if k in OFFSETS: snap[k]=metrics(p)
    alt=0; longest=0; cur=0; prev=None
    for z in zones[1:]:
        if z in (3,6) and prev in (3,6) and z!=prev: cur+=1
        elif z in (3,6): cur=1
        else: cur=0
        longest=max(longest,cur); prev=z
    trans=sum(1 for a,b in zip(zones,zones[1:]) if a in (3,6) and b in (3,6) and a!=b)
    occ=sum(1 for z in zones[1:] if z in (3,6))/max(1,len(zones)-1)
    return {"baseline":base,"snap":snap,"warp_occupancy":occ,"alternating_run":longest,"warp_transitions":trans,"distinct_zones":len(set(zones))}

def signflip_p(diffs,seed,one_sided=True):
    obs=statistics.mean(diffs) if diffs else 0.0
    rng=random.Random(seed); ge=0
    for _ in range(DRAWS):
        m=statistics.mean(d*(1 if rng.random()<.5 else -1) for d in diffs)
        if (m>=obs-1e-15 if one_sided else abs(m)>=abs(obs)-1e-15): ge+=1
    return (ge+1)/(DRAWS+1)

def holm(raw):
    ordered=sorted(raw.items(),key=lambda kv:(kv[1],kv[0])); m=len(ordered); out={}; running=0
    for i,(k,p) in enumerate(ordered):
        running=max(running,min(1.0,(m-i)*p)); out[k]=running
    return out

def multivar(real,matched):
    ds=[]
    for r,m in zip(real,matched):
        ds.append([ (r["snap"][0][c]-r["baseline"][c])-(m["snap"][0][c]-m["baseline"][c]) for c in COMPONENTS])
    sds=[]
    for j in range(len(COMPONENTS)):
        col=[d[j] for d in ds]; sds.append(statistics.stdev(col) if len(col)>1 and statistics.stdev(col)>0 else 0.0)
    def stat(signs=None):
        total=0.0
        for j,sd in enumerate(sds):
            if sd<=0: continue
            vals=[d[j]*(1 if signs is None else signs[i]) for i,d in enumerate(ds)]
            total+=(statistics.mean(vals)/sd)**2
        return total
    obs=stat(); rng=random.Random(PERM_SEED); ge=0
    for _ in range(DRAWS):
        signs=[1 if rng.random()<.5 else -1 for _ in ds]
        if stat(signs)>=obs-1e-15: ge+=1
    indiv={}
    for j,c in enumerate(COMPONENTS):
        diffs=[d[j] for d in ds]; indiv[c]={"mean_difference":statistics.mean(diffs),"p_two_sided":signflip_p(diffs,3204100+j,False)}
    adj=holm({c:v["p_two_sided"] for c,v in indiv.items()})
    for c in indiv: indiv[c]["holm_p"]=adj[c]
    return {"T":obs,"p":(ge+1)/(DRAWS+1),"components":indiv}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",default="experiments/warp_t1/results"); args=ap.parse_args(); os.makedirs(args.out,exist_ok=True)
    if os.path.exists(os.path.join(args.out,"summary.json")):
        print(open(os.path.join(args.out,"summary.json"),encoding="utf-8").read()); return 0
    rows=[]
    for i in range(N):
        seed=SEED_BASE+i; e=first_entry(seed)
        if e is None: rows.append({"seed":seed,"eligible":False}); continue
        arms={k:run_clone(e["pre"],e["input"],e["target"],e["remaining"],k) for k in ("real","topology","inscription","matched","open")}
        rows.append({"seed":seed,"eligible":True,"entry_step":e["index"],"source":e["pre"].current_zone,"target":e["target"],"arms":arms})
    eligible=[x for x in rows if x["eligible"]]
    R=[x["arms"]["real"] for x in eligible]; T=[x["arms"]["topology"] for x in eligible]; I=[x["arms"]["inscription"] for x in eligible]; M=[x["arms"]["matched"] for x in eligible]; O=[x["arms"]["open"] for x in eligible]
    mv=multivar(R,M)
    entry_claim=mv["p"]<=.01 and any(v["holm_p"]<=.05 for v in mv["components"].values())

    occ_rt=[r["warp_occupancy"]-t["warp_occupancy"] for r,t in zip(R,T)]
    p_rt=signflip_p(occ_rt,3205000,True)
    slow={}
    for j,c in enumerate(("hysteresis","strain_mass")):
        d=[(i["snap"][32][c]-i["baseline"][c])-(m["snap"][32][c]-m["baseline"][c]) for i,m in zip(I,M)]
        slow[c]={"mean_difference":statistics.mean(d),"p":signflip_p(d,3205001+j,True)}
    sadj=holm({k:v["p"] for k,v in slow.items()})
    for k in slow: slow[k]["holm_p"]=sadj[k]
    ins_claim=(holm({"occupancy":p_rt,"slow_min":min(v["p"] for v in slow.values())})["occupancy"]<=.05 and any(v["holm_p"]<=.05 for v in slow.values()))

    d_occ=[r["warp_occupancy"]-o["warp_occupancy"] for r,o in zip(R,O)]
    d_alt=[r["alternating_run"]-o["alternating_run"] for r,o in zip(R,O)]
    p_occ=signflip_p(d_occ,3205100,True); p_alt=signflip_p(d_alt,3205101,True)
    terminal=p_occ<=.01 and p_alt<=.01

    summary={"schema":"amelia-warp-t1-v1","eligible_lineages":len(eligible),"total_lineages":N,
      "entry_transformation":{"held":entry_claim,"multivariate":mv},
      "inscription":{"held":ins_claim,"real_minus_topology_occupancy_mean":statistics.mean(occ_rt),"real_vs_topology_p":p_rt,"slow_state":slow},
      "terminality":{"held":terminal,"real_minus_open_occupancy_mean":statistics.mean(d_occ),"occupancy_p":p_occ,"real_minus_open_alternating_run_mean":statistics.mean(d_alt),"alternating_p":p_alt},
      "arm_means":{k:{"warp_occupancy":statistics.mean(x["arms"][k]["warp_occupancy"] for x in eligible),"alternating_run":statistics.mean(x["arms"][k]["alternating_run"] for x in eligible),"distinct_zones":statistics.mean(x["arms"][k]["distinct_zones"] for x in eligible)} for k in ("real","topology","inscription","matched","open")},
      "rows":rows,
      "provenance":{"registration_sha256":sha256_file("experiments/warp_t1/REGISTRATION.md"),"amendment_sha256":sha256_file("experiments/warp_t1/AMENDMENT_1.md"),"runner_sha256":sha256_file("experiments/warp_t1/run.py"),"engine_sha256":sha256_file("experiments/p316/DynamicNumogram.py")}}
    with open(os.path.join(args.out,"summary.json"),"w",encoding="utf-8") as f:json.dump(summary,f,indent=2,sort_keys=True)
    report=[
      "# WARP-T1 — Warp Entry / Passage Transformation Result","",
      "- eligible first-entry lineages: {}/{}".format(len(eligible),N),
      "- entry-transformation claim: **{}**".format("PASS" if entry_claim else "FAIL"),
      "- inscription contribution: **{}**".format("PASS" if ins_claim else "FAIL"),
      "- terminality contribution: **{}**".format("PASS" if terminal else "FAIL"),
      "- multivariate entry p: {:.8g}".format(mv["p"]),
      "- REAL minus TOPOLOGY_ONLY 32-step Warp occupancy: {:.6f}, p={:.8g}".format(statistics.mean(occ_rt),p_rt),
      "- REAL minus WARP_OPEN occupancy: {:.6f}, p={:.8g}".format(statistics.mean(d_occ),p_occ),
      "- REAL minus WARP_OPEN alternating-run: {:.6f}, p={:.8g}".format(statistics.mean(d_alt),p_alt),"",
      "## Immediate components",""
    ]
    for c,v in mv["components"].items(): report.append("- {}: mean Δ={:.8g}, Holm p={:.8g}".format(c,v["mean_difference"],v["holm_p"]))
    report += ["","## Interpretation","",
      ("Warp entry produces a measurable immediate state transformation. " if entry_claim else "No registered multivariate immediate-entry transformation was established. ")+
      ("Entry inscription contributes beyond topology. " if ins_claim else "The entry-event inscription was not shown to add canalization beyond topology. ")+
      ("Canonical terminality is a causal contributor to 3::6 canalization." if terminal else "Canonical terminality did not satisfy its causal contribution gate."),""]
    with open(os.path.join(args.out,"REPORT.md"),"w",encoding="utf-8") as f:f.write("\n".join(report))
    print(json.dumps({k:summary[k] for k in ("eligible_lineages","entry_transformation","inscription","terminality","arm_means")},indent=2,sort_keys=True))
    return 0

if __name__=="__main__": raise SystemExit(main())
