# P3.21 Amendment 1 — Exact held-out communication statistics

Committed before runner implementation and before any registered lineage/probe executes.

## Mutual information estimator

On TEST responses, let A be the 64 equiprobable probe addresses and R the compressed reply-token alphabet selected from TRAIN.

Each address contributes the same number of TEST responses, so empirical token counts are converted to P(R|A=a) separately per address and then combined with the fixed prior P(A=a)=1/64.

The plug-in estimates are:

I(A;R) = sum_a,r P(a,r) log2[P(a,r)/(P(a)P(r))]

H(R) = -sum_r P(r) log2 P(r)

E = I/H(R), with E=0 when H(R)=0.

No finite-sample bias correction is applied.

## Decoder details

The TRAIN vocabulary contains 32 named motifs plus OTHER, V=33.

For each address, token probabilities use add-one smoothing over all 33 tokens. A held-out response with zero non-echo reply tokens is scored as zero log likelihood for every address and therefore resolves to probe 0 by the registered lowest-ID tie rule.

Correct-address margin is:
loglik(correct address) - max loglik(any incorrect address).

## Transition-entropy branching control

For each TEST response, calculate Shannon entropy over its directed response-transition occurrences. The controller's branching-freedom readout is the arithmetic mean over all 64 × 48 TEST responses.

The 8 branching-matched rewires are selected by absolute difference from CANONICAL_FULL on this mean only.

## Chance test

CANONICAL_FULL total correct TEST predictions is tested against Binomial(n=64×48, p=1/64) with the exact upper-tail probability.

## Developmental contribution test

Per-probe TEST accuracy is the fraction correct among the 48 TEST lineages for that probe.

CANONICAL_FULL minus CANONICAL_BLANK uses a two-sided paired sign-flip test of the 64 per-probe accuracy differences, 50,000 draws, seed 3237000.

For the efficiency difference, the TRAIN-selected vocabulary for each arm remains fixed. Bootstrap the 48 TEST lineage IDs with replacement, preserving all 64 responses belonging to each sampled lineage, recompute E_FULL-E_BLANK, 20,000 draws with seed 3238000. The percentile 99% interval is used.

## Atlas discriminative token

For a retained canonical motif and target probe p, use add-0.5 smoothed TEST presence odds:

odds_p = (present_p + 0.5)/(absent_p + 0.5)

odds_other = (present_other + 0.5)/(absent_other + 0.5)

log-odds = ln(odds_p/odds_other).

For each probe choose the retained motif with maximum TEST log-odds, tie-breaking by higher TEST prevalence, then lexical motif order.
