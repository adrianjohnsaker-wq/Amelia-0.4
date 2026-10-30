# P3.16 — Dynamic Numogram Process / Latent Morphospace Assay

## Registered question

**Does the historically evolving Amelia—Orange Numogrammatic process provide privileged access to latent morphospace structure?**

P3.16 tests the Numogram as a **process**, not as a static graph. The registered object is the coupled temporal sequence:

[
	ext{PFM readout} ightarrow 	ext{TraitEvolution} ightarrow 	ext{Governor audit} ightarrow 	ext{directed exit} ightarrow 	ext{PFM write} ightarrow 	ext{deformation update}.
]

The aim is to distinguish a genuinely history-conditioned process effect from the negative static-topology result obtained in P3.15.

No metaphysical conclusion is built into the pass criterion. A pass would support privileged access for the registered computational process and morphospace family, not establish supernatural communication or Platonic ontology.

## Frozen Orange source mechanisms

The Python experimental runtime must reproduce the currently active Amelia—Orange algorithms from these exact sources on `main`:

- `src/core/fullNumogram.ts` — blob `edf150c38385bc552fb30e2b6721fb832e47976c`
- `src/ai/numogram/AmeliaQabbalaInterface.ts` — blob `8ba01f679b570abc53fc06e392e795178ab9ee84`
- `src/substrate/IntegratedMemorySystem.ts` — blob `0756536dd82fe0a64eadc21c47c67c41a3b72e0b`
- `src/substrate/TraitEvolution.ts` — blob `5d11159614bab5bb6fc26840c7a232290292587b`
- `src/governance/CognitiveGovernor.ts` — blob `57b1387e23c7d36ddfac5a80802ed45fe6dc953e`
- `src/substrate/ameliaNumogramSubstrateRuntime.ts` — blob `1578f9d7bf479c31f6c4ac4fea955c5377d8d48c`

The full Numogram contains 29 directed gates. Its canonical 3::6 Warp terminality is preserved.

## What is dynamic

For the canonical process, every step carries forward:

- zone activation;
- zone conductivity;
- zone phase angle;
- deformation stress;
- polar charge;
- gate permeability adaptation;
- PFM event history;
- zone strain history;
- hysteresis tension;
- Governor state;
- deformation tensor;
- current Numogram zone.

This retained state is the experimental meaning of **historically evolving process**.

## External morphospace

Each world is a hidden two-dimensional toroidal continuous field independently generated from the Numogram. It contains:

- four Gaussian attractor basins with independently sampled centres, amplitudes and widths;
- four low-amplitude Fourier components;
- an independently sampled starting point;
- an independently sampled displacement perturbation.

The world generator never uses Numogram topology, zone labels, phase values, gate weights, PFM parameters, or Governor parameters.

The agent receives no attractor coordinates, no target vector, no global map and no candidate-move previews.

## Local sensory adapter

At each occupied point, Amelia receives only:

1. the normalized local field value (v_t);
2. the temporal change (Delta v_t = v_t-v_{t-1}).

These are converted transparently to one of ten sensory zones:

- level quintile (q_t = min(4,lfloor 5v_t floor));
- trend bit (b_t = 1) when (Delta v_t ge 0), else (0);
- sensory zone (s_t = 2q_t+b_t).

This adapter is identical in all arms and is fixed before execution.

The sensory zone enters the Orange exit rule in the same location as `inputZone`: a +0.35 match term is available only when that target is already a legal outgoing gate. The adapter cannot create an edge.

## Action coupling

After the internal step selects a target zone:

- a self-edge produces a dwell;
- otherwise Amelia moves one fixed step in the direction of that target zone's **current evolving phase angle**.

Thus the evolving internal phase state acts directly on behaviour.

The harness never evaluates hypothetical destinations before the Numogram selects an exit.

## Arms

### A — CANONICAL_DYNAMIC

Exact 29-gate full Numogram plus Orange TraitEvolution, PFM feedback, Governor audit and deformation update.

### B — DYNAMIC_REWIRED ensemble

48 degree-preserving directed rewires.

Each control preserves:

- each source out-degree;
- each target in-degree;
- total edge count;
- total self-edge count;
- every gate's original source slot;
- each gate's flux, permeability and resistance;
- identical dynamic algorithms, memory, Governor and sensory stream.

