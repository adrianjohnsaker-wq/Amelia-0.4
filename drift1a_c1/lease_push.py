"""Durable C1 lease acquisition. No admission until a pushed lease is confirmed.

Retry concurrent non-fast-forward updates by rebasing, never discarding a lease.
Any unresolved lease on the authoritative branch stops acquisition.
"""
import argparse
import subprocess
from pathlib import Path
from drift1a_c1.runner import claim

def git(*args):
    return subprocess.run(["git", *args], text=True, capture_output=True)

def acquire(identifier, remote="origin", branch="amelia-1.0", attempts=3):
    if attempts != 3:
        raise ValueError("C1 lease protocol requires exactly three attempts")
    fetch = git("fetch", remote, branch)
    if fetch.returncode:
        raise RuntimeError("Cannot fetch authoritative state: " + fetch.stderr)
    # This must start clean: no scientific or evidence changes can be discarded.
    if git("status", "--porcelain").stdout.strip():
        raise RuntimeError("Working tree not clean before lease acquisition")
    checkout = git("checkout", "-B", "c1-lease-local", "FETCH_HEAD")
    if checkout.returncode:
        raise RuntimeError(checkout.stderr)
    claim(Path("drift1a_c1/runner_state"), identifier)
    for cmd in [("add", "--", "drift1a_c1/runner_state"),
                ("commit", "-m", "C1: acquire recorder lease " + identifier)]:
        r = git(*cmd)
        if r.returncode:
            raise RuntimeError("Lease preparation failed: " + r.stderr)
    for attempt in range(1, attempts + 1):
        push = git("push", remote, "HEAD:" + branch)
        if push.returncode == 0:
            return {"status": "PUSHED", "attempts": attempt, "admission_authorized": True}
        if attempt == attempts:
            break
        fetch = git("fetch", remote, branch)
        if fetch.returncode:
            # A failed fetch cannot justify admission.
            continue
        rebased = git("rebase", "FETCH_HEAD")
        if rebased.returncode:
            git("rebase", "--abort")
            raise RuntimeError("Lease rebase conflict: no admission")
    raise RuntimeError("Lease push failed after three attempts: no admission")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("identifier")
    args = p.parse_args()
    print(acquire(args.identifier))

if __name__ == "__main__":
    main()
