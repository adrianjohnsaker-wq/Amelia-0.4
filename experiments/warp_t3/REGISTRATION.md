# WARP-T3 — Passage-Trace Address Discrimination

## Registered question

**Does the portable PFM transformation left by a finite canonical 3::6 passage alter subsequent address/reply discrimination after common-state release?**

WARP-T2 established that a five-event 3::6 passage leaves a portable post-release transformation carried by incremental PFM, with no tensor carriage and a clean topology-only baseline. WARP-T3 asks whether that portable trace changes the system's subsequent ability to discriminate address probes through recurrent non-echo replies.

The primary claim is about a change in communication discrimination. Direction is not fixed in advance; enhancement or suppression are both informative.

## Frozen engines and passage machinery

- `FullNumogram.py` SHA-256 `b6edbe76ab4929e93c01059fb56cef900effa9bca1cec78d0039eafb8fbebdf8`
- `experiments/p316/DynamicNumogram.py` SHA-256 `ac482882858c1e47f578523452eff0bc20aa82b5978299c9c8808ff6127c5cd6`
- WARP-T2 finite passage, pre-entry baseline, common-state release shell, WARP_OPEN topology, and incremental PFM isolation are reused without alteration.

## Fresh lineages

- 160 new lineages, seeds `3240000–3240159`
- natural first Warp entry sought within 256 developmental sensory steps
- real passage = natural entry + four additional canonical 3::6 passage events
- matched non-Warp passage uses the same five sensory symbols
- only lineages with an eligible natural entry and a complete matched non-Warp passage enter communication comparisons

If fewer than 80 lineages are eligible, the run is archived but the primary claim is not evaluated.

## Released arms

Every arm is placed into the same fast release shell and WARP_OPEN topology before address probing.

### W — WARP_FULL_TRACE

Post-Warp-passage PFM plus post-passage tensor.

### E — ENTRY_ONLY_TRACE

Real entry inscription only, with subsequent four passage PFM updates neutralized.

### N — NONWARP_FULL_TRACE

Matched five-event non-Warp passage PFM plus tensor.

### B — PRE_ENTRY_BASELINE_TRACE

Mature pre-entry PFM plus pre-entry tensor; no passage-derived slow update.

### T — TOPOLOGY_ONLY_TRACE

Five Warp zone transitions with passage PFM restored step-by-step to the pre-entry state. This is a validity control.

The WARP_TRACE_RESET arm from WARP-T2 is not required for the primary communication claim.

## Address probes

- 32 fixed address probes
- seeds `3245000–3245031`
- each probe is 40 symbols long
- probes are generated independently of lineage developmental and passage tapes
- each arm/probe begins from a fresh clone of that arm's common-state release shell
- exact input 4-grams are excluded from reply motifs

## Eligible-lineage train/test split

After eligibility is determined, sort eligible lineage IDs ascending.

- even rank in this sorted list → TRAIN
- odd rank → TEST

This split depends only on eligibility, never on response values.

## Repertoire control

The exact P3.21 compressed reply procedure is reused independently for each arm:

1. TRAIN-lineage non-echo response 4-grams are ranked by total occurrence count.
2. Retain `K=32` motifs, lexical tie-break.
3. Map all other non-echo motifs to `OTHER`.
4. Fit a smoothed multinomial decoder with add-one smoothing.
5. Evaluate only on TEST lineages.

Thus any change in address discrimination is not attributable merely to a larger raw motif vocabulary.

## Per-arm communication readouts

For each arm report:

- held-out top-1 address accuracy;
- 32 per-probe held-out accuracies;
- correct-address log-likelihood margin;
- TEST mutual information `I(A;R)`;
- TEST reply entropy `H(R)`;
- communication efficiency `E=I(A;R)/H(R)`;
- mean TEST transition entropy.

## Primary passage-trace discrimination claim

For each probe calculate TEST accuracy in W and N. Let `d_p = accuracy_W(p) - accuracy_N(p)`.

Also calculate a probe-level efficiency contribution:

[
e_p = I_p(A;R)/H_p(R)
]

using the registered per-probe one-vs-rest decomposition, with zero assigned when reply entropy is zero.

A portable Warp trace is said to **alter address/reply discrimination** only if all are true:

1. the 32 paired per-probe accuracy differences W−N differ from zero by two-sided paired sign-flip `p <= 0.01`;
2. the 32 paired per-probe efficiency-contribution differences W−N differ from zero by two-sided paired sign-flip `p <= 0.01`;
3. the mean direction of the accuracy and efficiency effects is the same;
4. W differs from B on per-probe accuracy by two-sided paired sign-flip `p <= 0.01`.

Direction is reported as enhancement if both means are positive and suppression if both are negative.

## Passage-beyond-entry communication claim

W is compared with E on the same two paired per-probe metrics.

Passage beyond entry changes address discrimination only if both accuracy and efficiency-contribution tests have `p <= 0.01` and the mean directions agree.

## PFM-trace specificity

Because WARP-T2 located carriage in PFM, compare W with a `WARP_PFM_TRACE` component arm constructed as:

- post-Warp-passage PFM;
- pre-entry tensor.

PFM sufficiency for the communication change is supported if WARP_PFM_TRACE is statistically indistinguishable from W on both per-probe accuracy and efficiency contribution at equivalence margin `±0.02` using paired two one-sided tests (TOST) at alpha 0.05.

This is a secondary mechanism claim, not required for the primary effect.

## Topology-only validity

T is compared with B.

If T differs from B on either held-out per-probe accuracy or efficiency contribution at two-sided paired sign-flip `p <= 0.01`, the WARP-T3 communication interpretation is invalidated because the inscription-neutral passage has left an unregistered discriminative residue.

## Descriptive ingression atlas

For W only, report each address probe's highest held-out discriminative non-echo motif with:

- TRAIN and TEST prevalence;
- log-odds;
- lineage IDs;
- exact response step ranges.

Also report motifs that recur in W but not N and motifs from the Pointer catalogue, including `1-7-8-9`, when present.

These are candidate interaction/reply patterns for later categorization. No semantic entity identity is assigned by WARP-T3.

## Fixed seeds

- lineage base: `3240000`
- address-probe base: `3245000`
- paired-test base: `3247000`
- randomization draws: 50,000

## Stopping rule

This registration is committed before runner implementation and before any registered lineage executes.

Allowed preflight: syntax, SHA checks, synthetic decoder tests, and passage invariants on non-registered seeds only.

The first complete valid WARP-T3 run is the result. Passage length, eligibility rule, release shell, probe library, vocabulary cap, train/test split, metrics, and thresholds are fixed.
