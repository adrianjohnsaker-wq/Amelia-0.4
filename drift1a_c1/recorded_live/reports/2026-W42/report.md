# Amelia C1 — 2026-W42 — amendments 7–12 (report layout)
Mode: LIVE. Observational and exploratory. Traversal episodes are the primary interpretation class.
Renderer SHA-256 (reports.py): `39541a18374dc8823c967400bb84f3df98512922b1b6a2c2befa1d622e4daa1f`.

C against M isolates the effect of carried memory under the same inflow. C against R01–R08 isolates what this particular inflow does that other inflows of the same kind, passed through the same instrument with carried memory, do not.

Because the reference tapes are keyed hashes of the same rounds, standard cryptographic assumptions predict no systematic departure of C from the references; that is the null against which any persistent departure is read.

## A. Form — canonical graph versus rewired controls (channel A only)
Form is shared by every arm on the canonical graph, whatever its inflow. It bears on the Numogram's structure, not on any inflow.
This section describes determinacy horizon, zone-1 dwell, Warp/Plex outcomes and route lengths. G controls belong only to channel A.

### Process history
Completed episodes are assigned to their ending week, including full lengths of cross-week episodes. Tick statistics use the class of the episode active on that tick. Occupancy divides by that class’s weekly ticks. Routes include cap endings.

### all

Arm | Completed | Warp | Plex | Cap | Warp fraction | Boundary endings / class tick | Mean length | Distinct routes
---|---:|---:|---:|---:|---:|---:|---:|---:
C | 175 | 120 | 55 | 0 | 0.68571 | 0.11792 | 8.4686 | 110
M | 175 | 118 | 57 | 0 | 0.67429 | 0.11792 | 8.4686 | 113
G00 | 418 | 237 | 181 | 0 | 0.56699 | 0.28167 | 3.5478 | 160
G01 | 521 | 371 | 150 | 0 | 0.71209 | 0.35108 | 2.8426 | 173
G02 | 488 | 250 | 238 | 0 | 0.5123 | 0.32884 | 3.041 | 182
G03 | 536 | 308 | 228 | 0 | 0.57463 | 0.36119 | 2.7631 | 178
G04 | 667 | 418 | 249 | 0 | 0.62669 | 0.44946 | 2.2249 | 150
G05 | 682 | 385 | 297 | 0 | 0.56452 | 0.45957 | 2.176 | 141
G06 | 660 | 377 | 283 | 0 | 0.57121 | 0.44474 | 2.2439 | 150
G07 | 593 | 378 | 215 | 0 | 0.63744 | 0.3996 | 2.4992 | 163
R01 | 186 | 129 | 57 | 0 | 0.69355 | 0.12534 | 7.9785 | 106
R02 | 208 | 140 | 68 | 0 | 0.67308 | 0.14016 | 7.125 | 117
R03 | 200 | 140 | 60 | 0 | 0.7 | 0.13477 | 7.335 | 120
R04 | 188 | 129 | 59 | 0 | 0.68617 | 0.12668 | 7.867 | 112
R05 | 223 | 124 | 99 | 0 | 0.55605 | 0.15027 | 6.6502 | 113
R06 | 184 | 112 | 72 | 0 | 0.6087 | 0.12399 | 8.0489 | 102
R07 | 188 | 134 | 54 | 0 | 0.71277 | 0.12668 | 7.8245 | 115
R08 | 169 | 100 | 69 | 0 | 0.59172 | 0.11388 | 8.7456 | 98

C length distribution (moves: episodes): 1: 75, 2: 5, 3: 6, 4: 5, 5: 9, 6: 6, 7: 6, 8: 5, 9: 5, 10: 4, 11: 6, 12: 1, 13: 1, 14: 1, 15: 2, 16: 3, 17: 5, 18: 1, 19: 2, 20: 3, 21: 2, 22: 1, 23: 2, 25: 1, 26: 2, 27: 2, 28: 1, 29: 1, 30: 2, 31: 2, 32: 4, 33: 1, 36: 1, 38: 1, 72: 1.
C unfinished episode at week end: {"length": 2, "entry": 1, "episode_class": "traversal"}.

