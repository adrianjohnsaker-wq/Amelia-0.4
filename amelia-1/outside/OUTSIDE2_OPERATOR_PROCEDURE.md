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

## Queue runner (from W020)

From W020 the per-working procedure is automated by `.github/workflows/outside2-queue.yml`.
The querent still performs the physical 32-toss cast while holding the registered question.
The repository request commit may be made directly by the querent or by a connected assistant
acting on the querent's explicit instruction. These are separate acts: the request receipt records
the request file/line and its Git commit provenance, while the cast itself remains the querent's act.

1. Put one or more consecutive casts in a text file under
   `amelia-1/outside/admission_requests/` using the format documented in that folder.
   A connected assistant may create and push this file when explicitly instructed by the querent.
2. That request commit starts the serialized queue. For each working, the runner calls the
   registered `Outside2.cast`, obtains and verifies an RFC 3161 timestamp for the READING hash,
   publishes the ledger and timestamp, and immediately publishes a request-bound admission receipt.
3. After the registered beacon time, the runner requires at least two reachable drand relays,
   requires every reachable relay to agree, verifies the BLS signature under the registered
   quicknet key, then calls the registered `Outside2.resolve`.
4. It replays the ledger and publishes relay responses, `W###_VERIFY.json`, and
   `W###_FEEDBACK.json`. A partial run is restart-safe: an admitted unresolved working and any
   missing admission receipt are handled before a new cast.
5. At run end it publishes `publication_outside2/batches/BATCH_<run>.json`. The file reports a
   batch verdict for workings handled in that run separately from the cumulative audit verdict,
   so the historical W015 timing gap does not turn a clean later batch into a false failure.
6. Any failed check halts before the next causal step and publishes `INCIDENT_<run>.json`.
   Nothing admitted is discarded. No ranks, P1, P2 or other interim test statistics are computed.

Queued internal pushes use GitHub's workflow token. GitHub suppresses recursive ordinary
push-workflow triggering for those writes, so the older push-capture workflow is not relied upon
for W020 onward. The queue's own RFC 3161 token, admission receipt, relay record, replay
verification and batch audit are the evidence path for queued workings.

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

## Push-time evidence and RFC 3161 audit (before W013)

The `OUTSIDE-2 push capture and trusted timestamp` workflow captures ledger pushes on
`amelia-1.0`. It requests a FreeTSA timestamp immediately after startup, then archives
GitHub's push webhook payload, matching repository PushEvent (if available), workflow-run
API response, pushed commit, reading hash and beacon deadline. Evidence lives in
`publication_outside2/timing/W###_PUSH.json`, `W###.tsq` and `W###.tsr`.
The complete TSR contains the signed token and included signing certificate chain.
The trust root is fixed in `timing_trust/freetsa-ca.pem`; a response cannot nominate a new root.

1. Publish this workflow before W013 and confirm its automatic synthetic dry run passes.
   Setup-code pushes with no new readings run a dummy-hash check and archive it under
   `timing/dry_runs/`. Manual runs are also synthetic only. These never write the ledger.
2. Push each CAST/READING promptly. Wait for the capture run and its evidence commit.
   Runner queues or TSA/network delays can make a token late: report this as FAIL,
   retain the working, and never recast. Missing tokens are INCOMPLETE, never PASS.
3. Install `pip install -r requirements-audit.txt` and run
   `python3 audit_beacon_outside2.py --online --json beacon_audit.json`.
   Timing verification itself is offline, using OpenSSL. It also audits unresolved readings.
4. Preserve failed-run artifacts if the evidence commit cannot be pushed. Do not overwrite
   earlier receipts or tokens. Every run uploads evidence before attempting its branch commit.

The timestamp imprint is the reading's SHA-256 event hash (the canonical event body digest),
not the hash of its hexadecimal spelling. OpenSSL verifies the signature, SHA-256 imprint,
TSA certificate purpose and chain against the fixed root, at the signed issuance time.
That time, plus any explicitly declared TSA accuracy, must be strictly before the beacon
round. If the TSA omits accuracy, the report says so and compares its signed time only.
This trusts the TSA's clock; it does not establish a numerical error bound when absent.
Offline validation does not assert current revocation status or indefinite archival validity.

GitHub event-feed records may lag. An absent matching PushEvent is explicitly recorded;
workflow `created_at` is a separate server-side upper bound, never called an exact push time.
Neither commit author time nor committer time is accepted as publication time. Archived
GitHub JSON preserves the server assertion but is not independently signed by GitHub.
A timestamp proves existence of the committed reading, not its public availability.
The two evidence layers must be described separately.

For the W013-W019 push-capture path, do not publish ledger changes with a workflow's default
`GITHUB_TOKEN`, because GitHub suppresses subsequent ordinary push workflows for those writes.
From W020 the queue runner is the explicit exception: it creates and verifies its own RFC 3161
evidence before/alongside its internal token-authenticated pushes and does not depend on recursive
execution of the older capture workflow. Avoid skip-CI commit annotations.

The admission rule still covers undisclosed casts; neither timestamping nor GitHub history
proves that no unpublished alternative cast occurred. None of these changes modifies
Outside2.py, its registration, reference distributions or calibration seal.
