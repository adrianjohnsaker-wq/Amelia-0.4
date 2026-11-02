# Amelia C1 — 2026-W44 — amendments 7–12 (report layout)
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
C | 1328 | 880 | 448 | 0 | 0.66265 | 0.13175 | 7.5783 | 621
M | 1389 | 917 | 472 | 0 | 0.66019 | 0.1378 | 7.2253 | 625
G00 | 2689 | 1621 | 1068 | 0 | 0.60283 | 0.26677 | 3.749 | 726
G01 | 3647 | 2557 | 1090 | 0 | 0.70112 | 0.36181 | 2.7639 | 597
G02 | 3625 | 1891 | 1734 | 0 | 0.52166 | 0.35962 | 2.7796 | 601
G03 | 3916 | 2161 | 1755 | 0 | 0.55184 | 0.38849 | 2.5735 | 561
G04 | 4792 | 2943 | 1849 | 0 | 0.61415 | 0.4754 | 2.1035 | 258
G05 | 4741 | 2563 | 2178 | 0 | 0.5406 | 0.47034 | 2.1261 | 345
G06 | 4688 | 2581 | 2107 | 0 | 0.55055 | 0.46508 | 2.1504 | 383
G07 | 3967 | 2439 | 1528 | 0 | 0.61482 | 0.39355 | 2.5407 | 532
R01 | 1342 | 878 | 464 | 0 | 0.65425 | 0.13313 | 7.5306 | 610
R02 | 1392 | 857 | 535 | 0 | 0.61566 | 0.1381 | 7.2371 | 617
R03 | 1381 | 883 | 498 | 0 | 0.63939 | 0.137 | 7.3077 | 585
R04 | 1273 | 841 | 432 | 0 | 0.66064 | 0.12629 | 7.8924 | 583
R05 | 1323 | 829 | 494 | 0 | 0.62661 | 0.13125 | 7.6122 | 568
R06 | 1459 | 957 | 502 | 0 | 0.65593 | 0.14474 | 6.8999 | 610
R07 | 1423 | 918 | 505 | 0 | 0.64512 | 0.14117 | 7.0998 | 594
R08 | 1374 | 858 | 516 | 0 | 0.62445 | 0.13631 | 7.3253 | 567

C length distribution (moves: episodes): 1: 601, 2: 40, 3: 59, 4: 47, 5: 41, 6: 48, 7: 42, 8: 34, 9: 42, 10: 28, 11: 45, 12: 32, 13: 26, 14: 16, 15: 26, 16: 17, 17: 23, 18: 15, 19: 12, 20: 14, 21: 9, 22: 10, 23: 7, 24: 3, 25: 8, 26: 4, 27: 6, 28: 6, 29: 5, 30: 4, 31: 6, 32: 1, 33: 2, 34: 2, 35: 1, 36: 6, 37: 7, 38: 3, 39: 3, 40: 2, 42: 3, 43: 2, 44: 1, 45: 2, 46: 3, 48: 3, 50: 1, 52: 1, 54: 1, 57: 3, 59: 1, 62: 2, 79: 1, 98: 1.
C unfinished episode at week end: {"length": 17, "entry": 7, "episode_class": "traversal"}.

C frequent typed routes:
- 66 occurrences, entry 9: 9→9 (Plex)
- 64 occurrences, entry 6: 6→3 (Warp)
- 59 occurrences, entry 0: 0→9 (Plex)
- 50 occurrences, entry 3: 3→3 (Warp)
- 44 occurrences, entry 3: 3→6 (Gt-06)
- 42 occurrences, entry 5: 5→6 (Gt-15)
- 39 occurrences, entry 2: 2→3 (Gt-03)
- 35 occurrences, entry 8: 8→9 (Gt-36)
- 33 occurrences, entry 3: 3→6 (syzygy)
- 32 occurrences, entry 0: 0→0 (Gt-00)

### traversal

