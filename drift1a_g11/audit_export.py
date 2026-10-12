"""Independent ledger, pairing, legal-move and numerical replay audit of a device ZIP."""
import copy
import json
from pathlib import Path
import sys
import zipfile
sys.path.insert(0,str(Path(__file__).resolve().parent/'runtime'))
from drift_core import canonical_edges, rewire, digest, empty_history
from episodic import POLICY, EpisodicSubstrate, variates, episode_metrics
from run_drift import synthetic_tape


def audit(path):
    max_error=0.0
    exact=True
    def equivalent(a,b):
        nonlocal max_error
        if type(a) in (float,int) and type(b) in (float,int):
            error=abs(a-b);max_error=max(max_error,error)
            return error<=1e-12
        if type(a)!=type(b):return False
        if isinstance(a,dict):
            return a.keys()==b.keys() and all(equivalent(a[k],b[k]) for k in a if not k.endswith('digest'))
        if isinstance(a,list):return len(a)==len(b) and all(equivalent(x,y) for x,y in zip(a,b))
        return a==b
    def check(ok,message):
        if not ok:raise ValueError(message)
    with zipfile.ZipFile(path) as z:
        names=z.namelist();n=len(names)-1
        check(len(set(names))==len(names) and set(names)=={'manifest.json'}|{f'tick_{i:06d}.json' for i in range(n)},'Archive schema/gap')
        m=json.loads(z.read('manifest.json'))
        check(m['policy']==POLICY and m['mode']=='OFFLINE_SYNTHETIC_G1.1' and m['anomaly_eligible'] is False,'Manifest policy')
        check(m['limit']==512 and 0<=n<=512,'Run horizon')
        check(m['canonical_edges']==canonical_edges() and m['control_edges']==rewire(canonical_edges()),'Graph identity')
        runtime=json.loads((Path(__file__).resolve().parent/'runtime/runtime_manifest.json').read_text())
        check(m['runtime_digest']==runtime['digest'],'Runtime identity')
        tape=synthetic_tape(m['seed'],m['limit']);check(digest(tape)==m['tape_digest'],'Input tape')
        arms={a:EpisodicSubstrate(m['control_edges'] if a=='G' else m['canonical_edges']) for a in 'CGM'}
        previous={a:s.snapshot() for a,s in arms.items()};head=digest(m);events={a:[] for a in arms}
        for i in range(n):
            r=json.loads(z.read(f'tick_{i:06d}.json'));h=r.pop('hash')
            check(r['previous_hash']==head and digest(r)==h and r['tick']==i,'Ledger hash/order')
            check(r['input']==tape[i] and r['anomaly_eligible'] is False,'Tick input/eligibility');head=h
            check(set(r['events'])==set(arms) and set(r['states'])==set(arms),'Arm schema')
            v=variates(tape[i],i)
            for a,s in arms.items():
                e=r['events'][a];snap=r['states'][a];b=e['embodiment']
                EpisodicSubstrate.restore(snap) # verifies outer and inner digests
                check(e['pre_embodiment_digest']==previous[a]['digest'] and e['post_embodiment_digest']==snap['digest'],'Embodiment causal chain')
                check(e['u']==v['transition'] and b['ingress_u']==v['ingress'] and b['proposed_entry']==int(10*v['ingress']),'Matched randomness')
                check(e['selected_edge'] in s.edges,'Forbidden move')
                before=copy.deepcopy(previous[a]['core']);before.pop('digest')
                if b['entry'] is not None:before['P']['zone']=b['entry']['zone']
                if a=='M':before['H']=empty_history()
                check(digest(before)==e['pre_state_digest'] and digest(before['H'])==e['memory_read_digest'],'Prior memory/reset')
                check(e['post_state_digest']==snap['core']['digest'],'Post-state digest')
                want=s.advance(v['transition'],v['ingress'],reset=a=='M');state=s.snapshot()
                exact=exact and want==e and state==snap
                check(equivalent(want,e) and equivalent(state,snap),f'Numerical replay mismatch at {i}/{a}')
                previous[a]=snap;events[a].append(e)
        return dict(pass_audit=True,ticks=n,head=head,exact_cross_runtime_replay=exact,
                    max_numeric_error=max_error,metrics={a:episode_metrics(es) for a,es in events.items()})

if __name__=='__main__':
    result=audit(sys.argv[1]);out=json.dumps(result,indent=2)
    if len(sys.argv)>2:Path(sys.argv[2]).write_text(out+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='metrics'},indent=2))
