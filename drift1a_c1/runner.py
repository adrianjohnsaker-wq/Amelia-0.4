"""Repository leases prevent an unpersisted hosted run from silently being replaced.

These operational records are outside the scientific ledger. A lease must be
pushed before admission; completion and all new evidence must be pushed together.
An orphaned lease never expires automatically.
"""
import argparse
import time
from pathlib import Path
from .common import cj, digest, publish, read


def claim(root, identifier):
    root = Path(root)
    pending = [p.stem for p in (root / 'leases').glob('*.json')
               if not (root / 'completions' / p.name).exists()]
    if pending:
        raise ValueError('Unreconciled recorder lease(s): ' + ', '.join(sorted(pending)))
    publish(root / 'leases' / (identifier + '.json'),
            cj(dict(workflow_run=identifier, claimed_at=time.time())))


def complete(root, identifier):
    root = Path(root)
    lease = read(root / 'leases' / (identifier + '.json'))
    publish(root / 'completions' / (identifier + '.json'),
            cj(dict(workflow_run=identifier, lease_digest=digest(lease), prepared_at=time.time())))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('action', choices=['claim', 'complete'])
    p.add_argument('identifier')
    p.add_argument('--root', default='drift1a_c1/runner_state')
    a = p.parse_args()
    if not a.identifier or any(c not in '0123456789-' for c in a.identifier):
        p.error('identifier must be a workflow run number and attempt separated by a hyphen')
    (claim if a.action == 'claim' else complete)(a.root, a.identifier)


if __name__ == '__main__':
    main()
