"""Frozen C1 measurement definitions. Routes retain entry plus typed edges."""
import math
from collections import Counter
from .common import week
from .engine import NAMES

VERSION='C1-measurements-0.2'

def blank():
    return dict(ticks=0,warp=0,plex=0,cap=0,entries=0,boundary_entries=0,
        completed=0,total_completed_length=0,occupancy=[0]*10,self_loops=[0]*10,
        phases=Counter(),memory={k:0 for k in ('commitment_active','governor_active','retention_active','commitment_changed','governor_changed','retention_changed','retention_floor')},
        remembered_choices=0,remembered_selected=0,remembered_base_expected=0.,remembered_final_expected=0.,
        commitment_episode_endings=Counter(),routes=Counter(),lag_pairs={k:[] for k in range(1,9)},unfinished=None)

def mutual_information(pairs):
    n=len(pairs)
    if not n:return dict(n=0,bits=None)
    joint=Counter(pairs);x=Counter(a for a,b in pairs);y=Counter(b for a,b in pairs)
    return dict(n=n,bits=sum(c/n*math.log2(c*n/(x[a]*y[b])) for (a,b),c in joint.items()))

def route_key(entry,edges):
    from .common import cj
    return cj([entry,edges]).decode('ascii')

def summarize(records):
    weeks={};current={a:None for a in NAMES};previous_week=None
    for r in records:
        w=week(r['round_time'])
        if w!=previous_week:
            if previous_week is not None:
                for a,p in current.items():
                    weeks[previous_week][a]['unfinished']=dict(length=len(p['edges']),entry=p['entry']) if p else None
            weeks.setdefault(w,{a:blank() for a in NAMES});previous_week=w
        for a,e in r['arms'].items():
            m=weeks[w][a];b=e['embodiment'];edge=e['edge'];src,dst=edge[:2]
            if b['entry'] is not None:
                if current[a] is not None:raise ValueError('entry before prior end')
                current[a]=dict(entry=b['entry']['zone'],zones=[b['entry']['zone']],edges=[],committed=False)
                m['entries']+=1;m['boundary_entries']+=int(b['entry']['zone'] in (0,3,6,9))
            p=current[a]
            if p is None:raise ValueError('route missing ingress')
            p['edges'].append(edge);p['zones'].append(dst);p['committed']|=e['commitment_active']
            m['ticks']+=1;m['occupancy'][dst]+=1;m['self_loops'][src]+=int(src==dst)
            m['phases'][e['phase_after']]+=1
            for k in m['memory']:m['memory'][k]+=int(e.get(k,e['effects'].get(k,False)))
            if e['remembered_exit'] is not None:
                m['remembered_choices']+=1;m['remembered_selected']+=int(dst==e['remembered_exit'])
                m['remembered_base_expected']+=e['remembered_base'];m['remembered_final_expected']+=e['remembered_final']
            if b['end']:
                if b['length']!=len(p['edges']):raise ValueError('episode length inconsistent')
                m['completed']+=1;m['total_completed_length']+=b['length']
                if b['end']=='cap':m['cap']+=1
                else:
                    outcome=b['outcome'].lower();m[outcome]+=1
                    m['routes'][route_key(p['entry'],p['edges'])]+=1
                    for k in range(1,min(8,len(p['edges']))+1):m['lag_pairs'][k].append((p['zones'][-1-k],outcome))
                if p['committed']:m['commitment_episode_endings'][b['outcome'] or 'cap']+=1
                current[a]=None
    if previous_week:
        for a,p in current.items():weeks[previous_week][a]['unfinished']=dict(length=len(p['edges']),entry=p['entry']) if p else None
    for w,arms in weeks.items():
        for a,m in arms.items():
            n=m['warp']+m['plex']
            m['warp_fraction']=m['warp']/n if n else None
            m['boundary_entry_rate']=m['boundary_entries']/m['entries'] if m['entries'] else None
            m['mean_completed_length']=m['total_completed_length']/m['completed'] if m['completed'] else None
            m['zone_occupancy']=[x/m['ticks'] for x in m['occupancy']]
            m['outcome_predictability_at_lag']={str(k):mutual_information(p) for k,p in m.pop('lag_pairs').items()}
            m['distinct_routes']=len(m['routes'])
            m['top_routes']=[dict(route=k,count=v) for k,v in sorted(m['routes'].items(),key=lambda x:(-x[1],x[0]))[:10]]
            for k in ('routes','phases','commitment_episode_endings'):m[k]=dict(m[k])
    return weeks

def js_divergence(a,b):
    na,nb=sum(a.values()),sum(b.values())
    if not na or not nb:return None
    result=0.
    for key in a.keys()|b.keys():
        p,q=a.get(key,0)/na,b.get(key,0)/nb;m=(p+q)/2
        if p:result+=.5*p*math.log2(p/m)
        if q:result+=.5*q*math.log2(q/m)
    return result

def scalar_values(x,path=''):
    if isinstance(x,dict):
        for k,v in x.items():
            if k not in ('routes','top_routes','unfinished'):yield from scalar_values(v,path+'/'+str(k))
    elif isinstance(x,list):
        for k,v in enumerate(x):yield from scalar_values(v,path+'/'+str(k))
    elif type(x) in (int,float) or x is None:yield path,x

def ranks(arms):
    refs=[dict(scalar_values(arms[f'R{i:02d}'])) for i in range(1,9)];out={}
    for key,c in scalar_values(arms['C']):
        values=[r.get(key) for r in refs]
        if c is None or any(v is None for v in values):out[key]=dict(status='undefined');continue
        lower=sum(v<c for v in values);ties=sum(v==c for v in values)
        out[key]=dict(value=c,rank_low=lower+1,rank_high=lower+ties+1,reference_min=min(values),reference_max=max(values),strict_outside=c<min(values) or c>max(values))
    return out
