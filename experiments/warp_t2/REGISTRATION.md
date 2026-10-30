# WARP-T2 — Portable Passage Trace

## Registered question

**After canonical terminal capture is removed and every arm is released into the same non-Warp fast state, does a finite passage through 3::6 leave a portable transformation that changes later development?**

WARP-T1 established two distinct facts:

1. crossing into the canonical Warp produces a measurable PFM state change;
2. the extraordinary 3::6 canalization is principally caused by canonical terminality, not by the entry inscription itself.

WARP-T2 therefore removes terminal capture from the downstream assay and asks whether any transformation survives **after release**.

## Frozen engines

- `FullNumogram.py` SHA-256 `b6edbe76ab4929e93c01059fb56cef900effa9bca1cec78d0039eafb8fbebdf8`
- `experiments/p316/DynamicNumogram.py` SHA-256 `ac482882858c1e47f578523452eff0bc20aa82b5978299c9c8808ff6127c5cd6`
- P3.17 sensory generator is reused.

No canonical Amelia parameter is strengthened.

## Lineages

- 192 new lineages
- seeds `3220000–3220191`
- each lineage develops until its first natural entry into Warp from outside {3,6}, within a maximum of 256 sensory steps
- lineages without an eligible entry remain in the archive but do not enter paired passage analyses

## Finite passage

From the exact pre-entry snapshot, the registered Warp passage consists of:

1. the natural entry step into zone 3 or 6;
2. four additional canonical steps while inside 3::6.

Thus the passage has exactly **five transition events** including entry.

The exact five sensory symbols used during the real Warp passage are reused across paired passage arms.

## Passage arms before release

### A — REAL_WARP_PASSAGE

Natural entry plus four canonical Warp steps with ordinary PFM inscription and constitutive deformation.

### B — ENTRY_ONLY

The exact natural entry event is completed and inscribed. The next four passage events are replaced by neutral bookkeeping events with zero fluxDelta and neutral phase coherence while current zone alternation is forced only for temporal matching. This preserves entry but removes subsequent slow-state passage inscription.

### C — TOPOLOGY_ONLY_PASSAGE

The same five zone transitions as REAL_WARP_PASSAGE occur, but all five PFM events are neutralized: zero fluxDelta and neutral recent-mean phase coherence.

### D — MATCHED_NONWARP_PASSAGE

From the exact pre-entry snapshot, each of the five passage steps chooses the highest-scoring legal non-Warp target under a Warp-open degree-preserving topology. The same five sensory symbols are used. This is a time- and input-matched exterior passage.

Only lineages for which all five matched steps can remain outside {3,6} are included in this arm's paired comparisons.

## Common-state release

Immediately after the five-event passage, **all downstream arms are placed into the same fast release shell**:

- zone activations copied from the lineage's exact pre-entry snapshot;
- conductivities copied from pre-entry;
- phase angles copied from pre-entry;
- polar charges copied from pre-entry;
- deformation stresses copied from pre-entry;
- Governor state copied from pre-entry;
- gate permeabilities reset to the same registered WARP_OPEN topology;
- current zone set to a deterministic non-Warp release zone chosen from `[0,1,2,4,5,7,8,9]` by `seed mod 8`;
- visit and transition counters reset.

Thus any post-release difference can arise only from retained slow-state material.

The WARP_OPEN topology remains active throughout the downstream probe so 3::6 cannot produce terminal recapture.

## Released slow-state arms

From each passage history construct:

### A1 — WARP_FULL_TRACE

Preserve REAL_WARP_PASSAGE PFM plus deformation tensor.

### A2 — WARP_PFM_TRACE

Preserve REAL_WARP_PASSAGE PFM; tensor reset to baseline.

### A3 — WARP_TENSOR_TRACE

PFM reset; preserve REAL_WARP_PASSAGE deformation tensor.

### A4 — WARP_TRACE_RESET

PFM reset and tensor reset.

### B1 — ENTRY_ONLY_TRACE

Preserve ENTRY_ONLY PFM plus tensor.

### C1 — TOPOLOGY_ONLY_TRACE

Preserve TOPOLOGY_ONLY_PASSAGE PFM plus tensor.

### D1 — NONWARP_FULL_TRACE

Preserve MATCHED_NONWARP_PASSAGE PFM plus tensor.

## Post-release probe

Every released arm receives the identical 64-symbol novel probe tape for that lineage.

The probe is generated independently of developmental and passage tapes and is rejection-filtered against exact 4-gram overlap with the five passage sensory symbols.

## Downstream response vector

Measure separately in early steps 0–31 and late steps 32–63:

1. zone occupancy entropy;
2. transition entropy;
3. distinct visited zones;
4. distinct response 4-grams;
5. non-echo response 4-gram breadth relative to the release probe;
6. Warp occupancy under WARP_OPEN;
7. mean absolute memory-bias magnitude;
8. activation concentration (Herfindahl index);
9. PFM hysteresis;
10. total strain mass.

Hysteresis is a readout only, not part of any response-form identity.

## Primary portable-transformation claim

The primary comparison is WARP_FULL_TRACE versus NONWARP_FULL_TRACE on the **late** 32-step ten-component response vector.

A portable Warp-passage transformation is supported only if:

1. paired multivariate sign-flip `p <= 0.01`;
2. at least one late component survives Holm correction at familywise 0.05;
3. the same surviving component differs in the same direction in the early window;
4. WARP_FULL_TRACE differs from WARP_TRACE_RESET on the late vector at multivariate `p <= 0.01`.

This establishes a downstream difference that survives release and requires retained passage trace.

## Passage-beyond-entry claim

WARP_FULL_TRACE is compared with ENTRY_ONLY_TRACE.

Finite passage contributes beyond the entry event only if their late response vectors differ at paired multivariate `p <= 0.01` with at least one Holm-significant component.

## PFM versus tensor carriage

- PFM carriage is supported if WARP_PFM_TRACE remains closer to WARP_FULL_TRACE than WARP_TRACE_RESET does on the late response vector, paired `p <= 0.01`.
- Tensor carriage is supported analogously for WARP_TENSOR_TRACE.

Both, one, or neither may hold.

## Topology-only passage control

TOPOLOGY_ONLY_TRACE is compared with WARP_TRACE_RESET.

If no slow-state inscription is retained, topology-only passage should not create a portable effect after common-state release. Any significant difference is treated as evidence that the release normalization failed or that an unregistered slow state survived, invalidating the portable-transformation interpretation.

## Address/reply descriptive atlas

For continuity with the main ingression programme, the post-release probe also yields a descriptive atlas of recurrent non-echo 4-gram reply motifs across lineages.

Motifs are reported with lineage IDs and step ranges but are not used to rescue a failed portable-transformation claim.

## Fixed seeds

- lineage base: `3220000`
- release-probe base: `3225000`
- paired permutation base: `3227000`
- permutation draws: 50,000

## Stopping rule

This registration is committed before runner implementation and before any registered lineage executes.

Preflight uses non-registered seeds only.

The first complete valid WARP-T2 run is the result. Passage length, release shell, downstream vector, probe length, and claim thresholds are fixed.