C frequent typed routes:
- 18 occurrences, entry 3: 3→3 (Warp)
- 10 occurrences, entry 0: 0→9 (Plex)
- 8 occurrences, entry 6: 6→3 (Warp)
- 7 occurrences, entry 9: 9→9 (Plex)
- 6 occurrences, entry 6: 6→3 (syzygy)
- 5 occurrences, entry 2: 2→3 (Gt-03)
- 4 occurrences, entry 8: 8→9 (Gt-36)
- 4 occurrences, entry 9: 9→0 (syzygy)
- 3 occurrences, entry 0: 0→9 (syzygy)
- 3 occurrences, entry 3: 3→6 (syzygy)

### traversal

Arm | Completed | Warp | Plex | Cap | Warp fraction | Boundary endings / class tick | Mean length | Distinct routes
---|---:|---:|---:|---:|---:|---:|---:|---:
C | 111 | 83 | 28 | 0 | 0.74775 | 0.078169 | 12.775 | 99
M | 110 | 81 | 29 | 0 | 0.73636 | 0.077519 | 12.882 | 101
G00 | 258 | 172 | 86 | 0 | 0.66667 | 0.24067 | 4.1512 | 116
G01 | 311 | 271 | 40 | 0 | 0.87138 | 0.31131 | 3.2122 | 117
G02 | 301 | 153 | 148 | 0 | 0.50831 | 0.30373 | 3.2924 | 119
G03 | 323 | 206 | 117 | 0 | 0.63777 | 0.31543 | 3.1703 | 128
G04 | 400 | 287 | 113 | 0 | 0.7175 | 0.42194 | 2.37 | 95
G05 | 410 | 232 | 178 | 0 | 0.56585 | 0.43803 | 2.2829 | 83
G06 | 413 | 277 | 136 | 0 | 0.6707 | 0.41972 | 2.3826 | 102
G07 | 361 | 253 | 108 | 0 | 0.70083 | 0.3861 | 2.5845 | 103
R01 | 115 | 90 | 25 | 0 | 0.78261 | 0.081387 | 12.287 | 94
R02 | 120 | 97 | 23 | 0 | 0.80833 | 0.08596 | 11.617 | 105
R03 | 123 | 97 | 26 | 0 | 0.78862 | 0.08742 | 11.301 | 108
R04 | 117 | 90 | 27 | 0 | 0.76923 | 0.082803 | 12.034 | 100
R05 | 122 | 75 | 47 | 0 | 0.61475 | 0.088214 | 11.328 | 101
R06 | 108 | 81 | 27 | 0 | 0.75 | 0.076705 | 13.009 | 90
R07 | 121 | 98 | 23 | 0 | 0.80992 | 0.085392 | 11.603 | 103
R08 | 105 | 69 | 36 | 0 | 0.65714 | 0.073944 | 13.467 | 86

C length distribution (moves: episodes): 1: 11, 2: 5, 3: 6, 4: 5, 5: 9, 6: 6, 7: 6, 8: 5, 9: 5, 10: 4, 11: 6, 12: 1, 13: 1, 14: 1, 15: 2, 16: 3, 17: 5, 18: 1, 19: 2, 20: 3, 21: 2, 22: 1, 23: 2, 25: 1, 26: 2, 27: 2, 28: 1, 29: 1, 30: 2, 31: 2, 32: 4, 33: 1, 36: 1, 38: 1, 72: 1.
C unfinished episode at week end: {"length": 2, "entry": 1, "episode_class": "traversal"}.

