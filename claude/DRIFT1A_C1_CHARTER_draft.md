# DRIFT-1A-C1: continuous observational phase — charter draft 0.3 (amendments 1–11)

Status: exploratory observation, not a registered hypothesis test. Live activation
has not occurred. This supersedes draft 0.1 with amendments 1–11. Amendments 7–10 were approved by the operator on 12 October 2026 following review of the synthetic W42 trial. That trial is engineering evidence only and says nothing about the inflow.
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
  and distinct/top routes concern completed episodes (boundary or cap), including
  cross-week starts, separately by entry class under amendment 7.

(b) Descriptive references use only the 29 declared statistics in amendments 9 and 11.
Undefined values are labelled, not filled. No calibrated anomaly finding is inferred.

(c) Retrospective traversal-route reading follows amendment 10. Full route-count
distributions, Jensen–Shannon divergence in bits (insufficient unless both weeks have at least 50 completed traversal episodes),
and dated novelty/rarity recurrence are retained. Every earlier week is cited by its
seal-receipt digest. These are recorded associations; the operator interprets them.

### Amendment 7 — episode entry classes

Traversal episodes enter {1,2,4,5,7,8}; boundary-entry episodes enter {0,3,6,9}.
This classification is identical in all arms, including G. Traversal is the primary
interpretation class. All completed-episode statistics are reported for all episodes,
traversal and boundary-entry: Warp, Plex, cap, Warp fraction, boundary-ending rate,
mean completed length, length distribution and typed routes. The unfinished episode
at week end carries its class. Every completed canonical boundary-entry episode
(C, M, R01–R08) must have length 1 and end at Plex for entry 0/9 or Warp for entry 3/6.
Reports state the diagnostic result, count checked, and failures; a failure is also
appended as an incident. G is not subject to the length-1 diagnostic.

Tick statistics are assigned to the class of the episode active on that tick,
including unfinished episodes. Occupancy denominators are weekly ticks in that
class. Class boundary-ending rates divide endings in that class by its weekly ticks;
the declared all-episode boundary-ending rate divides all endings by all weekly ticks.
Cross-week episode lengths/routes belong to their ending week; their individual
choices, memory changes and remembered-exit expectations belong to their choice week.
Routes include cap endings. Per-100-episode denominators include all completed
episodes in the indicated class. Routes count distinct typed sequences, not their
occurrences, when used as novelty/rarity counts or distinct-route rates.

### Amendment 8 — corrected outcome predictability

Primary population: traversal episodes ending at the boundary; all boundary-ending
episodes remain a secondary series. For each arm and lag k=1..8, use episodes of
length >=k. Z is the zone k moves before the ending; entry is eligible at k=length.
O is Warp/Plex. Never cross an embodiment entry. Report n, the plug-in mutual
information in bits and the Miller–Madow estimate:

I_MM = I_plugin + ((m_Z-1)+(m_O-1)-(m_ZO-1))/(2*n*ln(2)).

The m values count nonempty marginal/joint cells and are also reported. Preserve
negative corrected estimates. Empty populations are undefined; n<50 is insufficient
and its MM estimate is unavailable for the declared comparison. Nonempty insufficient
populations still receive descriptive estimates and permutation-null values.

B=200 within-week permutations of O across the eligible episodes. The exact seed is
SHA256(UTF8('DRIFT-1A-C1-PERM|' + week + '|' + arm + '|' + decimal(k))), where week
is YYYY-Www and k is unpadded. Interpret the digest as an unsigned big-endian integer
for Python random.Random (MT19937); shuffle a fresh copy of O on each permutation.
The frozen Python dependency/runtime choice is 3.12.14. Both populations independently
initialize this same specified stream. Report the nearest-rank 95th percentile
(sorted null value 190 of 200) and count(null >= observed plug-in)/200, without
adding one. A sufficient observation <= that percentile is described as
'indistinguishable from zero'; n<50 takes the label 'insufficient'. These are
within-episode forward associations, not evidence of external anticipation.

### Amendment 9 — declared flags and cross-week tally