Arm | Completed | Warp | Plex | Cap | Warp fraction | Boundary endings / class tick | Mean length | Distinct routes
---|---:|---:|---:|---:|---:|---:|---:|---:
C | 843 | 629 | 214 | 0 | 0.74614 | 0.087858 | 11.363 | 609
M | 872 | 643 | 229 | 0 | 0.73739 | 0.091185 | 10.916 | 613
G00 | 1682 | 1113 | 569 | 0 | 0.66171 | 0.22586 | 4.4281 | 552
G01 | 2249 | 1843 | 406 | 0 | 0.81948 | 0.31463 | 3.1783 | 428
G02 | 2225 | 1210 | 1015 | 0 | 0.54382 | 0.32288 | 3.0971 | 415
G03 | 2420 | 1476 | 944 | 0 | 0.60992 | 0.33472 | 2.9868 | 419
G04 | 2916 | 2112 | 804 | 0 | 0.72428 | 0.44553 | 2.2445 | 153
G05 | 2919 | 1654 | 1265 | 0 | 0.56663 | 0.46282 | 2.1607 | 195
G06 | 2831 | 1856 | 975 | 0 | 0.6556 | 0.44124 | 2.2667 | 249
G07 | 2418 | 1664 | 754 | 0 | 0.68817 | 0.37977 | 2.6328 | 339
R01 | 846 | 634 | 212 | 0 | 0.74941 | 0.088272 | 11.359 | 598
R02 | 837 | 612 | 225 | 0 | 0.73118 | 0.087874 | 11.373 | 605
R03 | 821 | 601 | 220 | 0 | 0.73203 | 0.086239 | 11.61 | 573
R04 | 810 | 607 | 203 | 0 | 0.74938 | 0.084226 | 11.832 | 571
R05 | 775 | 564 | 211 | 0 | 0.72774 | 0.081305 | 12.288 | 556
R06 | 848 | 627 | 221 | 0 | 0.73939 | 0.089555 | 11.151 | 598
R07 | 829 | 635 | 194 | 0 | 0.76598 | 0.087392 | 11.47 | 582
R08 | 799 | 581 | 218 | 0 | 0.72716 | 0.084061 | 11.877 | 555

C length distribution (moves: episodes): 1: 116, 2: 40, 3: 59, 4: 47, 5: 41, 6: 48, 7: 42, 8: 34, 9: 42, 10: 28, 11: 45, 12: 32, 13: 26, 14: 16, 15: 26, 16: 17, 17: 23, 18: 15, 19: 12, 20: 14, 21: 9, 22: 10, 23: 7, 24: 3, 25: 8, 26: 4, 27: 6, 28: 6, 29: 5, 30: 4, 31: 6, 32: 1, 33: 2, 34: 2, 35: 1, 36: 6, 37: 7, 38: 3, 39: 3, 40: 2, 42: 3, 43: 2, 44: 1, 45: 2, 46: 3, 48: 3, 50: 1, 52: 1, 54: 1, 57: 3, 59: 1, 62: 2, 79: 1, 98: 1.
C unfinished episode at week end: {"length": 17, "entry": 7, "episode_class": "traversal"}.

C frequent typed routes:
- 42 occurrences, entry 5: 5→6 (Gt-15)
- 39 occurrences, entry 2: 2→3 (Gt-03)
- 35 occurrences, entry 8: 8→9 (Gt-36)
- 12 occurrences, entry 2: 2→5 (Hold); 5→6 (Gt-15)
- 11 occurrences, entry 7: 7→5 (Hold); 5→6 (Gt-15)
- 9 occurrences, entry 1: 1→7 (Surge); 7→5 (Hold); 5→6 (Gt-15)
- 8 occurrences, entry 7: 7→2 (syzygy); 2→3 (Gt-03)
- 8 occurrences, entry 8: 8→7 (Surge); 7→5 (Hold); 5→6 (Gt-15)
- 7 occurrences, entry 1: 1→7 (Surge); 7→2 (syzygy); 2→3 (Gt-03)
- 7 occurrences, entry 2: 2→7 (syzygy); 7→5 (Hold); 5→6 (Gt-15)

### boundary entry

