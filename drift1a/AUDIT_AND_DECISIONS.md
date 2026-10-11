# Repository audit and G1 result

## Sources checked

- Amelia-0.45: `460c3324ca476b0d5f248dac3e5b22c4588a86b7`.
  https://github.com/adrianjohnsaker-wq/Amelia-0.45/tree/460c3324ca476b0d5f248dac3e5b22c4588a86b7
- Previously inspected Amelia-0.95: `c69416223e68d77c7014403e29f958a29be7190f`.
- `Amelia-1.0-M1.1-exact-byte.zip`, existing sealed Android archive. Its
  `assets/chaquopy/app.imy` contains source Python. Modules were recovered unchanged;
  the canonical module hashes, Numogram digest and typed-graph digest all verify.
- `DRIFT-1_Draft_Protocol_v0.1.md`, 8 October 2026; read in full.

Comparison of *.ts files in 0.45 against 0.95: 249 identical, 22 changed, 3 present
only in 0.45. This is a file-level comparison, not an assertion that every module
was semantically audited. The four proposed selector/commitment/retention/helper
files are identical. The important addition below is new to our previous inventory,
not unique to the older repository.

## Additional usable material

| Element | Finding | Treatment |
|---|---|---|
| `src/ai/substrate/ProcessFieldMemory.ts` | Six dynamic variables plus three previous-value registers; deterministic update and modulation; different from the relay event recorder with the same class name. No integration call found for this class in the inspected runtime. | Arithmetic port, validated against 400 TS updates. Wired into the new Governor through explicitly declared signals. |
| `src/ai/substrate/SubstrateStatePersistence.ts` | Full-memory snapshot idea is useful, but restoration uses wall-clock aging and generated session identity. | Replaced with full deterministic logical-state checkpoints, no wall-clock decay. |
| `src/numogram/SubstrateMemoryCompressor.ts` | Aggregates diagnostic snapshots; no demonstrated causal selection role. | Recorded for future reporting, not used to claim memory-steered dynamics. |
| `src/ai/substrate/AssemblageMetrics.ts` and `FieldClassification.ts` | Executable descriptive heuristics with zone-specific edge sets and interpretive labels. Some listed edges do not exist in the sealed M1.1 graph. | Not used as evidence of intelligence or as the active Governor objective. |
| `src/ai/coupling/CouplingDeltaMonitor.ts` | Useful substrate/relay disagreement monitor. | Future Android relay audit; kept outside the experimental causal loop. |
| 0.45-only coupling wrappers | `CouplingArchitecture.ts` and `amelia-coupling.ts` delegate to relay triggers. | No new substrate candidate Governor. |
| `src/ai/runtime/substrateHeartbeat.ts` | Timer-driven continuation with performance clock and random jitter. | Replaced by explicit logical ticks; suitable future scheduling separation, not deterministic dynamics. |

`src/ai/coupling/ProcessFieldMemory.ts` is a relay/deformation recorder. Its
`continuityReport()` sets `a6TracePresentInA7Context = true` unconditionally.
Its PASS report therefore cannot establish causal incorporation. The Python
causal witness compares actual distributions under a matched present state.

`MetaSubstrateCoordinator.ts` also references unavailable RDG classifier paths in
this checkout. Its interpretive orchestration is not a complete phase-classifier
implementation ready to port. `presenceGovernor.ts` regulates expression modes;
it is not a Governor over graph transitions.

## A decisive graph constraint

M1.1 contains 30 typed directed edges, ten of each type: current, syzygy, gate.
Its legal self-loop locations are 0, 1, 3 and 9 (two distinct typed self-loops at 9).
Zone 2 has none. Therefore importing zone-2-only retention while preserving the
graph would yield an inactive retention mechanism. DRIFT uses all existing legal
self-loop locations, a declared change, and preserves these loops in G.

Canonical graph digest:
`9760268dd784186434ea3d86efd2f8ae9f861b245f64f58c97f70f1e75fb3087`.
Canonical Numogram digest:
`df164ce751d53db17ba16049f656d98806c806df5cf558cef0e49ea782f864ff`.

