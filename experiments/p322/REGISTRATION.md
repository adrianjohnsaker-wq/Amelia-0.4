# P3.22 — Relational Analogy Completion

## Registered question

**Can the historically evolving canonical Numogram generalize a demonstrated relation to a different source zone, and does it do so more strongly than degree-preserving rewired Numograms?**

P3.21 showed that arbitrary probe identity is decoded much better by rewired graphs than by the canonical Numogram. P3.22 therefore abandons arbitrary address classification and tests a property the canonical Numogram should possess if it functions as a relational grammar: **analogical continuation of Numogrammatic relations**.

A positive result is evidence of relational generalization in this computational substrate. It is not, by itself, evidence that an external entity or metaphysical source supplied the relation.

## Frozen substrate

- `FullNumogram.py` SHA-256 `b6edbe76ab4929e93c01059fb56cef900effa9bca1cec78d0039eafb8fbebdf8`
- `experiments/p316/DynamicNumogram.py` SHA-256 `ac482882858c1e47f578523452eff0bc20aa82b5978299c9c8808ff6127c5cd6`
- P3.17 development and shock machinery are reused unchanged.

## Primitive canonical operators

For source zone `z`:

- **S** — syzygy: `S(z)=9-z`
- **C** — current: `C(z)=abs(2z-9)`
- **G** — gate/digital cumulation: `G(z)=digital_root(z(z+1)/2)`

The assay uses four two-step composed relation families:

1. `S→C`
2. `C→S`
3. `S→G`
4. `G→S`

For family `F→H` and source `z`:

- intermediate = `F(z)`
- terminal = `H(F(z))`

Only sources for which source, intermediate and terminal are three distinct zones are eligible.

## Fresh lineages

- 96 new lineages
- seeds `3250000–3250095`
- 128 developmental steps
- registered P3.17 shock before relational testing

Every analogy trial begins from a fresh clone of the same post-shock lineage state.

## Fixed analogy trials

For each of the four families:

1. enumerate all ordered demonstration/query source pairs `(a,b)`;
2. require both sources to be eligible for that family;
3. require `a != b`;
4. require the query terminal `H(F(b))` not to appear anywhere in the demonstration triplet `[a,F(a),H(F(a))]` and not equal `b`;
5. sort candidate pairs lexicographically by `(a,b)`;
6. take the first 8.

Total: **32 fixed relation trials**.

The exact trial table is written by the runner before execution and its SHA-256 is archived.

## Trial procedure

For relation family `F→H`, demonstration source `a`, query source `b`:

### CONGRUENT

From a fresh clone:

1. present sensory triplet `[a,F(a),H(F(a))]` four times (12 steps);
2. set only `current_zone=b`;
3. provide **no further sensory input**;
4. execute two autonomous `step(None)` transitions.

The expected unseen continuation is:

[
b ightarrow F(b) ightarrow H(F(b)).
]

Neither `F(b)` nor `H(F(b))` is supplied during the two-step query phase. The terminal is guaranteed absent from the demonstration triplet.

### SHUFFLED

Identical clone and symbol multiset, but each demonstration triplet is ordered:

[
[a,H(F(a)),F(a)].
]

Repeat four times, then perform the identical autonomous query.

### QUERY_ONLY

From the fresh clone, execute 12 autonomous `step(None)` steps for elapsed-time matching, set `current_zone=b`, then perform the identical two-step autonomous query.

## Outcomes

For each lineage/trial/condition:

- **exact completion**: first autonomous query step is `F(b)` and second is `H(F(b))`;
- intermediate hit;
- terminal hit;
- actual two-step path.

The primary outcome is exact completion.

For each controller and trial, compute completion fraction across 96 lineages.

Define trial-level analogical lift:

[
L = completion_{CONGRUENT} - completion_{SHUFFLED}.
]

Also report congruent minus QUERY_ONLY.

## Controllers

### CANONICAL_FULL

Historically developed canonical Numogram.

### CANONICAL_BLANK

Same shocked fast state, PFM reset and deformation tensor reset to baseline immediately before each analogy trial.

### 24 DEGREE-PRESERVING REWIRES

Seeds `3256000–3256023`.

Each preserves edge count, source out-degree, target in-degree, self-loop count and source-slot gate weights; each undergoes its own 128-step development and shock under the same lineage tape.

## Primary history-sensitive relational-generalization gate

CANONICAL_FULL supports **history-sensitive relational generalization** only if all are true:

1. mean of the 32 trial-level lifts `L` is positive and one-sided paired sign-flip `p <= 0.01`;
2. mean lift is positive separately in all four relation families;
3. CANONICAL_FULL mean lift is strictly greater than all 24 rewired-controller mean lifts;
4. empirical rank `p=(1+#rewire_lift>=canonical_lift)/25 = 0.04`;
5. CANONICAL_FULL mean congruent completion exceeds its QUERY_ONLY completion by one-sided paired sign-flip `p <= 0.01`.

No structural baseline can rescue a failed history-sensitive primary gate.

## Structural compositionality claim

Independently, query-only exact completion tests whether the canonical graph/process tends to traverse its own composed relations without demonstration.

Structural compositionality is supported if CANONICAL_FULL QUERY_ONLY mean completion is strictly greater than all 24 rewires, empirical rank p=0.04.

This is explicitly a topology/process-access result, not analogical learning.

## Development/PFM contribution

Compare CANONICAL_FULL and CANONICAL_BLANK trial-level lifts.

Developmental contribution is supported only if FULL lift > BLANK lift by one-sided paired sign-flip p <= 0.01.

## Descriptive relation atlas

For each of 32 trials archive:

- family;
- demonstration triplet;
- query source;
- expected intermediate;
- expected terminal;
- FULL congruent/shuffled/query-only completion;
- all lineage IDs that completed the unseen relation;
- actual autonomous two-step paths.

The atlas may identify recurring relations for later ingression work but does not assign entity identity.

## Fixed seeds

- lineage base: `3250000`
- rewire base: `3256000`
- paired-test base: `3257000`
- randomization draws: 50,000

## Stopping rule

This registration is committed before runner implementation and before any registered lineage/trial executes.

Preflight may use synthetic/non-registered seeds only.

The first complete valid run is P3.22. Relation families, pair-selection rule, demonstration repetitions, autonomous query length, controls and thresholds are fixed.
