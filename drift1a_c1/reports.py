"""Immutable weekly reports; rendering can evolve, measurement code is frozen."""
import base64
import hashlib
import json
from pathlib import Path
from .common import cj,digest,sha,publish,read,week,project_journal
from .beacon import round_time
from .metrics import summarize,ranks,flag_summary,retrospective as route_history,VERSION,CLASSES,PRIMARY_KEYS,leave_one_out_flags
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
            retrospective=route_history(arms,earlier,w)
            references=ranks(arms)
            for arm,measurements in arms.items():
                diagnostic=measurements['boundary_entry_diagnostic']
                if diagnostic['status']=='FAIL':
                    engine.incident('canonical_boundary_entry_diagnostic',
                        dict(week=w,arm=arm,diagnostic=diagnostic),engine.g['R0']+20*engine.tick)
            records_digest,last=week_record_digest(engine.records(),w)
            report=dict(version='C1-report-0.4-A12-render',mode=engine.g['mode'],week=w,genesis_digest=digest(engine.g),
                measurement_version=VERSION,generated_at=engine.clock(),last_included_round=last['beacon']['round'],
                last_included_round_time=last['round_time'],records_digest=records_digest,
                renderer_sha256=sha(Path(__file__).read_bytes()),arms=arms,references=references,flags=flag_summary(references,earlier),leave_one_out_flags=leave_one_out_flags(arms),retrospective=retrospective,
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
    number=lambda v:'undefined' if v is None else (str(v) if type(v) is int else f'{v:.5g}')
    lines=[f'# Amelia C1 — {r["week"]} — amendments 7–12 (report layout)',
        f'Mode: {r["mode"]}. Observational and exploratory. Traversal episodes are the primary interpretation class.',
        f'Renderer SHA-256 (reports.py): `{r["renderer_sha256"]}`.',
        '',
        'C against M isolates the effect of carried memory under the same inflow. C against R01–R08 isolates what this particular inflow does that other inflows of the same kind, passed through the same instrument with carried memory, do not.',
        '',
        'Because the reference tapes are keyed hashes of the same rounds, standard cryptographic assumptions predict no systematic departure of C from the references; that is the null against which any persistent departure is read.',
        '\n## A. Form — canonical graph versus rewired controls (channel A only)',
        'Form is shared by every arm on the canonical graph, whatever its inflow. It bears on the Numogram\'s structure, not on any inflow.',
        'This section describes determinacy horizon, zone-1 dwell, Warp/Plex outcomes and route lengths. G controls belong only to channel A.',
        '\n### Process history',
        'Completed episodes are assigned to their ending week, including full lengths of cross-week episodes. Tick statistics use the class of the episode active on that tick. Occupancy divides by that class’s weekly ticks. Routes include cap endings.']
    for cl in CLASSES:
        lines += [f'\n### {cl.replace("_"," ")}',
            '\nArm | Completed | Warp | Plex | Cap | Warp fraction | Boundary endings / class tick | Mean length | Distinct routes',
            '---|---:|---:|---:|---:|---:|---:|---:|---:']
        for a,m in r['arms'].items():
            c=m['episode_classes'][cl]
            lines.append(f'{a} | {c["completed"]} | {c["warp"]} | {c["plex"]} | {c["cap"]} | {number(c["warp_fraction"])} | {number(c["boundary_ending_rate"])} | {number(c["mean_completed_length"])} | {c["distinct_routes"]}')
        c=r['arms']['C']['episode_classes'][cl]
        lengths=', '.join(f'{k}: {v}' for k,v in sorted(c['length_distribution'].items(),key=lambda kv:int(kv[0]))) or 'none'
        lines += [f'\nC length distribution (moves: episodes): {lengths}.',f'C unfinished episode at week end: {json.dumps(c["unfinished"])}.','\nC frequent typed routes:']
        for row in c['top_routes']:
            entry,edges=json.loads(row['route']);route='; '.join(f'{e[0]}→{e[1]} ({e[3] or e[2]})' for e in edges)
            lines.append(f'- {row["count"]} occurrences, entry {entry}: {route}')
        if not c['top_routes']:lines.append('- None.')
    lines += ['\n### Canonical boundary-entry diagnostic', 'Every completed canonical boundary-entry episode must have length 1 and the outcome fixed by entry: 0/9 → Plex; 3/6 → Warp. G arms are not subject to this diagnostic.']
    for a,m in r['arms'].items():
        d=m['boundary_entry_diagnostic']
        lines.append(f'- {a}: {d["status"]}; checked {d["checked"]}; failures {len(d["failures"])}. Unfinished: {json.dumps(m["unfinished"])}.')
    lines += ['\n### Outcome predictability',
        'This quantity is within-episode forward association, not evidence of external anticipation. Traversal boundary endings are primary; all boundary endings are secondary. Miller–Madow estimates are signed and are not clipped to zero. A lag with n < 50 is insufficient. Values within the permutation null are reported as indistinguishable from zero.',
        'B = 200; null 95th percentile uses nearest rank; ≥ proportion is the number of permuted plug-in values at least as large as observed divided by 200. The JSON contains every arm’s values and exact seed.']
    for cl in ('traversal','all'):
        lines += [f'\n### {cl} series: C and M',
            '\nArm | Lag | n | Plug-in bits | MM bits | Null 95% bits | ≥ proportion | Interpretation',
            '---|---:|---:|---:|---:|---:|---:|---']
        for a in ('C','M'):
            for k,v in r['arms'][a]['episode_classes'][cl]['outcome_predictability_at_lag'].items():
                lines.append(f'{a} | {k} | {v["n"]} | {number(v["bits"])} | {number(v["miller_madow_bits"])} | {number(v["null_95_bits"])} | {number(v["permutation_ge_proportion"])} | {v["interpretation"]}')
    lines += ['\n## B. Memory — matched inflow, C versus M',
        'C and M receive identical inflow. C carries memory; M resets it before each choice. This is a memory contrast, not evidence of Outside access.',
        'Compare the C and M rows above for outcome predictability and process history; full memory activity is archived in the JSON.']
    f=r['flags']
    lines += ['\n## C. Signal — C versus eight canonical reference arms (channel A)',
        'Only Signal bears on the proposed Outside hypothesis; it is exploratory and not a registered hypothesis test.',
        '\n### Declared comparisons and cross-week tally',
        f'N = {f["N"]} declared statistics; {f["N_compared"]} comparable this week; F = {f["F"]} flagged. Expected flags under exchangeability without ties: 2N/9 = {f["expected_flags"]:.4f}; for the comparable subset: {f["expected_flags_comparable"]:.4f}.',
        f['dependence'],f['ties'],
        'Self-loop counts at 0, 3 and 9 use boundary-entry episodes; zone 1 uses traversal episodes. Zone occupancy 0 is descriptive only.',
        'An unavailable statistic is not flagged and does not count as a compared week. The table gives flagged / compared weeks and expectation 2/9 per compared week; JSON also gives total reported weeks. Persistent departures across weeks are the pattern of interest; a single week’s flag is not.',
        '\nStatistic | C | R range | Tied rank | Flag | Weeks flagged / compared | Expected',
        '---|---:|---|---|---|---|---:']
    for k in PRIMARY_KEYS:
        v=r['references'][k];t=f['cross_week'][k]
        span='unavailable' if v['status']=='undefined' else f'{number(v["reference_min"])}–{number(v["reference_max"])}'
        rank='unavailable' if v['status']=='undefined' else f'{v["rank_low"]}–{v["rank_high"]}'
        lines.append(f'{k} | {number(v.get("value"))} | {span} | {rank} | {"YES" if v["strict_outside"] else "—"} | {t["weeks_flagged"]}/{t["weeks_compared"]} | {t["expected_flags"]:.3f}')
    lines += ['\nLeave-one-out flag counts (each arm against the other eight; descriptive empirical comparison, not an independent null sample):', '\nArm | F | Comparable', '---|---:|---:']
    for a,v in r['leave_one_out_flags'].items():lines.append(f'{a} | {v["F"]} | {v["N_compared"]}')
    lines += ['\nAll other values, including eligible counts, visit sums and route novelty/rarity ranks, are derived descriptions and are never flagged.',
        '\n### Traversal route novelty, rarity and recurrence',
        'Counts are distinct typed routes; rates are per 100 completed traversal episodes. Reference rarity is leave-one-out among C and R01–R08, with occurrence in at most one of the other eight arms. It is not defined for M or G. Recurring rare routes were rare at first appearance, not merely rare now.',
        '\nArm | Novel | Novel / 100 | Reference-rare | Rare / 100 | Recurring rare this week',
        '---|---:|---:|---:|---:|---:']
    for a,v in r['retrospective'].items():
        lines.append(f'{a} | {v["novel_count"]} | {number(v["novel_per_100_episodes"])} | {number(v["reference_rare_count"])} | {number(v["reference_rare_per_100_episodes"])} | {v["recurring_rare_this_week"]}')
    lines += ['\nC descriptive ranks among nine canonical memory-carrying arms:']
    for key,v in r['retrospective']['C']['ranks_among_nine'].items():
        lines.append(f'- {key}: '+('undefined' if v['status']=='undefined' else f'{v["rank_low"]}–{v["rank_high"]}')+'.')
    for a,v in r['retrospective'].items():
        if v['comparisons']:
            lines.append(f'\n{a} traversal-route Jensen–Shannon divergence:')
            for old,x in v['comparisons'].items():lines.append(f'- Against {old}: {number(x["js_divergence_bits"])+" bits" if x["status"]=="sufficient" else "insufficient (requires 50 traversal episodes in both weeks)"}; seal `{x["prior_seal_digest"]}`.')
        if v['recurring_rare_routes']:
            lines.append(f'\n{a} recurring rare routes:')
            for x in v['recurring_rare_routes']:
                lines.append(f'- Typed route `{x["route"]}`; first week {x["first_week"]}; recurrence weeks {", ".join(x["recurrence_weeks"])}; first seal `{x["first_seal_digest"]}`.')
    lines += ['\nFull class-specific length distributions, routes, memory activity, occupancy and lag statistics for every arm are retained in JSON.',
        '\n## Timing','Priority begins only at the verified seal timestamp in seal/receipt.json. No priority is claimed over inputs already available before that time.',*r['limitations']]
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
