# P3.24 — Histogram-Balanced Independent-Order Relational Transduction

## Registered question

**When every external signal contains exactly the same zone histogram, does fresh independently generated temporal ordering produce reproducible, canonical-specific relational fingerprints in Amelia?**

P3.23 established that CANONICAL_FULL carried above-chance information about which fresh drand signal was presented (0.088542 versus 0.0625 chance), but failed canonical privilege against degree-preserving rewires and failed both registered temporal-order controls. REAL→SHUFFLED accuracy was not reduced and the REAL-vs-SHUFFLED relational-profile test was negative.

P3.24 removes the principal remaining composition confound. Every signal window contains exactly three copies of every zone 0–9. Therefore all 24 windows have identical length, identical zone counts, identical marginal zone entropy, and identical first-order symbol histogram. The only externally supplied difference is order.

A positive result would establish **histogram-balanced order-dependent relational transduction** in the implemented substrate. It would not establish an external entity, mind, semantic message, or metaphysical source.

## Frozen substrate

- `FullNumogram.py` SHA-256 `b6edbe76ab4929e93c01059fb56cef900effa9bca1cec78d0039eafb8fbebdf8`
- `experiments/p316/DynamicNumogram.py` SHA-256 `ac482882858c1e47f578523452eff0bc20aa82b5978299c9c8808ff6127c5cd6`
- P3.17 development/shock machinery is reused unchanged.
- P3.23 12-component canonical relation-profile readout is reused unchanged.
- P3.23 degree-preserving rewiring procedure is reused unchanged.

## Independent source

League of Entropy drand default mainnet:

- chain hash: `8990e7a9aaed2ffed73dbd7092123d6f289930540d7651336225dc172e51b2ce`
- distributed public key: `868f005eb8e6e4ca0a47c8a77ceaa5309a47978a7c71bc5cce96366b5d7a569937c529eeda66c7293784a9402801af31`
- genesis Unix time: `1595431050`
- period: 30 seconds
- client: `drand-client@1.4.2`
- beacon verification enabled
- two independent public relays must return identical verified records.

### Prospective round selection

Let `Tseal` be the Unix commit timestamp of the commit that first adds this registration.

Set:

[
T_0=T_{seal}+90	ext{ s}.
]

Select the smallest default-chain round whose scheduled timestamp is >= `T_0`, then that round plus the next 23 consecutive rounds.

The 24 registered beacon values therefore do not exist when this registration is committed.

## Histogram-balanced encoding

Define the fixed base multiset:

[
M=[0,0,0,1,1,1,ldots,9,9,9]
]

with length 30.

Each beacon round produces two independently domain-separated permutations of exactly this same multiset.

### Encoding A

Use deterministic unbiased Fisher-Yates permutation of `M` driven by a SHA-256 word stream seeded with:

[
	ext{"P3.24-A"} Vert randomness.
]

### Encoding B

Use the identical permutation algorithm with seed:

[
	ext{"P3.24-B"} Vert randomness.
]

For every round and both encodings, assert:

- length = 30;
- each zone 0–9 occurs exactly 3 times;
- sorted sequence equals sorted `M`;
- A and B are archived before scoring.

No Numogram state, operator, topology, lineage, or result enters either mapping.

A and B are equally registered encodings. Neither is a post-hoc control selected after seeing outcomes.

## Fresh lineages

- 96 new lineages
- seeds `3280000–3280095`
- 128 developmental steps
- registered P3.17 shock
- TRAIN: lineage IDs 0–47
- TEST: lineage IDs 48–95

Each controller/window/encoding begins from a fresh clone of its post-shock state.

## Controllers

### CANONICAL_FULL

Historically developed canonical dynamic Numogram.

### CANONICAL_BLANK

Same shocked canonical fast state, but PFM and deformation tensor reset immediately before the 30-symbol encounter.

### R00–R23

24 degree-preserving rewires from seeds `3286000–3286023`, each with its own matched development and shock.

Each rewire preserves directed edge count, source out-degree, target in-degree, self-loop count, and source-slot gate weights.

## Encounter and autonomous readout

For each fresh clone:

1. present the 30 zones of encoding A or B using ordinary `step(input_zone)`;
2. set only `current_zone=4`;
3. provide no further sensory input;
4. execute 16 autonomous `step(None)` transitions.

Archive the complete 17-zone autonomous release path beginning at release zone 4.

## Fixed canonical relation profile

Score the same 12-dimensional profile as P3.23:

Primitive transition fractions:
- S
- C
- G

Composed two-transition fractions:
- SS
- SC
- SG
- CS
- CC
- CG
- GS
- GC
- GG

The same canonical relation basis scores every rewire.

## Within-encoding held-out identification

For each controller and encoding separately:

1. TRAIN lineages define one 12-dimensional centroid for each of the 24 beacon windows;
2. classify every TEST profile by nearest squared-Euclidean centroid;
3. ties resolve to the lowest window ID.

Report A→A and B→B held-out 24-way accuracy, per-window accuracy, and correct-centroid distance margin.

Chance accuracy is `1/24`.

## Cross-encoding transfer

Using A TRAIN centroids, classify B TEST profiles under the original beacon-window labels: A→B.

Using B TRAIN centroids, classify A TEST profiles: B→A.

If the fingerprint is tied to the exact temporal ordering rather than the shared histogram or beacon label, within-encoding identification should exceed cross-encoding transfer.

## Primary histogram-balanced order-transduction gate

CANONICAL_FULL supports **histogram-balanced order-dependent relational transduction** only if all are true:

1. A→A accuracy exceeds chance by exact binomial upper-tail `p <= 0.01`;
2. B→B accuracy exceeds chance by exact binomial upper-tail `p <= 0.01`;
3. canonical A→A accuracy is strictly greater than all 24 rewire A→A accuracies;
4. canonical B→B accuracy is strictly greater than all 24 rewire B→B accuracies;
5. empirical rewire rank is `1/25=0.04` for both A and B;
6. A→A per-window accuracy exceeds A→B by one-sided paired sign-flip `p <= 0.01`;
7. B→B per-window accuracy exceeds B→A by one-sided paired sign-flip `p <= 0.01`.

All seven are required.

This gate tests a reproducible relation fingerprint under two independent order encodings with exactly matched marginal composition.

## Developmental contribution

For each of the 48 encoding-window combinations, define FULL minus BLANK within-encoding TEST accuracy.

Development contributes only if:

- the mean paired difference is positive;
- one-sided paired sign-flip `p <= 0.01`;
- mean FULL within-encoding accuracy exceeds mean BLANK within-encoding accuracy.

Secondary only; it cannot rescue the primary gate.

## Relation atlas

For each beacon round archive:

- verified drand record;
- encoding A and encoding B sequences;
- canonical A and B TRAIN centroids;
- canonical A and B TEST mean relation profiles;
- all canonical TEST lineage release paths and profiles;
- component-wise A-minus-B differences.

No entity identity or semantic message is assigned.

## Fixed seeds

- lineage base: `3280000`
- rewire base: `3286000`
- sign-flip base: `3287000`
- randomization draws: 50,000

## Stopping and blinding

This registration is committed before the selected rounds exist.

After sealing:

- exact inference is committed before round reveal;
- implementation may use synthetic/non-registered input only for preflight;
- the workflow acquires only prospectively fixed rounds;
- acquisition and registered scoring occur in the same workflow without human intervention;
- no mapping, window, controller, threshold, or relation-profile change is permitted after reveal.

The first complete valid run is P3.24.