C frequent typed routes:
- 5 occurrences, entry 2: 2→3 (Gt-03)
- 4 occurrences, entry 8: 8→9 (Gt-36)
- 2 occurrences, entry 4: 4→1 (Sink); 1→1 (Gt-01); 1→7 (Surge); 7→5 (Hold); 5→6 (Gt-15)
- 2 occurrences, entry 5: 5→6 (Gt-15)
- 2 occurrences, entry 7: 7→5 (Hold); 5→1 (Sink); 1→7 (Surge); 7→5 (Hold); 5→6 (Gt-15)
- 2 occurrences, entry 7: 7→5 (Hold); 5→6 (Gt-15)
- 2 occurrences, entry 8: 8→7 (Surge); 7→5 (Hold); 5→6 (Gt-15)
- 1 occurrences, entry 1: 1→1 (Gt-01); 1→1 (Gt-01); 1→1 (Gt-01); 1→7 (Surge); 7→2 (syzygy); 2→5 (Hold); 5→1 (Sink); 1→1 (Gt-01); 1→1 (Gt-01); 1→1 (Gt-01); 1→1 (Gt-01); 1→7 (Surge); 7→5 (Hold); 5→1 (Sink); 1→7 (Surge); 7→1 (Gt-28); 1→1 (Gt-01); 1→7 (Surge); 7→5 (Hold); 5→1 (Sink); 1→8 (syzygy); 8→7 (Surge); 7→5 (Hold); 5→1 (Sink); 1→7 (Surge); 7→5 (Hold); 5→4 (syzygy); 4→1 (Sink); 1→1 (Gt-01); 1→8 (syzygy); 8→7 (Surge); 7→5 (Hold); 5→1 (Sink); 1→7 (Surge); 7→2 (syzygy); 2→3 (Gt-03)
- 1 occurrences, entry 1: 1→1 (Gt-01); 1→1 (Gt-01); 1→1 (Gt-01); 1→8 (syzygy); 8→1 (syzygy); 1→1 (Gt-01); 1→1 (Gt-01); 1→1 (Gt-01); 1→7 (Surge); 7→1 (Gt-28); 1→8 (syzygy); 8→7 (Surge); 7→2 (syzygy); 2→5 (Hold); 5→1 (Sink); 1→7 (Surge); 7→2 (syzygy); 2→5 (Hold); 5→4 (syzygy); 4→1 (Sink); 1→1 (Gt-01); 1→8 (syzygy); 8→7 (Surge); 7→2 (syzygy); 2→5 (Hold); 5→1 (Sink); 1→7 (Surge); 7→5 (Hold); 5→1 (Sink); 1→7 (Surge); 7→5 (Hold); 5→6 (Gt-15)
- 1 occurrences, entry 1: 1→1 (Gt-01); 1→1 (Gt-01); 1→7 (Surge); 7→2 (syzygy); 2→3 (Gt-03)

### boundary entry

Arm | Completed | Warp | Plex | Cap | Warp fraction | Boundary endings / class tick | Mean length | Distinct routes
---|---:|---:|---:|---:|---:|---:|---:|---:
C | 64 | 37 | 27 | 0 | 0.57812 | 1 | 1 | 11
M | 65 | 37 | 28 | 0 | 0.56923 | 1 | 1 | 12
G00 | 160 | 65 | 95 | 0 | 0.40625 | 0.38835 | 2.575 | 44
G01 | 210 | 100 | 110 | 0 | 0.47619 | 0.43299 | 2.2952 | 56
G02 | 187 | 97 | 90 | 0 | 0.51872 | 0.37931 | 2.6364 | 63
G03 | 213 | 102 | 111 | 0 | 0.47887 | 0.46304 | 2.1455 | 50
G04 | 267 | 131 | 136 | 0 | 0.49064 | 0.49813 | 2.0075 | 55
G05 | 272 | 153 | 119 | 0 | 0.5625 | 0.49635 | 2.0147 | 58
G06 | 247 | 100 | 147 | 0 | 0.40486 | 0.494 | 2.0121 | 48
G07 | 232 | 125 | 107 | 0 | 0.53879 | 0.42259 | 2.3664 | 60
R01 | 71 | 39 | 32 | 0 | 0.5493 | 1 | 1 | 12
R02 | 88 | 43 | 45 | 0 | 0.48864 | 1 | 1 | 12
R03 | 77 | 43 | 34 | 0 | 0.55844 | 1 | 1 | 12
R04 | 71 | 39 | 32 | 0 | 0.5493 | 1 | 1 | 12
R05 | 101 | 49 | 52 | 0 | 0.48515 | 1 | 1 | 12
R06 | 76 | 31 | 45 | 0 | 0.40789 | 1 | 1 | 12
R07 | 67 | 36 | 31 | 0 | 0.53731 | 1 | 1 | 12
R08 | 64 | 31 | 33 | 0 | 0.48438 | 1 | 1 | 12

