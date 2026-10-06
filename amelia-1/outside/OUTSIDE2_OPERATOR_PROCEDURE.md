# OUTSIDE-2 operator procedure

Series: OUTSIDE-2-numogram-reader, version 1.1.0, workings W013–W100 (N = 88).
Registration and protocol: `outside/outside2_registration.json`, `outside/Outside2.py`.
Predecessor closure: `outside/publication_v2_1/OUTSIDE1_V2_1_CLOSURE.json`.

All commands run from `amelia-1/outside`. The branch must not be force-pushed at any point.

## Before W013 (once)

1. Confirm `python3 Outside2.py status` shows `registered: true`, `calibration_gate: true`, `next: W013`.
2. An auditor may re-run `reference` and `calibrate` in a clean copy. Both are deterministic and must
   reproduce `outside2_reference.json` and `outside2_calibration_seal.json` byte for byte.

## Each working

1. **Cast.** The querent holds the question, *what is the scene that will be shown at the close of
   this working?*, and makes 32 physical tosses. Every cast made for a working is admitted; none may
   be discarded or repeated.
2. **Admit.** `python3 Outside2.py cast W### <32 H/T>`. This writes the CAST and READING events
   together and prints the beacon round fixed for the working, about ten minutes ahead.
3. **Publish.** Commit `ledger_outside2.jsonl` and push to the public branch **before** the printed
   round time. A late push is recorded and reported, and never grounds for discarding the working.
4. **Fetch the beacon round** after its time has passed: `python3 Outside2.py beacon W###` prints
   the URL (drand quicknet). Copy the round's `randomness` and `signature`.
5. **Resolve.** `python3 Outside2.py resolve W### <randomness> <signature>`. The script checks that
   the randomness is SHA-256 of the signature and that the round has passed, then computes the
   target. Commit and push.
6. **Feedback.** `python3 Outside2.py feedback W###` gives the target scene and both readings for the
   querent. Arm identity is in the ledger; the feedback order is presentation only.

## Beacon audit

`verify` checks that each recorded randomness is SHA-256 of the recorded signature, which an
invented signature can satisfy. `audit_beacon_outside2.py` establishes that every signature is a
genuine drand quicknet signature for the registered round (BLS verification under the quicknet
public key, which the script shows hashes to the chain hash in the registration), recomputes each
round and target from the protocol rules independently of `Outside2.py`, and with `--online`
compares every round against at least two independent drand relays.

    pip install py_ecc
    python3 audit_beacon_outside2.py --online --json beacon_audit.json

Run it at every intermediate audit and before the final analysis. Exit status 0 means PASS,
1 FAIL, 2 INCOMPLETE (library missing or relays unreachable); only 0 counts as an audit pass.
Publication timing (each READING pushed before its round) is checked separately from the
repository history.

## Rules

- No interim analysis. Target ranks are not written to the ledger, and `analyse` refuses until
  W100 is resolved. No one computes running P1 or P2 by hand.
- Early closure only for a software or apparatus fault demonstrated on synthetic data and
  independently audited; never on outcomes. On any closure, all completed workings are analysed
  and reported.
- `python3 Outside2.py verify` replays every event (seed, both traces, scores, ranks, beacon round,
  target) and should be run before each push.