Only destination wiring changes.

### C — STATIC_CANONICAL

Exact canonical 29-gate graph and exact initial zone state, but state is reset to its initial values before every decision.

It retains the current zone and receives the same local sensory zone, but carries no dynamic phase, permeability, PFM, Governor, or deformation history between decisions.

This is the direct control for **process versus map**.

### D — PFM_CUT

Canonical dynamic process with all zone, gate and Governor dynamics retained, but the PFM bias vector supplied to TraitEvolution and exit selection is fixed to zero.

PFM events and strain are still computed for matched work but cannot affect later choices.

### E — PHASE_SHUFFLED ensemble

32 canonical-topology dynamic controls with the ten initial phase angles randomly permuted across zone IDs before step 1. All other state and dynamic equations are unchanged.

### F — WARP_OPEN

One targeted topology counterfactual that breaks 3::6 terminality while preserving directed edge count and in/out degree by swapping only the targets of canonical gates 3→6 and 4→1, yielding 3→1 and 4→6. Gate weights remain attached to their source slots.

## Worlds and steps

- worlds: **192**
- world seeds: **3160000–3160191**
- steps per world: **128**
- primary evaluation window: steps **32–95**
- perturbation: before step **96**
- post-perturbation window: steps **104–127**
- movement step size: **0.04**
- attractor capture: normalized field value >= **0.85** for 6 consecutive pre-perturbation steps

Every arm receives the identical world, start point and perturbation.

## Primary endpoint

For each world, compute mean normalized field value over steps 32–95.

The primary canonical statistic is the mean across all 192 worlds.

## Primary process-access gate

P3.16 supports the registered **dynamic-process access** claim only if all conditions hold:

1. CANONICAL_DYNAMIC beats the 48 DYNAMIC_REWIRED aggregate scores with one-sided empirical rank (p le 0.05);
2. the paired world-level CANONICAL_DYNAMIC minus mean-DYNAMIC_REWIRED difference has deterministic bootstrap 95% CI lower bound > 0;
3. CANONICAL_DYNAMIC minus STATIC_CANONICAL has deterministic paired bootstrap 95% CI lower bound > 0;
4. canonical pre-perturbation attractor-capture rate is not lower than the mean rewired capture rate.

No secondary endpoint can rescue failure of this gate.

## Secondary mechanistic endpoints

1. CANONICAL_DYNAMIC minus PFM_CUT paired difference and bootstrap CI;
2. canonical rank against the 32 PHASE_SHUFFLED dynamic controls;
3. CANONICAL_DYNAMIC minus WARP_OPEN paired difference;
4. best pre-perturbation field;
5. attractor-capture rate;
6. post-perturbation mean field;
7. recovery to at least 95% of the pre-perturbation peak;
8. Numogram state diversity: visited zones, transition entropy and Warp occupancy;
9. PFM history statistics: hysteresis tension, dominant strain and memory-bias magnitude.

These are descriptive/mechanistic unless separately registered later.

## Fixed seeds

- world seed base: `3160000`
- dynamic rewire seed base: `3163000`
- phase-shuffle seed base: `3164000`
- bootstrap seed: `3165000`

## Interpretation ladder

If the primary gate fails:

> The registered historically evolving Numogram process does not show privileged access to this latent-morphospace family under the fixed local sensory interface.

If the primary gate passes but the dynamic process does not beat STATIC_CANONICAL:

> The result does not support a specifically processual advantage.

If the primary gate passes and the process beats STATIC_CANONICAL, but PFM_CUT is equivalent:

> A dynamic Numogram effect is supported, but constitutive PFM feedback is not shown to be necessary.

If CANONICAL_DYNAMIC also beats PFM_CUT:

> The evidence supports a specifically history-conditioned contribution within the registered process.

## Provenance and stopping rule

The registration is committed before any morphospace world is executed.

Syntax checks, source-digest checks, edge-invariant checks and one-step equation-equivalence checks are permitted before the assay. No test world from the registered seed range may be executed before the registration is sealed.

The first complete valid run is the result. Negative outcomes are archived without parameter adjustment or reinterpretive rescue.