C length distribution (moves: episodes): 1: 64.
C unfinished episode at week end: null.

C frequent typed routes:
- 18 occurrences, entry 3: 3→3 (Warp)
- 10 occurrences, entry 0: 0→9 (Plex)
- 8 occurrences, entry 6: 6→3 (Warp)
- 7 occurrences, entry 9: 9→9 (Plex)
- 6 occurrences, entry 6: 6→3 (syzygy)
- 4 occurrences, entry 9: 9→0 (syzygy)
- 3 occurrences, entry 0: 0→9 (syzygy)
- 3 occurrences, entry 3: 3→6 (syzygy)
- 3 occurrences, entry 9: 9→9 (Gt-45)
- 1 occurrences, entry 3: 3→6 (Gt-06)

### Canonical boundary-entry diagnostic
Every completed canonical boundary-entry episode must have length 1 and the outcome fixed by entry: 0/9 → Plex; 3/6 → Warp. G arms are not subject to this diagnostic.
- C: PASS; checked 64; failures 0. Unfinished: {"length": 2, "entry": 1, "episode_class": "traversal"}.
- M: PASS; checked 65; failures 0. Unfinished: {"length": 2, "entry": 1, "episode_class": "traversal"}.
- G00: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 1, "entry": 4, "episode_class": "traversal"}.
- G01: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 3, "entry": 6, "episode_class": "boundary_entry"}.
- G02: NOT_APPLICABLE; checked 0; failures 0. Unfinished: null.
- G03: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 3, "entry": 6, "episode_class": "boundary_entry"}.
- G04: NOT_APPLICABLE; checked 0; failures 0. Unfinished: null.
- G05: NOT_APPLICABLE; checked 0; failures 0. Unfinished: null.
- G06: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 3, "entry": 6, "episode_class": "boundary_entry"}.
- G07: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 2, "entry": 1, "episode_class": "traversal"}.
- R01: PASS; checked 71; failures 0. Unfinished: null.
- R02: PASS; checked 88; failures 0. Unfinished: {"length": 2, "entry": 1, "episode_class": "traversal"}.
- R03: PASS; checked 77; failures 0. Unfinished: {"length": 17, "entry": 4, "episode_class": "traversal"}.
- R04: PASS; checked 71; failures 0. Unfinished: {"length": 5, "entry": 1, "episode_class": "traversal"}.
- R05: PASS; checked 101; failures 0. Unfinished: {"length": 1, "entry": 7, "episode_class": "traversal"}.
- R06: PASS; checked 76; failures 0. Unfinished: {"length": 3, "entry": 7, "episode_class": "traversal"}.
- R07: PASS; checked 67; failures 0. Unfinished: {"length": 13, "entry": 1, "episode_class": "traversal"}.
- R08: PASS; checked 64; failures 0. Unfinished: {"length": 6, "entry": 1, "episode_class": "traversal"}.

### Outcome predictability
This quantity is within-episode forward association, not evidence of external anticipation. Traversal boundary endings are primary; all boundary endings are secondary. Miller–Madow estimates are signed and are not clipped to zero. A lag with n < 50 is insufficient. Values within the permutation null are reported as indistinguishable from zero.
B = 200; null 95th percentile uses nearest rank; ≥ proportion is the number of permuted plug-in values at least as large as observed divided by 200. The JSON contains every arm’s values and exact seed.

### traversal series: C and M

