"""
OUTSIDE-1 v2.1 Publication Series working runner.
Prospective event-envelope ledger for W007-W106.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import sys
from typing import Sequence

HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE)
import Outside1_v2 as O
import Outside1_v2_1 as P

SCHEMA_VERSION="outside1-publication-evidence-v1"


def entries():
    if not os.path.exists(P.LEDGER):
        return []
    with open(P.LEDGER,encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def verify_chain():
    parent="0"*64
    seq=0
    for e in entries():
        seq+=1
        if e.get("event_seq")!=seq: return False
        if e.get("parent_event_hash")!=parent: return False
        payload=e.get("payload")
        if e.get("payload_sha256")!=P.sha(payload): return False
        body={k:v for k,v in e.items() if k!="event_hash"}
        if e.get("event_hash")!=P.sha(body): return False
        parent=e["event_hash"]
    return True


def _event(event_type,working_id,payload):
    P.calibration_open()
    if not verify_chain(): raise RuntimeError("publication ledger chain invalid")
    es=entries()
    seq=len(es)+1
    parent=es[-1]["event_hash"] if es else "0"*64
    reg=P.load_registration()
    e={
        "schema_version":SCHEMA_VERSION,
        "series_id":P.SERIES_ID,
        "event_seq":seq,
        "event_id":"%s.%06d.%s"%(working_id,seq,event_type.upper()),
        "event_type":event_type,
        "working_id":working_id,
        "created_utc":P.utc_now(),
        "serialization":P.SERIALIZATION,
        "protocol_sha256":P.PROTOCOL_SHA256,
        "registration_sha256":reg["registration_sha256"],
        "parent_event_hash":parent,
        "payload_sha256":P.sha(payload),
        "payload":payload,
    }
    e["event_hash"]=P.sha(e)
    with open(P.LEDGER,"a",encoding="utf-8") as f:
        f.write(P.canonical_json(e)+"\n")
    return e


def find(event_type,working_id,slot=None):
    for e in entries():
        if e["event_type"]==event_type and e["working_id"]==working_id:
            if slot is None or e["payload"].get("slot")==slot:
                return e
    return None


def wn(w):
    if not re.fullmatch(r"W\d{3}",w): raise ValueError("working format")
    n=int(w[1:])
    if not P.SERIES_START<=n<=P.SERIES_STOP:
        raise ValueError("working outside W007-W106")
    return n


def _require_order(w):
    n=wn(w)
    casts=[int(e["working_id"][1:]) for e in entries() if e["event_type"]=="cast"]
    if not casts and n!=P.SERIES_START: raise RuntimeError("first publication working must be W007")
    if casts and n!=max(casts)+1: raise RuntimeError("publication workings must be sequential")
    if n>P.SERIES_START and not find("resolved","W%03d"%(n-1)):
        raise RuntimeError("previous working not resolved")


def _slot_map(entropy_hex):
    if P.binary_choice(entropy_hex,":slot")==0:
        return {"R1":"canonical","R2":"null"}
    return {"R1":"null","R2":"canonical"}


def prepare(w,tosses):
    P.calibration_open()
    if not verify_chain(): raise RuntimeError("publication ledger chain invalid")
    _require_order(w)
    if find("cast",w): raise RuntimeError("already cast")
    n=wn(w)
    seed=O.seed_of(w,tosses)
    arms={}
    for arm in ("canonical","null"):
        tr=O.trace(O.graph(arm,n),seed)
        fr=O.deal(tr)
        arms[arm]={
            "trace":tr,
            "rawTraceDigest":P.channel_digest(tr),
            "fragments":fr,
            "fragmentDigest":P.channel_digest(fr),
        }

    slot_entropy=secrets.token_bytes(32).hex()
    slot_map=_slot_map(slot_entropy)
    judge_entropy={"R1":secrets.token_bytes(32).hex(),"R2":secrets.token_bytes(32).hex()}
    judge_orders={
        s:P.keyed_permutation4(judge_entropy[s],":judge-order:"+s) for s in ("R1","R2")
    }
    quartet=O.target_quartet(w)

    payload={
        "working_number":n,
        "input":{
            "question":O.PROTOCOL["question"],
            "tosses":tosses,
            "input_sha256":hashlib.sha256(tosses.encode("ascii")).hexdigest(),
            "seed":seed,
        },
        "runtime":{
            "canonical_runtime_digest":O.CANONICAL_DIGEST,
            "parent_protocol_sha256":O.PROTOCOL_SHA256,
            "publication_protocol_sha256":P.PROTOCOL_SHA256,
        },
        "arms":arms,
        "blind":{
            "slot_assignment_entropy_hex":slot_entropy,
            "slot_assignment_entropy_sha256":hashlib.sha256(bytes.fromhex(slot_entropy)).hexdigest(),
            "slot_map":slot_map,
            "judge_order_entropy_hex":judge_entropy,
            "judge_orders":judge_orders,
        },
        "quartet":quartet,
        "quartet_sha256":P.channel_digest(quartet),
    }
    ev=_event("cast",w,payload)
    public={"working":w,"cast_event_hash":ev["event_hash"],"slots":{}}
    for s in ("R1","R2"):
        arm=slot_map[s]
        fr=arms[arm]["fragments"]
        prompt=O.COMPOSE_PROMPT.format(
            fragments="\n".join("%d. %s"%(i+1,x["text"]) for i,x in enumerate(fr))
        )
        public["slots"][s]={
            "fragments":[x["text"] for x in fr],
            "fragmentDigest":arms[arm]["fragmentDigest"],
            "compose_prompt":prompt,
            "compose_prompt_sha256":hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        }
    return public


def seal_reading(w,slot,reading,method):
    if slot not in ("R1","R2"): raise ValueError(slot)
    P.validate_method(method)
    c=find("cast",w)
    if not c: raise RuntimeError("cast absent")
    if find("reading",w,slot): raise RuntimeError("reading already sealed")
    arm=c["payload"]["blind"]["slot_map"][slot]
    fr=[x["text"] for x in c["payload"]["arms"][arm]["fragments"]]
    for x in fr:
        if x not in reading: raise ValueError("reading omits dealt fragment")
    wc=len(re.findall(r"\b[\w’'-]+\b",reading))
    if not 90<=wc<=160: raise ValueError("reading word count %d"%wc)
    prompt=O.COMPOSE_PROMPT.format(
        fragments="\n".join("%d. %s"%(i+1,x) for i,x in enumerate(fr))
    )
    payload={
        "slot":slot,
        "source_cast_event_hash":c["event_hash"],
        "prompt":prompt,
        "prompt_sha256":hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "output":reading,
        "output_sha256":hashlib.sha256(reading.encode("utf-8")).hexdigest(),
        "word_count":wc,
        "method":method,
    }
    return _event("reading",w,payload)


def judge_material(w,slot):
    c=find("cast",w); r=find("reading",w,slot)
    if not c or not r: raise RuntimeError("cast/reading absent")
    order=c["payload"]["blind"]["judge_orders"][slot]
    quartet=c["payload"]["quartet"]
    labels="ABCD"
    candidates=[
        {"label":labels[k],"scene":quartet[idx]["text"],"pool_index":idx}
        for k,idx in enumerate(order)
    ]
    prompt=O.JUDGE_PROMPT.format(
        reading=r["payload"]["output"],
        candidates="\n".join("%s. %s"%(x["label"],x["scene"]) for x in candidates)
    )
    return {
        "working":w,"slot":slot,
        "reading_event_hash":r["event_hash"],
        "reading":r["payload"]["output"],
        "candidates":[{"label":x["label"],"scene":x["scene"]} for x in candidates],
        "judge_prompt":prompt,
        "judge_prompt_sha256":hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
    }


def seal_ranking(w,slot,ranking,method,raw_output):
    if slot not in ("R1","R2"): raise ValueError(slot)
    P.validate_method(method)
    c=find("cast",w); r=find("reading",w,slot)
    if not c or not r: raise RuntimeError("cast/reading absent")
    if find("ranking",w,slot): raise RuntimeError("ranking already sealed")
    ranking=list(ranking)
    if sorted(ranking)!=list("ABCD"): raise ValueError("bad ranking")
    jm=judge_material(w,slot)
    payload={
        "slot":slot,
        "source_reading_event_hash":r["event_hash"],
        "prompt":jm["judge_prompt"],
        "prompt_sha256":jm["judge_prompt_sha256"],
        "raw_output":raw_output,
        "raw_output_sha256":hashlib.sha256(raw_output.encode("utf-8")).hexdigest(),
        "ranking":ranking,
        "method":method,
    }
    return _event("ranking",w,payload)


def _rank_for_pool_index(c,slot,ranking,pool_index):
    order=c["payload"]["blind"]["judge_orders"][slot]
    label="ABCD"[order.index(pool_index)]
    return list(ranking).index(label)+1


def draw(w):
    if find("resolved",w): raise RuntimeError("already resolved")
    c=find("cast",w)
    rs={s:find("reading",w,s) for s in ("R1","R2")}
    ks={s:find("ranking",w,s) for s in ("R1","R2")}
    if not c or not all(rs.values()) or not all(ks.values()):
        raise RuntimeError("cast/readings/rankings must be sealed")
    pre_state={
        "cast":c["event_hash"],
        "readings":{s:rs[s]["event_hash"] for s in ("R1","R2")},
        "rankings":{s:ks[s]["event_hash"] for s in ("R1","R2")},
        "ledger_parent":entries()[-1]["event_hash"],
    }
    pre_digest=P.sha(pre_state)
    entropy=secrets.token_bytes(32).hex()
    target_index=P.target_choice(entropy)
    slot_ranks={
        s:_rank_for_pool_index(c,s,ks[s]["payload"]["ranking"],target_index)
        for s in ("R1","R2")
    }
    arm_ranks={c["payload"]["blind"]["slot_map"][s]:slot_ranks[s] for s in ("R1","R2")}
    payload={
        "pre_draw_state":pre_state,
        "pre_draw_state_sha256":pre_digest,
        "target_draw":{
            "entropy_hex":entropy,
            "entropy_sha256":hashlib.sha256(bytes.fromhex(entropy)).hexdigest(),
            "derivation":"int(SHA256(entropy || ':target-draw'), big-endian) mod 4",
            "target_index":target_index,
        },
        "slot_ranks":slot_ranks,
        "arm_ranks":arm_ranks,
        "target_scene":c["payload"]["quartet"][target_index]["text"],
    }
    ev=_event("resolved",w,payload)
    return {
        "working":w,
        "resolution_event_hash":ev["event_hash"],
        "target_scene":payload["target_scene"],
        "readings_unlabelled":{s:rs[s]["payload"]["output"] for s in ("R1","R2")},
    }


def status():
    es=entries()
    return {
        "series_id":P.SERIES_ID,
        "chain_ok":verify_chain(),
        "workings_cast":sum(e["event_type"]=="cast" for e in es),
        "workings_resolved":sum(e["event_type"]=="resolved" for e in es),
        "next_working":"W%03d"%(P.SERIES_START+sum(e["event_type"]=="resolved" for e in es)),
        "analysis_locked":sum(e["event_type"]=="resolved" for e in es)<P.SERIES_N,
    }


def analyse():
    if sum(e["event_type"]=="resolved" for e in entries())!=P.SERIES_N:
        raise RuntimeError("analysis forbidden before W106")
    # Same exact-randomization statistics as frozen v2, but over W007-W106 only.
    p1_obs=0; p2_obs=0; p1_null=[]; p2_null=[]; rc=[]; rn=[]
    for n in range(P.SERIES_START,P.SERIES_STOP+1):
        w="W%03d"%n
        c=find("cast",w); z=find("resolved",w)
        cr=z["payload"]["arm_ranks"]["canonical"]; nr=z["payload"]["arm_ranks"]["null"]
        rc.append(cr); rn.append(nr); p1_obs+=cr; p2_obs+=nr-cr
        slot_c=next(s for s,a in c["payload"]["blind"]["slot_map"].items() if a=="canonical")
        slot_n=next(s for s,a in c["payload"]["blind"]["slot_map"].items() if a=="null")
        kc=find("ranking",w,slot_c)["payload"]["ranking"]
        kn=find("ranking",w,slot_n)["payload"]["ranking"]
        vc=[]; vd=[]
        for idx in range(4):
            a=_rank_for_pool_index(c,slot_c,kc,idx)
            b=_rank_for_pool_index(c,slot_n,kn,idx)
            vc.append(a); vd.append(b-a)
        p1_null.append(vc); p2_null.append(vd)

    def conv(rows):
        d={0:1}
        for vals in rows:
            nd={}
            for a,ca in d.items():
                for v in vals: nd[a+v]=nd.get(a+v,0)+ca
            d=nd
        return d
    d1=conv(p1_null); d2=conv(p2_null)
    p1=sum(c for v,c in d1.items() if v<=p1_obs)/sum(d1.values())
    p2=sum(c for v,c in d2.items() if v>=p2_obs)/sum(d2.values())
    result={
        "P1":{"canonical_rank_sum":p1_obs,"p_one_sided_exact":p1,"held":p1<=0.05},
        "P2":{"sum_null_minus_canonical":p2_obs,"p_one_sided_exact":p2,"held":p2<=0.05},
        "secondary":{
            "canonical_rank_distribution":{str(k):rc.count(k) for k in range(1,5)},
            "null_rank_distribution":{str(k):rn.count(k) for k in range(1,5)},
        },
        "ledger_final_event_hash":entries()[-1]["event_hash"],
        "ledger_sha256":O.file_sha256(P.LEDGER),
    }
    return result
