# DRIFT-1A engineering amendment — candidate v0.1

This amendment accompanies the Python implementation. It supersedes no registered
experiment. The 8 October draft remains a proposal; these choices must be frozen
with the final protocol before any prospective cohort starts. G1 pilot data are
excluded from confirmatory scoring.

## Architecture

At logical tick t:

1. In M only, replace the entire history H with its declared empty state.
2. Read P=(zone,tick) and H. Obtain the graph-legal D1 typed-edge prior.
3. Read the prior commitment snapshot for the current zone. Boost its preferred
   destination and suppress rivals that are still in the legal row. Multiply
   parallel typed edges proportionally so their relative base weights are retained.
4. The Governor evaluates each candidate from an isolated copy of the SAME prior
   H. Predict one field update using that candidate's outcome, compute cost, and
   multiply its weight by 1/(1+2*cost). It never updates live memory while evaluating.
5. Normalize. If an eligible prior retention window is active, enforce a true
   final self-loop probability floor by proportional redistribution within the
   legal row. Never create a self-loop. Retention is applied after soft Governor
   weighting; therefore it can offset that preference. This is deliberate.
6. Use a single externally supplied operation-keyed variate to select a typed edge.
7. Commit the selected outcome's field update. Update the current source's observed
   destinations, phase traces, commitment capture and retention trigger for use at
   t+1. Increment the logical tick, archive the full event and state atomically.

Reports and linguistic relays have no write path into this sequence.

## State and interventions

P: canonical zone integer 0..9 and logical tick. H:

- nine PFM registers: six field variables and three prior-signal values;
- last 32 completed destination observations per source zone;
- last four phase traces per source zone;
- commitment snapshots per source zone;
- retention threshold-side flags, activation and expiry ticks per eligible zone;
- retained update count.

C uses canonical graph + retained H. G uses a frozen typed-degree-matched rewiring
+ retained H. M uses canonical graph with ALL H cleared before every read. M is
therefore a **full operational-history reset**, stronger than the original draft's
PFM-tensor-only reset. P's current zone and logical time remain. Reclassify that
intervention explicitly in any final analysis; do not call it a selective tensor
ablation. The diagnostic ledger is outside the dynamics and is never reread to
reconstruct memory. A future PFM-only reset would require its own arm.

This memory is structured state, not a single tensor. Do not report a tensor
Frobenius norm or use the original tensor-based predictor features without amendment.
The scorer offers an explicit-dimensional learner, but a final live feature schema
is intentionally not claimed to have been registered or integrated.

## Canonical graph and base law

Use unchanged M1.1 canonical typed graph, 30 edges; D1 weights current:syzygy:gate
= 2:1:1. Include disputed Gt-00 in this engineering default. Exclusion is implemented
and tested, but choosing it would change the final configuration. No graph mutation
occurs during an epoch. The D1 prior matches original Fraction-law probabilities.
New memory and Governor modulation define a new dynamics contract over that graph.

Keep typed edges distinct even when they share a destination. Candidate order is
(source, type rank syzygy/current/gate, destination, label). Zones are ten integers.
No latent/crystal substates are introduced, avoiding hidden zone-0 mode dynamics.
Remove the legacy 1->0-crystal preference and 0-flux->9 capture exception; this is
an intentional label-neutral adaptation, not an exact port of those exceptions.

G: 100 accepted typed directed double-edge swaps, using SHA-256-derived index pairs
from the fixed string `DRIFT-1A-G1-20261011` and attempt index. Reject introduced
self-loops and duplicate same-type edges; preserve existing self-loops exactly,
typed in/out degrees, and source labels/weights. Stop/refuse after 20,000 attempts
if unable to finish. Freeze the resulting edge list, not only the seed.
Reciprocal syzygy pairing, terminal SCCs and arithmetic gate destinations are NOT
preserved. G is one explicit directed typed-degree control, not all conceivable
Numogram nulls. Strong graph attribution still requires a declared ensemble.

## Empirical phase and field inputs (new operational definitions)

For the current source, keep at most 32 actual completed destination observations.
Self-loop depth here means the fraction of those departures that stayed in that
source, not consecutive dwell length and not predicted self-loop probability.
Phase distribution uses those destination counts plus ONE D1 prior pseudocount.
Divide its Shannon entropy by log2(number of distinct legal destinations); use zero
when only one destination exists.

