# WARP-T2 Amendment 3 — Incremental carrier isolation

Committed before any registered lineage executes.

Implementation review found two further ways in which a component arm could accidentally remove pre-existing developmental state rather than isolate the incremental Warp-passage contribution. This amendment fixes both.

## PFM and tensor carrier arms

Revise the component carriers:

### WARP_PFM_TRACE

- preserve the **post-Warp-passage PFM**;
- preserve the **pre-entry deformation tensor**.

Thus the only incremental slow-state material carried from the Warp passage is PFM.

### WARP_TENSOR_TRACE

- preserve the **pre-entry PFM**;
- preserve the **post-Warp-passage deformation tensor**.

Thus the only incremental slow-state material carried from the Warp passage is tensor deformation.

The fully blank WARP_TRACE_RESET remains descriptive only.

## Truly inscription-neutral passage steps

For ENTRY_ONLY steps 2–5 and all TOPOLOGY_ONLY_PASSAGE steps, the fast Numogram update and forced zone transition occur, but the PFM object is restored to its value immediately before that step after the transition is completed.

Therefore:

- ENTRY_ONLY retains exactly the real entry PFM inscription and no later passage PFM update;
- TOPOLOGY_ONLY retains exactly the pre-entry PFM state and receives no passage PFM update.

Tensor evolution caused by the fast dynamics is not restored; the PRE_ENTRY_BASELINE_TRACE validity comparison will reveal whether this non-PFM residue is itself portable.

This amendment makes “entry only,” “topology only,” “PFM carriage,” and “tensor carriage” genuinely incremental relative to the shared mature pre-entry state.
