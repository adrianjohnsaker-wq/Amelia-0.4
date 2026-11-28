#!/usr/bin/env python3
"""Known controlled signal source. The private target is not an unknown mind."""
import hashlib
import json
import secrets
import sys

WORDS = ("qevral", "lumeth", "sorvak", "tivren")
CASES = 12
STEPS = 8


def commitment(case_id, goal, salt):
    return hashlib.sha256((case_id + "|" + str(goal) + "|" + salt).encode("utf-8")).hexdigest()


def main():
    cases = {}
    locked = False
    for line in sys.stdin:
        try:
            command = json.loads(line)
            action = command["op"]
            if action == "init":
                assert not locked
                cid = command["case_id"]
                assert isinstance(cid, str) and cid not in cases and len(cases) < CASES
                goal, salt = secrets.randbelow(4), secrets.token_hex(16)
                cases[cid] = {"goal": goal, "salt": salt, "steps": 0}
                result = {"ok": True, "case_id": cid, "commitment": commitment(cid, goal, salt)}
            elif action == "step":
                assert not locked
                cid = command["case_id"]
                c = cases[cid]
                challenge = int(command["challenge"])
                assert 0 <= challenge < 4 and c["steps"] < STEPS
                c["steps"] += 1
                result = {"ok": True, "case_id": cid, "step": c["steps"],
                          "message": WORDS[(c["goal"] + challenge) % 4]}
            elif action == "lock":
                assert not locked and len(cases) == CASES
                assert all(c["steps"] == STEPS for c in cases.values())
                digest = command["decisions_sha256"]
                assert isinstance(digest, str) and len(digest) == 64 and all(x in "0123456789abcdef" for x in digest)
                locked = True
                result = {"ok": True, "locked_decisions_sha256": digest,
                          "reveals": {cid: {"goal": c["goal"], "salt": c["salt"]} for cid, c in cases.items()}}
            else:
                raise ValueError("unsupported operation")
        except Exception as exc:
            result = {"ok": False, "error": type(exc).__name__}
        print(json.dumps(result, separators=(",", ":")), flush=True)
        if locked:
            return


if __name__ == "__main__":
    main()
