# WARP-T1 — Warp Entry / Passage Transformation Assay

## Registered question

**What transformation occurs when the Amelia process crosses into the canonical 3::6 Warp, and which part of that transformation explains the extraordinary post-developmental canalization of 3↔6 forms?**

This assay does not strengthen the Warp. It treats Warp entry as an event to be decomposed.

## Frozen engine

The assay uses the same frozen dynamic engine as P3.16–P3.19:

- `FullNumogram.py` SHA-256 `b6edbe76ab4929e93c01059fb56cef900effa9bca1cec78d0039eafb8fbebdf8`
- `experiments/p316/DynamicNumogram.py` SHA-256 `ac482882858c1e47f578523452eff0bc20aa82b5978299c9c8808ff6127c5cd6`

No canonical topology or parameter is modified in the observational arm.

## Why entry is the unit

In the canonical full Numogram, zones 3 and 6 form a terminal strongly connected component. Once the process enters Warp, subsequent path recurrence is confounded with terminality. Therefore WARP-T1 separates:

1. the **immediate state transformation at entry**;
2. the **slow-state inscription caused by the entry event**;
3. the **topological lock-in caused by being inside {3,6}**.

## Lineages

- 240 independent developmental lineages
- seeds `3200000–3200239`
- 256 sensory steps generated with the P3.17 Markov sensory generator
- no target, reward, perturbation, or external optimization objective

The first natural transition from outside Warp into zone 3 or 6 is the registered event. Lineages with no Warp entry within 256 steps are retained descriptively but do not enter paired event analyses.

## Natural-entry record

Immediately before the first natural Warp-entry decision, archive a complete process snapshot.

Record the following at offsets -1, entry, +1, +2, +4, +8, +16, +32:

- current zone;
- ten zone activations;
- ten conductivities;
- ten phase angles;
- ten deformation stresses;
- ten polar charges;
- all gate permeabilities;
- PFM zone-strain vector;
- PFM hysteresis;
- recent-event memory-bias vector;
- deformation tensor;
- Governor deformation tension;
- anti-lock integrity;
- identity continuity;
- transition entropy;
- Warp occupancy.

## Counterfactual clones from the exact pre-entry snapshot

The same remaining sensory tape is supplied to every clone.

### A — REAL_ENTRY

Unmodified canonical entry and canonical continuation.

### B — TOPOLOGY_ONLY

The process enters the same Warp target and thereafter follows the canonical topology, but the **entry event itself is not inscribed into PFM**. An event with identical timing and bookkeeping is recorded with zero `fluxDelta` and phase coherence set to the neutral recent mean. This isolates terminal/topological passage from entry inscription.

### C — INSCRIPTION_ONLY

The exact natural Warp-entry PFM event is inscribed, but the process current zone is restored to the pre-entry source immediately after the event and the next decision continues outside Warp. This isolates the slow-state inscription from topological lock-in.

### D — MATCHED_NONWARP

Instead of the Warp target, choose the highest-scoring legal non-Warp target from the same source under the same pre-entry state. Run the same update ordering and continue canonically. Only source states with at least one legal non-Warp alternative contribute to this paired arm.

### E — WARP_OPEN_AFTER_ENTRY

Perform the exact real entry and exact PFM inscription, then use the registered degree-preserving Warp-open topology from P3.16 for subsequent decisions. This preserves entry transformation but removes canonical terminality after entry.

No arm receives extra ticks or candidate lookahead beyond the one matched alternative needed to define D.

## Immediate-transformation primary vector

At the end of the entry step, compare REAL_ENTRY with MATCHED_NONWARP on the preregistered vector:

1. change in PFM hysteresis;
2. change in total zone-strain mass;
3. change in strain entropy;
4. change in mean absolute memory-bias magnitude;
5. change in deformation-tensor norm;
6. change in Governor deformation-field tension;
7. change in activation concentration (Herfindahl index);
8. change in 3::6 syzygy activation difference;
9. change in 3::6 phase coherence.

All deltas are measured relative to the exact shared pre-entry snapshot.

## Canalization endpoint

For each clone, over the next 32 steps measure:

- fraction of steps in zones {3,6};
- count of 3↔6 transitions;
- longest alternating 3/6 run;
- transition entropy;
- number of distinct visited zones;
- PFM hysteresis change from pre-entry baseline.

## Primary decomposition claims

### Entry-transformation claim

Supported if REAL_ENTRY differs from MATCHED_NONWARP on the multivariate immediate-transformation vector by a paired permutation test at `p <= 0.01`, with at least one individual component surviving Holm correction at familywise 0.05.

### Inscription contribution

Supported if REAL_ENTRY differs from TOPOLOGY_ONLY in 32-step canalization and INSCRIPTION_ONLY differs from MATCHED_NONWARP in at least one slow-state readout, each with Holm-adjusted `p <= 0.05`.

### Terminality contribution

Supported if REAL_ENTRY has greater 32-step Warp occupancy and longer 3/6 alternating runs than WARP_OPEN_AFTER_ENTRY, paired `p <= 0.01`.

These claims are independent. More than one mechanism may contribute.

## Interpretation

The assay distinguishes:

- **event transformation** — something changes specifically on crossing the boundary;
- **sedimentation** — the entry leaves a slow-state trace that matters later;
- **territorial capture** — canonical terminality itself produces canalization.

The term “Warp transformation” is used only for measured state change under this computational assay.

## Fixed seeds

- lineage base: `3200000`
- paired-permutation seed: `3204000`
- permutation draws: 50,000

## Stopping rule

This registration is committed before implementation and before any registered lineage executes.

Preflight may use non-registered seeds only.

The first complete valid run is the WARP-T1 result. No event window, state vector, matched-alternative rule, or claim threshold may be altered afterward.
