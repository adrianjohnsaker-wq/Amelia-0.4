"""RFC 3161 evidence for OUTSIDE-2; never changes the registered apparatus."""
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import urllib.request
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
TRUST = HERE / 'timing_trust' / 'freetsa-ca.pem'
TSA_URL = 'https://freetsa.org/tsr'
TIMING = HERE / 'publication_outside2' / 'timing'

def command(args):
    return subprocess.run(args, capture_output=True, check=True, timeout=40).stdout

def utc(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()

def deadline(reading, registration):
    beacon = registration['beacon']
    # Independently implements the registered rule, rather than trusting payload time.
    rnd = math.ceil((utc(reading['created_utc']) + 600 - beacon['genesis_time']) / beacon['period']) + 1
    if reading['payload']['beacon_round'] != rnd:
        raise ValueError('reading beacon round does not match registered time rule')
    return beacon['genesis_time'] + (rnd - 1) * beacon['period']

def verify_token(response, digest, before, ca=TRUST):
    """Offline chain/signature/imprint verification, with certificate validity at token time.

    The explicitly supplied CA parameter is for synthetic tests. Production uses the
    repository-pinned FreeTSA root, never a root supplied by the timestamp response.
    No online revocation or long-term archival renewal is claimed.
    """
    response = Path(response)
    if not response.exists():
        return {'status': 'INCOMPLETE', 'reason': 'timestamp response missing'}
    try:
        from asn1crypto import tsp
        if not re.fullmatch('[0-9a-f]{64}', digest):
            raise ValueError('invalid reading event hash')
        info = tsp.TimeStampResp.load(response.read_bytes(), strict=True)
        if info['status']['status'].native not in ('granted', 'granted_with_mods'):
            raise ValueError('TSA did not grant request')
        content = info['time_stamp_token']['content']['encap_content_info']['content'].parsed
        imprint = content['message_imprint']
        if imprint['hash_algorithm']['algorithm'].native != 'sha256' or imprint['hashed_message'].native.hex() != digest:
            raise ValueError('timestamp imprint differs from reading event hash')
        generated = content['gen_time'].native
        accuracy = content['accuracy'].native
        declared_accuracy = accuracy is not None
        accuracy = accuracy or {}
        uncertainty = (accuracy.get('seconds') or 0) + (accuracy.get('millis') or 0)/1000 + (accuracy.get('micros') or 0)/1000000
        command(['openssl', 'ts', '-verify', '-in', str(response), '-digest', digest,
                 '-CAfile', str(ca), '-attime', str(int(generated.timestamp()))])
        upper = generated.timestamp() + uncertainty
        return {'status': 'PASS' if upper < before else 'FAIL',
                'reason': 'signed issuance time (plus declared accuracy, if any) must precede beacon',
                'accuracy_declared': declared_accuracy,
                'gen_time': generated.isoformat(), 'accuracy_seconds': uncertainty,
                'comparison_time_unix': upper, 'deadline_unix': before,
                'response_sha256': hashlib.sha256(response.read_bytes()).hexdigest(),
                'trust_anchor_sha256': hashlib.sha256(Path(ca).read_bytes()).hexdigest()}
    except (ImportError, FileNotFoundError) as exc:
        return {'status': 'INCOMPLETE', 'reason': str(exc)}
    except Exception as exc:
        return {'status': 'FAIL', 'reason': str(exc)}

def obtain_token(stem, digest):
    """Never replace an existing response; retain request nonce and complete signed response."""
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    query, response = stem.with_suffix('.tsq'), stem.with_suffix('.tsr')
    if response.exists():
        return response
    if not query.exists():
        query.write_bytes(command(['openssl', 'ts', '-query', '-sha256', '-digest', digest, '-cert']))
    request = urllib.request.Request(TSA_URL, data=query.read_bytes(), headers={
        'Content-Type': 'application/timestamp-query', 'Accept': 'application/timestamp-reply'})
    with urllib.request.urlopen(request, timeout=30) as stream:
        raw = stream.read(1024 * 1024)
    with response.open('xb') as output:
        output.write(raw)
    return response

def audit_readings(events, registration, directory=TIMING):
    results = {}
    for event in events:
        if event.get('event_type') != 'READING':
            continue
        w = event['working']
        if not re.fullmatch(r'W\d{3}', w) or w in results:
            results[w] = {'status': 'FAIL', 'reason': 'invalid or duplicate reading'}
            continue
        try:
            end = deadline(event, registration)
            row = verify_token(Path(directory) / (w + '.tsr'), event['event_hash'], end)
            receipt = Path(directory) / (w + '_PUSH.json')
            if receipt.exists():
                data = json.loads(receipt.read_text())
                if data.get('reading_event_hash') != event['event_hash']:
                    row = {'status': 'FAIL', 'reason': 'push receipt bound to another reading'}
                else:
                    row['github_push_evidence'] = data.get('github_timing')
            else:
                row['github_push_evidence'] = 'INCOMPLETE: push receipt absent'
                if row['status'] == 'PASS':
                    row['status'] = 'INCOMPLETE'
            results[w] = row
        except Exception as exc:
            results[w] = {'status': 'FAIL', 'reason': str(exc)}
    return results