After at least four observations, classify pre_lock when depth >=.35 and normalized
entropy <=.85; near_lock when depth >=.65 and entropy <=.85. Otherwise neutral.
Capture is attempted only after the selected event, using the last four local
traces. The input confidence is 1.0 as a deterministic qualification flag, not a
statistical confidence claim. gammaOccupancy and btl are explicitly 0: these
unimplemented measurements are not fabricated. The original formula's foreclosure
and commitment thresholds (.18, .55) still decide capture. Bias application also
checks the original .55 confidence threshold. Capture may refresh a continuing
qualified state; decay .9985^age applies since the most recent capture.

The exact PFM update arithmetic is preserved; mapping observable events into its
inputs is new. For each candidate (and later the selected outcome):

- selfLoopDepth: source-local fraction including the hypothetical/selected outcome;
- corridorSignal: one minus normalized entropy of the resulting empirical counts,
  without pseudocount; normalization uses distinct legal destinations;
- ringSignal: 1 if its destination occurred in the prior local buffer, otherwise 0;
- latentSignal: 1 if its destination did not occur in that buffer, otherwise 0;
- releaseSignal: 1 for departure from the current source, otherwise 0;
- compressionActive: resulting selfLoopDepth >=.35;
- transitionSuccess: departure when the prior local self-loop fraction was >=.35.

These are declared operational proxies. In particular ringSignal is recurrence,
not membership in a CCRU ring, and transitionSuccess is a designer-defined event,
not independently established developmental success.

## New candidate Governor

Simulate the PFM update for every legal candidate. Predicted cost is
compressionDebt + releaseDebt. Weight multiplier is 1/(1+2*cost). All finite legal
candidates remain admitted; ordering and costs are logged. No destination target,
LLM output, future input, arm label, wall clock or stochastic rollout is consulted.
No adaptive Governor cache exists beyond H. The hard legality boundary belongs to
the graph adapter. The Governor's soft preference is an explicit design choice;
one-step regulation does not demonstrate self-generated purposes or intelligence.

## Corrected retention

- Eligible zones: any source with a legal self-loop (canonical: 0,1,3,9).
- Trigger: completed-event local depth crosses from below .35 to >=.35.
- Active selections: the next 500 GLOBAL logical ticks, [activation,expiry).
- Requalification requires going below threshold and then a new crossing at or
  after expiry. A permanently high historical peak never reactivates a window.
- Apply only when pre-retention self-loop probability is >=.08 and below .40.
- Set total final self-loop probability to .40, redistributing proportionally
  within self/non-self groups. Leave values already >=.40 unchanged.
- Remove the legacy .985 slow-weight reduction and .90 release reduction. They
  were weight-level behavior; this model implements a bounded probability floor.

## Randomness and serialization

No core RNG or clock. The driver supplies exactly one 32-byte input per tick.
SHA256(canonical JSON [version,stream,tick,operation] || zero byte || input bytes)
provides its first 53 bits / 2^53 as a variate in [0,1). Shared operation='transition'
and stream='DRIFT-1A' exclude arm and graph IDs. Candidate evaluations use no draws.
Zero-weight entries are skipped; cumulative intervals use strict u<cumulative.

State/event JSON uses sorted keys, compact separators, ASCII escaping, finite
Python binary64 values and SHA256. Python float serialization is the registered
engineering representation. Cross-runtime TS parity uses numerical tolerance;
actual phone checkpoint-byte parity remains to be established. Local ledger hashes
are reproducibility aids, not evidence of independent pre-release publication.

## Acceptance status

G1 engineering: PASS on the included environment and fixtures.
Offline deterministic three-arm pilot: completed and replayed exactly.
Android JSON API: desktop roundtrip passed; Kotlin/APK/device tests outstanding.
Live timing, verified beacon ingestion, forecast commit/witness publication,
receipt validation, training/forecast service, false-alert/power simulations,
84-day calendar and independent registration: not completed by this package.

The implemented e-process/Brier/logistic utilities and synthetic timing rejection
checks are prerequisites, not certification of those missing live services.
The next gate should be device parity plus a timing/outage pilot, followed by a
separate registration. Do not reinterpret G1 as a confirmatory research result.
