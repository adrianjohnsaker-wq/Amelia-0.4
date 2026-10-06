"""Actions entrypoint: immutable push receipts and RFC3161 responses; synthetic dry run if no new reading."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import urllib.request
from datetime import datetime, timezone
import outside2_timing as T

ROOT = T.HERE.parents[1]
LEDGER = 'amelia-1/outside/ledger_outside2.jsonl'

def api(path):
    req = urllib.request.Request('https://api.github.com/' + path, headers={
        'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
        'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'})
    with urllib.request.urlopen(req, timeout=20) as stream:
        return json.load(stream)

def at_commit(commit):
    if not commit or set(commit) == {'0'}:
        return b''
    exists = subprocess.run(['git', 'cat-file', '-e', commit], cwd=ROOT, capture_output=True)
    if exists.returncode:
        raise RuntimeError('push base commit unavailable; refusing to infer new readings')
    files = subprocess.check_output(['git','ls-tree','--name-only',commit,'--',LEDGER],cwd=ROOT)
    return subprocess.check_output(['git','show',commit+':'+LEDGER],cwd=ROOT) if files.strip() else b''

def write_once(path, obj):
    if not path.exists():
        with path.open('x') as f:
            json.dump(obj, f, indent=2, sort_keys=True)
            f.write('\n')

def main():
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    commit = os.environ['GITHUB_SHA']
    repo = os.environ['GITHUB_REPOSITORY']
    runid = os.environ['GITHUB_RUN_ID']
    before = event.get('before')
    old, new = at_commit(before), at_commit(commit)
    if not new.startswith(old):
        raise RuntimeError('ledger is not append-only relative to push base')
    readings = [e for line in new[len(old):].splitlines() if (e := json.loads(line)).get('event_type') == 'READING']
    if os.environ.get('GITHUB_EVENT_NAME') != 'push':
        readings = []  # manual runs are synthetic only; never claim a manual run was a push
    reg = json.loads((T.HERE/'outside2_registration.json').read_text())
    # Request timestamps before slower GitHub event-feed lookups.
    pending = []
    if not readings:
        name = 'DRY_RUN_' + runid
        folder = T.TIMING/'dry_runs'
        digest = hashlib.sha256(('OUTSIDE-2 TIMING DRY RUN:'+commit+':'+runid).encode()).hexdigest()
        pending = [(name, digest, time.time()+600, None, folder)]
    else:
        for e in readings:
            if not __import__('re').fullmatch(r'W\d{3}', e['working']):
                raise ValueError('invalid working')
            pending.append((e['working'],e['event_hash'],T.deadline(e,reg),e,T.TIMING))
    captured = []
    for name,digest,end,reading,folder in pending:
        folder.mkdir(parents=True,exist_ok=True)
        try:
            response=T.obtain_token(folder/name,digest)
            result=T.verify_token(response,digest,end)
        except Exception as exc:
            result={'status':'INCOMPLETE','reason':str(exc)}
        captured.append((name,digest,end,reading,folder,result))
    run, matching, errors = None, None, []
    try:
        run=api('repos/'+repo+'/actions/runs/'+runid)
    except Exception as exc:
        errors.append('run API: '+str(exc))
    # Event feed may lag. The run creation time remains a separately labelled upper bound.
    try:
        for page in range(1,4):
            events=api('repos/'+repo+'/events?per_page=100&page='+str(page))
            matching=next((e for e in events if e.get('type')=='PushEvent'
                and (e.get('payload',{}).get('head')==commit or e.get('payload',{}).get('after')==commit)
                and e.get('payload',{}).get('ref')==os.environ['GITHUB_REF']),None)
            if matching or len(events)<100: break
    except Exception as exc:
        errors.append('events API: '+str(exc))
    for name,digest,end,reading,folder,result in captured:
        push_time=matching.get('created_at') if matching else None
        run_time=run.get('created_at') if run else None
        record={'schema':'OUTSIDE-2-push-timing-1','reading_event_hash':digest,
                'synthetic':reading is None,'pushed_commit':commit,'ref':os.environ['GITHUB_REF'],
                'run_id':runid,'captured_utc':datetime.now(timezone.utc).isoformat(),
                'beacon_deadline_unix':end,'reading':reading,'tsa':result,
                'github_timing':{'push_event_created_at':push_time,
                    'push_before_deadline':T.utc(push_time)<end if push_time else None,
                    'run_created_at':run_time,
                    'run_created_before_deadline':T.utc(run_time)<end if run_time else None,
                    'note':'run creation is a server-side upper bound on push time, not an exact push time'},
                'push_webhook_payload':event,'repository_push_event':matching,
                'workflow_run_api':run,'api_errors':errors}
        write_once(folder/(name+'_PUSH.json'),record)
        print(name,result['status'],json.dumps(record['github_timing']),flush=True)
    return 0 if all(x[-1]['status']=='PASS' for x in captured) else 1

if __name__=='__main__':
    raise SystemExit(main())
