# WARP-T3 Amendment 1 — Balanced per-probe information and equivalence

Committed before runner implementation and before any registered lineage executes.

## Balanced one-vs-rest efficiency contribution

For a target probe p, define binary Y with equal prior:

P(Y=1)=P(Y=0)=0.5.

P(R|Y=1) is the empirical compressed-token distribution over TEST responses to probe p.

P(R|Y=0) is the arithmetic mean of the 31 empirical token distributions from the other probes, giving every other address equal weight regardless of token count.

From this balanced mixture compute I(Y;R) and H(R), then:

e_p = I(Y;R)/H(R),

with e_p=0 if H(R)=0.

Thus each of the 32 probes contributes one comparable efficiency value.

## Paired communication tests

Two-sided paired sign-flip tests use 50,000 draws.

Seeds:
- W vs N accuracy: 3247000
- W vs N efficiency contribution: 3247001
- W vs B accuracy: 3247002
- W vs E accuracy: 3247003
- W vs E efficiency contribution: 3247004
- T vs B accuracy: 3247005
- T vs B efficiency contribution: 3247006

A two-sided test compares |mean paired difference| with the paired sign-flip null.

## PFM equivalence test

The registered ±0.02 equivalence margin applies separately to the 32 paired per-probe differences:

d_p = metric_WARP_PFM_TRACE(p) - metric_W(p).

For each metric, form a deterministic 90% percentile bootstrap interval of the mean paired difference by resampling the 32 probe IDs with replacement, 20,000 draws.

Seeds:
- accuracy equivalence: 3247100
- efficiency equivalence: 3247101

That metric is equivalent when the complete 90% interval lies strictly inside [-0.02,+0.02]. PFM sufficiency requires equivalence for both accuracy and efficiency contribution.

This bootstrap operationalizes the registered TOST equivalence criterion without requiring a parametric normality assumption.

## Direction

For the primary W−N effect, enhancement requires both mean paired differences >0; suppression requires both <0. Opposite signs fail the registered direction-consistency gate even if both p-values are significant.