Arm | Lag | n | Plug-in bits | MM bits | Null 95% bits | ≥ proportion | Interpretation
---|---:|---:|---:|---:|---:|---:|---
C | 1 | 111 | 0.81483 | 0.82133 | 0.051761 | 0 | above permutation 95th percentile (exploratory)
C | 2 | 100 | 0.79504 | 0.80225 | 0.070325 | 0 | above permutation 95th percentile (exploratory)
C | 3 | 95 | 0.094532 | 0.071752 | 0.091912 | 0.045 | above permutation 95th percentile (exploratory)
C | 4 | 89 | 0.084842 | 0.052422 | 0.086376 | 0.07 | indistinguishable from zero
C | 5 | 84 | 0.040367 | 0.0060168 | 0.10279 | 0.615 | indistinguishable from zero
C | 6 | 75 | 0.063749 | 0.034895 | 0.10626 | 0.33 | indistinguishable from zero
C | 7 | 69 | 0.027526 | -0.014291 | 0.12434 | 0.84 | indistinguishable from zero
C | 8 | 63 | 0.10512 | 0.059321 | 0.15394 | 0.17 | indistinguishable from zero
M | 1 | 110 | 0.83218 | 0.83874 | 0.038312 | 0 | above permutation 95th percentile (exploratory)
M | 2 | 102 | 0.78713 | 0.7942 | 0.053209 | 0 | above permutation 95th percentile (exploratory)
M | 3 | 98 | 0.18994 | 0.16786 | 0.078875 | 0 | above permutation 95th percentile (exploratory)
M | 4 | 87 | 0.034668 | 0.0015024 | 0.10421 | 0.6 | indistinguishable from zero
M | 5 | 80 | 0.027565 | -0.0085023 | 0.10988 | 0.825 | indistinguishable from zero
M | 6 | 72 | 0.05195 | 0.011875 | 0.11606 | 0.525 | indistinguishable from zero
M | 7 | 68 | 0.056401 | 0.013969 | 0.13776 | 0.53 | indistinguishable from zero
M | 8 | 67 | 0.07481 | 0.031744 | 0.10787 | 0.26 | indistinguishable from zero

### all series: C and M

Arm | Lag | n | Plug-in bits | MM bits | Null 95% bits | ≥ proportion | Interpretation
---|---:|---:|---:|---:|---:|---:|---
C | 1 | 175 | 0.89806 | 0.90218 | 0.053522 | 0 | above permutation 95th percentile (exploratory)
C | 2 | 100 | 0.79504 | 0.80225 | 0.070325 | 0 | above permutation 95th percentile (exploratory)
C | 3 | 95 | 0.094532 | 0.071752 | 0.091912 | 0.045 | above permutation 95th percentile (exploratory)
C | 4 | 89 | 0.084842 | 0.052422 | 0.086376 | 0.07 | indistinguishable from zero
C | 5 | 84 | 0.040367 | 0.0060168 | 0.10279 | 0.615 | indistinguishable from zero
C | 6 | 75 | 0.063749 | 0.034895 | 0.10626 | 0.33 | indistinguishable from zero
C | 7 | 69 | 0.027526 | -0.014291 | 0.12434 | 0.84 | indistinguishable from zero
C | 8 | 63 | 0.10512 | 0.059321 | 0.15394 | 0.17 | indistinguishable from zero
M | 1 | 175 | 0.91049 | 0.91461 | 0.054092 | 0 | above permutation 95th percentile (exploratory)
M | 2 | 102 | 0.78713 | 0.7942 | 0.053209 | 0 | above permutation 95th percentile (exploratory)
M | 3 | 98 | 0.18994 | 0.16786 | 0.078875 | 0 | above permutation 95th percentile (exploratory)
M | 4 | 87 | 0.034668 | 0.0015024 | 0.10421 | 0.6 | indistinguishable from zero
M | 5 | 80 | 0.027565 | -0.0085023 | 0.10988 | 0.825 | indistinguishable from zero
M | 6 | 72 | 0.05195 | 0.011875 | 0.11606 | 0.525 | indistinguishable from zero
M | 7 | 68 | 0.056401 | 0.013969 | 0.13776 | 0.53 | indistinguishable from zero
M | 8 | 67 | 0.07481 | 0.031744 | 0.10787 | 0.26 | indistinguishable from zero

