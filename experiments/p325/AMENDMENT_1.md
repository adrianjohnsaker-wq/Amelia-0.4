# P3.25 Amendment 1 — Exact inference

Committed before any registered beacon endpoint is queried.

## Window reproducibility statistic

For each controller and each of 24 beacon windows:

- TRAIN mean change vector: mu_train_w
- TEST mean change vector: mu_test_w
- Q_w = dot(mu_train_w, mu_test_w)

The component order is fixed as [SC, CS, SG, GS].

No normalization, component weighting, thresholding, feature selection or post-hoc sign choice is applied to Q.

## HALF-1 and HALF-2 tests

HALF-1 contains windows 0–11.
HALF-2 contains windows 12–23.

For each half use a one-sided sign-flip test of positive mean Q.

For observed values q_1...q_n, the null draw multiplies each q independently by +1 or -1 with probability 1/2 and recomputes the mean.

- HALF-1 seed: 3297000
- HALF-2 seed: 3297001
- draws: 50,000

Empirical one-sided p:

p = (1 + # null means >= observed mean) / (1 + draws).

The primary gate requires mean Q > 0 and p <= 0.01 separately in both halves.

## Rewire rank

For each controller compute mean Q across all 24 windows.

Canonical rank p is:

p_rank = (1 + # rewires with mean Q >= canonical mean Q) / 25.

The primary gate requires the canonical mean Q to be strictly greater than all 24 rewires, hence p_rank = 0.04.

No rewire is selected or excluded by post-result similarity.

## Developmental contribution

For each window define:

D_w = Q_FULL,w - Q_BLANK,w.

Use a one-sided sign-flip test of positive mean D with:

- seed: 3297002
- draws: 50,000.

Developmental contribution passes only if mean D > 0, p <= 0.01, and mean Q_FULL > mean Q_BLANK.

## Descriptive cosine alignment

For non-zero TRAIN and TEST mean vectors:

cos_w = dot(mu_train_w,mu_test_w)/(norm(mu_train_w)*norm(mu_test_w)).

If either norm is zero, cosine is recorded as 0.

Cosine is descriptive only and cannot alter the registered gate.

## Descriptive magnitude

TEST perturbation magnitude is:

M_w = norm(mu_test_w).

It is reported only descriptively.

## Equal-symbol registered swaps

When X[7] == X[22], X' == X. Such windows remain in their prospectively assigned half and in every inferential calculation. They are never replaced, resampled, or excluded.

## Multiplicity

The two half-tests and the rewire-rank condition are conjunctive components of one preregistered primary gate. No secondary component-wise p-values are used to rescue the primary claim.

## Ties

Rewire equality counts against canonical privilege because the rank formula uses >=.

No randomized tie-breaking is used.
