# Amelia: DRIFT-1A-C1 continuous observation

C1 keeps the accepted G1.1 Numogram instrument running with memory across episodes. It records a verified external input every minute and produces sealed weekly accounts for interpretation. This is exploratory observation, not a registered hypothesis test or evidence of an Outside connection.

**Delivery status: live operation disabled; no genesis or live rounds consumed.** The Android G1.1 pilot and its saved runs are unchanged. The continuous recorder runs on GitHub; its Markdown reports can be read on a phone.

**Amendments 7–10 validation complete:** 33 C1 tests and 40 accepted-substrate tests passed in [GitHub run 38314170412](https://github.com/adrianjohnsaker-wq/Amelia-0.4/actions/runs/38314170412). All 18 arms completed 10,082 synthetic ticks and replayed exactly (181,476 arm moves). Every tick record and checkpoint also matches the earlier baseline: these amendments changed measurement only. The canonical boundary-entry diagnostics passed. Read the [regenerated full-week example](evidence/SIMULATION-2026-W42-A7-A10-report.md) before genesis; the original examples are preserved. The [audit summary](evidence/validation-status-A7-A10.json) records report hashes and the [downloadable complete evidence artifact](https://github.com/adrianjohnsaker-wq/Amelia-0.4/actions/runs/38314170412/artifacts/11777921172). All simulation seals are synthetic, and live operation remains disabled.

**Earlier six-amendment baseline validation (retained):** 25 C1 tests and 40 accepted-substrate tests passed in [GitHub run 38272274430](https://github.com/adrianjohnsaker-wq/Amelia-0.4/actions/runs/38272274430). All 18 arms completed 10,082 synthetic ticks and replayed exactly (181,476 arm moves). Outage recovery and two simulated weekly seals passed. See [validation evidence](evidence/validation-status.json), the [full-week report example](evidence/SIMULATION-2026-W42-report.md), and the [downloadable full evidence artifact](https://github.com/adrianjohnsaker-wq/Amelia-0.4/actions/runs/38272274430/artifacts/11759339186). The artifact includes the complete simulation ledger and checkpoints; its SHA-256 is recorded in the evidence summary. Simulation timestamps are explicitly synthetic.

The [charter](../claude/DRIFT1A_C1_CHARTER_draft.md) incorporates all eleven approved amendments. Genesis freezes its exact bytes, the accepted substrate, admission and measurement code, graph definitions, dependencies and trust material. Report rendering may evolve; every report identifies its renderer hash. Changing a frozen file halts an existing run.

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

## Live activation after amendment 11 validation

The workflow must exist on **main** for its hourly schedule; it checks out **amelia-1.0**, where all code, state and reports live. Installation alone starts no experiment.

The operator reviewed the A7–A10 report on 13 October 2026 and authorized genesis after amendment 11 is implemented, validated and its report regenerated. That authorization does not substitute for a successful cryptographic genesis seal.

1. Set the repository Actions variable `DRIFT_C1_ENABLE_LIVE` to the exact string `true`.
2. Manually dispatch `Amelia C1 continuous observation` from `main`, selecting **genesis**. Genesis is never created by the scheduled **run** action.
3. Check the successful genesis receipt and pinned source/graph digests. Its RFC 3161 seal must precede R0's publication; otherwise the attempt is retained and no run is admitted.
4. The hourly **run** action then resumes the next eligible round. It may also be dispatched manually. Set the variable to `false` to pause; restoring it resumes the same sequence and records lag.

Live genesis requires working drand and FreeTSA services. The FreeTSA root is pinned. The drand round number recorded at sealing is calculated from the receipt time and pinned round schedule; it is contextual information, not an independently verified publication attestation. Only a verified RFC 3161 token establishes the stated seal time, with its accuracy allowance.

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

## Amendments 7–10

The new measurement layer separates all, traversal and boundary-entry episodes.
Traversal is primary; canonical boundary-entry diagnostics are reported and any
failure is an incident. Outcome predictability now includes signed Miller–Madow
estimates and 200 reproducible within-week permutations, with n < 50 marked
insufficient. Only the declared 29 statistics receive outside-range flags, with
available denominators and cross-week tallies explicit. Traversal-route rarity
is leave-one-out among C and R01–R08; first-week rare status and seal provenance
are retained for later recurrence. All these calculations are in frozen metrics.py.

The previous report files and evidence are retained. New evidence filenames carry
`A7-A10`; their simulation seals are synthetic. The substrate, arm definitions,
beacon admission, ledger and sealing mechanisms have not changed.

## Amendment 11

Self-loop statistics at 0, 3 and 9 now use boundary-entry episodes; zone 1 remains
on traversal episodes. Zone-0 traversal occupancy remains descriptive, outside
the declared 29-statistic set. The fixed full validation week must contain no
constant declared statistic across C and R01–R08. Reports include descriptive
leave-one-out flag counts, and route divergence requires 50 traversal episodes
in both weeks. The charter is draft 0.3.

The A11 example is a reanalysis of the already replay-verified A7–A10 synthetic
ledger. Its provenance identifies the source artifact and original report; all
raw arm measurements must match, and only the declared comparisons and reporting
change. It does not claim a new dynamics run or live timestamp. Reproduce with:

```bash
python -m drift1a_c1.remeasure --archive C1-A7-A10-validation.zip --root /tmp/C1-A11-reanalysis
```

36 C1 tests passed. Reanalysis of all 10,082 source ticks across 18 arms passed;
all raw arm measurements match the earlier report, all 29 declared full-week
statistics vary across the nine canonical memory-carrying arms, and C has 2 flags.

See [the regenerated A11 example](evidence/SIMULATION-2026-W42-A11-report.md) and
[its validation record](evidence/validation-status-A11.json). All earlier examples
are retained. GitHub validation additionally reruns the complete simulation on
code pushes; its full-week check rejects any constant declared statistic.
