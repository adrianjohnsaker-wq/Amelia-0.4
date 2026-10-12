# DRIFT-1A-C1: continuous observational phase — charter 0.2

Status: exploratory observation, not a registered hypothesis test. Live activation
has not occurred. This supersedes draft 0.1 with the six approved amendments.
The motivating hypothesis is that the Numogram can be explored as an operational
channel for an Outside whose temporal relations need not match internal progressive
time. This is motivation, not a property established by the apparatus.

## 1. Inflow, time and genesis

Quicknet chain: 52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971.
Genesis time 1692803367 Unix seconds; period 3 seconds; scheme
bls-unchained-g1-rfc9380 (G1 signatures). Full key, group hash and DST from the
vendored OUTSIDE-2 verifier are embedded in genesis.json and bound to the chain
hash. Randomness must equal SHA256(signature) and the round-specific BLS signature
must verify under the pinned key. Known-answer positive and wrong-round negative
checks run when the live verifier starts.

Tick t consumes selected round R0+20t. This is one sampled round per minute,
not ingestion of every three-second beacon round. R0 is the first positive round
divisible by 20 whose scheduled publication is at least 600 seconds after genesis
creation. Genesis fails unless its RFC3161 signed time plus declared accuracy
precedes R0 publication. Failed genesis attempts are retained and not activated.
The pinned FreeTSA root and verification code are frozen. A timestamp establishes
existence, not publication or uniqueness of private genesis attempts.

The hourly job ingests already published selected rounds in order. Publication,
actual receipt and seal times remain distinct. Receipt lag is recorded; lag >5400
seconds is labelled catch-up. An hourly batch is not minute-by-minute reception.
Retrieval failure and invalid signature are separate incidents. Neither advances
the input cursor. The next invocation resumes at that selected round.

## 2. Arms and frozen behavior

All 18 arms run accepted G1.1 unchanged: uniform ingress before one legal move,
common destination boundary {0,3,6,9}, cap 1260, global selector clock, C/G/R memory
carried across episodes, M complete selector-history reset before every choice.
Initial ingress is uniform. Ingress is not a graph edge or extra occupancy sample.

C and M use canonical M1.1. G00–G07 use eight distinct degree-matched rewirings
with seeds DRIFT-1A-C1-ENS-00 through DRIFT-1A-C1-ENS-07 and the accepted 100-swap
rewire procedure. These controls are descriptive and do not establish universal
Numogram specificity. Warp/Plex labels in G identify the common boundary labels,
not graph-specific terminal components.

C/M/G share ingress and transition variates at each global tick. R01–R08 share
the tick and derivation procedure but receive transformed tapes. For Rk, input is
SHA256(ASCII('DRIFT-1A-C1-REF-'+decimal(k)+'|') || decoded_32_randomness_bytes),
encoded as lowercase 64-character hexadecimal for G1.1 variates. k is unpadded
1 through 8. All variates use G1.1's versioned stream and operation keys, unchanged.
Proposed entry is shared for C/M/G even when their restart schedules differ.

Reference tapes are deterministic transformations of one inflow, not independently
sourced beacons. They contextualize regularities for this instrument and these tapes.
All graph digests, substrate, engine, measurement, beacon, timestamp, trust-root,
requirements and charter file SHA256s are bound at genesis. A mismatch halts
admission. Rendering may change with its source digest recorded; any correction
to frozen measurement definitions requires a dated amendment and a new version.
Original reports remain immutable.

## 3. Continuity and records

State has no weekly reset. Immutable gzip chunks, split by invocation and UTC ISO
week, form the authority for state and cursor. Each contains sequence/start tick,
previous compressed chunk SHA256 (initially the genesis digest), per-tick records
and full final checkpoints for all arms. Deterministic gzip metadata is used.
A fully fsynced temporary inode is published atomically without overwriting a
committed filename. A crash before publication leaves that batch uncommitted;
restart repeats its selected inputs from the previous checkpoint. No second cursor
file can advance independently. A process lock and workflow concurrency serialize
writers. Git updates use a fast-forward lease; conflicts do not force overwrite.

Every tick records beacon round, signature, randomness, scheduled publication,
receipt, lag/catch-up, and for each arm: typed edge, proposed/applied ingress,
episode index/length/termination/outcome, phase AFTER the event, memory mechanism
activity, actual probability-change flags (>1e-12), remembered exit, its base and
final destination probability, prior-memory digest, pre/post embodiment digests.
All arm states can be recomputed by exact replay in the original runtime.

