"""Offline three-arm runner with atomic tick bundles and fail-closed resume.
Usage: python run_drift.py --output PATH --steps 256 --seed 101
All generated records are engineering-pilot data, ineligible for anomaly claims.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
from drift_core import Substrate, canonical_edges, canonical_json, digest, keyed_uniform, rewire, VERSION, DEFAULTS
from scoring import describe


def atomic_json(path, value):
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('w', encoding='ascii') as f:
        f.write(canonical_json(value))
        f.flush()
        os.fsync(f.fileno())
    os.replace(str(tmp), str(path))
    # Directory sync where supported (Linux desktop/Android).
    fd = os.open(str(path.parent), os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def source_digest():
    root = Path(__file__).parent
    names = ['drift_core.py', 'memory.py', 'run_drift.py', 'scoring.py']
    paths = [root / n for n in names] + sorted((root / 'canonical').glob('*.py')) + [root / 'canonical/canonical_manifest.json']
    return digest({str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})


def run(output, tape, start=1):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    lock = output / 'writer.lock'
    fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    try:
        canonical = canonical_edges()
        control = rewire(canonical)
        # Validate all inputs before mutating trajectory.
        for tick, x in enumerate(tape):
            keyed_uniform(x, tick)
        manifest = dict(version=VERSION, mode='OFFLINE_ENGINEERING_ONLY', anomaly_eligible=False,
                        start=start, tape=tape, tape_digest=digest(tape), source_digest=source_digest(),
                        config=DEFAULTS, canonical_edges=canonical, control_edges=control,
                        control_recipe=dict(seed='DRIFT-1A-G1-20261011', accepted_swaps=100,
                                            preserves='typed degrees; exact self-loops; source labels/weights',
                                            not_preserved='reciprocal syzygies; SCCs; arithmetic destination identities'),
                        reset_scope='all H, before every read; P zone/tick retained')
        mpath = output / 'manifest.json'
        if mpath.exists():
            if json.loads(mpath.read_text()) != manifest:
                raise ValueError('resume manifest differs: refusing changed tape/code/config')
        else:
            if list(output.glob('tick_*.json')):
                raise ValueError('orphaned ticks without manifest')
            atomic_json(mpath, manifest)
        arms = {a: Substrate(control if a == 'G' else canonical, start) for a in ('C', 'G', 'M')}
        head = digest(manifest)
        summaries = {a: [] for a in arms}
        committed = sorted(output.glob('tick_*.json'))
        if len(committed) > len(tape):
            raise ValueError('too many ticks')
        for i, path in enumerate(committed):
            if path.name != 'tick_%06d.json' % i:
                raise ValueError('ledger gap')
            d = json.loads(path.read_text())
            claimed = d.pop('hash')
            if d['previous_hash'] != head or d['tick'] != i or digest(d) != claimed:
                raise ValueError('corrupt ledger')
            # Replay validates dynamics, checksums alone are insufficient.
            u = keyed_uniform(tape[i], i)
            expected = {a: arms[a].advance(u, reset=a == 'M') for a in arms}
            if d['events'] != expected or d['states'] != {a: s.snapshot() for a, s in arms.items()}:
                raise ValueError('replay mismatch')
            for a in arms:
                summaries[a].append(expected[a])
            head = claimed
        for i in range(len(committed), len(tape)):
            u = keyed_uniform(tape[i], i)
            events = {a: arms[a].advance(u, reset=a == 'M') for a in arms}
            body = dict(tick=i, input=tape[i], previous_hash=head, anomaly_eligible=False,
                        events=events, states={a: s.snapshot() for a, s in arms.items()})
            head = digest(body)
            atomic_json(output / ('tick_%06d.json' % i), dict(body, hash=head))
            for a in arms:
                summaries[a].append(events[a])
        result = dict(status='OFFLINE_PILOT_COMPLETE', ticks=len(tape), ledger_head=head,
                      anomaly_eligible=False,
                      measures={a: describe(summaries[a], arms[a].edges) for a in arms},
                      final_states={a: s.snapshot() for a, s in arms.items()})
        atomic_json(output / 'summary.json', result)
        return result
    finally:
        lock.unlink()


def synthetic_tape(seed, n):
    return [hashlib.sha256(('SYNTHETIC|%d|%d' % (seed, i)).encode()).hexdigest() for i in range(n)]


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', required=True)
    p.add_argument('--steps', type=int, default=256)
    p.add_argument('--seed', type=int, default=101)
    p.add_argument('--start', type=int, default=1)
    p.add_argument('--tape', help='JSON array of hex inputs; still OFFLINE, no signature verification')
    a = p.parse_args()
    if a.steps <= 0:
        p.error('steps must be positive')
    tape = json.loads(Path(a.tape).read_text()) if a.tape else synthetic_tape(a.seed, a.steps)
    r = run(a.output, tape, a.start)
    print(canonical_json(dict(status=r['status'], ticks=r['ticks'], ledger_head=r['ledger_head'], anomaly_eligible=False)))
