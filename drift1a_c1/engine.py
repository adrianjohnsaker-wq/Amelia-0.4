"""C1 runner. Immutable compressed chunks are the sole committed state authority."""
import copy
import fcntl
import gzip
import platform
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from .common import ROOT,cj,sha,digest,publish,read,week,project_journal
sys.path.insert(0,str(ROOT/'drift1a_g11/runtime'))
from episodic import EpisodicSubstrate,POLICY,variates
from drift_core import canonical_edges,rewire
from .beacon import QUICKNET,round_time,first_round,Sealer,SyntheticSealer,VerificationError

NAMES=['C','M']+[f'G{i:02d}' for i in range(8)]+[f'R{i:02d}' for i in range(1,9)]

def frozen_files():
    paths=list((ROOT/'drift1a_g11/runtime').rglob('*.py'))
    paths += list((ROOT/'drift1a_g11/runtime/canonical').glob('*.json'))
    paths += [ROOT/'claude/DRIFT1A_C1_CHARTER_draft.md']
    paths += [ROOT/'drift1a_c1'/n for n in ('__init__.py','common.py','engine.py','beacon.py','metrics.py','cli.py','requirements.txt')]
    paths += list((ROOT/'drift1a_c1/vendor').rglob('*.py'))+list((ROOT/'drift1a_c1/vendor').rglob('*.pem'))
    return {p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in sorted(paths)}

def graphs():
    c=canonical_edges()
    return {a:rewire(c,seed=f'DRIFT-1A-C1-ENS-{int(a[1:]):02d}') if a.startswith('G') else c for a in NAMES}

def input_for(a,randomness):
    return sha(f'DRIFT-1A-C1-REF-{int(a[1:])}|'.encode('ascii')+bytes.fromhex(randomness)) if a.startswith('R') else randomness

@contextmanager
def locked(root):
    p=Path(root);p.mkdir(parents=True,exist_ok=True)
    with (p/'.lock').open('a') as f:
        fcntl.flock(f,fcntl.LOCK_EX);yield

def genesis(root,mode,created,sealer):
    p=Path(root);p.mkdir(parents=True,exist_ok=True)
    if (p/'genesis.json').exists():raise ValueError('genesis already exists')
    if mode not in ('LIVE','SIMULATION'):raise ValueError('invalid mode')
    if (mode=='LIVE') != isinstance(sealer,Sealer):raise ValueError('mode/sealer mismatch')
    g=graphs();r0=first_round(created)
    body=dict(version='DRIFT-1A-C1-0.2',mode=mode,created_at=created,R0=r0,stride=20,
        policy=POLICY,beacon={k:(v.decode('ascii') if isinstance(v,bytes) else v) for k,v in QUICKNET.items()},
        files=frozen_files(),graphs=g,graph_digests={a:digest(v) for a,v in g.items()},
        python=platform.python_version(),platform=platform.platform())
    # Failed or late genesis remains an abandoned attempt; never replace it.
    attempt=p/'genesis_attempts'/digest(body)
    publish(attempt/'genesis.json',cj(body))
    sealer.seal(attempt/'seal',digest(body),round_time(r0))
    sealer.verify(attempt/'seal',digest(body),round_time(r0))
    publish(p/'genesis.json',cj(dict(body,seal_attempt=attempt.name)))
    return read(p/'genesis.json')

