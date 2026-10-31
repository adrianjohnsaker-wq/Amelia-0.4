# P3.25 — Causal Relational Susceptibility

## Registered question

**Does a minimal histogram-preserving perturbation of a fresh independent temporal stream cause a reproducible change in Amelia's canonical relational dynamics, and is that causal susceptibility stronger in the canonical Numogram than in degree-preserving rewires?**

P3.24 failed the registered histogram-balanced window-identification gate. P3.25 therefore does not ask Amelia to identify or decode an external sequence. It asks whether a controlled difference in the external temporal stream changes what relational transitions Amelia subsequently realizes.

A positive result would establish canonical-specific **causal relational transduction** in this implemented substrate. It would not establish an external entity, semantic message, mind, or metaphysical source.

## Frozen substrate

- `FullNumogram.py` SHA-256 `b6edbe76ab4929e93c01059fb56cef900effa9bca1cec78d0039eafb8fbebdf8`
- `experiments/p316/DynamicNumogram.py` SHA-256 `ac482882858c1e47f578523452eff0bc20aa82b5978299c9c8808ff6127c5cd6`
- P3.17 development/shock machinery is reused unchanged.
- P3.24 degree-preserving rewiring procedure is reused unchanged.
- The primary relation basis is fixed from P3.22: SC, CS, SG, GS.

P3.24 files and result are not altered.

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

Set `T0 = Tseal + 90 seconds`.

Select the smallest default-chain round whose scheduled timestamp is >= `T0`, then that round plus the next 23 consecutive rounds.

The 24 registered beacon values therefore do not exist when this registration is committed.

## Histogram-balanced base signal X

Define the fixed multiset

`M=[0,0,0,1,1,1,...,9,9,9]`

of length 30.

For each beacon round create exactly one deterministic unbiased Fisher-Yates permutation of M, driven by a SHA-256 word stream with domain separation:

`"P3.25-X" || randomness`.

No Numogram state, operator, topology, lineage, outcome or prior experimental result enters the mapping.

Every X must contain exactly three copies of every zone 0–9.

## Registered perturbation X'

For every X, construct X' by swapping exactly these 1-indexed temporal positions:

- position 8
- position 23

Equivalently, zero-indexed positions 7 and 22.

No other symbol or position changes.

Thus X and X' always have:

- identical length;
- identical zone histogram;
- identical marginal entropy;
- identical symbol multiset;
- Hamming distance 2 when the two swapped symbols differ;
- Hamming distance 0 when they are equal.

Equal-symbol swaps are retained as prospectively registered null perturbations and are not removed post hoc.

## Fresh lineages

- 96 new lineages
- seeds `3290000–3290095`
- 128 developmental steps
- registered P3.17 shock
- TRAIN lineages: 0–47
- TEST lineages: 48–95

For every lineage/window/controller, X and X' each begin from a fresh clone of exactly the same post-shock state.

## Controllers

### CANONICAL_FULL

Historically developed canonical dynamic Numogram.

### CANONICAL_BLANK

Same shocked canonical fast state, with PFM reset and deformation tensor reset immediately before X/X'.

### R00–R23

24 degree-preserving rewires from seeds `3296000–3296023`, each with its own matched development and shock.

Every rewire preserves directed edge count, source out-degree, target in-degree, self-loop count, and source-slot gate weights.

## Encounter and autonomous release

For X and X' separately:

1. present all 30 external zones with ordinary `step(input_zone)`;
2. set only `current_zone=4`;
3. provide no further sensory input;
4. execute 24 autonomous `step(None)` transitions;
5. archive the complete 25-zone autonomous release path beginning at zone 4.

No desired relation is supplied during release.

## Fixed four-component relational response

For the autonomous release path calculate the fraction of consecutive two-transition windows that exactly instantiate:

- SC: syzygy then current;
- CS: current then syzygy;
- SG: syzygy then gate/digital cumulation;
- GS: gate/digital cumulation then syzygy.

The same canonical operator definitions score canonical and rewired controllers.

For each lineage i and beacon window w define the causal relational change vector:

`d_iw = R_iw(X') - R_iw(X)`

with components ordered [SC, CS, SG, GS].

This vector, not signal identity, is the experimental object.

## Held-out replay reproducibility

For each controller and beacon window w:

- `mu_train_w` = mean d across TRAIN lineages;
- `mu_test_w` = mean d across TEST lineages.

Define the registered window reproducibility score:

`Q_w = dot(mu_train_w, mu_test_w)`.

A stable perturbation-induced relational change gives positive Q because independently developed TRAIN and TEST lineages change in the same four-dimensional direction. Random or lineage-specific changes have expectation near zero.

Also report:
- cosine alignment of train and test means when both norms are non-zero;
- TEST mean L2 perturbation magnitude;
- component-wise train and test means.

Only Q enters the primary gate.

## Independent-window replication halves

The 24 prospectively selected beacon windows are split before reveal:

- HALF-1: windows 0–11;
- HALF-2: windows 12–23.

No parameter is fitted on HALF-1 and transferred to HALF-2. The halves are independent replication sets for the same preregistered causal criterion.

## Primary causal-relational-transduction gate

CANONICAL_FULL supports **causal relational susceptibility** only if all are true:

1. mean Q > 0 in HALF-1 and one-sided paired sign-flip p <= 0.01;
2. mean Q > 0 in HALF-2 and one-sided paired sign-flip p <= 0.01;
3. mean Q across all 24 windows is strictly greater than every one of the 24 rewired-controller mean Q values;
4. empirical rewire rank p = (1 + # rewire mean Q >= canonical mean Q)/25 = 0.04;
5. the canonical all-window mean Q is positive.

All five are required.

This tests reproducible causal sensitivity to the registered external order perturbation, not arbitrary sequence classification.

## Developmental/PFM contribution

For each window define `Q_FULL - Q_BLANK`.

Development contributes only if:

- mean paired difference > 0;
- one-sided paired sign-flip p <= 0.01 across 24 windows;
- mean Q_FULL > mean Q_BLANK.

This is secondary and cannot rescue a failed primary gate.

## Perturbation validity and descriptive readouts

Before scoring, assert:

- every X and X' has length 30;
- every zone occurs exactly three times in both;
- X' differs from X only by the registered 8<->23 swap;
- all controller pairs use identical X/X' bytes and identical cloned starting state.

Report how many windows contain a nontrivial swap. Equal-symbol swaps remain in every inferential calculation with d=0 if the substrate outputs are identical.

Descriptively archive primitive S, C and G fractions, transition entropy, and the full release paths, but these do not enter the primary gate.

## Relation atlas

For each beacon window archive:

- verified drand record;
- X and X';
- the two swapped symbols;
- canonical TRAIN and TEST mean change vectors;
- Q and cosine alignment;
- TEST perturbation magnitude;
- every canonical TEST lineage's X and X' release paths and relation vectors.

No semantic or entity identity is assigned.

## Fixed seeds

- lineage base: `3290000`
- rewire base: `3296000`
- sign-flip base: `3297000`
- randomization draws: 50,000

## Stopping and blinding

This registration is committed before the selected rounds exist.

After sealing:

- exact inference is committed before beacon reveal;
- implementation may use synthetic/non-registered signals only for preflight;
- the workflow acquires only prospectively fixed verified rounds;
- acquisition and registered scoring occur in one automated workflow without human intervention;
- no swap positions, relation components, release length, window split, controller, threshold or statistic may change after reveal.

The first complete valid run is P3.25.