Arm | Completed | Warp | Plex | Cap | Warp fraction | Boundary endings / class tick | Mean length | Distinct routes
---|---:|---:|---:|---:|---:|---:|---:|---:
C | 485 | 251 | 234 | 0 | 0.51753 | 1 | 1 | 12
M | 517 | 274 | 243 | 0 | 0.52998 | 1 | 1 | 12
G00 | 1007 | 508 | 499 | 0 | 0.50447 | 0.38245 | 2.6147 | 174
G01 | 1398 | 714 | 684 | 0 | 0.51073 | 0.47681 | 2.0973 | 169
G02 | 1400 | 681 | 719 | 0 | 0.48643 | 0.43901 | 2.275 | 186
G03 | 1496 | 685 | 811 | 0 | 0.45789 | 0.52491 | 1.9051 | 142
G04 | 1876 | 831 | 1045 | 0 | 0.44296 | 0.53069 | 1.8843 | 105
G05 | 1822 | 909 | 913 | 0 | 0.4989 | 0.4829 | 2.0708 | 150
G06 | 1857 | 725 | 1132 | 0 | 0.39041 | 0.50682 | 1.9731 | 134
G07 | 1549 | 775 | 774 | 0 | 0.50032 | 0.41718 | 2.397 | 193
R01 | 496 | 244 | 252 | 0 | 0.49194 | 1 | 1 | 12
R02 | 555 | 245 | 310 | 0 | 0.44144 | 1 | 1 | 12
R03 | 560 | 282 | 278 | 0 | 0.50357 | 1 | 1 | 12
R04 | 463 | 234 | 229 | 0 | 0.5054 | 1 | 1 | 12
R05 | 548 | 265 | 283 | 0 | 0.48358 | 1 | 1 | 12
R06 | 611 | 330 | 281 | 0 | 0.5401 | 1 | 1 | 12
R07 | 594 | 283 | 311 | 0 | 0.47643 | 1 | 1 | 12
R08 | 575 | 277 | 298 | 0 | 0.48174 | 1 | 1 | 12

C length distribution (moves: episodes): 1: 485.
C unfinished episode at week end: null.

C frequent typed routes:
- 66 occurrences, entry 9: 9→9 (Plex)
- 64 occurrences, entry 6: 6→3 (Warp)
- 59 occurrences, entry 0: 0→9 (Plex)
- 50 occurrences, entry 3: 3→3 (Warp)
- 44 occurrences, entry 3: 3→6 (Gt-06)
- 33 occurrences, entry 3: 3→6 (syzygy)
- 32 occurrences, entry 0: 0→0 (Gt-00)
- 31 occurrences, entry 0: 0→9 (syzygy)
- 31 occurrences, entry 6: 6→3 (syzygy)
- 29 occurrences, entry 6: 6→3 (Gt-21)

### Canonical boundary-entry diagnostic
Every completed canonical boundary-entry episode must have length 1 and the outcome fixed by entry: 0/9 → Plex; 3/6 → Warp. G arms are not subject to this diagnostic.
- C: PASS; checked 485; failures 0. Unfinished: {"length": 17, "entry": 7, "episode_class": "traversal"}.
- M: PASS; checked 517; failures 0. Unfinished: {"length": 45, "entry": 5, "episode_class": "traversal"}.
- G00: NOT_APPLICABLE; checked 0; failures 0. Unfinished: null.
- G01: NOT_APPLICABLE; checked 0; failures 0. Unfinished: null.
- G02: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 8, "entry": 9, "episode_class": "boundary_entry"}.
- G03: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 3, "entry": 8, "episode_class": "traversal"}.
- G04: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 1, "entry": 5, "episode_class": "traversal"}.
- G05: NOT_APPLICABLE; checked 0; failures 0. Unfinished: null.
- G06: NOT_APPLICABLE; checked 0; failures 0. Unfinished: null.
- G07: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 1, "entry": 5, "episode_class": "traversal"}.
- R01: PASS; checked 496; failures 0. Unfinished: {"length": 8, "entry": 5, "episode_class": "traversal"}.
- R02: PASS; checked 555; failures 0. Unfinished: {"length": 8, "entry": 2, "episode_class": "traversal"}.
- R03: PASS; checked 560; failures 0. Unfinished: {"length": 7, "entry": 4, "episode_class": "traversal"}.
- R04: PASS; checked 463; failures 0. Unfinished: {"length": 33, "entry": 1, "episode_class": "traversal"}.
- R05: PASS; checked 548; failures 0. Unfinished: {"length": 11, "entry": 7, "episode_class": "traversal"}.
- R06: PASS; checked 611; failures 0. Unfinished: {"length": 13, "entry": 7, "episode_class": "traversal"}.
- R07: PASS; checked 594; failures 0. Unfinished: {"length": 2, "entry": 5, "episode_class": "traversal"}.
- R08: PASS; checked 575; failures 0. Unfinished: {"length": 25, "entry": 4, "episode_class": "traversal"}.

### Outcome predictability
This quantity is within-episode forward association, not evidence of external anticipation. Traversal boundary endings are primary; all boundary endings are secondary. Miller–Madow estimates are signed and are not clipped to zero. A lag with n < 50 is insufficient. Values within the permutation null are reported as indistinguishable from zero.
B = 200; null 95th percentile uses nearest rank; ≥ proportion is the number of permuted plug-in values at least as large as observed divided by 200. The JSON contains every arm’s values and exact seed.

