# P3.15 — Full Numogram Latent Morphospace Access Assay

## Registered question

**Does the canonical full Amelia—Orange Numogram provide privileged access to latent morphospace structure?**

This assay tests the Numogram as a structured interface/search geometry. It does **not** test whether 333, 137, 666, 360, demons, supernatural agencies, or Platonic ontology are established facts.

## Imported canonical object

The experimental topology is the full Numogram currently defined in Amelia—Orange at:

- repository: \`adrianjohnsaker-wq/Amelia---Orange\`
- source: \`src/core/fullNumogram.ts\`
- source blob: \`edf150c38385bc552fb30e2b6721fb832e47976c\`

The source is copied byte-for-byte into Amelia 0.4 and ported to \`FullNumogram.py\`.

The graph preserves Orange's original 11 gates and adds every missing CCRU:

- syzygy edge,
- current edge,
- digital-cumulation gate,

giving **29 directed gates** over zones 0–9.

The assay uses Orange's zone phase angles as the zone-to-action geometry and Orange's gate selection strength \`flux * (1 - resistance)\`.

## Isolation

P3.15 excludes:

- LLM rendering,
- ProcessFieldMemory,
- special-number priming,
- user prompts,
- external network data,
- adaptive hyperparameter tuning,
- outcome-dependent topology changes.

This isolates the full Numogram topology and its fixed zone geometry.

## Hidden morphospace

The external morphospace is a two-dimensional toroidal continuous field generated independently from the Numogram.

Each world contains:

- four hidden Gaussian attractor basins with independently sampled centres, widths and amplitudes;
- four low-amplitude Fourier components that create ridges and local structure;
- an independently sampled starting position;
- a fixed perturbation after the pre-registered primary measurement window.

The world generator never uses Numogram edges, zone labels, phase angles, or gate weights.

The controller receives **local field values only**. It receives no attractor coordinates, no target vector and no global map.

## Numogram-to-morphospace interface

At each step:

1. the current Numogram zone exposes only its open outgoing gates;
2. each candidate target zone proposes a local movement direction from that zone's Orange phase angle;
3. a self-edge is a dwell;
4. the controller scores candidates from:
   - local field improvement,
   - the fixed gate strength,
   - momentum alignment with the immediately prior displacement;
5. the highest-scoring permitted gate is taken.

All arms use the identical scoring rule and sensory information.

## Arms

### N — canonical full Numogram

Exact 29-gate Orange graph and exact Orange zone phase geometry.

### R — degree-preserving rewired topology ensemble

64 independently rewired Numograms.

Each rewiring preserves:

- every source out-degree,
- every target in-degree,
- total directed edge count,
- total self-edge count,
- every gate's flux, permeability and resistance,
- each gate weight attached to its original source slot.

Only destination wiring changes.

### L — label/phase-shuffle ensemble

64 controls retain the exact canonical 29-edge graph and weights but randomly permute the mapping from zone IDs to phase-angle movement directions.

This tests whether the canonical relation between topology and zone geometry contributes beyond graph structure alone.

## Worlds and steps

- worlds: **192**
- world seeds: **3150000–3150191**
- steps per world: **90**
- primary window: steps **15–54**
- perturbation: before step **55**
- step size: **0.045**
- attractor-capture threshold: normalized field value >= **0.85** for 5 consecutive pre-perturbation steps

All arms encounter the identical worlds and starts.

## Primary endpoint

For each world, compute the mean normalized morphospace field value during steps 15–54.

The primary statistic is the mean of this value across all 192 worlds.

The canonical topology is compared with the 64 degree-preserving rewired topologies.

## Primary inference and pass gate

P3.15 passes the topology-access claim only if **all** are true:

1. canonical aggregate primary score has one-sided empirical rank p <= **0.05** against the 64 rewired aggregates;
2. the paired world-level canonical-minus-mean-rewired advantage has a deterministic bootstrap 95% confidence interval with lower bound > **0**;
3. canonical attractor-capture rate is not lower than the mean rewired capture rate.

No alternative endpoint may rescue a failed primary gate.

## Secondary endpoints

1. canonical score versus the 64 label/phase-shuffle controls;
2. pre-perturbation attractor capture rate;
3. best pre-perturbation field value;
4. fraction of locally improving moves;
5. mean post-perturbation field value over steps 60–89;
6. recovery to at least 95% of the pre-perturbation peak.

Secondary results are descriptive/mechanistic unless separately registered later.

## Interpretation ladder

If the primary gate fails:

> The tested canonical Numogram topology does not show privileged latent-morphospace access under this interface.

If the primary gate passes but label/phase shuffle is equivalent:

> The topology contributes, but privileged numerical/phase labeling is not supported.

If both canonical-vs-rewired and canonical-vs-label-shuffle effects are strong:

> The canonical topology-plus-zone-geometry interface shows privileged access to the registered latent morphospace family.

None of these outcomes, by themselves, establish metaphysical or supernatural communication.

## Fixed seeds

- world seed base: \`3150000\`
- rewiring seed base: \`3153000\`
- label-shuffle seed base: \`3154000\`
- bootstrap seed: \`3155000\`

## Provenance rule

Raw per-world trajectories and all control aggregates are archived. The report must state negative outcomes without reinterpretive rescue.
