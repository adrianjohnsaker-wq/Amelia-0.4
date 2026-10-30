# P3.17 — Ingression / Developmental Canalization Atlas

## Registered question

**Does the historically evolving full Numogram give rise, after developmental history and perturbation, to recurrent internal forms that were not present in the prior developmental repertoire and are not reducible to immediate input replay?**

P3.17 is deliberately centred on **ingression**: what appears that was not there before.

It does not reward movement toward an external scalar optimum. It does not define a target morphology in advance. Instead, it lets the dynamic Numogram develop under local sensory history, perturbs its fast state, and then asks whether previously absent forms emerge and recur across independent lineages.

A positive result would support a bounded computational claim: history-conditioned developmental dynamics generated recurrent novel forms under the registered assay. It would not by itself establish a metaphysical source, supernatural entity, or Platonic ontology.

## Relationship to P3.16

P3.16 found no privileged scalar morphospace-navigation advantage for the canonical dynamic process. P3.17 therefore changes the question rather than tuning P3.16:

- P3.16: can the process optimize navigation through a hidden scalar field?
- P3.17: can the process **develop new recurrent forms after perturbation** that depend on its history?

The dynamic engine is frozen from the first valid P3.16 run:

- `FullNumogram.py` SHA-256: `b6edbe76ab4929e93c01059fb56cef900effa9bca1cec78d0039eafb8fbebdf8`
- `experiments/p316/DynamicNumogram.py` SHA-256: `ac482882858c1e47f578523452eff0bc20aa82b5978299c9c8808ff6127c5cd6`

No dynamic equation is tuned for P3.17.

## Developmental sensory worlds

Each lineage receives a private sensory history generated independently of the Numogram.

A sensory world consists of two discrete ten-symbol tapes:

1. **developmental tape** — 128 symbols;
2. **post-perturbation tape** — 128 symbols.

For each tape, a ten-state transition matrix is sampled from an independent random generator. Rows are normalized positive random weights. The tape is then sampled from that matrix.

The post-perturbation tape is generated from a separate transition matrix and is rejection-filtered so that **no exact 4-symbol post tape window occurs in that lineage's developmental tape**.

The sensory generator never uses Numogram edges, phases, gate weights, memory state, or prior form identities.

## Cohorts

192 independent lineages are fixed before execution.

- discovery cohort: `D000–D095`, seeds **3170000–3170095**
- confirmation cohort: `C000–C095`, seeds **3170096–3170191**

The discovery cohort may identify candidate forms. The confirmation cohort is never used to define or modify candidate identities.

## Developmental phase

Every dynamic lineage begins with the same frozen full-Numogram process used in P3.16, with initial current zone `seed mod 10`.

For 128 developmental steps:

- the current sensory symbol is supplied through the registered Orange input-zone match channel;
- the dynamic process updates PFM, TraitEvolution, Governor, gate permeability, phase, deformation and current zone;
- every internal step is recorded.

There is no target morphology and no external reward.

## Perturbation

After developmental step 127, the lineage is cloned into matched post-development arms.

The same **fast-state shock** is applied to all history-bearing clones:

- current zone is set to `(seed * 7 + 3) mod 10`;
- each zone activation is compressed 90% toward 0.5;
- each zone phase angle is rotated by π;
- each conductivity is compressed 75% toward 0.5;
- polar charge is set to 0;
- deformation stress is compressed 80% toward 0.1;
- each gate permeability is reset to its original full-Numogram value.

The shock deliberately erases much of the immediately active state while leaving constitutive history available in the retained-history arm.

## Post-development arms

### A — HISTORY_RETAINED

Canonical full dynamic process after the fast-state shock. PFM event history, zone strain history, hysteresis and deformation tensor are retained.

### B — HISTORY_RESET

Identical shocked canonical state, but PFM events, strain history and hysteresis are reset before the novel post tape.

### C — HISTORY_PERMUTED

Identical shocked canonical state, but PFM state and deformation tensor are replaced by those of another lineage in the same cohort under a fixed derangement. The donor never equals the recipient.

### D — FRESH

A newly initialized canonical dynamic process begins the novel post tape from the same shocked current-zone index, without developmental history.

### E — STATIC_CANONICAL

The canonical graph is used as in P3.16's static arm: dynamic internal state is discarded between decisions; current zone alone carries forward.

### F — INPUT_REPLAY

The HISTORY_RETAINED shocked process receives its **developmental tape again**, rather than the novel post tape. This is a replay diagnostic, not a primary control.

### G — DYNAMIC_REWIRED

24 degree-preserving full dynamic Numogram controls undergo their own developmental phase, the identical shock, and the identical novel post tape. Every control preserves source out-degree, target in-degree, edge count, self-loop count and source-slot gate weights.