class Engine:
    def __init__(self,root,beacon,sealer,clock=time.time):
        self.root=Path(root);self.beacon=beacon;self.sealer=sealer;self.clock=clock
        self.g=read(self.root/'genesis.json')
        if self.g['mode']!=beacon.mode:raise ValueError('source mode mismatch')
        if self.g['files']!=frozen_files():raise ValueError('frozen code/charter changed')
        attempt=self.g['seal_attempt'];body={k:v for k,v in self.g.items() if k!='seal_attempt'}
        if attempt!=digest(body):raise ValueError('genesis seal binding')
        sealer.verify(self.root/'genesis_attempts'/attempt/'seal',digest(body),round_time(self.g['R0']))
        self.arms={a:EpisodicSubstrate(self.g['graphs'][a]) for a in NAMES}
        self.tick=0;self.head=digest(self.g);self.seq=0
        last=None
        for chunk in self.chunks():
            if chunk['previous']!=self.head or chunk['start']!=self.tick or chunk['sequence']!=self.seq:raise ValueError('chunk chain/gap')
            if not chunk['records'] or len({week(x['round_time']) for x in chunk['records']})!=1:raise ValueError('chunk week/schema')
            for r in chunk['records']:
                if r['tick']!=self.tick or r['beacon']['round']!=self.g['R0']+20*self.tick or r['round_time']!=round_time(r['beacon']['round']):raise ValueError('record order')
                self.tick+=1
            self.head=chunk['_hash'];self.seq+=1;last=chunk
        if last:self.arms={a:EpisodicSubstrate.restore(last['states'][a]) for a in NAMES}
    def chunks(self):
        for p in sorted((self.root/'record/chunks').glob('*.json.gz')):
            raw=p.read_bytes();x=__import__('json').loads(gzip.decompress(raw))
            if p.name!=f'{x["sequence"]:08d}-{x["week"]}.json.gz':raise ValueError('chunk filename')
            x['_hash']=sha(raw);yield x
    def records(self):
        for c in self.chunks():yield from c['records']
    def incident(self,kind,message,r):
        p=self.root/'record/incidents';p.mkdir(parents=True,exist_ok=True)
        entries=sorted(p.glob('*.json'));prev=sha(entries[-1].read_bytes()) if entries else digest(self.g)
        publish(p/f'{len(entries):08d}.json',cj(dict(kind=kind,message=str(message),round=r,observed_at=self.clock(),previous=prev)))
        project_journal(p,self.root/'record/incidents.jsonl')
    def advance(self,b,receipt):
        r=self.g['R0']+20*self.tick
        self.beacon.verify(b,r)
        if receipt<round_time(r):raise VerificationError('receipt predates publication')
        es={}
        for a,s in self.arms.items():
            v=variates(input_for(a,b['randomness']),self.tick)
            e=s.advance(v['transition'],v['ingress'],reset=a=='M');sel=e['selection'];bias=sel['commitment_bias']
            remembered=int(bias['preferredExit'].split('-')[1]) if bias else None
            es[a]=dict(edge=e['selected_edge'],embodiment=e['embodiment'],effects=e['effects'],
                phase_after=e['phase_after_event'],commitment_active=bool(bias),retention_active=sel['retention']['active'],
                governor_active=any(x['multiplier']!=1.0 for x in sel['governor']),
                retention_floor=sel['retention']['floor_applied'],remembered_exit=remembered,
                remembered_base=sum(p for edge,p in zip(sel['candidates'],sel['base']) if edge[1]==remembered),
                remembered_final=sum(p for edge,p in zip(sel['candidates'],sel['probabilities']) if edge[1]==remembered),
                memory_read_digest=e['memory_read_digest'],pre_digest=e['pre_embodiment_digest'],post_digest=e['post_embodiment_digest'])
        x=dict(tick=self.tick,beacon=b,round_time=round_time(r),received_at=receipt,lag=receipt-round_time(r),catch_up=receipt-round_time(r)>5400,arms=es)
        self.tick+=1;return x
    def commit(self,records):
        if not records:return
        w=week(records[0]['round_time'])
        if any(week(r['round_time'])!=w for r in records):raise ValueError('mixed-week transaction')
        x=dict(sequence=self.seq,week=w,start=records[0]['tick'],previous=self.head,records=records,states={a:s.snapshot() for a,s in self.arms.items()})
        raw=gzip.compress(cj(x),mtime=0)
        publish(self.root/'record/chunks'/f'{self.seq:08d}-{w}.json.gz',raw)
        self.head=sha(raw);self.seq+=1
    def ingest(self,until,max_ticks=120):
        batch=[];count=0
        while count<max_ticks:
            r=self.g['R0']+20*self.tick
            if round_time(r)>until:break
            w=week(round_time(r))
            if batch and week(batch[0]['round_time'])!=w:self.commit(batch);batch=[]
            try:b=self.beacon.fetch(r);receipt=self.clock();self.beacon.verify(b,r)
            except Exception as exc:
                self.commit(batch)
                self.incident('verification_failure' if isinstance(exc,VerificationError) else 'retrieval_failure',exc,r)
                return dict(ticks=count,blocked_round=r)
            batch.append(self.advance(b,receipt));count+=1
        self.commit(batch)
        return dict(ticks=count,next_round=self.g['R0']+20*self.tick)
    def replay(self):
        fresh=object.__new__(Engine);fresh.__dict__=dict(self.__dict__)
        fresh.arms={a:EpisodicSubstrate(self.g['graphs'][a]) for a in NAMES};fresh.tick=0
        for chunk in self.chunks():
            for r in chunk['records']:
                if fresh.advance(r['beacon'],r['received_at'])!=r:raise ValueError('replay mismatch at tick '+str(r['tick']))
            if {a:s.snapshot() for a,s in fresh.arms.items()}!=chunk['states']:raise ValueError('checkpoint mismatch')
        return dict(ticks=fresh.tick,head=self.head,exact_replay=True)
