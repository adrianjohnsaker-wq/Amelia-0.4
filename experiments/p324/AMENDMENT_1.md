# P3.24 Amendment 1 — Exact inference

Committed before any registered beacon endpoint is queried.

## A and B chance tests

For each encoding separately, CANONICAL_FULL within-encoding classification has:

- n = 24 windows × 48 TEST lineages = 1152;
- chance probability = 1/24.

Use the exact Binomial upper-tail probability for A→A and B→B correct counts.

Primary conditions 1 and 2 require p <= 0.01 independently.

## Rewire ranks

For each encoding separately:

[
p_{rank}=(1+#{rewire accuracy ge canonical accuracy})/25.
]

Primary conditions 3–5 require canonical accuracy to be strictly greater than all 24 rewires for both A→A and B→B, so each rank p must equal 0.04.

## Order-specific cross-encoding tests

For each of the 24 beacon windows define:

[
d^A_w=accuracy_{A	o A}(w)-accuracy_{A	o B}(w)
]

and

[
d^B_w=accuracy_{B	o B}(w)-accuracy_{B	o A}(w).
]

Use one-sided paired sign-flip tests of positive mean difference with 50,000 draws.

- A self > A→B seed: 3287000
- B self > B→A seed: 3287001

Empirical one-sided p:

[
(1+#{null mean ge observed mean})/(1+draws).
]

Primary conditions 6 and 7 each require positive mean and p <= 0.01.

## Developmental contribution

For every encoding-window pair create one paired accuracy difference:

[
d_{e,w}=accuracy_{FULL,e	o e}(w)-accuracy_{BLANK,e	o e}(w),
]

giving 48 paired values.

Use a one-sided paired sign-flip test with seed 3287002 and 50,000 draws.

Developmental contribution requires positive mean, p <= 0.01, and higher pooled FULL within-encoding accuracy.

## Marginal-balance invariant

Before scoring, the runner must assert for every A and B signal:

- length 30;
- exactly three occurrences of each zone 0–9;
- identical sorted sequence across all 48 encoded windows.

Failure invalidates the run before any result is calculated.

## Cross-encoding self symmetry

Report B→B minus A→A accuracy descriptively. No equality or superiority threshold is imposed because the two registered encodings are independent deterministic permutations.

## Ties

Nearest-centroid exact squared-distance ties resolve to the lowest beacon-window ID.

No randomized tie-breaking is used.
