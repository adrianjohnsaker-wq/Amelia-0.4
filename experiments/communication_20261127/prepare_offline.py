"""Pre-render only: use pinned 0.4 P3.12 source to seal all 12 A/B/C inputs.

There are no provider requests, credentials or mutations to the live app.
"""
import hashlib,json,sys
from pathlib import Path
import run as harness

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
sys.path.insert(0,str(REPO))
import P312AssayCore as core

def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def main():
    harness.selftest()
    bank=json.loads((HERE/'bank.json').read_text(encoding='utf-8'))
    out=HERE/'offline_output';out.mkdir(exist_ok=False)
    rows=[];summary=[]
    with (out/'sealed_inputs.jsonl').open('w',encoding='utf-8') as f:
        for case in bank:
            first,second=case['conditioning_prompt'],case['critical_prompt']
            result=json.loads(core.run_assay(first,second,seed=3606,dimension=3))
            if not result['primary_endpoint']['causal_memory_contrast_held']:
                raise RuntimeError('matched Numogram/PFM gate failed')
            events=[]
            for arm,condition in harness.CONDITIONS:
                branch=result['branches'][condition]
                packet=harness.make_prompt(first,second,branch['event_one'],branch['event_two'],branch['pfm_event_two'])
                status=json.loads(core.get_branch_status(condition))
                if not status['state_unchanged_from_seal']:
                    raise RuntimeError('Numogram changed before rendering')
                row={'trial_id':case['trial_id'],'arm':arm,'expected_letter':case['expected_letter'],
                     'prompt':packet['render_prompt'],'prompt_sha256':packet['prompt_sha256'],
                     'payload_sha256':packet['payload_sha256'],'expected_token':packet['expected_token'],
                     'event_one':branch['event_one'],'event_two':branch['event_two'],
                     'memory_depth':(branch['pfm_event_two'] or {}).get('history_depth'),
                     'numogram_sealed_digest':branch['sealed_system_digest']}
                rows.append(row);f.write(canonical(row)+'\n');f.flush()
                print('AMELIA_SEALED_PAYLOAD='+canonical(row),flush=True)
                events.append({'arm':arm,'memory_depth':row['memory_depth'],'first':branch['event_one']['to'],
                               'second':branch['event_two']['to']})
            summary.append({'trial_id':case['trial_id'],'upstream_gate':True,'conditions':events})
    result={'status':'ready_for_authorized_provider_execution','cases':len(bank),'sealed_inputs':len(rows),
            'source':'0.4 P3.12 Python with P3.12 Kotlin prompt-template reproduction',
            'provider_calls':0,'live_tablet':False,'all_upstream_gates':all(x['upstream_gate'] for x in summary),
            'cases_summary':summary}
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print('AMELIA_UPSTREAM_SUMMARY='+canonical(result),flush=True)
if __name__=='__main__':main()
