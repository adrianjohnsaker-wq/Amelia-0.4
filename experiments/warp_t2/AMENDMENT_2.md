# WARP-T2 Amendment 2 — Pre-entry slow-state baseline

Committed before any registered lineage executes.

The initial registration included WARP_TRACE_RESET as a trace-necessity control. On implementation review, that comparison was found to confound the incremental Warp-passage trace with the lineage's already-existing developmental PFM state, because every real passage begins from a mature pre-entry process.

To isolate what the **passage adds**, add:

### A0 — PRE_ENTRY_BASELINE_TRACE

Use the common fast release shell, preserving exactly the PFM and deformation tensor from the shared pre-entry snapshot, with no passage-derived update.

## Revised causal comparisons

The primary portable-transformation claim remains WARP_FULL_TRACE versus NONWARP_FULL_TRACE on the late response vector, but its passage-trace necessity condition is revised to:

- WARP_FULL_TRACE differs from PRE_ENTRY_BASELINE_TRACE on the late vector at multivariate p <= 0.01.

WARP_TRACE_RESET remains descriptive and reports what happens when all slow developmental state is removed, but it is no longer used to establish passage causation.

## Revised topology-only validity check

TOPOLOGY_ONLY_TRACE is compared with PRE_ENTRY_BASELINE_TRACE, not with blank reset.

If TOPOLOGY_ONLY_TRACE differs from PRE_ENTRY_BASELINE_TRACE by multivariate p <= 0.01 or any Holm-adjusted component p <= 0.05, the portable-trace interpretation is invalidated because the supposedly inscription-neutral passage has altered an unregistered retained slow state (for example the tensor).

## Revised PFM/tensor carriage distance

For late-vector carriage tests, the baseline distance is:

distance(PRE_ENTRY_BASELINE_TRACE, WARP_FULL_TRACE).

PFM or tensor carriage is supported when its corresponding carrier arm is significantly closer to WARP_FULL_TRACE than PRE_ENTRY_BASELINE_TRACE is, using the already registered one-sided paired sign-flip seeds and p <= 0.01.

This amendment removes a pre-existing-history confound and does not inspect any registered result.