Exactly N=29 statistics (as corrected by amendment 11) are declared, all on traversal episodes unless stated:
Warp fraction (1); boundary-ending rate per tick, all episodes (1); mean completed
length (1); distinct routes per 100 episodes (1); zone occupancy 1–9 (9); self-loop
selection counts at 0,3,9 on boundary-entry episodes and at 1 on traversal episodes (4); commitment/governor/retention probability-change
counts (3); remembered-exit selected/final-probability expectation ratio (1);
Miller–Madow outcome predictability at lags 1–8 (8).

Only this set receives strict outside-reference-range flags. Eligible counts,
visit sums, totals, length distributions, and amendment-10 ranks are derived,
never additional flag tests. A tie with a reference extreme is not outside; tied
ranks span all equal values. If C or any reference is undefined, that statistic is
unavailable and not flagged. Report declared N=29, N_compared, F, nominal expectation
2N/9=6.4444, and 2*N_compared/9 for the available subset, conditional on exchangeability
and no ties. Correlation can make F vary more than a binomial count (correlation
alone does not mathematically guarantee increased variance); linearity preserves
its expectation under those assumptions. Hash-related references do not establish
exchangeability. No inferential calibration is claimed.

For each declared statistic, retain cumulative weeks flagged, weeks compared,
total weeks reported, expected flags 2/9 per compared week, and nominal expectation
2/9 per reported week. An unavailable week is not counted as an unflagged comparison.
Memory carries across weeks, so weeks are serially dependent and a binomial
reference is approximate. Persistent flags over many weeks are the pattern of
interest, not a single week's flag.

### Amendment 10 — traversal-route novelty, rarity and recurrence

A route is the typed move sequence of a completed traversal episode, from entry
to boundary or cap ending (entry plus full typed edges uniquely identifies it).
First appearance is in that arm's completed-route history, attributed to ending week.
Report novel distinct routes as count and per 100 completed traversal episodes.

Among canonical memory-carrying arms C and R01–R08, route r is reference-rare for X
in week w iff r occurs in at most one of the other eight arms that week. Presence,
not frequency, determines this leave-one-out rule, applied symmetrically to all nine.
Report rare-route count and rate per 100 completed traversal episodes. M and G have
novelty and divergence statistics, but leave-one-out rarity is not defined for them.

A recurring rare route was reference-rare in its first appearance week and occurs
again in a later week in the same arm. Keep its first week, recurrence weeks and
first report's seal digest; show the accumulated list and current-week recurrence
count. Later changes in rarity do not alter its first-week status. Novelty and
rarity counts/rates and recurrence counts carry descriptive tied ranks among nine
for C and each R arm, without adding flags. Jensen–Shannon divergence now uses
traversal-route distributions for every arm.

All classification, MI/permutation definitions, declared comparisons, tallies,
rarity and recurrence calculations live in frozen metrics.py, not the mutable
renderer. The two operator-specified explanatory sentences are printed verbatim
in each report.

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

## 7. Amendment 11 and pre-genesis gate

Approved by the operator on 13 October 2026 after review of the regenerated
simulation report at f70f23b. Self-loop selections at zones 0, 3 and 9 are measured
on boundary-entry episodes; zone 1 remains on traversal episodes. Traversal
zone_occupancy_0 is retained descriptively but removed from the declared set.
The declared set has N=29, with nominal expected flags 58/9, conditional on
exchangeability without ties. The validation week must fail its validation check
if any declared statistic is constant across C and R01–R08. This check is specific
to the fixed synthetic validation week; it does not censor constant or tied
statistics in later live weeks, and does not establish exchangeability.

Each report also gives leave-one-out F counts for each of C and R01–R08 against
the other eight. This is a descriptive empirical comparison with shared,
dependent data, not an independently calibrated null distribution. Weekly
traversal-route divergence requires at least 50 completed traversal episodes
in each week; otherwise it is marked insufficient.

Amendments 7–11 change measurement and reporting only. The substrate, arms,
inflow, cadence, ledger and sealing remain unchanged. Earlier example reports
are retained; the A11 example is a new evidence file. The operator has read the
A7–A10 report and authorizes genesis after the corrected declared set is
implemented, validated and its report regenerated. No genesis may precede
successful validation. Synthetic seals never serve as live timing evidence.