The graph's Warp and Plex are closed. This runtime adds no re-entry edges or
embodiment resets. Persistent confinement is an expected structural possibility.

## G1 checks actually executed

28 unittest cases passed on Python 3.12.14 / Linux. Source syntax also parses as
Python 3.8. The Kotlin adapter and an Android APK were not built or executed.

1. Graph integrity: 1,600 sampled transitions across every start zone in both graphs;
   fixed typed candidates; exact D1 prior compared with original Fraction law;
   Gt-00 exclusion; no fabricated zone-2 self-loop.
2. Causal ordering: evaluation is read-only; candidate simulations start from the
   same field; only the selected candidate's field is committed after sampling.
3. Complete reset: all nine field registers, classifier buffers, commitment,
   retention and update count are zeroed before the selection/Governor read.
4. Matched randomness: one operation-keyed variate shared across arms per tick;
   candidate evaluations do not consume draws; boundary/zero-probability checks.
5. Validation: numeric TS/Python parity for preserved formulas, regression tests
   for corrected floor/expiry, matched-present memory intervention, checkpoint
   restoration, corrupt-ledger refusal, replay, single-writer lock, basic scorer
   and synthetic timing/leakage checks.

The TS commitment confidence and arithmetic are retained. This is not full behavioral
parity with the original selector: graph mapping, label exceptions, timing, phase
inputs, retention semantics, typed-edge handling and Governor integration are
explicit new design choices.

## Concrete causal witness

A declared fixture starts at zone 9 and conditions for 20 steps with u=0.99.
At the same present state (zone 9, tick 20), erase only H in one copy.
Candidate order is syzygy 9->0, current 9->9, gate 9->9.

| Condition | P(syzygy 9->0) | P(current 9->9) | P(gate 9->9) |
|---|---:|---:|---:|
| Retained H | 0.20110936434016555 | 0.5325937571065563 | 0.26629687855327816 |
| Reset H | 0.25 | 0.50 | 0.25 |

The identical u=0.2255546821700828 chooses current 9->9 with retained H and syzygy
9->0 with reset H. Full states and evaluations are in
`evidence/memory_causal_witness.json`. This is a causal engineering fixture, not a
natural cohort effect-size estimate, significance test or evidence of an Outside.

## Offline pilot (synthetic seed 101, start zone 1, 512 ticks)

| Arm | Commitment applied | Retention floor applied | Governor reweighted candidates | Distinct typed edges |
|---|---:|---:|---:|---:|
| C | 359 | 1 | 365 | 11 |
| G | 222 | 66 | 353 | 28 |
| M | 0 | 0 | 0 | 11 |

C and M both entered the canonical Warp. Zone-3 occupancies were 0.7109375 and
0.67578125 respectively. This paired synthetic trajectory demonstrates execution
and active memory effects; it does not establish general superiority or autonomous
intelligence. G changes connectivity, so its greater edge coverage is not by itself
a developmental advantage.

Replaying all 512 committed ticks reproduced the identical ledger head:
`d48c9be70293a0fc6745feee8dff48f3d984879c9e936641963c7e32a3f1f387`.
Every tick is explicitly ineligible for anomaly inference.

## What is now established, and what is not

- Established: executable memory-steered Python dynamics on the verified canonical
  graph; a new frozen candidate evaluator; three-arm offline execution; G1 results.
- The Governor is a one-step, soft viability evaluator using designer-declared
  compression/release costs. It admits all graph-legal finite candidates and changes
  their probabilities. It is not a recovered historical Governor or a long-horizon
  planner. All candidate costs and multipliers are exposed.
- Autonomous continuation is implemented at the logical-tick level: no prompt or
  relay is required to advance. Self-generated aims, open-ended individuation,
  autopoiesis and autonomous developmental intelligence are not established.
- Next acceptance requirements: device parity; timing/outage pilot; pinned beacon
  verifier; independent receipt mechanism; revised predictor features; registration
  with actual start/end dates; independent prospective evidence and replication.

No live deployment, confirmatory run, paid service, GitHub publication, or change to
OUTSIDE-2 was made by this work.
