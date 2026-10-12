"""Android storage/UI adapter. Accepted G1 dynamics remain unchanged.
All sessions use synthetic inputs; no live beacon or registered forecasts.
"""
import hashlib
import json
import os
from pathlib import Path
import uuid
import threading
import functools

_SESSION_LOCK = threading.RLock()

def serialized(fn):
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        with _SESSION_LOCK:
            return fn(*args, **kwargs)
    return wrapped
from drift_core import Substrate, canonical_edges, canonical_json, digest, keyed_uniform, rewire, verify_canonical
from run_drift import atomic_json, synthetic_tape
from episodic import EpisodicSubstrate, POLICY, VERSION, variates, episode_metrics

LIMIT = 512


def _current(root):
    p = Path(root) / 'current.json'
    if not p.exists():
        return None
    key = json.loads(p.read_text())['session']
    if len(key) != 32 or any(c not in '0123456789abcdef' for c in key):
        raise ValueError('invalid session identifier')
    return Path(root) / key


@serialized
def create(root, seed=101):
    verify_canonical()
    seed = int(seed)
    if not 0 <= seed <= 2147483647:
        raise ValueError('Seed must be 0..2147483647')
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    key = uuid.uuid4().hex  # storage identity only, excluded from dynamics/random keys
    p = root / key
    p.mkdir()
    edges = canonical_edges()
    control = rewire(edges)
    tape = synthetic_tape(seed, LIMIT)
    m = dict(seed=seed, policy=POLICY, limit=LIMIT, tape_digest=digest(tape),
             canonical_edges=edges, control_edges=control, mode='OFFLINE_SYNTHETIC_G1.1',
             runtime_digest=json.loads((Path(__file__).parent/'runtime_manifest.json').read_text())['digest'],
             anomaly_eligible=False)
    atomic_json(p/'manifest.json', m)
    atomic_json(root/'current.json', dict(session=key))
    return status(str(root))


def _load(root):
    p = _current(root)
    if p is None:
        raise ValueError('Create a new run first')
    m = json.loads((p/'manifest.json').read_text())
    runtime = json.loads((Path(__file__).parent/'runtime_manifest.json').read_text())['digest']
    if m['runtime_digest'] != runtime:
        raise ValueError('Run belongs to different runtime; export it and start a new run')
    if m['policy'] != POLICY or m['mode'] != 'OFFLINE_SYNTHETIC_G1.1':
        raise ValueError('Run policy mismatch')
    tape = synthetic_tape(m['seed'], m['limit'])
    if digest(tape) != m['tape_digest']:
        raise ValueError('Input tape mismatch')
    arms = {a: EpisodicSubstrate(m['control_edges'] if a == 'G' else m['canonical_edges']) for a in ('C','G','M')}
    head = digest(m)
    records = []
    for i, path in enumerate(sorted(p.glob('tick_*.json'))):
        if path.name != 'tick_%06d.json' % i:
            raise ValueError('Ledger gap; refusing recovery from incomplete history')
        record = json.loads(path.read_text())
        claimed = record.pop('hash')
        if record['tick'] != i or record['previous_hash'] != head or digest(record) != claimed:
            raise ValueError('Ledger integrity mismatch')
        if record['input'] != tape[i] or any(e['u'] != variates(tape[i], i)['transition'] for e in record['events'].values()):
            raise ValueError('Random input mismatch')
        v = variates(tape[i], i)
        if any(e['embodiment']['ingress_u'] != v['ingress'] or e['embodiment']['proposed_entry'] != int(10*v['ingress']) for e in record['events'].values()):
            raise ValueError('Ingress input mismatch')
        records.append(record)
        head = claimed
    if records:
        arms = {a: EpisodicSubstrate.restore(records[-1]['states'][a]) for a in arms}
    return p, m, tape, arms, records, head


