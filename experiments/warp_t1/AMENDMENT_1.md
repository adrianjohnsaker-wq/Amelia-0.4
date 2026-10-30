# WARP-T1 Amendment 1 — Exact paired statistics

Committed before any registered lineage is executed.

The registration fixed the state vector and claim thresholds but did not specify the scalar multivariate statistic or exact continuous paired tests. This amendment fixes them before execution.

## Immediate multivariate entry statistic

For each eligible lineage, let d_i be the nine-component vector REAL_ENTRY minus MATCHED_NONWARP at the end of the entry step, each component measured as change from the exact shared pre-entry snapshot.

For component j:

- compute sample standard deviation s_j across lineage-level differences;
- if s_j = 0, set its contribution to zero;
- z_j = mean(d_j) / s_j.

Observed multivariate statistic:

T = sum_j z_j^2.

Null distribution: 50,000 deterministic paired sign-flip draws using seed 3204000. On each draw one ±1 sign is sampled per lineage and applied to the **entire nine-component vector**, preserving within-lineage covariance. Recompute T. Upper-tail empirical p uses (1 + null >= observed)/(1 + draws).

Individual immediate components use two-sided paired sign-flip p values based on |mean difference|, using deterministic seeds 3204100 + component index, 50,000 draws each. Holm correction is applied across the nine components.

## Continuous paired tests

Unless otherwise stated, a directional continuous paired claim uses a one-sided paired sign-flip test of mean difference with 50,000 draws and deterministic seeds beginning 3205000.

## Inscription contribution

The registered phrase “32-step canalization” is operationalized as next-32-step Warp occupancy.

Inscription contribution requires BOTH:

1. REAL_ENTRY > TOPOLOGY_ONLY in next-32-step Warp occupancy, one-sided paired sign-flip Holm-adjusted p <= 0.05 within the two inscription tests;
2. INSCRIPTION_ONLY > MATCHED_NONWARP on at least one of:
   - PFM hysteresis change from pre-entry baseline at +32,
   - total strain-mass change from pre-entry baseline at +32,
   using one-sided paired sign-flip tests and Holm correction across these two slow-state readouts.

## Terminality contribution

Terminality contribution requires BOTH:

1. REAL_ENTRY > WARP_OPEN_AFTER_ENTRY in next-32-step Warp occupancy, one-sided paired sign-flip p <= 0.01;
2. REAL_ENTRY > WARP_OPEN_AFTER_ENTRY in longest alternating 3/6 run, one-sided paired sign-flip p <= 0.01.

No other metric can rescue a failed registered mechanism claim.
