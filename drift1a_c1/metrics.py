"""Frozen C1 measurements, approved amendments 1–11 (charter draft 0.3)."""
import copy
import hashlib
import math
import random
from collections import Counter
from .common import week, cj
from .engine import NAMES

VERSION = 'C1-measurements-0.3-A11'
CANONICAL_MEMORY = ['C'] + [f'R{i:02d}' for i in range(1, 9)]
BOUNDARY = {0, 3, 6, 9}
CLASSES = ('all', 'traversal', 'boundary_entry')
PERMUTATIONS = 200


def episode_class(entry):
    return 'boundary_entry' if entry in BOUNDARY else 'traversal'


def blank():
    return dict(ticks=0, warp=0, plex=0, cap=0, entries=0, boundary_entries=0,
        completed=0, total_completed_length=0, length_distribution=Counter(),
        occupancy=[0]*10, self_loops=[0]*10, phases=Counter(),
        memory={k:0 for k in ('commitment_active','governor_active','retention_active',
            'commitment_changed','governor_changed','retention_changed','retention_floor')},
        remembered_choices=0, remembered_selected=0, remembered_base_expected=0.,
        remembered_final_expected=0., commitment_episode_endings=Counter(),
        routes=Counter(), lag_pairs={k:[] for k in range(1,9)}, unfinished=None)


def mutual_information(pairs):
    n=len(pairs)
    if not n:return dict(n=0, bits=None, miller_madow_bits=None, m_Z=0, m_O=0, m_ZO=0)
    joint=Counter(pairs);x=Counter(a for a,b in pairs);y=Counter(b for a,b in pairs)
    bits=sum(c/n*math.log2(c*n/(x[a]*y[b])) for (a,b),c in joint.items())
    correction=((len(x)-1)+(len(y)-1)-(len(joint)-1))/(2*n*math.log(2))
    return dict(n=n, bits=bits, miller_madow_bits=bits+correction,
                m_Z=len(x), m_O=len(y), m_ZO=len(joint))


def outcome_predictability(pairs, w, arm, k):
    result=mutual_information(pairs)
    seed=hashlib.sha256(f'DRIFT-1A-C1-PERM|{w}|{arm}|{k}'.encode('utf-8')).hexdigest()
    result.update(seed_sha256=seed, permutations=PERMUTATIONS, null_95_bits=None,
                  permutation_ge_proportion=None, status='insufficient', interpretation='insufficient')
    if not pairs:return result
    rng=random.Random(int(seed,16));zones=[z for z,o in pairs];outcomes=[o for z,o in pairs]
    null=[]
    # Shuffle a fresh copy for each permutation; both populations use this exact key.
    for _ in range(PERMUTATIONS):
        shuffled=outcomes.copy();rng.shuffle(shuffled)
        null.append(mutual_information(list(zip(zones,shuffled)))['bits'])
    q=sorted(null)[math.ceil(.95*PERMUTATIONS)-1]
    result.update(null_95_bits=q,
        permutation_ge_proportion=sum(v>=result['bits'] for v in null)/PERMUTATIONS)
    if len(pairs)>=50:
        result['status']='sufficient'
        result['interpretation']='indistinguishable from zero' if result['bits']<=q else 'above permutation 95th percentile (exploratory)'
    return result


def route_key(entry,edges):return cj([entry,edges]).decode('ascii')


def boundary_diagnostic(entry, length, end, outcome):
    expected='Warp' if entry in (3,6) else 'Plex'
    return length==1 and end=='boundary' and outcome==expected