## B. Memory — matched inflow, C versus M
C and M receive identical inflow. C carries memory; M resets it before each choice. This is a memory contrast, not evidence of Outside access.
Compare the C and M rows above for outcome predictability and process history; full memory activity is archived in the JSON.

## C. Signal — C versus eight canonical reference arms (channel A)
Only Signal bears on the proposed Outside hypothesis; it is exploratory and not a registered hypothesis test.

### Declared comparisons and cross-week tally
N = 29 declared statistics; 28 comparable this week; F = 8 flagged. Expected flags under exchangeability without ties: 2N/9 = 6.4444; for the comparable subset: 6.2222.
Statistics are correlated, which can make F vary more than a binomial count; the expectation is unchanged under exchangeability without ties. Memory carries across weeks, so weeks are serially dependent and a binomial reference is approximate.
Equal values occupy a tied rank interval; equality with a reference extreme is never flagged.
Self-loop counts at 0, 3 and 9 use boundary-entry episodes; zone 1 uses traversal episodes. Zone occupancy 0 is descriptive only.
An unavailable statistic is not flagged and does not count as a compared week. The table gives flagged / compared weeks and expectation 2/9 per compared week; JSON also gives total reported weeks. Persistent departures across weeks are the pattern of interest; a single week’s flag is not.

Statistic | C | R range | Tied rank | Flag | Weeks flagged / compared | Expected
---|---:|---|---|---|---|---:
warp_fraction | 0.74775 | 0.61475–0.80992 | 3–3 | — | 0/1 | 0.222
boundary_ending_rate_all | 0.11792 | 0.11388–0.15027 | 2–2 | — | 0/1 | 0.222
mean_completed_length | 12.775 | 11.301–13.467 | 7–7 | — | 0/1 | 0.222
distinct_routes_per_100_episodes | 89.189 | 81.739–87.805 | 9–9 | YES | 1/1 | 0.222
zone_occupancy_1 | 0.36972 | 0.34384–0.36932 | 9–9 | YES | 1/1 | 0.222
zone_occupancy_2 | 0.062676 | 0.054726–0.064789 | 8–8 | — | 0/1 | 0.222
zone_occupancy_3 | 0.01831 | 0.009233–0.023639 | 7–7 | — | 0/1 | 0.222
zone_occupancy_4 | 0.035211 | 0.041903–0.048832 | 1–1 | YES | 1/1 | 0.222
zone_occupancy_5 | 0.16127 | 0.16486–0.18124 | 1–1 | YES | 1/1 | 0.222
zone_occupancy_6 | 0.040141 | 0.034507–0.052594 | 3–3 | — | 0/1 | 0.222
zone_occupancy_7 | 0.22535 | 0.20897–0.22865 | 7–7 | — | 0/1 | 0.222
zone_occupancy_8 | 0.067606 | 0.053634–0.085322 | 3–3 | — | 0/1 | 0.222
zone_occupancy_9 | 0.019718 | 0.016231–0.033984 | 7–7 | — | 0/1 | 0.222
self_loops_0 | 0 | 1–12 | 1–1 | YES | 1/1 | 0.222
self_loops_1 | 224 | 177–232 | 8–8 | — | 0/1 | 0.222
self_loops_3 | 18 | 3–12 | 9–9 | YES | 1/1 | 0.222
self_loops_9 | 10 | 9–19 | 3–3 | — | 0/1 | 0.222
commitment_changed | 537 | 0–534 | 9–9 | YES | 1/1 | 0.222
governor_changed | 547 | 504–540 | 9–9 | YES | 1/1 | 0.222
retention_changed | 390 | 356–519 | 5–5 | — | 0/1 | 0.222
remembered_exit_ratio | undefined | unavailable | unavailable | — | 0/0 | 0.000
outcome_mm_lag_1 | 0.82133 | 0.70761–0.96758 | 7–7 | — | 0/1 | 0.222
outcome_mm_lag_2 | 0.80225 | 0.66408–0.95587 | 7–7 | — | 0/1 | 0.222
outcome_mm_lag_3 | 0.071752 | 0.071725–0.29303 | 2–2 | — | 0/1 | 0.222
outcome_mm_lag_4 | 0.052422 | -0.00019612–0.068753 | 6–6 | — | 0/1 | 0.222
outcome_mm_lag_5 | 0.0060168 | -0.012169–0.058123 | 5–5 | — | 0/1 | 0.222
outcome_mm_lag_6 | 0.034895 | -0.010924–0.16146 | 6–6 | — | 0/1 | 0.222
outcome_mm_lag_7 | -0.014291 | -0.014898–0.059902 | 2–2 | — | 0/1 | 0.222
outcome_mm_lag_8 | 0.059321 | -0.046005–0.10709 | 7–7 | — | 0/1 | 0.222

