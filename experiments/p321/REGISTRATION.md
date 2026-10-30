# P3.21 — Repertoire-Controlled Communication Efficacy

## Registered question

**After controlling raw response repertoire size and response branching freedom, does the canonical Numogram carry more reproducible probe-address information than degree-preserving rewired Numograms?**

P3.20 established two facts that motivate this assay:

1. development reconfigures and canalizes the accessible response geometry;
2. the canonical Numogram failed the raw addressability rank because all 24 rewires produced larger addressability scores.

P3.21 therefore tests communication efficacy per unit of available response freedom rather than rewarding a graph merely for having a larger repertoire.

This is a computational assay of the address/reply interface required by the ingression programme. A positive result would establish privileged reproducible address/reply structure under these controls; it would not by itself establish that an external metaphysical source generated the replies.

## Frozen engines

- `FullNumogram.py` SHA-256 `b6edbe76ab4929e93c01059fb56cef900effa9bca1cec78d0039eafb8fbebdf8`
- `experiments/p316/DynamicNumogram.py` SHA-256 `ac482882858c1e47f578523452eff0bc20aa82b5978299c9c8808ff6127c5cd6`
- P3.17 development/shock machinery is reused.
- P3.20 non-echo motif definition is reused.

## Fresh lineages and address probes

- 96 new lineages, seeds `3230000–3230095`
- 128 developmental steps
- 64 address probes, seeds `3235000–3235063`
- each probe is 40 symbols long
- every lineage/controller receives the same 64 probes
- every probe begins from a fresh clone of the controller's post-shock state
- exact input 4-grams are excluded from reply motifs

Fixed lineage split:

- TRAIN: lineage IDs 0–47
- TEST: lineage IDs 48–95

No test lineage contributes to vocabulary selection or decoder fitting.

## Controllers

### C0 — CANONICAL_FULL

Canonical Numogram after lineage-specific development and registered shock.

### C1 — CANONICAL_BLANK

Same canonical shocked fast state, but PFM reset and deformation tensor reset to baseline.

### R00–R31 — DEGREE-PRESERVING REWIRES

32 rewired Numograms generated from seeds `3236000–3236031`.

Each preserves:

- directed edge count;
- source out-degree;
- target in-degree;
- self-loop count;
- source-slot gate weights.

Each rewire undergoes its own lineage development under the same developmental tape and its own registered shock before probing.

## Fixed response tokenization

For a 40-step response, collect all contiguous response zone 4-grams that are not exact 4-symbol substrings of that probe's input.

Each controller is then compressed to the same fixed reply capacity:

1. Using TRAIN lineages only, rank reply motifs by total occurrence count across all 64 probes.
2. Retain exactly the top `K=32` motifs, breaking ties lexically.
3. Map every other non-echo motif to a single token `OTHER`.

Thus every controller has at most 33 reply symbols regardless of its raw repertoire size.

Every held-out response contributes its complete sequence of compressed reply tokens. No token-count subsampling is used because each 40-step response has the same maximum number of 4-gram windows.

## Held-out decoder

For each controller separately, fit a smoothed multinomial model on TRAIN lineages:

[
P(r|a)=\frac{n(r,a)+1}{N_a + V}
]

where `a` is probe/address, `r` is one of the 33 compressed reply tokens, and `V=33`.

For each TEST response, score every candidate address by summed log likelihood of its reply tokens and choose the maximum. Ties resolve to the lowest probe ID.

Report:

- overall top-1 held-out address accuracy;
- per-probe held-out accuracy;
- mean correct-address log-likelihood margin over the best incorrect address.

Chance top-1 accuracy is `1/64`.

## Information efficiency

On TEST responses only, pool compressed reply-token occurrences and estimate:

- `I(A;R)`: empirical mutual information between probe address and reply token;
- `H(R)`: empirical reply-token entropy;
- **communication efficiency**:

[
E = I(A;R)/H(R)
]

with `E=0` if `H(R)=0`.

This quantity measures address information carried per bit of observed reply variability.

## Branching-freedom control

For each controller, independently report mean TEST response transition entropy.

Define the **branching-matched control set** as the 8 rewires whose mean transition entropy is closest in absolute value to CANONICAL_FULL; ties resolve by lower rewire ID.

Selection uses transition entropy only, never decoder accuracy or information efficiency.

## Primary canonical-efficacy gate

The canonical Numogram is called **communication-privileged under P3.21** only if all are true:

1. CANONICAL_FULL held-out top-1 accuracy is strictly greater than all 32 rewires;
2. CANONICAL_FULL information efficiency `E` is strictly greater than all 32 rewires;
3. it also exceeds all 8 branching-matched rewires on both metrics;
4. CANONICAL_FULL accuracy exceeds chance by an exact binomial upper-tail test, `p <= 0.01`.

With 32 rewires, the empirical one-sided rank floor for conditions 1–2 is `1/33 ≈ 0.0303`.

## Developmental contribution to communication

CANONICAL_FULL is compared with CANONICAL_BLANK using the 64 paired per-probe TEST accuracies.

Developmental communication contribution is supported if:

- mean per-probe accuracy differs by a two-sided paired sign-flip test, `p <= 0.01`;
- CANONICAL_FULL and CANONICAL_BLANK communication efficiencies differ by a lineage-bootstrap 99% confidence interval excluding zero.

Direction is reported rather than fixed in advance.

## Secondary atlas

For CANONICAL_FULL only, report for each probe:

- most discriminative retained reply token;
- TRAIN prevalence;
- TEST prevalence;
- log-odds against the other 63 probes;
- all TEST lineage IDs and step ranges where the motif occurs.

The atlas is descriptive and cannot rescue a failed primary canonical-efficacy gate.

## Fixed seeds

- lineage base: `3230000`
- probe base: `3235000`
- rewire base: `3236000`
- paired-test base: `3237000`
- bootstrap base: `3238000`
- randomization draws: 50,000
- bootstrap draws: 20,000

## Stopping rule

This registration is committed before runner implementation and before any registered lineage/probe pair executes.

Allowed preflight: syntax, SHA checks, graph invariants, and synthetic decoder tests on non-registered records.

The first complete valid P3.21 run is the result. Vocabulary size, train/test split, decoder, information efficiency, branching-match rule, controller count, and thresholds are fixed.
