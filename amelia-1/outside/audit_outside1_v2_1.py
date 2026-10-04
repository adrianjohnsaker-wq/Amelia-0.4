"""
Independent recomputation audit for OUTSIDE-1 v2.1 publication evidence.
Run from amelia-1:
    python outside/audit_outside1_v2_1.py
"""
from __future__ import annotations
import hashlib, json, os, re, sys
from datetime import datetime

HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE)
import Outside1_v2 as O
import Outside1_v2_1 as P
import Outside1_v2_1_working as W


def fail(msg):
    raise SystemExit("AUDIT_FAIL: "+msg)


def check_timestamp(x):
    if not isinstance(x,str) or not x.endswith("Z"):
        return False
    try:
        datetime.fromisoformat(x[:-1]+"+00:00")
        return True
    except Exception:
        return False


def audit_registration():
    r=P.check_registration()
    for k,v in r["sources"].items():
        p=v["path"]
        got=O.file_sha256(os.path.join(HERE,p) if not os.path.isabs(p) else p)
        if got!=v["sha256"]: fail("source hash mismatch "+k)
    return r


def audit_calibration():
    c=P.calibration_open()
    if c["protocol_sha256"]!=P.PROTOCOL_SHA256: fail("calibration protocol mismatch")
    if c["registration_sha256"]!=P.load_registration()["registration_sha256"]:
        fail("calibration registration mismatch")
    if not all(c[k]["pass"] for k in ("D1","D2","positive_control")):
        fail("calibration gate not passed")
    return c


def audit_ledger():
    if not os.path.exists(P.LEDGER):
        return {"events":0,"chain_ok":True}
    es=W.entries()
    if not W.verify_chain(): fail("event hash chain")
    parent="0"*64
    for i,e in enumerate(es,1):
        for field in P.PROTOCOL["evidence_schema"]["required_event_fields"]:
            if field not in e: fail("missing field %s event %d"%(field,i))
        if e["event_seq"]!=i: fail("event seq")
        if e["parent_event_hash"]!=parent: fail("parent")
        if not check_timestamp(e["created_utc"]): fail("timestamp")
        if e["serialization"]!=P.SERIALIZATION: fail("serialization")
        if e["protocol_sha256"]!=P.PROTOCOL_SHA256: fail("protocol")
        if e["payload_sha256"]!=P.sha(e["payload"]): fail("payload digest")
        body={k:v for k,v in e.items() if k!="event_hash"}
        if e["event_hash"]!=P.sha(body): fail("event digest")
        if e["event_type"]=="cast":
            a=e["payload"]["arms"]
            for arm in ("canonical","null"):
                if a[arm]["rawTraceDigest"]!=P.channel_digest(a[arm]["trace"]):
                    fail("raw trace digest "+arm)
                if a[arm]["fragmentDigest"]!=P.channel_digest(a[arm]["fragments"]):
                    fail("fragment digest "+arm)
            blind=e["payload"]["blind"]
            if W._slot_map(blind["slot_assignment_entropy_hex"])!=blind["slot_map"]:
                fail("slot assignment")
            for s in ("R1","R2"):
                if P.keyed_permutation4(blind["judge_order_entropy_hex"][s],":judge-order:"+s)!=blind["judge_orders"][s]:
                    fail("judge order "+s)
        elif e["event_type"]=="reading":
            p=e["payload"]
            if hashlib.sha256(p["prompt"].encode()).hexdigest()!=p["prompt_sha256"]: fail("reading prompt")
            if hashlib.sha256(p["output"].encode()).hexdigest()!=p["output_sha256"]: fail("reading output")
            P.validate_method(p["method"])
        elif e["event_type"]=="ranking":
            p=e["payload"]
            if hashlib.sha256(p["prompt"].encode()).hexdigest()!=p["prompt_sha256"]: fail("judge prompt")
            if hashlib.sha256(p["raw_output"].encode()).hexdigest()!=p["raw_output_sha256"]: fail("judge output")
            if sorted(p["ranking"])!=list("ABCD"): fail("ranking")
            P.validate_method(p["method"])
        elif e["event_type"]=="resolved":
            p=e["payload"]
            if P.sha(p["pre_draw_state"])!=p["pre_draw_state_sha256"]: fail("pre-draw commitment")
            td=p["target_draw"]
            if hashlib.sha256(bytes.fromhex(td["entropy_hex"])).hexdigest()!=td["entropy_sha256"]:
                fail("target entropy digest")
            if P.target_choice(td["entropy_hex"])!=td["target_index"]:
                fail("target derivation")
        parent=e["event_hash"]
    return {
        "events":len(es),
        "chain_ok":True,
        "final_event_hash":es[-1]["event_hash"] if es else None,
        "ledger_sha256":O.file_sha256(P.LEDGER) if es else None,
    }


def main():
    r=audit_registration()
    c=audit_calibration()
    l=audit_ledger()
    print(json.dumps({
        "audit":"OUTSIDE-1-v2.1-publication",
        "registration_sha256":r["registration_sha256"],
        "protocol_sha256":P.PROTOCOL_SHA256,
        "calibration_sha256":c["calibration_sha256"],
        "ledger":l,
        "PASS":True,
    },sort_keys=True,indent=2))


if __name__=="__main__":
    main()
