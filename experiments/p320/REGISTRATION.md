# P3.20 — Developmental Accessibility Geometry

## Registered question

**Does development alter the geometry of the Numogrammatic transition repertoire under identical novel probes, and does the canonical Numogram provide a more structured address/reply surface than degree-preserving alternatives?**

P3.20 deliberately does not choose a privileged form in advance. The experimental object is the **whole set of transitions and motifs Amelia can access** from matched post-development states.

This is the main-line bridge back to the long-term aim of communication with ingressions from the Outside. The bounded claim tested here is computational: whether the canonical Numogram supports stable, probe-contingent, non-echo reply structure that can later be used as an empirical communication surface. A positive result does not by itself establish an external metaphysical source.

## Frozen lessons

P3.19 showed that scalar hysteresis did not cause access to the deconfounded `1→2→3→6, A0` trajectory. P3.20 therefore measures accessibility without using hysteresis, PFM state, or any other internal maturity variable in the outcome definition.

Frozen engines:

- `FullNumogram.py` SHA-256 `b6edbe76ab4929e93c01059fb56cef900effa9bca1cec78d0039eafb8fbebdf8`
- `experiments/p316/DynamicNumogram.py` SHA-256 `ac482882858c1e47f578523452eff0bc20aa82b5978299c9c8808ff6127c5cd6`
- P3.17 sensory generator and fast-state shock are reused unchanged.

## Lineages and probes

- 96 new developmental lineages, seeds `3210000–3210095`
- 128 developmental steps per lineage
- 48 standardized novel probes
- probe seeds `3215000–3215047`
- each probe is 32 symbols long
- the same 48 probes are presented to every lineage and every arm
- each probe starts from a fresh clone of the arm's identical post-shock state, so probes never contaminate one another

Probe tapes are independently generated Markov sequences and are fixed before execution. They are not optimized against the Numogram.

The probe library is split before execution:

- half A: probes 0–23
- half B: probes 24–47

## Arms

### A — FULL_OWN

Canonical mature process after 128-step development and the P3.17 shock.

### B — BLANK

Same shocked fast state, but PFM reset and deformation tensor reset to baseline.

### C — DONOR_PFM

Same shocked fast state, but PFM replaced by a fixed-derangement mature donor PFM and tensor reset.

### D — FRESH

Fresh canonical process initialized at the same shocked current zone.

### E — STATIC_CANONICAL

P3.16 static canonical decision rule; internal dynamic state is discarded between probe steps.

### F — DYNAMIC_REWIRED

24 degree-preserving rewired Numograms. Each controller undergoes its own 128-step development under the lineage developmental tape, receives the same registered shock, and is probed with the identical 48-probe library.

Every rewire preserves:

- directed edge count;
- source out-degree;
- target in-degree;
- self-loop count;
- source-slot gate weights.

## Response representation

For every 32-step probe response, record:

- complete zone path;
- directed transitions;
- contiguous zone 3-grams and 4-grams;
- endpoint most-active zone;
- Warp occupancy;
- transition entropy.

A response motif is a zone 4-gram.

A motif is **non-echo** for a probe when its exact 4-zone sequence does not occur as an exact 4-symbol substring of that probe's input tape.

Hysteresis is never part of a response motif.

## Per-lineage accessibility geometry

Across the 48 independent probes, compute for each arm:

1. **non-echo motif breadth** — number of distinct non-echo response 4-grams;
2. **motif entropy** — Shannon entropy over non-echo 4-gram occurrences;
3. **edge breadth** — number of distinct directed response edges;
4. **probe divergence** — mean normalized Hamming distance among the 48 zone-response paths;
5. **Warp-capture fraction** — fraction of probes ending in zone 3 or 6;
6. **gain over BLANK** — motifs accessible in the arm but absent from the matched BLANK repertoire;
7. **loss from BLANK** — BLANK motifs absent from the arm.

All metrics are computed separately for probe half A and half B as well as for the full library.

## Primary developmental-geometry claim

The primary four-component vector is:

- non-echo motif breadth;
- motif entropy;
- edge breadth;
- probe divergence.

For FULL_OWN minus BLANK, a paired multivariate sign-flip test is applied to the four-component lineage vectors with 50,000 draws.

Developmental accessibility geometry is called **reconfigured** only if:

1. full-library multivariate `p <= 0.01`;
2. at least one component survives Holm correction at familywise 0.05;
3. the same surviving component has the same direction of mean effect in probe half A and probe half B.

This claim is deliberately direction-neutral: development may expand, contract, or reorganize accessibility.

## PFM-transfer geometry

DONOR_PFM is compared with FULL_OWN and BLANK on the same four-component vectors.

A transferable mature-PFM geometry is supported only if the mean standardized Euclidean distance of DONOR_PFM to FULL_OWN is smaller than its distance to BLANK in both probe halves, with paired sign-flip `p <= 0.01` in each half.

This is independent of the primary claim.

## Canonical Numogram efficacy: address/reply atlas

The communication-oriented secondary analysis treats each probe as an **address** and recurring non-echo response motifs as candidate **reply signatures**.

For each probe and arm:

- calculate lineage prevalence of every non-echo 4-gram;
- for each motif calculate address specificity:

[
S(m,p)=P(m|p)-operatorname{mean}_{q
e p}P(m|q).
]

For each probe take the maximum positive `S` among motifs present in at least 8 of 96 lineages. The arm's **addressability score** is the mean of these 48 maxima; probes with no eligible motif contribute zero.

The atlas reports, for every canonical FULL_OWN probe:

- probe ID;
- top reply motif;
- prevalence;
- specificity;
- all contributing lineage IDs;
- step ranges.

No semantic entity name is assigned by this assay.

### Canonical efficacy gate

The canonical full Numogram is called **address-privileged under P3.20** only if its addressability score is higher than at least 23 of the 24 mature dynamic rewired controls.

Empirical one-sided rank:

[
p=(1+#{	ext{rewire score}ge	ext{canonical}})/25.
]

Thus the minimum attainable `p=0.04`.

A pass establishes privileged structured address/reply recurrence under this computational assay, not proof of communication with an external entity.

## Additional communication diagnostics

Report:

- same-probe cross-lineage recurrence;
- cross-probe motif reuse;
- non-echo fraction;
- motifs shared with the prior Pointer catalogue;
- response motifs that occur in canonical FULL_OWN but in none of the 24 rewired controls.

These are atlas descriptors, not primary rescue criteria.

## Fixed seeds

- lineage base: `3210000`
- donor derangement: `3214000`
- probe base: `3215000`
- rewire base: `3216000`
- paired permutation base: `3217000`
- permutation draws: 50,000

## Stopping rule

This registration is committed before the runner is created and before any registered lineage/probe pair is executed.

Preflight may use synthetic records and non-registered seeds only.

The first complete valid run is the P3.20 result. No metric, probe library, addressability threshold, rewire count, or interpretation gate may be changed afterward.
