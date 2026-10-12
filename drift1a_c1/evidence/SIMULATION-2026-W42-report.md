# Amelia C1 — 2026-W42
Mode: SIMULATION. Observational and exploratory.

## Process history
Arm | Ticks | Warp | Plex | Cap | Mean completed length
---|---:|---:|---:|---:|---:
C | 10080 | 882 | 471 | 0 | 7.450
M | 10080 | 936 | 478 | 0 | 7.129
G00 | 10080 | 1551 | 1082 | 0 | 3.828
G01 | 10080 | 2491 | 1013 | 0 | 2.875
G02 | 10080 | 1952 | 1622 | 0 | 2.820
G03 | 10080 | 2134 | 1696 | 0 | 2.631
G04 | 10080 | 2978 | 1801 | 0 | 2.109
G05 | 10080 | 2584 | 2163 | 0 | 2.123
G06 | 10080 | 2630 | 2110 | 0 | 2.126
G07 | 10080 | 2452 | 1554 | 0 | 2.516
R01 | 10080 | 914 | 488 | 0 | 7.190
R02 | 10080 | 866 | 504 | 0 | 7.350
R03 | 10080 | 851 | 562 | 0 | 7.134
R04 | 10080 | 845 | 470 | 0 | 7.659
R05 | 10080 | 828 | 480 | 0 | 7.692
R06 | 10080 | 830 | 473 | 0 | 7.729
R07 | 10080 | 857 | 493 | 0 | 7.466
R08 | 10080 | 898 | 496 | 0 | 7.230

### Amelia: choices and memory
Applied entries: 1353; entries onto the boundary: 534. Distinct completed boundary routes: 601.
Unfinished episode at week end: {"length": 1, "entry": 8}. Phase counts: {"near_lock": 111, "neutral": 9873, "pre_lock": 96}.

Mechanism | C active | C probability changed | M active | M probability changed
---|---:|---:|---:|---:
commitment | 2636 | 2636 | 0 | 0
governor | 10080 | 3893 | 10080 | 0
retention | 2539 | 2531 | 0 | 0

Retention floor applied: 2531 C choices, 0 M choices.
Remembered-exit choices: 2636; selected: 1076; summed base expectation: 720.500; summed final expectation: 1056.227. These expectations describe the implemented choice bias.

Zone | C post-move visits | C self-loops | M post-move visits | M self-loops
---|---:|---:|---:|---:
0 | 60 | 37 | 62 | 38
1 | 3335 | 1290 | 2965 | 783
2 | 544 | 0 | 582 | 0
3 | 371 | 65 | 390 | 60
4 | 451 | 0 | 481 | 0
5 | 1593 | 0 | 1672 | 0
6 | 511 | 0 | 546 | 0
7 | 2079 | 0 | 2215 | 0
8 | 725 | 0 | 751 | 0
9 | 411 | 93 | 416 | 95

### Frequent Amelia routes
Counts refer to complete typed routes; each listed move includes its edge label.
- 77 occurrences, entry 0: 0→9 (Plex)
- 73 occurrences, entry 6: 6→3 (Warp)
- 65 occurrences, entry 3: 3→3 (Warp)
- 52 occurrences, entry 9: 9→9 (Plex)
- 41 occurrences, entry 9: 9→9 (Gt-45)
- 38 occurrences, entry 3: 3→6 (Gt-06)
- 37 occurrences, entry 0: 0→0 (Gt-00)
- 37 occurrences, entry 6: 6→3 (Gt-21)
- 32 occurrences, entry 3: 3→6 (syzygy)
- 32 occurrences, entry 6: 6→3 (syzygy)

### Outcome predictability at lag
Within-episode forward association; plug-in estimates have finite-sample upward bias.

Lag (moves) | C eligible episodes | C bits | M bits | Reference bits range
---|---:|---:|---:|---:
1 | 1353 | 0.9324 | 0.9229 | 0.9323–0.9696
2 | 736 | 0.8134 | 0.7949 | 0.7765–0.8642
3 | 672 | 0.1895 | 0.2192 | 0.1346–0.2001
4 | 611 | 0.0175 | 0.0132 | 0.0136–0.0395
5 | 562 | 0.0083 | 0.0091 | 0.0052–0.0326
6 | 513 | 0.0044 | 0.0068 | 0.0054–0.0179
7 | 467 | 0.0108 | 0.0094 | 0.0024–0.0151
8 | 424 | 0.0109 | 0.0071 | 0.0039–0.0158

The JSON retains detailed measurements for every arm, full route frequencies and reference ranks.

## Departures from reference
Strict outside-range flags (descriptive only):
- /self_loops/9: C=93; reference range 95–127; tied rank 1–1.
- /outcome_predictability_at_lag/2/n: C=736; reference range 691–729; tied rank 9–9.
- /outcome_predictability_at_lag/3/n: C=672; reference range 636–669; tied rank 9–9.
- /outcome_predictability_at_lag/6/bits: C=0.0044138397064594475; reference range 0.0054155646604170885–0.017935375952103583; tied rank 1–1.

## Retrospective reading
These are recorded associations, not an assertion of meaning. Operator interpretations are filed separately.
- C: 0 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.
- M: 0 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.
- G00: 1 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.
- G01: 1 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.
- G02: 0 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.
- G03: 0 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.
- G04: 0 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.
- G05: 1 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.
- G06: 1 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.
- G07: 0 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.
- R01: 1 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.
- R02: 0 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.
- R03: 0 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.
- R04: 0 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.
- R05: 1 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.
- R06: 0 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.
- R07: 0 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.
- R08: 0 distinct routes recur from earlier sealed weeks. Pairwise divergences and first-observed weeks are in JSON.

## Timing
Priority begins only at the verified seal timestamp in seal/receipt.json. No priority is claimed over inputs already available before that time.
Exploratory; no hypothesis test or calibrated anomaly claim.
References are deterministic transformations of the same inflow, not independent sources.
2/9 is conditional on exchangeability and no ties; many weekly flags are expected.
Outcome predictability is within-episode forward association, not evidence of external anticipation.