def summarize(records):
    weeks={};current={a:None for a in NAMES};previous=None;diagnostics={}
    def close_week(w):
        for a,p in current.items():
            if p:
                value=dict(length=len(p['edges']),entry=p['entry'],episode_class=p['class'])
                for c in ('all',p['class']):weeks[w][a][c]['unfinished']=value
    for r in records:
        w=week(r['round_time'])
        if w!=previous:
            if previous is not None:close_week(previous)
            weeks.setdefault(w,{a:{c:blank() for c in CLASSES} for a in NAMES})
            diagnostics.setdefault(w,{a:dict(status='NOT_APPLICABLE' if a.startswith('G') else 'PASS',checked=0,failures=[]) for a in NAMES})
            previous=w
        for a,e in r['arms'].items():
            b=e['embodiment'];edge=e['edge'];src,dst=edge[:2]
            if b['entry'] is not None:
                if current[a] is not None:raise ValueError('entry before prior end')
                entry=b['entry']['zone'];cl=episode_class(entry)
                current[a]=dict(entry=entry,zones=[entry],edges=[],committed=False,**{'class':cl})
                for c in ('all',cl):
                    m=weeks[w][a][c];m['entries']+=1;m['boundary_entries']+=int(entry in BOUNDARY)
            p=current[a]
            if p is None:raise ValueError('route missing ingress')
            p['edges'].append(edge);p['zones'].append(dst);p['committed']|=e['commitment_active']
            for c in ('all',p['class']):
                m=weeks[w][a][c]
                m['ticks']+=1;m['occupancy'][dst]+=1;m['self_loops'][src]+=int(src==dst)
                m['phases'][e['phase_after']]+=1
                for key in m['memory']:m['memory'][key]+=int(e.get(key,e['effects'].get(key,False)))
                if e['remembered_exit'] is not None:
                    m['remembered_choices']+=1;m['remembered_selected']+=int(dst==e['remembered_exit'])
                    m['remembered_base_expected']+=e['remembered_base'];m['remembered_final_expected']+=e['remembered_final']
                if b['end']:
                    if b['length']!=len(p['edges']):raise ValueError('episode length inconsistent')
                    m['completed']+=1;m['total_completed_length']+=b['length'];m['length_distribution'][str(b['length'])]+=1
                    m['routes'][route_key(p['entry'],p['edges'])]+=1
                    if b['end']=='cap':m['cap']+=1
                    else:
                        m[b['outcome'].lower()]+=1
                        for k in range(1,min(8,len(p['edges']))+1):m['lag_pairs'][k].append((p['zones'][-1-k],b['outcome']))
                    if p['committed']:m['commitment_episode_endings'][b['outcome'] or 'cap']+=1
            if b['end']:
                if not a.startswith('G') and p['class']=='boundary_entry':
                    d=diagnostics[w][a];d['checked']+=1
                    if not boundary_diagnostic(p['entry'],b['length'],b['end'],b['outcome']):
                        d['status']='FAIL';d['failures'].append(dict(tick=r['tick'],entry=p['entry'],length=b['length'],end=b['end'],outcome=b['outcome']))
                current[a]=None
    if previous:close_week(previous)
    result={}
    for w,arms in weeks.items():
        result[w]={}
        for a,classes in arms.items():
            for cl,m in classes.items():
                n=m['warp']+m['plex'];ticks=m['ticks'];completed=m['completed']
                m['warp_fraction']=m['warp']/n if n else None
                m['boundary_ending_rate']=n/ticks if ticks else None
                m['boundary_entry_rate']=m['boundary_entries']/m['entries'] if m['entries'] else None
                m['mean_completed_length']=m['total_completed_length']/completed if completed else None
                m['zone_occupancy']=[x/ticks if ticks else None for x in m['occupancy']]
                m['distinct_routes']=len(m['routes'])
                m['distinct_routes_per_100_episodes']=100*len(m['routes'])/completed if completed else None
                m['remembered_exit_ratio']=m['remembered_selected']/m['remembered_final_expected'] if m['remembered_final_expected'] else None
                pairs=m.pop('lag_pairs')
                m['outcome_predictability_at_lag']={str(k):(outcome_predictability(p,w,a,k) if cl in ('all','traversal') else mutual_information(p)) for k,p in pairs.items()}
                m['top_routes']=[dict(route=k,count=v) for k,v in sorted(m['routes'].items(),key=lambda x:(-x[1],x[0]))[:10]]
                for key in ('routes','phases','commitment_episode_endings','length_distribution'):m[key]=dict(m[key])
            # Retain old top-level all-episode fields for readers of the earlier schema.
            result[w][a]=dict(classes['all'],episode_classes=classes,boundary_entry_diagnostic=diagnostics[w][a])
    return result


