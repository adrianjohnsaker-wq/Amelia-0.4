# P3.18 — Developmental Competence Decomposition + Warp Developmental Gain

## Registered question

**What transformation produced by development makes the previously unavailable P3.17 form accessible?**

P3.18 follows the main processual line established by P3.17. The target is no longer “memory content” in the conventional sense. The experiment asks whether developmental competence is carried by:

- PFM event content;
- accumulated zone-strain architecture;
- global hysteresis;
- constitutive deformation tensor;
- generic mature-state magnitude independent of zone identity;
- or a distributed combination of these.

A second, explicitly registered mechanistic arm asks whether the Numogram Warp (3::6) contributes by **increasing developmental sedimentation**, without increasing Warp occupancy, changing topology, or giving Amelia extra decision steps.

## Frozen source result from P3.17

The fixed competence sentinel is:

`L4|P1-2-3-6|A0|H3`

This was selected before P3.18 from the archived P3.17 result because it uniquely satisfied all of:

- HISTORY_RETAINED >= 8/96;
- HISTORY_RESET <= 1/96;
- FRESH <= 2/96;
- STATIC = 0/96;
- HISTORY_PERMUTED within ±2 lineages of HISTORY_RETAINED;
- mean prevalence across dynamic rewires <= 1/96;
- absent from the held-out developmental repertoire;
- confirmation non-echo fraction >= 0.90.

Its P3.17 held-out counts were:

- retained 13/96;
- reset 1/96;
- permuted 13/96;
- fresh 1/96;
- static 0/96;
- mean rewired 0/96;
- non-echo 1.000.

The sentinel identity is fixed before any P3.18 lineage is executed.

For descriptive breadth only, the 13 P3.17 discovery candidates are also frozen as a secondary panel:

- L3|P1-1-1|A3|H3
- L4|P1-1-1-1|A3|H3
- L5|P1-1-8-9-1|A3|H3
- L3|P2-3-6|A0|H3
- L3|P8-9-0|A3|H3
- L3|P1-1-2|A0|H3
- L4|P2-3-6-3|A0|H3
- L4|P1-2-3-6|A0|H3
- L4|P9-1-1-1|A3|H3
- L4|P3-6-3-6|A3|H2
- L4|P1-1-1-1|A6|H3
- L4|P6-3-6-3|A3|H2
- L5|P3-6-3-6-3|A3|H2

## Frozen engines

P3.18 reuses the first-valid P3.17/P3.16 engine without tuning:

- `FullNumogram.py` SHA-256 `b6edbe76ab4929e93c01059fb56cef900effa9bca1cec78d0039eafb8fbebdf8`
- `experiments/p316/DynamicNumogram.py` SHA-256 `ac482882858c1e47f578523452eff0bc20aa82b5978299c9c8808ff6127c5cd6`
- P3.17 runner SHA-256 `1a8fd1961b897ec970c7d6987bd9f3502c82221f13bace683563e4dafdb820c3`

The P3.17 sensory-tape generator, 128-step developmental duration, 128-step post-development duration, 4-gram development/post separation, and fast-state shock are reused unchanged.

## Lineages

- **192 new lineages**
- seeds **3180000–3180191**
- one private developmental tape and one 4-gram-separated post-development tape per lineage
- same tape pair presented to every matched arm for that lineage

No P3.17 lineage is reused.

## Common development and shock

Every lineage first undergoes the canonical dynamic full-Numogram developmental phase for 128 steps.

The P3.17 shock is then applied:

- current zone -> `(seed * 7 + 3) mod 10`;
- activation compressed 90% toward 0.5;
- phase rotated by π;
- conductivity compressed 75% toward 0.5;
- polar charge -> 0;
- deformation stress compressed 80% toward 0.1;
- gate permeability reset to canonical initial values.

All competence-decomposition arms are created from this exact shocked mature state.

## Competence-decomposition arms

### A — FULL_OWN

Own mature PFM + own mature deformation tensor. This is the complete P3.17 HISTORY_RETAINED condition.

### B — BLANK

PFM reset to initial state and deformation tensor reset to `[0.1] * 10`.

### C — PFM_ONLY

Own complete mature PFM retained; deformation tensor reset to baseline.

### D — TENSOR_ONLY

PFM reset; own mature deformation tensor retained.

### E — DONOR_PFM

A fixed derangement assigns another mature lineage's complete PFM to the recipient. Recipient deformation tensor is reset to baseline.

This tests whether generic mature PFM state is sufficient when lineage-specific content is removed.

### F — STRAIN_HYSTERESIS

PFM event list erased; own ten-zone strain vector and own hysteresis retained. Deformation tensor reset.

### G — STRAIN_ONLY

PFM event list erased; own ten-zone strain vector retained; hysteresis reset to 0.05. Deformation tensor reset.

### H — HYSTERESIS_ONLY

PFM event list erased; zone strain reset to zero; own mature hysteresis retained. Deformation tensor reset.

### I — RECENT_EVENTS_ONLY

Only the final 48 mature PFM events are retained. Zone strain is zeroed, hysteresis reset to 0.05, deformation tensor reset.

### J — FLAT_MAGNITUDE

