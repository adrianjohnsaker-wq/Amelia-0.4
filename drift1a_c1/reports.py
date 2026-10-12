"""Immutable weekly reports; rendering can evolve, measurement code is frozen."""
import base64
import hashlib
import json
from pathlib import Path
from .common import cj,digest,sha,publish,read,week,project_journal
from .beacon import round_time
from .metrics import summarize,ranks,js_divergence,VERSION
from .engine import NAMES

def weekly(engine):
    next_time=round_time(engine.g['R0']+20*engine.tick)
    # Engine startup has already checked these immutable chunk names and order.
    complete_weeks=sorted({p.name.split('-',1)[1].removesuffix('.json.gz')
        for p in (engine.root/'record/chunks').glob('*.json.gz')
        if p.name.split('-',1)[1].removesuffix('.json.gz')<min(week(next_time),week(engine.clock()))})
    needed=[w for w in complete_weeks if not (engine.root/'reports'/w/'prepared.json').exists()]
    # Recompute measurements only for a newly completed week. Retrying a seal
    # uses exactly its old packet and never materializes the entire tick ledger.
    summaries=summarize(engine.records()) if needed else {};result=[]
    for w in complete_weeks:
        folder=engine.root/'reports'/w;packet=folder/'report.json'
        prepared=folder/'prepared.json'
        if prepared.exists():
            saved=read(prepared)
            publish(packet,cj(saved['report']))
            publish(folder/'report.md',saved['markdown'].encode())
        if not packet.exists():
            arms=summaries[w]
            earlier={}
            for old in sorted((engine.root/'reports').glob('*/report.json')):
                if old.parent.name>=w:continue
                seal=old.parent/'seal/receipt.json'
                if not seal.exists():raise ValueError('prior report still unsealed')
                earlier[old.parent.name]=dict(report=read(old),seal_digest=sha(seal.read_bytes()))
            retrospective={}
            for a in NAMES:
                current=arms[a]['routes'];first={}
                for old,v in earlier.items():
                    for route in v['report']['arms'][a]['routes']:first.setdefault(route,old)
                retrospective[a]=dict(first_observed_week={r:first.get(r,w) for r in current},
                    recurring_routes=sum(r in first for r in current),
                    comparisons={old:dict(js_divergence_bits=js_divergence(current,v['report']['arms'][a]['routes']),
                        shared_routes=len(current.keys()&v['report']['arms'][a]['routes'].keys()),prior_seal_digest=v['seal_digest']) for old,v in earlier.items()})
            records_digest,last=week_record_digest(engine.records(),w)
            report=dict(version='C1-report-0.2',mode=engine.g['mode'],week=w,genesis_digest=digest(engine.g),
                measurement_version=VERSION,generated_at=engine.clock(),last_included_round=last['beacon']['round'],
                last_included_round_time=last['round_time'],records_digest=records_digest,
                renderer_sha256=sha(Path(__file__).read_bytes()),arms=arms,references=ranks(arms),retrospective=retrospective,
                limitations=['Exploratory; no hypothesis test or calibrated anomaly claim.',
                    'References are deterministic transformations of the same inflow, not independent sources.',
                    '2/9 is conditional on exchangeability and no ties; many weekly flags are expected.',
                    'Outcome predictability is within-episode forward association, not evidence of external anticipation.'])
            # JSON is authoritative; Markdown can be recovered from it after interrupted generation.
            publish(prepared,cj(dict(report=report,markdown=render(report))))
            publish(packet,cj(report))
        report=read(packet)
        md=folder/'report.md'
        if not md.exists():publish(md,read(prepared)['markdown'].encode())
        bundle=dict(json_sha256=sha(packet.read_bytes()),markdown_sha256=sha(md.read_bytes()))
        publish(folder/'bundle.json',cj(bundle))
        receipt=engine.sealer.seal(folder/'seal',digest(bundle))
        engine.sealer.verify(folder/'seal',digest(bundle))
        result.append(dict(week=w,seal=receipt))
    return result

def week_record_digest(records,w):
    """Exactly SHA256(canonical JSON list), without retaining that list in memory."""
    h=hashlib.sha256();h.update(b'[');last=None
    for r in records:
        if week(r['round_time'])!=w:continue
        if last is not None:h.update(b',')
        h.update(cj(r));last=r
    h.update(b']')
    if last is None:raise ValueError('empty completed week')
    return h.hexdigest(),last

