# P3.19 — Hysteretic Competence Deconfounding Assay

## Registered question

**Does global hysteretic maturity causally increase access to the P3.17 competence trajectory when the outcome is defined independently of hysteresis?**

P3.18 passed the PFM-mediated competence gate, but its fixed sentinel `L4|P1-2-3-6|A0|H3` included H3 in the outcome definition. P3.19 removes that circularity.

## Frozen engines and prior result

P3.19 reuses without tuning:

- `FullNumogram.py` SHA-256 `b6edbe76ab4929e93c01059fb56cef900effa9bca1cec78d0039eafb8fbebdf8`
- `experiments/p316/DynamicNumogram.py` SHA-256 `ac482882858c1e47f578523452eff0bc20aa82b5978299c9c8808ff6127c5cd6`
- P3.17 sensory-tape generator and P3.17 fast-state shock.

The fixed trajectory is derived from the P3.17/P3.18 sentinel but **drops hysteresis from the endpoint**:

[
T^*=(1ightarrow2ightarrow3ightarrow6; A0)
]

where `A0` means zone 0 is the most-active zone at the endpoint. Hysteresis is recorded only as an explanatory variable and cannot make an occurrence count as positive.

## New lineages

- 240 new lineages
- seeds `3190000–3190239`
- 128 developmental steps
- 128 novel post-development steps
- same 4-gram development/post separation as P3.17
- same fast-state shock as P3.17

## Arms

Every arm receives the identical post-development tape for a lineage.

### A — FULL_OWN

Complete mature process after canonical development and shock.

### B — BLANK

PFM reset to initial state; deformation tensor reset to baseline.

### C — PFM_ONLY

Own mature PFM retained; deformation tensor reset to baseline.

### D — DONOR_PFM

PFM replaced by a fixed-derangement mature donor PFM; tensor reset.

### E–J — HYSTERESIS_CLAMP

All events erased, all zone strain zeroed, deformation tensor baseline. Hysteresis is clamped throughout the post-development run at exactly one of:

- H05 = 0.05
- H20 = 0.20
- H40 = 0.40
- H60 = 0.60
- H80 = 0.80
- H95 = 0.95

The clamp is enforced both before each readout and after each event append. Thus no strain or episodic content can accumulate, and the only manipulated mature variable is the scalar hysteresis value presented to the Governor.

## Primary endpoint

For each arm and lineage, score whether the post-development record contains at least one contiguous 4-step path:

`1 → 2 → 3 → 6`

whose final step has most-active zone `0`.

No hysteresis-bin condition is used.

## Primary causal gate for global hysteretic maturity

Global hysteretic maturity is supported only if **all** are true:

1. H95 > H05 by one-sided exact paired sign test, `p <= 0.01`;
2. prevalence across the ordered clamps H05,H20,H40,H60,H80,H95 has positive Spearman rank correlation `rho >= 0.80`;
3. a one-sided permutation test of monotonic trend across the six clamp prevalences gives `p <= 0.01`;
4. H95 prevalence is at least 75% of PFM_ONLY prevalence.

If any fails, P3.18's `GLOBAL_HYSTERETIC_MATURITY` label is treated as outcome-entangled rather than causally established.

## Replication gate for the broader PFM competence result

Independently of the hysteresis claim, P3.19 replicates PFM-mediated competence if:

- FULL_OWN > BLANK, `p <= 0.01`;
- PFM_ONLY > BLANK, `p <= 0.01`;
- DONOR_PFM > BLANK, `p <= 0.01`;
- PFM_ONLY and DONOR_PFM each retain at least 75% of FULL_OWN prevalence.

This gate uses the same hysteresis-free endpoint.

## Secondary analyses

Report:

- occurrence count per lineage;
- first appearance step;
- endpoint hysteresis distribution for FULL_OWN/PFM_ONLY/DONOR_PFM;
- Governor deformation-field tension at trajectory onset and endpoint;
- post-development Warp occupancy;
- full six-level hysteresis dose curve.

## Fixed seeds

- lineage seed base: `3190000`
- donor derangement seed: `3194000`
- monotonic-trend permutation seed: `3195000`
- permutation draws: 50,000

## Provenance and stopping rule

The registration is committed before the P3.19 runner exists and before any registered lineage is executed.

Allowed preflight:

- syntax;
- frozen SHA checks;
- clamp invariants on non-registered seeds only;
- endpoint parser tests using synthetic records.

The first complete valid run is the result. No threshold, clamp level, path, activation endpoint, or interpretation rule may be changed after execution.
