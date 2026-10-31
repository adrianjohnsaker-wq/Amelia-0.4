# P3.23 Amendment 1 — Exact inference

Committed before the prospectively selected beacon rounds exist and before any beacon endpoint is queried.

## Primary decoder tests

For CANONICAL_FULL, REAL→REAL uses the 16 per-window TEST accuracies (48 TEST lineages per window).

The temporal-order condition compares, window by window:

d_w = accuracy_REAL→REAL(w) - accuracy_REAL→SHUFFLED(w).

Use a one-sided paired sign-flip test of mean d > 0 with 50,000 draws and seed 3277000.

One-sided empirical p:

(1 + # null means >= observed mean)/(1 + draws).

The overall REAL→REAL correct count is tested against Binomial(n=16×48, p=1/16) using the exact upper tail.

## Rewire rank

Each of the 24 degree-preserving rewires receives the identical 16 REAL beacon windows and identical TRAIN/TEST lineage split.

Canonical rewire-rank p:

p_rank = (1 + # rewires with REAL→REAL accuracy >= canonical accuracy)/25.

The primary gate requires the canonical accuracy to be strictly greater than every rewire, giving p_rank=0.04.

## Paired multivariate REAL-vs-SHUFFLED relation-profile test

For each signal window w, calculate the TEST-lineage mean 12-dimensional relational profile separately for REAL and SHUFFLED.

Define:

d_w = profile_REAL(w) - profile_SHUFFLED(w).

For component j calculate sample SD s_j across the 16 window differences. Components with s_j <= 1e-12 contribute zero.

Observed statistic:

T = sum_j (mean_w(d_wj)/s_j)^2.

The null uses 50,000 paired sign flips with seed 3277001. One sign is sampled per signal window and applied to that window's complete 12-dimensional vector, preserving component covariance.

Upper-tail empirical p:

(1 + # null T >= observed T)/(1 + draws).

Primary condition 5 requires p <= 0.01. Direction is reported component-by-component; no global positive direction is required.

## Developmental contribution

For each of the 16 windows define:

d_w = FULL_REAL→REAL_accuracy(w) - BLANK_REAL→REAL_accuracy(w).

Use a one-sided paired sign-flip test of mean d > 0 with 50,000 draws and seed 3277002.

Developmental contribution requires p <= 0.01 and FULL overall accuracy > BLANK overall accuracy.

## Distance margin

For a TEST profile x with correct window c:

margin = min_{k != c} ||x-centroid_k||^2 - ||x-centroid_c||^2.

Positive values favor the correct signal identity.

## Ties

Nearest-centroid exact distance ties resolve to the lowest window ID. No randomized tie-breaking is used.