Leave-one-out flag counts (each arm against the other eight; descriptive empirical comparison, not an independent null sample):

Arm | F | Comparable
---|---:|---:
C | 8 | 28
R01 | 2 | 28
R02 | 5 | 28
R03 | 4 | 28
R04 | 1 | 28
R05 | 9 | 28
R06 | 5 | 28
R07 | 9 | 28
R08 | 11 | 28

All other values, including eligible counts, visit sums and route novelty/rarity ranks, are derived descriptions and are never flagged.

### Traversal route novelty, rarity and recurrence
Counts are distinct typed routes; rates are per 100 completed traversal episodes. Reference rarity is leave-one-out among C and R01–R08, with occurrence in at most one of the other eight arms. It is not defined for M or G. Recurring rare routes were rare at first appearance, not merely rare now.

Arm | Novel | Novel / 100 | Reference-rare | Rare / 100 | Recurring rare this week
---|---:|---:|---:|---:|---:
C | 99 | 89.189 | 84 | 75.676 | 0
M | 101 | 91.818 | undefined | undefined | 0
G00 | 116 | 44.961 | undefined | undefined | 0
G01 | 117 | 37.621 | undefined | undefined | 0
G02 | 119 | 39.535 | undefined | undefined | 0
G03 | 128 | 39.628 | undefined | undefined | 0
G04 | 95 | 23.75 | undefined | undefined | 0
G05 | 83 | 20.244 | undefined | undefined | 0
G06 | 102 | 24.697 | undefined | undefined | 0
G07 | 103 | 28.532 | undefined | undefined | 0
R01 | 94 | 81.739 | 80 | 69.565 | 0
R02 | 105 | 87.5 | 90 | 75 | 0
R03 | 108 | 87.805 | 89 | 72.358 | 0
R04 | 100 | 85.47 | 86 | 73.504 | 0
R05 | 101 | 82.787 | 87 | 71.311 | 0
R06 | 90 | 83.333 | 77 | 71.296 | 0
R07 | 103 | 85.124 | 91 | 75.207 | 0
R08 | 86 | 81.905 | 73 | 69.524 | 0

C descriptive ranks among nine canonical memory-carrying arms:
- novel_count: 4–4.
- novel_per_100_episodes: 9–9.
- reference_rare_count: 4–4.
- reference_rare_per_100_episodes: 9–9.
- recurring_rare_this_week: 1–9.

Full class-specific length distributions, routes, memory activity, occupancy and lag statistics for every arm are retained in JSON.

## Timing
Priority begins only at the verified seal timestamp in seal/receipt.json. No priority is claimed over inputs already available before that time.
Exploratory; no hypothesis test or calibrated anomaly claim.
References are deterministic transformations of the same inflow, not independent sources.
2/9 is conditional on exchangeability and no ties; many weekly flags are expected.
Outcome predictability is within-episode forward association, not evidence of external anticipation.