### traversal series: C and M

Arm | Lag | n | Plug-in bits | MM bits | Null 95% bits | ≥ proportion | Interpretation
---|---:|---:|---:|---:|---:|---:|---
C | 1 | 843 | 0.81733 | 0.81819 | 0.0048581 | 0 | above permutation 95th percentile (exploratory)
C | 2 | 727 | 0.80523 | 0.80622 | 0.0072941 | 0 | above permutation 95th percentile (exploratory)
C | 3 | 687 | 0.14039 | 0.13724 | 0.011925 | 0 | above permutation 95th percentile (exploratory)
C | 4 | 628 | 0.012053 | 0.0063096 | 0.012974 | 0.085 | indistinguishable from zero
C | 5 | 581 | 0.014742 | 0.0085341 | 0.014117 | 0.05 | above permutation 95th percentile (exploratory)
C | 6 | 540 | 0.0061217 | -0.0005574 | 0.012651 | 0.48 | indistinguishable from zero
C | 7 | 492 | 0.012897 | 0.0055661 | 0.016999 | 0.115 | indistinguishable from zero
C | 8 | 450 | 0.0056996 | -0.0023153 | 0.017353 | 0.605 | indistinguishable from zero
M | 1 | 872 | 0.83067 | 0.83149 | 0.0047967 | 0 | above permutation 95th percentile (exploratory)
M | 2 | 757 | 0.8271 | 0.82806 | 0.0082521 | 0 | above permutation 95th percentile (exploratory)
M | 3 | 711 | 0.1999 | 0.19685 | 0.011248 | 0 | above permutation 95th percentile (exploratory)
M | 4 | 642 | 0.016625 | 0.011007 | 0.012998 | 0.02 | above permutation 95th percentile (exploratory)
M | 5 | 585 | 0.012158 | 0.0059931 | 0.016354 | 0.125 | indistinguishable from zero
M | 6 | 545 | 0.0086617 | 0.0020439 | 0.015327 | 0.29 | indistinguishable from zero
M | 7 | 493 | 0.014817 | 0.0075008 | 0.015996 | 0.07 | indistinguishable from zero
M | 8 | 454 | 0.013838 | 0.0058939 | 0.017974 | 0.15 | indistinguishable from zero

### all series: C and M

Arm | Lag | n | Plug-in bits | MM bits | Null 95% bits | ≥ proportion | Interpretation
---|---:|---:|---:|---:|---:|---:|---
C | 1 | 1328 | 0.92226 | 0.9228 | 0.0074352 | 0 | above permutation 95th percentile (exploratory)
C | 2 | 727 | 0.80523 | 0.80622 | 0.0072941 | 0 | above permutation 95th percentile (exploratory)
C | 3 | 687 | 0.14039 | 0.13724 | 0.011925 | 0 | above permutation 95th percentile (exploratory)
C | 4 | 628 | 0.012053 | 0.0063096 | 0.012974 | 0.085 | indistinguishable from zero
C | 5 | 581 | 0.014742 | 0.0085341 | 0.014117 | 0.05 | above permutation 95th percentile (exploratory)
C | 6 | 540 | 0.0061217 | -0.0005574 | 0.012651 | 0.48 | indistinguishable from zero
C | 7 | 492 | 0.012897 | 0.0055661 | 0.016999 | 0.115 | indistinguishable from zero
C | 8 | 450 | 0.0056996 | -0.0023153 | 0.017353 | 0.605 | indistinguishable from zero
M | 1 | 1389 | 0.92464 | 0.92516 | 0.0059899 | 0 | above permutation 95th percentile (exploratory)
M | 2 | 757 | 0.8271 | 0.82806 | 0.0082521 | 0 | above permutation 95th percentile (exploratory)
M | 3 | 711 | 0.1999 | 0.19685 | 0.011248 | 0 | above permutation 95th percentile (exploratory)
M | 4 | 642 | 0.016625 | 0.011007 | 0.012998 | 0.02 | above permutation 95th percentile (exploratory)
M | 5 | 585 | 0.012158 | 0.0059931 | 0.016354 | 0.125 | indistinguishable from zero
M | 6 | 545 | 0.0086617 | 0.0020439 | 0.015327 | 0.29 | indistinguishable from zero
M | 7 | 493 | 0.014817 | 0.0075008 | 0.015996 | 0.07 | indistinguishable from zero
M | 8 | 454 | 0.013838 | 0.0058939 | 0.017974 | 0.15 | indistinguishable from zero