@serialized
def status(root):
    if _current(root) is None:
        return canonical_json(dict(exists=False, status='Ready for a new run'))
    p,m,tape,arms,records,head = _load(root)
    counts = {a: [0]*10 for a in arms}
    for r in records:
        for a in arms:
            counts[a][r['events'][a]['selected_edge'][1]] += 1
    return canonical_json(dict(exists=True, session=p.name, ticks=len(records), limit=m['limit'],
        seed=m['seed'], policy=POLICY, metrics={a:episode_metrics([r['events'][a] for r in records]) for a in arms}, zones={a:s.P['zone'] for a,s in arms.items()}, counts=counts,
        last_events=records[-1]['events'] if records else {}, ledger_head=head, anomaly_eligible=False))


@serialized
def advance(root, steps=1):
    steps=int(steps)
    if not 1 <= steps <= LIMIT:
        raise ValueError('Invalid step count')
    p,m,tape,arms,records,head = _load(root)
    for i in range(len(records), min(len(records)+steps,m['limit'])):
        v=variates(tape[i],i)
        events={a:arms[a].advance(v['transition'],v['ingress'],reset=a=='M') for a in arms}
        body=dict(tick=i,input=tape[i],previous_hash=head,anomaly_eligible=False,
                  events=events,states={a:s.snapshot() for a,s in arms.items()})
        head=digest(body)
        atomic_json(p/('tick_%06d.json'%i),dict(body,hash=head))
    return status(root)


def reference_result():
    verify_canonical()
    edges=canonical_edges()
    arms={a:EpisodicSubstrate(rewire(edges) if a=='G' else edges) for a in ('C','G','M')}
    paths={a:[] for a in arms}
    for i,x in enumerate(synthetic_tape(101,512)):
        v=variates(x,i)
        for a,s in arms.items():
            paths[a].append(s.advance(v['transition'],v['ingress'],reset=a=='M'))
    # Hash strings depend on floating-point serialization; numerical parity is checked separately.
    def strip_hashes(obj):
        if isinstance(obj, dict): return {k:strip_hashes(v) for k,v in obj.items() if not k.endswith('digest')}
        if isinstance(obj, list): return [strip_hashes(v) for v in obj]
        return obj
    return strip_hashes(dict(version=VERSION, paths=paths, states={a:s.snapshot() for a,s in arms.items()}))


def check_reference():
    expected=json.loads((Path(__file__).parent/'device_reference.json').read_text())
    actual=reference_result()
    def same(a,b):
        if type(a) in (int,float) and type(b) in (int,float):
            return abs(a-b)<=1e-12
        if isinstance(a,dict) and isinstance(b,dict):
            return set(a)==set(b) and all(same(a[k],b[k]) for k in a)
        if isinstance(a,list) and isinstance(b,list):
            return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
        return a==b
    ok=same(actual,expected)
    if not ok:
        raise ValueError('Device parity MISMATCH: do not use this runtime for an assay')
    return 'PASS: canonical source bytes verified; 512-tick G1.1 C/G/M events and states match; state tolerance 1e-12.'


@serialized
def verify_run(root):
    p,m,tape,arms,records,head = _load(root)
    replay={a:EpisodicSubstrate(m['control_edges'] if a=='G' else m['canonical_edges']) for a in arms}
    for i,r in enumerate(records):
        expected={a:s.advance(variates(tape[i],i)['transition'],variates(tape[i],i)['ingress'],reset=a=='M') for a,s in replay.items()}
        if expected!=r['events'] or {a:s.snapshot() for a,s in replay.items()}!=r['states']:
            raise ValueError('Replay mismatch at tick %d'%i)
    return 'PASS: %d ticks replayed exactly; head %s'%(len(records),head)


@serialized
def export_zip(root, destination):
    import zipfile
    p,_,_,_,_,_=_load(root)
    with zipfile.ZipFile(destination,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(p.glob('*.json')):
            z.write(str(f), f.name)
    return destination