Incident and interpretation journal entries are individually immutable and chained.
Their JSONL files are append-only projections of those records; interrupted
projection updates can be rebuilt without changing the underlying events.

## 4. Weekly measurements and seals

Weeks are ISO weeks in UTC, assigned by selected-round publication time. A week
is complete only after all its selected rounds have been admitted and wall time
has passed its end. The first week may be partial and its tick count is explicit.
Reports contain immutable JSON plus Markdown; their byte digests are sealed as
one bundle. A failed timestamp leaves GENERATED BUT UNSEALED bytes for retry;
prior weeks must be sealed before later retrospective reports cite them.
The bundle records last included round/time and generation time; seal receipts
record verified time with accuracy, actual sealing observation and current round.
Priority begins at verified sealing time, never at the beginning of the next week.
No advance-knowledge claim is made about already consumed or published rounds.

(a) Process history per arm:
- Warp/Plex boundary endings and cap terminations, assigned to ending week.
- Warp fraction = Warp/(Warp+Plex), undefined if no boundary endings.
- Boundary-entry rate = applied ingresses landing in {0,3,6,9}/all applied ingresses.
- Mean completed length includes boundary and cap episodes; full lengths of
  cross-week episodes are assigned to ending week. An unfinished episode's
  elapsed length is reported separately at each week end, never treated completed.
- Post-move occupancy divided by weekly graph moves; self-loop counts by source.
- Activity separately from actual probability changes for commitment, field
  Governor and retention; phase counts refer to phase after the observed event.
  Governor activity means at least one candidate multiplier differs from 1;
  a shared multiplier can be active without changing normalized probabilities.
  Retention-floor applications are also counted separately.
- Commitment choices and remembered-destination successes: sum base probabilities
  and sum FINAL probabilities alongside observed successes, assigned to choice
  week. Excess over base can follow the implemented bias and is not an anomaly.
  Endings of episodes containing any commitment choice are assigned to ending week.
- Routes encode entry plus ordered full typed edges (including labels). Frequencies
  and distinct/top routes concern completed boundary episodes, including cross-week
  starts. Cap episodes are counted separately. This definition is fixed.

(b) Descriptive references: each defined numeric statistic of C is ranked against
R01–R08 with a tied rank interval, reference range, and STRICT outside-range flag.
Undefined values are labelled, not filled. 2/9 applies only under exchangeability
and no ties; these hash-related arms do not establish those assumptions. Multiple
weekly flags are expected. No calibrated p-values or findings are inferred.
M and G are shown descriptively, with the same counting conventions.

(c) Retrospective reading: full route-count distributions, Jensen–Shannon divergence
in bits between weeks (undefined for an empty distribution), shared/distinct route
recurrence, and first observed week in the completed-route record. Every earlier
week is cited by its seal-receipt digest. All reference arms use the same scale.
These are recorded associations; the operator supplies interpretations separately.

Outcome predictability at lag k: plug-in mutual information in bits between the
zone k moves before a boundary ending and Warp/Plex, for k=1..8. Only episodes
with length >=k qualify; their entry zone is eligible at k=length. Never cross an
embodiment entry. Include n at every k; acknowledge finite-sample upward bias.
'Retrochronic horizon' may be used interpretively, but this metric measures
within-episode forward association and is not a test of external anticipation.

## 5. Interpretation records

New note files are observed under drift1a_c1/interpretations. Exact bytes are copied
to immutable content-addressed records; revisions get new digests. Store operator
stated authorship time as unverified text, first job observation time, and verified
seal time separately. Only verified seal time supports independent priority.
Pending notes are retried even if the original source file later disappears.
Anticipation requires a target and matching rule sealed before the relevant material
becomes available; retroactive readings remain explicitly later interpretations.
A note's timestamp alone does not certify its target's availability or its claims.

## 6. Limits and activation

Reports do not assert meaning or contact with an Outside. Comparison flags prompt
interpretation. Other readers such as I Ching or Tarot require an amendment.
Live workflow requires an explicit repository enable variable AND separately
sealed genesis. No implementation test consumes live inflow into Amelia state.
Synthetic tests use visibly marked synthetic beacons and seals; they cannot be
admitted as live cryptographic evidence. G1/G1.1 Android installations are unaffected.