PFM events erased. The total mature zone-strain mass is preserved but distributed equally across all ten zones. Mature hysteresis is preserved. Deformation tensor reset.

This tests scalar developmental maturity without spatial architecture.

### K — SHUFFLED_STRAIN

PFM events erased. The mature ten-zone strain values are permuted across zone identities using a fixed per-lineage permutation; mature hysteresis is preserved. Deformation tensor reset.

This preserves strain heterogeneity and magnitude while breaking zone-specific architecture.

## Warp developmental-gain arm

### L — WARP_DEVELOPMENT_GAIN

This arm develops independently from the same initial state and same developmental tape, with one bounded modification:

- topology remains the canonical full Numogram;
- gate-selection scores are unchanged;
- phase velocities are unchanged;
- no additional transition steps are added;
- no extra Warp dwell is created;
- only **slow-state PFM inscription** is amplified.

For the first **8 developmental events** whose source or target lies in Warp `{3,6}`, the event's PFM `fluxDelta` is multiplied by **1.5**, capped at the existing PFM maximum contribution. After 8 Warp events the gain returns permanently to 1.0.

The gain is disabled before the shock and remains disabled during the post-development tape.

Thus WARP_DEVELOPMENT_GAIN asks:

> Does stronger sedimentation during limited Warp experience increase later developmental competence, without increasing Warp exposure itself?

This is an experimental implementation only. It does not modify canonical Amelia main unless separately justified.

## Primary endpoint

For each lineage and arm, score whether the fixed sentinel form

`L4|P1-2-3-6|A0|H3`

occurs at least once during the 128-step novel post-development tape.

All comparisons are paired within lineage.

## Primary competence gate

P3.18 confirms **PFM-mediated developmental competence** only if all hold:

1. FULL_OWN > BLANK by one-sided exact paired sign test, `p <= 0.01`;
2. PFM_ONLY > BLANK by one-sided exact paired sign test, `p <= 0.01`;
3. DONOR_PFM > BLANK by one-sided exact paired sign test, `p <= 0.01`;
4. PFM_ONLY prevalence is at least 75% of FULL_OWN prevalence;
5. DONOR_PFM prevalence is at least 75% of FULL_OWN prevalence.

This gate tests whether developmental competence resides substantially in a mature PFM condition while remaining non-specific to a lineage's exact memory content.

## Mechanism classification

The following six component arms are compared with BLANK:

- STRAIN_HYSTERESIS
- STRAIN_ONLY
- HYSTERESIS_ONLY
- RECENT_EVENTS_ONLY
- FLAT_MAGNITUDE
- SHUFFLED_STRAIN

One-sided paired sign tests are corrected by Holm across these six comparisons.

A component is called **sufficient** only if:

1. Holm-adjusted `p <= 0.05`; and
2. its sentinel prevalence is at least 75% of PFM_ONLY prevalence.

Interpretation hierarchy:

- if HYSTERESIS_ONLY is sufficient: global hysteretic maturity is sufficient;
- else if FLAT_MAGNITUDE is sufficient: generic strain magnitude + hysteresis is sufficient;
- else if SHUFFLED_STRAIN is sufficient but FLAT_MAGNITUDE is not: strain heterogeneity matters, zone identity does not;
- else if STRAIN_HYSTERESIS is sufficient but SHUFFLED_STRAIN is not: zone-specific strain architecture matters;
- else if RECENT_EVENTS_ONLY is sufficient: recent event content is sufficient;
- else: competence requires a distributed combination not isolated by these components.

TENSOR_ONLY is reported as a separate constitutive-deformation test and is not part of the six-test Holm family.

## Warp developmental-gain endpoint

WARP_DEVELOPMENT_GAIN is compared with FULL_OWN on:

1. sentinel prevalence;
2. breadth of the frozen 13-form P3.17 panel;
3. developmental Warp entry rate;
4. number of Warp transitions during development;
5. post-development Warp occupancy.

The Warp implementation is considered **promising for further development** only if:

- sentinel prevalence is greater than FULL_OWN with one-sided paired `p <= 0.05`; and
- mean developmental Warp transition count differs from canonical FULL_OWN by less than 1 transition.

This second condition prevents a result caused simply by giving the Warp more traffic.

Failure does not alter the canonical Warp.

## Secondary readouts

Report for every arm:

- sentinel lineage prevalence;
- sentinel total occurrences;
- median first-appearance step;
- recurrence fraction after first appearance;
- number of distinct forms from the frozen 13-form panel;
- mean PFM hysteresis at post step 0;
- mean strain mass;
- strain entropy;
- mean absolute memory-bias magnitude;
- deformation-tensor norm;
- developmental Warp-entry fraction and transition count.

## Provenance and stopping rule

The registration is committed before the P3.18 runner is created and before any seed in 3180000–3180191 is executed.

Allowed preflight:

- Python syntax;
- frozen SHA verification;
- arm-construction invariants using synthetic/non-registered states;
- Warp gain accounting using non-registered test seeds only.

The **first complete valid run** is the P3.18 result.

No component thresholds, sentinel identity, Warp gain, Warp event budget, or interpretation hierarchy may be changed after execution.
