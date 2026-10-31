# WARP-T4 Amendment 1 — Exact relational-profile statistics

Committed before runner implementation and before any registered lineage executes.

## Four-component paired multivariate statistic

For each eligible lineage, define the paired arm difference vector across the four family priming scores:

d_i = [L_SC, L_CS, L_SG, L_GS]_left - [L_SC, L_CS, L_SG, L_GS]_right.

For component j calculate its sample SD s_j across lineages. Components with s_j <= 1e-12 contribute zero.

Observed statistic:

T = sum_j (mean(d_j)/s_j)^2.

The null uses 50,000 deterministic paired sign flips, one sign per lineage applied to the entire four-component vector, preserving within-lineage covariance.

Seeds:
- W vs N: 3267000
- W vs E: 3267001
- T vs B: 3267002

Upper-tail empirical multivariate p is (1 + # null T >= observed T)/(1 + draws).

## Family tests

For each comparison, each family uses a two-sided paired sign-flip test on |mean difference| with 50,000 draws.

Seeds:
- W vs N components: 3267100..3267103
- W vs B components: 3267110..3267113
- W vs E components: 3267120..3267123
- T vs B components: 3267130..3267133

Holm correction is applied separately across the four families within each comparison.

The primary W-vs-N condition requires at least one family Holm p <= 0.05 and that same family must also have Holm p <= 0.05 in W-vs-B.

## PFM sufficiency

For each family separately define lineage-level difference:

D_f = L_f(P) - L_f(W).

Bootstrap eligible lineage IDs with replacement 20,000 times, preserving all four family values for a sampled lineage. Seeds 3268000..3268003.

Use the percentile 90% interval. PFM sufficiency requires every family's complete interval to lie strictly inside [-0.05,+0.05].

## Topology-only validity

The registered interpretation is invalidated if T-vs-B has multivariate p <= 0.01 or any family Holm p <= 0.05.

No secondary result rescues a failed validity control.
