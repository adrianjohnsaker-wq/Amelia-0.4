# Amelia: DRIFT-1A-C1 continuous observation

C1 keeps the accepted G1.1 Numogram instrument running with memory across episodes. It records a verified external input every minute and produces sealed weekly accounts for interpretation. This is exploratory observation, not a registered hypothesis test or evidence of an Outside connection.

**Delivery status: live operation disabled; no genesis or live rounds consumed.** The Android G1.1 pilot and its saved runs are unchanged. The continuous recorder runs on GitHub; its Markdown reports can be read on a phone.

The [charter](../claude/DRIFT1A_C1_CHARTER_draft.md) incorporates the six approved amendments. Genesis freezes its exact bytes, the accepted substrate, admission and measurement code, graph definitions, dependencies and trust material. Report rendering may evolve; every report identifies its renderer hash. Changing a frozen file halts an existing run.

## What runs

There are 18 arms: Amelia C, the fully reset M, eight degree-matched graph controls, and eight transformed-tape references. C/M/G share each tick's keyed ingress and transition variates. R arms use the explicitly specified SHA-256 tape transformations. Shared ingress *proposals* do not imply simultaneous episode starts: each arm enters only when its own prior episode ended.

Every tick makes one legal graph move. The common boundary is `{0,3,6,9}` and the episode cap is 1,260 moves. C/G/R preserve history between episodes; M clears all selector and classifier history before each choice. The G1.1 implementation is imported, not rewritten.

The inflow is one cryptographically verified quicknet round out of every 20. An hourly workflow catches up in round order, at most 120 ticks per invocation. It never substitutes randomness or skips a missing round. Delayed scheduling changes recorded reception lag, not selected input rounds. GitHub cron is best effort, not a minute-by-minute real-time receiver.

## Offline validation

Python 3.12.14 and OpenSSL are used by the workflow. From the repository root:

```bash
python -m venv .venv-c1
.venv-c1/bin/pip install -r drift1a_c1/requirements.txt
.venv-c1/bin/python -m unittest discover -s drift1a_c1/tests -v
.venv-c1/bin/python -m drift1a_c1.simulate --root /tmp/amelia-c1-simulation
```

Use a fresh simulation directory. The default simulation runs 10,082 ticks per arm across three ISO week labels, including one complete week. It exercises an outage, restart, an abandoned temporary file, exact replay, weekly reporting and interpretation deduplication. Its seals say `SIMULATED_NOT_RFC3161`; it never supplies live evidence. Cryptographic tests separately use a known-answer quicknet signature and a local test RFC 3161 authority, including rejection cases.

The `Amelia C1 continuous observation` workflow's **validate** action runs these checks and uploads an evidence artifact. A local simulation may take tens of minutes. The accepted G1.1 tests are also run in CI.

## Live activation, after reviewing the charter and evidence

The workflow must exist on **main** for its hourly schedule; it checks out **amelia-1.0**, where all code, state and reports live. Installation alone starts no experiment.

1. Set the repository Actions variable `DRIFT_C1_ENABLE_LIVE` to the exact string `true`.
2. Manually dispatch `Amelia C1 continuous observation` from `main`, selecting **genesis**. Genesis is never created by the scheduled **run** action.
3. Check the successful genesis receipt and pinned source/graph digests. Its RFC 3161 seal must precede R0's publication; otherwise the attempt is retained and no run is admitted.
4. The hourly **run** action then resumes the next eligible round. It may also be dispatched manually. Set the variable to `false` to pause; restoring it resumes the same sequence and records lag.

Live genesis requires working drand and FreeTSA services. The FreeTSA root is pinned. A recorded drand round at sealing is contextual information; it is not an independent timestamp service. Only a verified RFC 3161 token establishes the stated seal time, with its accuracy allowance.

Do not delete or recreate `recorded_live/genesis.json` to recover a run. Do not modify frozen files underneath an active run. A new protocol needs a separately identified genesis.

## Records and recovery

`recorded_live/record/chunks/` contains immutable, hash-linked gzip transactions, split at ISO week boundaries. Each transaction includes all admitted signed beacons, all arm events and all final arm checkpoints. A chunk is atomically published before it becomes the durable cursor. Failed batches resume from the last committed chunk; unpublished temporary files have no authority.

Before admission, the workflow pushes an operational lease to `runner_state/`. Its completion marker and new evidence are then committed together. An unfinished lease blocks subsequent hosted runs; it never expires automatically. The workflow uploads a state artifact **before** attempting that final push. A push/rebase failure is visible as a failed workflow. Preserve and reconcile that artifact, especially if it contains a genesis or seal absent from the branch, then append the lease completion with the recovered evidence. If the worker never reached admission, document that fact before completing its lease. Never force-push competing observation histories.

For a full offline audit of a downloaded live record (no relay requests required):

```bash
python -m drift1a_c1.cli replay --root drift1a_c1/recorded_live
```

This verifies genesis, the chunk chain, every beacon and every recomputed event/checkpoint. Appending is locked within a process host, and the workflow concurrency group serializes scheduled/manual runs. External manual writers must coordinate through the same branch; hash links alone do not prevent an authorized repository owner from deleting an unsealed tail.

Incidents are immutable entries with an append-only JSONL projection. Evidence, lag and timestamps remain available even when reporting or retrieval fails. The repository and workflow artifacts should be backed up; artifact retention is 90 days. Ledger growth and full-history weekly analysis should be monitored during this exploratory phase.

## Weekly reading and interpretations

Read `recorded_live/reports/YYYY-Www/report.md`; detailed measurements are in `report.json`. Reports cover process history, descriptive reference comparisons and retrospective route recurrence. The report JSON and Markdown are sealed together. Failed seals leave the exact prepared report intact for retry. Sealing establishes priority only from the actual verified timestamp, never from the nominal week boundary.

The first week may be partial. Episodes crossing a week boundary contribute their full length and route to their ending week; unfinished episodes are disclosed. Outcome predictability at lags 1–8 is within-episode forward association, not a test of nonprogressive time. Reference ranks include ties; transformed tapes are not independent external sources. Repeated flags are expected under ordinary randomness and are not findings.

Add new interpretation files to `drift1a_c1/interpretations/`. The next run retains their bytes, records when it first observed them and obtains a separate seal. Revisions are new files. Dates written in a note remain operator assertions. A prospective anticipation needs an explicit target and matching rule, and a verified seal before that target material exists; retrospective reading is kept distinct.

No language model generates claims or readings inside this recorder. Human interpretation remains yours.
