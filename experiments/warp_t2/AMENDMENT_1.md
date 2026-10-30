# WARP-T2 Amendment 1 — Exact multivariate and carriage statistics

Committed before runner implementation and before any registered lineage executes.

## Multivariate response statistic

For each paired ten-component response-vector difference, compute component sample SD across eligible lineages. Components with SD <= 1e-12 contribute zero.

T = sum_j (mean(d_j) / sd(d_j))^2.

The null uses 50,000 deterministic paired sign flips, one sign per lineage applied to the entire ten-component vector.

Primary late-vector seeds:
- WARP_FULL_TRACE vs NONWARP_FULL_TRACE: 3227000
- WARP_FULL_TRACE vs WARP_TRACE_RESET: 3227001
- WARP_FULL_TRACE vs ENTRY_ONLY_TRACE: 3227002
- TOPOLOGY_ONLY_TRACE vs WARP_TRACE_RESET: 3227003

Individual components use two-sided paired sign-flip tests with seeds beginning 3227100 for each comparison and Holm correction within its ten-component family.

The “same direction in early window” criterion uses the sign of the unstandardized mean difference for the late Holm-surviving component.

## PFM/tensor carriage distance

For the late ten-component response vector, each component is scaled by the pooled sample SD of WARP_FULL_TRACE and WARP_TRACE_RESET. Components with pooled SD <= 1e-12 are omitted.

For each eligible lineage:

D_carrier = distance(carrier arm, WARP_FULL_TRACE)
D_reset = distance(WARP_TRACE_RESET, WARP_FULL_TRACE)

Test D_reset - D_carrier > 0 by one-sided paired sign flips:
- PFM carriage seed 3227200
- tensor carriage seed 3227201

Both require p <= 0.01.

## Topology-only validity check

The portable-transformation interpretation is invalidated if TOPOLOGY_ONLY_TRACE differs from WARP_TRACE_RESET on the late response by either:

- multivariate p <= 0.01, or
- any Holm-adjusted component p <= 0.05.

If invalidated, the run remains archived but no portable-trace claim is made.

## Release-probe construction

For lineage i, generate a 64-symbol Markov probe from transition-matrix seed 3225000 + i and sampling seeds incremented deterministically on rejection.

Reject a candidate if any exact 4-symbol substring of the release probe equals an exact 4-symbol substring of the five passage sensory symbols.

The first accepted probe is used for every released arm in that lineage.