def js_divergence(a,b):
    na,nb=sum(a.values()),sum(b.values())
    if not na or not nb:return None
    value=0.
    for key in sorted(a.keys()|b.keys()):
        p,q=a.get(key,0)/na,b.get(key,0)/nb;m=(p+q)/2
        if p:value+=.5*p*math.log2(p/m)
        if q:value+=.5*q*math.log2(q/m)
    return value


PRIMARY_KEYS=(['warp_fraction','boundary_ending_rate_all','mean_completed_length','distinct_routes_per_100_episodes']+
    [f'zone_occupancy_{z}' for z in range(1,10)]+[f'self_loops_{z}' for z in (0,1,3,9)]+
    [f'{s}_changed' for s in ('commitment','governor','retention')]+['remembered_exit_ratio']+
    [f'outcome_mm_lag_{k}' for k in range(1,9)])
assert len(PRIMARY_KEYS)==29


def primary_values(arm):
    t=arm['episode_classes']['traversal']
    values={k:t[k] for k in ('warp_fraction','mean_completed_length','distinct_routes_per_100_episodes','remembered_exit_ratio')}
    values['boundary_ending_rate_all']=arm['boundary_ending_rate']
    values.update({f'zone_occupancy_{z}':t['zone_occupancy'][z] for z in range(1,10)})
    values.update({f'self_loops_{z}':arm['episode_classes']['traversal' if z==1 else 'boundary_entry']['self_loops'][z] for z in (0,1,3,9)})
    values.update({f'{s}_changed':t['memory'][f'{s}_changed'] for s in ('commitment','governor','retention')})
    for k in range(1,9):
        v=t['outcome_predictability_at_lag'][str(k)]
        values[f'outcome_mm_lag_{k}']=v['miller_madow_bits'] if v['status']=='sufficient' else None
    return {k:values[k] for k in PRIMARY_KEYS}


def compare(value, references):
    if value is None or any(v is None for v in references):return dict(status='undefined',strict_outside=False)
    lower=sum(v<value for v in references);ties=sum(v==value for v in references)
    return dict(status='compared',value=value,rank_low=lower+1,rank_high=lower+ties+1,
        reference_min=min(references),reference_max=max(references),strict_outside=value<min(references) or value>max(references))


def ranks(arms):
    values={a:primary_values(arms[a]) for a in CANONICAL_MEMORY}
    return {k:compare(values['C'][k],[values[a][k] for a in CANONICAL_MEMORY[1:]]) for k in PRIMARY_KEYS}


def flag_summary(rows,earlier):
    n=sum(v['status']=='compared' for v in rows.values())
    tally={}
    for k in PRIMARY_KEYS:
        past=[v['report']['references'][k] for v in earlier.values()]
        history=past+[rows[k]];compared=sum(x['status']=='compared' for x in history)
        tally[k]=dict(weeks_reported=len(history),weeks_compared=compared,
            weeks_flagged=sum(x['strict_outside'] for x in history),expected_flags=2*compared/9,
            nominal_expected_all_weeks=2*len(history)/9)
    return dict(N=len(PRIMARY_KEYS),N_compared=n,F=sum(v['strict_outside'] for v in rows.values()),expected_flags=2*len(PRIMARY_KEYS)/9,
        expected_flags_comparable=2*n/9,cross_week=tally,
        ties='Equal values occupy a tied rank interval; equality with a reference extreme is never flagged.',
        dependence='Statistics are correlated, which can make F vary more than a binomial count; the expectation is unchanged under exchangeability without ties. Memory carries across weeks, so weeks are serially dependent and a binomial reference is approximate.')


