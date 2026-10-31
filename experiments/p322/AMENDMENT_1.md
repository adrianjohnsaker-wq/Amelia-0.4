# P3.22 Amendment 1 — Exact inference

Committed before runner implementation and before any registered lineage/trial executes.

## Trial-level sign-flip tests

For CANONICAL_FULL, each of the 32 trials contributes:

- congruent completion fraction across 96 lineages;
- shuffled completion fraction;
- query-only completion fraction.

Define:

L_i = congruent_i - shuffled_i

Q_i = congruent_i - queryonly_i.

The primary congruent-vs-shuffled test is a one-sided paired sign-flip test of mean L > 0 with 50,000 draws, seed 3257000.

The congruent-vs-query-only test is a one-sided paired sign-flip test of mean Q > 0 with seed 3257001.

FULL-vs-BLANK developmental contribution uses per-trial lift difference L_FULL-L_BLANK and seed 3257002.

A one-sided sign-flip p is:

(1 + # null means >= observed mean)/(1 + draws).

## Relation-family direction

The four family means are arithmetic means over their eight registered trials. Condition 2 of the primary gate requires each of SC, CS, SG and GS to have mean L > 0. No family-level significance threshold is added.

## Rewire rank

Each rewire receives exactly the same 32 trials and its mean L is calculated identically.

Canonical relational-priming rank p is:

p_rank=(1 + # rewires with mean L >= canonical mean L)/25.

The primary gate requires the canonical mean L to be strictly greater than all 24 rewires; therefore p_rank=0.04.

## Structural compositionality

Each controller's structural score is mean QUERY_ONLY exact completion across the 32 trials.

Canonical structural compositionality passes only when CANONICAL_FULL is strictly above all 24 rewires, with empirical rank p=0.04.

No test involving structural score can rescue the history-sensitive relational-generalization claim.

## Ties

Exact completion is binary at lineage/trial level. No randomized tie-breaking is used anywhere in the assay.