## What counts as a developmental form

No form identity is named in advance.

At every step, the atlas records:

- selected Numogram zone;
- most-active zone after the step;
- PFM hysteresis bin:
  - H0: <0.20
  - H1: 0.20–<0.40
  - H2: 0.40–<0.60
  - H3: >=0.60.

A candidate form is an exact contiguous Numogram path of length **3, 4 or 5** plus the endpoint state class:

[
F = (	ext{zone path}; 	ext{dominant activation zone}; 	ext{hysteresis bin}).
]

This makes the form more than a bare graph path while keeping it readable and traceable.

## Prior form catalogue

The following already-known Pointer paths are logged but do **not** count as new P3.17 forms when the full candidate path is exactly equal to one of them:

- `1-7`
- `1-7-8-9`
- `1-2-7`
- `7-8`
- `1-7-8`
- `1-8-7`

Because P3.17 candidate lengths are 3–5, only exact path matches at those lengths are excluded; longer paths containing a known shorter path remain eligible but are tagged as containing prior material.

## Discovery rule

A candidate may enter the discovery atlas only when all are true:

1. it occurs in HISTORY_RETAINED **after perturbation** in at least **8 of 96 discovery lineages**;
2. it has at least **12 total post-perturbation occurrences** in those lineages;
3. the exact form signature occurs **zero times** in the entire HISTORY_RETAINED developmental phase of the 96 discovery lineages;
4. its full zone path is not exactly one of the prior Pointer paths;
5. in at least 90% of discovery lineages containing the form, that form's zone path does **not** occur anywhere as an equal-length substring of that lineage's novel post sensory tape.

Candidates are ranked by discovery-lineage count, then total occurrence count, then lexical form ID. At most the top **20** candidates advance to confirmation.

The discovery algorithm and thresholds are fixed before execution; candidate identities are not.

## Confirmation rule

For each discovery candidate, presence/absence is scored independently in all 96 confirmation lineages for:

- HISTORY_RETAINED;
- HISTORY_RESET;
- HISTORY_PERMUTED;
- FRESH;
- STATIC_CANONICAL;
- INPUT_REPLAY;
- every DYNAMIC_REWIRED controller.

For HISTORY_RETAINED versus HISTORY_RESET and versus HISTORY_PERMUTED, one-sided exact paired sign tests are calculated from discordant lineage pairs.

If `K` candidates enter confirmation, the primary family threshold is Bonferroni:

[
alpha_* = 0.05/(2K).
]

A **confirmed new ingression form** must satisfy all of:

1. present in at least **8 of 96** HISTORY_RETAINED confirmation lineages;
2. HISTORY_RETAINED > HISTORY_RESET with one-sided paired `p <= alpha_*`;
3. HISTORY_RETAINED > HISTORY_PERMUTED with one-sided paired `p <= alpha_*`;
4. in at least 90% of HISTORY_RETAINED confirmation lineages containing it, its zone path is absent as an equal-length substring of that lineage's novel post sensory tape;
5. its exact form signature remains absent from the complete confirmation developmental-phase repertoire.

## Primary outcome

**INGRESSION CONFIRMED** if at least one discovery candidate becomes a confirmed new ingression form.

Otherwise:

**NO CONFIRMED NEW INGRESSING FORM UNDER P3.17.**

No secondary result may rescue failure of this primary outcome.

## Canalization and recurrence measures

For every discovery candidate, report:

- lineage prevalence in every arm;
- total occurrences;
- first post-perturbation appearance step;
- fraction of positive lineages in which the form appears at least twice after its first appearance;
- median recurrence interval;
- presence in the INPUT_REPLAY arm;
- mean prevalence across 24 dynamic rewires;
- whether the form contains any shorter prior Pointer path;
- all contributing lineage IDs and step ranges.

These measures describe whether a newly appearing form becomes canalized after its first appearance.

## Developmental-return atlas

Separately from the primary novelty test, the report also lists forms that were present during development and reappear after the shock. These are **return forms**, not new ingression forms. They are kept separate so developmental memory and genuine novelty are not conflated.

## Fixed seeds

- lineage seed base: `3170000`
- dynamic rewire seed base: `3173000`
- history-permutation seed: `3174000`

## Provenance and stopping rule

The registration is committed before the runner is created and before any lineage in seeds 3170000–3170191 is executed.

Permitted pre-run checks:

- Python syntax;
- frozen P3.16 engine SHA-256;
- control degree/self-loop invariants;
- history-permutation derangement;
- sensory-tape 4-gram separation on non-registered test seeds only.

No registered lineage may be executed during preflight.

The **first complete valid run** is the P3.17 result. Negative outcomes are archived without threshold or parameter adjustment.