def constant_primary_statistics(arms):
    """Validation-week diagnostic, not a rule for censoring live reports."""
    values={a:primary_values(arms[a]) for a in CANONICAL_MEMORY}
    return [k for k in PRIMARY_KEYS if len({values[a][k] for a in CANONICAL_MEMORY})==1]


def leave_one_out_flags(arms):
    values={a:primary_values(arms[a]) for a in CANONICAL_MEMORY}
    result={}
    for a in CANONICAL_MEMORY:
        rows=[compare(values[a][k],[values[b][k] for b in CANONICAL_MEMORY if b!=a]) for k in PRIMARY_KEYS]
        result[a]=dict(F=sum(r['strict_outside'] for r in rows),N_compared=sum(r['status']=='compared' for r in rows))
    return result


def route_divergence(current,prior):
    n,m=current['completed'],prior['completed']
    sufficient=n>=50 and m>=50
    return dict(status='sufficient' if sufficient else 'insufficient',current_episodes=n,prior_episodes=m,
        js_divergence_bits=js_divergence(current['routes'],prior['routes']) if sufficient else None)


def route_rarity(arms):
    present={a:set(arms[a]['episode_classes']['traversal']['routes']) for a in CANONICAL_MEMORY}
    return {a:{route:sum(route in present[b] for b in CANONICAL_MEMORY if b!=a)<=1 for route in present[a]} for a in CANONICAL_MEMORY}


def retrospective(arms,earlier,w):
    rarity=route_rarity(arms);out={}
    for a in NAMES:
        current=arms[a]['episode_classes']['traversal'];routes=current['routes'];history={}
        for old,v in sorted(earlier.items()):
            for route in v['report']['arms'][a]['episode_classes']['traversal']['routes']:
                if route not in history:
                    first_rare=v['report']['retrospective'][a]['reference_rare_routes']
                    history[route]=dict(first_week=old,reference_rare_at_first=(route in first_rare) if first_rare is not None else None,
                        first_seal_digest=v['seal_digest'],recurrence_weeks=[])
                else:history[route]['recurrence_weeks'].append(old)
        novel=[r for r in sorted(routes) if r not in history]
        for route in sorted(routes):
            if route not in history:history[route]=dict(first_week=w,reference_rare_at_first=rarity[a][route] if a in rarity else None,first_seal_digest=None,recurrence_weeks=[])
            else:history[route]['recurrence_weeks'].append(w)
        rare=sorted(r for r,v in rarity[a].items() if v) if a in rarity else None
        recurring=[dict(route=r,**v) for r,v in sorted(history.items()) if v['reference_rare_at_first'] and v['recurrence_weeks']]
        denom=current['completed'];rate=lambda n:100*n/denom if denom else None
        out[a]=dict(novel_routes=novel,novel_count=len(novel),novel_per_100_episodes=rate(len(novel)),
            reference_rare_routes=rare,reference_rare_count=len(rare) if rare is not None else None,
            reference_rare_per_100_episodes=rate(len(rare)) if rare is not None else None,
            recurring_rare_routes=recurring,recurring_rare_this_week=sum(w in x['recurrence_weeks'] for x in recurring),
            route_history=history,comparisons={old:dict(route_divergence(current,v['report']['arms'][a]['episode_classes']['traversal']),prior_seal_digest=v['seal_digest']) for old,v in sorted(earlier.items())})
    # Descriptive ranks only: amendment 10 does not enlarge the 29-statistic flag set.
    for a in CANONICAL_MEMORY:
        out[a]['ranks_among_nine']={}
        for key in ('novel_count','novel_per_100_episodes','reference_rare_count','reference_rare_per_100_episodes','recurring_rare_this_week'):
            rank=compare(out[a][key],[out[b][key] for b in CANONICAL_MEMORY if b!=a]);rank.pop('strict_outside',None)
            out[a]['ranks_among_nine'][key]=rank
    return out