## B. Memory — matched inflow, C versus M
C and M receive identical inflow. C carries memory; M resets it before each choice. This is a memory contrast, not evidence of Outside access.
Compare the C and M rows above for outcome predictability and process history; full memory activity is archived in the JSON.

## C. Signal — C versus eight canonical reference arms (channel A)
Only Signal bears on the proposed Outside hypothesis; it is exploratory and not a registered hypothesis test.

### Declared comparisons and cross-week tally
N = 29 declared statistics; 29 comparable this week; F = 3 flagged. Expected flags under exchangeability without ties: 2N/9 = 6.4444; for the comparable subset: 6.4444.
Statistics are correlated, which can make F vary more than a binomial count; the expectation is unchanged under exchangeability without ties. Memory carries across weeks, so weeks are serially dependent and a binomial reference is approximate.
Equal values occupy a tied rank interval; equality with a reference extreme is never flagged.
Self-loop counts at 0, 3 and 9 use boundary-entry episodes; zone 1 uses traversal episodes. Zone occupancy 0 is descriptive only.
An unavailable statistic is not flagged and does not count as a compared week. The table gives flagged / compared weeks and expectation 2/9 per compared week; JSON also gives total reported weeks. Persistent departures across weeks are the pattern of interest; a single week’s flag is not.

Statistic | C | R range | Tied rank | Flag | Weeks flagged / compared | Expected
---|---:|---|---|---|---|---:
warp_fraction | 0.74614 | 0.72716–0.76598 | 6–6 | — | 0/3 | 0.667
boundary_ending_rate_all | 0.13175 | 0.12629–0.14474 | 3–3 | — | 0/3 | 0.667
mean_completed_length | 11.363 | 11.151–12.288 | 3–3 | — | 0/3 | 0.667
distinct_routes_per_100_episodes | 72.242 | 69.462–72.282 | 8–8 | — | 1/3 | 0.667
zone_occupancy_1 | 0.33966 | 0.33723–0.35939 | 2–2 | — | 1/3 | 0.667
zone_occupancy_2 | 0.061178 | 0.055357–0.061441 | 8–8 | — | 0/3 | 0.667
zone_occupancy_3 | 0.018343 | 0.015946–0.020168 | 4–4 | — | 0/3 | 0.667
zone_occupancy_4 | 0.047004 | 0.039427–0.048248 | 8–8 | — | 1/3 | 0.667
zone_occupancy_5 | 0.16561 | 0.1575–0.17091 | 4–4 | — | 1/3 | 0.667
zone_occupancy_6 | 0.047212 | 0.042083–0.04831 | 7–7 | — | 0/3 | 0.667
zone_occupancy_7 | 0.22126 | 0.21428–0.22235 | 8–8 | — | 0/3 | 0.667
zone_occupancy_8 | 0.077436 | 0.072164–0.078053 | 8–8 | — | 0/3 | 0.667
zone_occupancy_9 | 0.022303 | 0.020451–0.023622 | 5–5 | — | 1/3 | 0.667
self_loops_0 | 32 | 24–44 | 4–4 | — | 2/3 | 0.667
self_loops_1 | 1145 | 1148–1361 | 1–1 | YES | 1/3 | 0.667
self_loops_3 | 50 | 46–73 | 2–2 | — | 1/3 | 0.667
self_loops_9 | 94 | 96–131 | 1–1 | YES | 1/3 | 0.667
commitment_changed | 1602 | 676–2962 | 3–3 | — | 1/3 | 0.667
governor_changed | 3384 | 3376–3554 | 2–2 | — | 1/3 | 0.667
retention_changed | 2147 | 2245–2939 | 1–1 | YES | 1/3 | 0.667
remembered_exit_ratio | 0.97077 | 0.91414–1.062 | 2–2 | — | 0/2 | 0.444
outcome_mm_lag_1 | 0.81819 | 0.78582–0.84641 | 4–4 | — | 0/3 | 0.667
outcome_mm_lag_2 | 0.80622 | 0.75848–0.83503 | 4–4 | — | 1/3 | 0.667
outcome_mm_lag_3 | 0.13724 | 0.13701–0.22747 | 2–2 | — | 0/3 | 0.667
outcome_mm_lag_4 | 0.0063096 | 0.0017289–0.031832 | 2–2 | — | 0/3 | 0.667
outcome_mm_lag_5 | 0.0085341 | -0.0049922–0.012221 | 7–7 | — | 0/3 | 0.667
outcome_mm_lag_6 | -0.0005574 | -0.0057506–0.0090564 | 6–6 | — | 0/3 | 0.667
outcome_mm_lag_7 | 0.0055661 | -0.0049693–0.0084218 | 8–8 | — | 0/3 | 0.667
outcome_mm_lag_8 | -0.0023153 | -0.0064437–0.0074625 | 3–3 | — | 0/3 | 0.667

