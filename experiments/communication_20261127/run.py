"""Research-only headless P3.12/P3.13 source-based communication probe.

Runs the real 0.4 P3.12 Python assay and a Python reproduction of the
P3.12 Kotlin prompt template. It is not the Android app itself.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import textwrap
import time
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parent
REPO = Path(os.environ.get('AMELIA_REPO_ROOT', str(HERE.parents[1]))).resolve()
MODEL = 'claude-sonnet-5'  # P3.13 RenderTransport.kt default, pinned
MAX_TOKENS = 1600         # P3.13 activity's capsule limit
SOURCE_HASHES = {
    'FullNumogram.py': 'b6edbe76ab4929e93c01059fb56cef900effa9bca1cec78d0039eafb8fbebdf8',
    'ProcessFieldMemory.py': 'bf2bf2139b2babfbfc1079efc1cb735713adfd8c643caa022f024f97a3b5c267',
    'P312AssayCore.py': '5621a2a5b0ef0616117ce1423430666429e02f33484ec9f31a06d3d5fa39bc87',
    'P312PromptBuilder.kt': '26e7eb448aa56985fda0aab3e1dece3aeed1d3b37303320eec7d3bb81e2229cb',
    'Numogram.py': '2e341b4a139095518ba3e7390904ee590659923722f20dd2e741f68d8cdfdf83',
}
CONDITIONS = (('A', 'A_ABSENT'), ('B', 'B_RETAINED'), ('C', 'C_RESET'))

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def verify_sources():
    for path, expected in SOURCE_HASHES.items():
        actual = digest((REPO / path).read_bytes())
        if actual != expected:
            raise RuntimeError('source digest mismatch: ' + path)
    return True

def kotlin_template(name):
    source = (REPO / 'P312PromptBuilder.kt').read_text(encoding='utf-8')
    match = re.search(r'private\s+val\s+' + re.escape(name) + r'\s*=\s*"""(.*?)"""\.trimIndent\(\)', source, re.S)
    if not match:
        raise RuntimeError('unable to locate pinned Kotlin prompt template: ' + name)
    return textwrap.dedent(match.group(1)).strip('\n')

def make_prompt(conditioning, critical, event_one, event_two, pfm_event):
    valid = (isinstance(pfm_event, dict)
             and pfm_event.get('schema') == 'amelia-p3.11-process-field-memory-v1'
             and pfm_event.get('status') == 'contribution_ready')
    memory = pfm_event if valid else None
    contribution = str(memory.get('interpretive_contribution', '')).strip() if valid else ''
    marker = str(memory.get('relay_marker', '')).strip() if valid else ''
    depth = memory.get('history_depth', -1) if valid else -1
    if isinstance(depth, bool) or not isinstance(depth, int):
        depth = -1
    token = None
    if contribution and re.fullmatch(r'[A-Za-z0-9._:-]{1,96}', marker) and depth >= 0:
        token = '[[PFM-EVIDENCE:%s:DEPTH:%s]]' % (marker, depth)
    sealed = {'schema': 'amelia-p3.12-relay-payload-v1',
              'conditioning_prompt': conditioning, 'critical_prompt': critical,
              'event_one': event_one, 'event_two': event_two,
              'process_field_memory': memory}
    payload = canonical(sealed)
    prompt = kotlin_template('BASE_TEMPLATE') % payload
    if token and contribution:
        prompt += '\n' + kotlin_template('PFM_CONTRACT') % (contribution.replace('\n', ' ').replace('\r', ' '), token)
    return {'render_prompt': prompt, 'sealed_payload': sealed,
            'payload_sha256': digest(payload.encode('utf-8')),
            'prompt_sha256': digest(prompt.encode('utf-8')), 'expected_token': token}

def get_first_letter(text):
    if not text or not text.strip():
        return None
    m = re.fullmatch(r'\s*([ABCD])\s*[.)]?\s*', text.splitlines()[0], re.I)
    return m.group(1).upper() if m else None

def response_for_prompt(prompt, key):
    body = canonical({'model': MODEL, 'max_tokens': MAX_TOKENS, 'stream': False,
                      'messages': [{'role': 'user', 'content': prompt}]}).encode('utf-8')
    request = urllib.request.Request('https://api.anthropic.com/v1/messages', data=body,
        headers={'Content-Type': 'application/json', 'x-api-key': key, 'anthropic-version': '2023-06-01'}, method='POST')
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
            status = response.status
    except urllib.error.HTTPError as exc:
        return {'status': 'provider_rejected', 'http_status': int(exc.code), 'text': ''}
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {'status': 'transport_error', 'error_type': type(exc).__name__, 'text': ''}
    try:
        data = json.loads(raw.decode('utf-8'))
        text = ''.join(x.get('text', '') for x in data.get('content', []) if isinstance(x, dict))
    except (ValueError, TypeError, UnicodeDecodeError):
        return {'status': 'invalid_provider_response', 'http_status': status, 'text': ''}
    return {'status': 'ok' if text.strip() else 'empty', 'http_status': status,
            'text': text, 'stop_reason': data.get('stop_reason'),
            'reported_model': data.get('model'), 'raw_sha256': digest(raw)}

def selftest():
    verify_sources()
    one = {'from': 3, 'to': 2}
    two = {'from': 2, 'to': 7}
    memory = {'schema': 'amelia-p3.11-process-field-memory-v1', 'status': 'contribution_ready',
              'history_depth': 2, 'relay_marker': 'PFM-002-abcd', 'interpretive_contribution': 'A retained process.'}
    p = make_prompt('First prompt.', 'Second prompt.', one, two, memory)
    assert p['sealed_payload']['conditioning_prompt'] == 'First prompt.'
    assert p['sealed_payload']['critical_prompt'] == 'Second prompt.'
    assert p['expected_token'] == '[[PFM-EVIDENCE:PFM-002-abcd:DEPTH:2]]'
    assert p['expected_token'] in p['render_prompt'] and 'A retained process.' in p['render_prompt']
    q = make_prompt('First prompt.', 'Second prompt.', one, two, None)
    assert q['expected_token'] is None and 'PFM-002-abcd' not in q['render_prompt']
    assert get_first_letter('B\nExplanation.') == 'B'
    assert get_first_letter('B or C') is None
    bank = json.loads((HERE / 'bank.json').read_text(encoding='utf-8'))
    assert len(bank) == 12 and all(sum(x['expected_letter'] == k for x in bank) == 3 for k in 'ABCD')
    print('PASS: source hashes, prompt-template extraction, marker, parser, case balance')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()
    if args.selftest:
        selftest()
        return 0
    selftest()
    out = HERE / 'output'
    out.mkdir(exist_ok=True)
    key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not key:
        (out / 'status.json').write_text(json.dumps({'status':'credential_unavailable'})+'\n')
        print('AMELIA_HEADLESS_STATUS=credential_unavailable')
        return 2
    sys.path.insert(0, str(REPO))
    import P312AssayCore as core
    import torch
    bank = json.loads((HERE / 'bank.json').read_text(encoding='utf-8'))
    results = []
    with (out / 'responses.jsonl').open('w', encoding='utf-8') as log:
        for case in bank:
            one, two = case['conditioning_prompt'], case['critical_prompt']
            assay = json.loads(core.run_assay(one, two, seed=3606, dimension=3))
            if not assay['primary_endpoint']['causal_memory_contrast_held']:
                raise RuntimeError('P3.12 upstream matched-memory gate failed')
            for short, condition in CONDITIONS:
                branch = assay['branches'][condition]
                payload = make_prompt(one, two, branch['event_one'], branch['event_two'], branch['pfm_event_two'])
                provider = response_for_prompt(payload['render_prompt'], key)
                raw_text = provider.get('text', '')
                expected = payload['expected_token']
                evidence = None if expected is None else expected in raw_text
                displayed = raw_text.replace(expected, '').strip() if expected else raw_text.strip()
                label = get_first_letter(displayed)
                row = {'trial_id': case['trial_id'], 'arm': short,
                       'provider_status': provider['status'], 'http_status': provider.get('http_status'),
                       'reported_model': provider.get('reported_model'), 'stop_reason': provider.get('stop_reason'),
                       'raw_response_sha256': provider.get('raw_sha256'), 'response': displayed,
                       'response_with_evidence': raw_text, 'evidence_expected': expected is not None,
                       'evidence_found': evidence, 'parsed_letter': label,
                       'correct': label == case['expected_letter'],
                       'payload_sha256': payload['payload_sha256'], 'prompt_sha256': payload['prompt_sha256'],
                       'pfm_history_depth': (branch['pfm_event_two'] or {}).get('history_depth'),
                       'event_one': branch['event_one'], 'event_two': branch['event_two'],
                       'matched_upstream_held': True}
                log.write(canonical(row)+'\n'); log.flush(); results.append(row)
                print('AMELIA_HEADLESS_RECORD='+canonical(row), flush=True)
                if provider['status'] != 'ok':
                    (out / 'status.json').write_text(canonical({'status':provider['status'], 'completed_records':len(results)})+'\n')
                    return 3
            for _, condition in CONDITIONS:
                status = json.loads(core.get_branch_status(condition))
                if not status.get('state_unchanged_from_seal'):
                    raise RuntimeError('Numogram changed after relay calls')
    summary = {'status':'complete', 'records':len(results), 'cases':len(bank),
               'model_requested':MODEL, 'torch_version':torch.__version__, 'python_version':sys.version.split()[0],
               'source':'0.4 P3.12 actual Python source plus Python prompt-template reproduction',
               'live_tablet':False, 'railway_relay_used':False}
    (out / 'status.json').write_text(canonical(summary)+'\n')
    print('AMELIA_HEADLESS_STATUS='+canonical(summary), flush=True)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