def render(r):
    lines=[f'# Amelia C1 — {r["week"]}',f'Mode: {r["mode"]}. Observational and exploratory.',
        '\n## Process history','Arm | Ticks | Warp | Plex | Cap | Mean completed length','---|---:|---:|---:|---:|---:']
    for a,m in r['arms'].items():
        mean='undefined' if m['mean_completed_length'] is None else f'{m["mean_completed_length"]:.3f}'
        lines.append(f'{a} | {m["ticks"]} | {m["warp"]} | {m["plex"]} | {m["cap"]} | {mean}')
    c=r['arms']['C'];m=r['arms']['M']
    lines += ['\n### Amelia: choices and memory',
        f'Applied entries: {c["entries"]}; entries onto the boundary: {c["boundary_entries"]}. Distinct completed boundary routes: {c["distinct_routes"]}.',
        f'Unfinished episode at week end: {json.dumps(c["unfinished"])}. Phase counts: {json.dumps(c["phases"],sort_keys=True)}.',
        '\nMechanism | C active | C probability changed | M active | M probability changed',
        '---|---:|---:|---:|---:']
    for mechanism in ('commitment','governor','retention'):
        active=mechanism+'_active';changed=mechanism+'_changed'
        lines.append(f'{mechanism} | {c["memory"][active]} | {c["memory"][changed]} | {m["memory"][active]} | {m["memory"][changed]}')
    lines += [f'\nRetention floor applied: {c["memory"]["retention_floor"]} C choices, {m["memory"]["retention_floor"]} M choices.',
        f'Remembered-exit choices: {c["remembered_choices"]}; selected: {c["remembered_selected"]}; summed base expectation: {c["remembered_base_expected"]:.3f}; summed final expectation: {c["remembered_final_expected"]:.3f}. These expectations describe the implemented choice bias.',
        '\nZone | C post-move visits | C self-loops | M post-move visits | M self-loops',
        '---|---:|---:|---:|---:']
    for z in range(10):lines.append(f'{z} | {c["occupancy"][z]} | {c["self_loops"][z]} | {m["occupancy"][z]} | {m["self_loops"][z]}')
    lines += ['\n### Frequent Amelia routes','Counts refer to complete typed routes; each listed move includes its edge label.']
    for row in c['top_routes']:
        entry,edges=json.loads(row['route'])
        route='; '.join(f'{e[0]}→{e[1]} ({e[3] or e[2]})' for e in edges)
        lines.append(f'- {row["count"]} occurrences, entry {entry}: {route}')
    if not c['top_routes']:lines.append('No completed boundary routes this week.')
    lines += ['\n### Outcome predictability at lag',
        'Within-episode forward association; plug-in estimates have finite-sample upward bias.',
        '\nLag (moves) | C eligible episodes | C bits | M bits | Reference bits range',
        '---|---:|---:|---:|---:']
    number=lambda v:'undefined' if v is None else f'{v:.4f}'
    for k,v in c['outcome_predictability_at_lag'].items():
        values=[r['arms'][f'R{i:02d}']['outcome_predictability_at_lag'][k]['bits'] for i in range(1,9)]
        ref='undefined' if any(v is None for v in values) else number(min(values))+'–'+number(max(values))
        lines.append(f'{k} | {v["n"]} | {number(v["bits"])} | {number(m["outcome_predictability_at_lag"][k]["bits"])} | {ref}')
    lines += ['\nThe JSON retains detailed measurements for every arm, full route frequencies and reference ranks.',
        '\n## Departures from reference','Strict outside-range flags (descriptive only):']
    for k,v in r['references'].items():
        if v.get('strict_outside'):lines.append(f'- {k}: C={v["value"]}; reference range {v["reference_min"]}–{v["reference_max"]}; tied rank {v["rank_low"]}–{v["rank_high"]}.')
    lines += ['\n## Retrospective reading','These are recorded associations, not an assertion of meaning. Operator interpretations are filed separately.']
    for a,v in r['retrospective'].items():lines.append(f'- {a}: {v["recurring_routes"]} distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.')
    lines += ['\n## Timing','Priority begins only at the verified seal timestamp in seal/receipt.json. No priority is claimed over inputs already available before that time.',*r['limitations']]
    return '\n'.join(lines)+'\n'

def interpretations(engine,source):
    root=engine.root/'interpretations';root.mkdir(parents=True,exist_ok=True)
    index=root/'index';index.mkdir(exist_ok=True)
    entries=sorted(index.glob('*.json'));known={read(p)['sha256'] for p in entries}
    # First-seen packets retain exact original bytes even if the source later changes.
    for f in sorted(Path(source).glob('*')):
        if not f.is_file() or f.name.startswith('.'):continue
        raw=f.read_bytes();h=sha(raw);p=root/h
        if not (p/'prepared.json').exists():
            observed=dict(name=f.name,sha256=h,first_observed_at=engine.clock(),authored_time='operator text only; unverified')
            publish(p/'prepared.json',cj(dict(observed=observed,content_base64=base64.b64encode(raw).decode('ascii'))))
    for p in sorted(root.iterdir()):
        if not p.is_dir() or p.name=='index':continue
        h=p.name
        if h in known:continue
        saved=read(p/'prepared.json')
        raw=base64.b64decode(saved['content_base64'],validate=True)
        if sha(raw)!=h:raise ValueError('interpretation content binding')
        publish(p/'note',raw)
        publish(p/'observed.json',cj(saved['observed']))
        observed=read(p/'observed.json');packet=dict(note_sha256=h,observed_sha256=digest(observed))
        publish(p/'bundle.json',cj(packet))
        receipt=engine.sealer.seal(p/'seal',digest(packet));engine.sealer.verify(p/'seal',digest(packet))
        prev=sha(entries[-1].read_bytes()) if entries else digest(engine.g)
        row=dict(observed,seal_digest=digest(receipt),verified_sealing_time=receipt['comparison_time_unix'],previous=prev)
        target=index/f'{len(entries):08d}.json';publish(target,cj(row));entries.append(target);known.add(h)

    project_journal(index,engine.root/'record/interpretations_index.jsonl')