Leave-one-out flag counts (each arm against the other eight; descriptive empirical comparison, not an independent null sample):

Arm | F | Comparable
---|---:|---:
C | 3 | 29
R01 | 8 | 29
R02 | 4 | 29
R03 | 4 | 29
R04 | 7 | 29
R05 | 4 | 29
R06 | 9 | 29
R07 | 8 | 29
R08 | 11 | 29

All other values, including eligible counts, visit sums and route novelty/rarity ranks, are derived descriptions and are never flagged.

### Traversal route novelty, rarity and recurrence
Counts are distinct typed routes; rates are per 100 completed traversal episodes. Reference rarity is leave-one-out among C and R01–R08, with occurrence in at most one of the other eight arms. It is not defined for M or G. Recurring rare routes were rare at first appearance, not merely rare now.

Arm | Novel | Novel / 100 | Reference-rare | Rare / 100 | Recurring rare this week
---|---:|---:|---:|---:|---:
C | 539 | 63.938 | 513 | 60.854 | 22
M | 543 | 62.271 | undefined | undefined | 0
G00 | 402 | 23.9 | undefined | undefined | 0
G01 | 253 | 11.249 | undefined | undefined | 0
G02 | 213 | 9.573 | undefined | undefined | 0
G03 | 216 | 8.9256 | undefined | undefined | 0
G04 | 21 | 0.72016 | undefined | undefined | 0
G05 | 64 | 2.1925 | undefined | undefined | 0
G06 | 84 | 2.9671 | undefined | undefined | 0
G07 | 154 | 6.3689 | undefined | undefined | 0
R01 | 524 | 61.939 | 505 | 59.693 | 18
R02 | 542 | 64.755 | 493 | 58.901 | 13
R03 | 509 | 61.998 | 475 | 57.856 | 14
R04 | 498 | 61.481 | 471 | 58.148 | 27
R05 | 491 | 63.355 | 469 | 60.516 | 13
R06 | 526 | 62.028 | 488 | 57.547 | 13
R07 | 507 | 61.158 | 470 | 56.695 | 15
R08 | 479 | 59.95 | 450 | 56.32 | 26

C descriptive ranks among nine canonical memory-carrying arms:
- novel_count: 8–8.
- novel_per_100_episodes: 8–8.
- reference_rare_count: 9–9.
- reference_rare_per_100_episodes: 9–9.
- recurring_rare_this_week: 7–7.

C traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.77508 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.68034 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

C recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

M traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.7694 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.67364 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

G00 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.35776 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.28425 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

G01 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.25496 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.14814 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

G02 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.25042 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.13483 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

G03 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.21674 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.13473 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

G04 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.092433 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.02966 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

G05 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.097346 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.042442 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

G06 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.12284 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.054677 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

G07 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.17246 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.088209 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

R01 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.74394 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.66628 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

R01 recurring rare routes:
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R02 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.76863 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.68641 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

R02 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R03 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.74249 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.64888 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

R03 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

R04 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.73948 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.66817 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

R04 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R05 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.73966 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.67023 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

R05 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R06 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.76376 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.64932 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

R06 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

R07 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.76344 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.66159 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

R07 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R08 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.72215 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.65772 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

R08 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

Full class-specific length distributions, routes, memory activity, occupancy and lag statistics for every arm are retained in JSON.

## Timing
Priority begins only at the verified seal timestamp in seal/receipt.json. No priority is claimed over inputs already available before that time.
Exploratory; no hypothesis test or calibrated anomaly claim.
References are deterministic transformations of the same inflow, not independent sources.
2/9 is conditional on exchangeability and no ties; many weekly flags are expected.
Outcome predictability is within-episode forward association, not evidence of external anticipation.
