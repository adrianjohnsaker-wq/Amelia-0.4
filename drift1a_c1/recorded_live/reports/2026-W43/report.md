# Amelia C1 — 2026-W43 — amendments 7–12 (report layout)
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
C | 1430 | 902 | 528 | 0 | 0.63077 | 0.14187 | 7.0497 | 607
M | 1448 | 917 | 531 | 0 | 0.63329 | 0.14365 | 6.962 | 619
G00 | 2622 | 1575 | 1047 | 0 | 0.60069 | 0.26012 | 3.8444 | 733
G01 | 3748 | 2698 | 1050 | 0 | 0.71985 | 0.37183 | 2.6902 | 593
G02 | 3588 | 1912 | 1676 | 0 | 0.53289 | 0.35595 | 2.8082 | 619
G03 | 3720 | 2048 | 1672 | 0 | 0.55054 | 0.36905 | 2.7102 | 585
G04 | 4655 | 2837 | 1818 | 0 | 0.60945 | 0.46181 | 2.1652 | 278
G05 | 4709 | 2493 | 2216 | 0 | 0.52941 | 0.46716 | 2.1406 | 328
G06 | 4727 | 2601 | 2126 | 0 | 0.55024 | 0.46895 | 2.1329 | 376
G07 | 4013 | 2496 | 1517 | 0 | 0.62198 | 0.39812 | 2.5123 | 515
R01 | 1344 | 845 | 499 | 0 | 0.62872 | 0.13333 | 7.4747 | 600
R02 | 1399 | 898 | 501 | 0 | 0.64189 | 0.13879 | 7.2051 | 597
R03 | 1446 | 930 | 516 | 0 | 0.64315 | 0.14345 | 6.9696 | 598
R04 | 1293 | 833 | 460 | 0 | 0.64424 | 0.12827 | 7.7997 | 589
R05 | 1354 | 883 | 471 | 0 | 0.65214 | 0.13433 | 7.4439 | 587
R06 | 1377 | 891 | 486 | 0 | 0.64706 | 0.13661 | 7.3224 | 581
R07 | 1306 | 861 | 445 | 0 | 0.65926 | 0.12956 | 7.709 | 580
R08 | 1377 | 892 | 485 | 0 | 0.64779 | 0.13661 | 7.3174 | 593

C length distribution (moves: episodes): 1: 695, 2: 50, 3: 51, 4: 52, 5: 61, 6: 40, 7: 39, 8: 33, 9: 33, 10: 38, 11: 26, 12: 23, 13: 23, 14: 25, 15: 21, 16: 17, 17: 17, 18: 14, 19: 9, 20: 19, 21: 21, 22: 15, 23: 8, 24: 5, 25: 7, 26: 7, 27: 5, 28: 10, 29: 5, 30: 9, 31: 4, 32: 5, 33: 3, 34: 6, 35: 6, 36: 2, 37: 3, 38: 2, 39: 4, 41: 1, 42: 2, 43: 3, 44: 1, 45: 2, 46: 1, 48: 1, 49: 1, 51: 1, 53: 1, 54: 1, 56: 1, 57: 1.
C unfinished episode at week end: {"length": 1, "entry": 8, "episode_class": "traversal"}.

C frequent typed routes:
- 72 occurrences, entry 6: 6→3 (Warp)
- 72 occurrences, entry 9: 9→9 (Plex)
- 70 occurrences, entry 0: 0→9 (Plex)
- 68 occurrences, entry 3: 3→3 (Warp)
- 51 occurrences, entry 9: 9→9 (Gt-45)
- 47 occurrences, entry 0: 0→0 (Gt-00)
- 46 occurrences, entry 3: 3→6 (Gt-06)
- 38 occurrences, entry 5: 5→6 (Gt-15)
- 37 occurrences, entry 2: 2→3 (Gt-03)
- 36 occurrences, entry 6: 6→3 (Gt-21)

### traversal

Arm | Completed | Warp | Plex | Cap | Warp fraction | Boundary endings / class tick | Mean length | Distinct routes
---|---:|---:|---:|---:|---:|---:|---:|---:
C | 838 | 611 | 227 | 0 | 0.72912 | 0.088322 | 11.323 | 595
M | 858 | 619 | 239 | 0 | 0.72145 | 0.090411 | 11.062 | 607
G00 | 1542 | 1017 | 525 | 0 | 0.65953 | 0.21978 | 4.5499 | 537
G01 | 2247 | 1899 | 348 | 0 | 0.84513 | 0.32608 | 3.0668 | 426
G02 | 2121 | 1144 | 977 | 0 | 0.53937 | 0.32229 | 3.1028 | 398
G03 | 2207 | 1337 | 870 | 0 | 0.6058 | 0.31269 | 3.1976 | 424
G04 | 2767 | 1997 | 770 | 0 | 0.72172 | 0.4312 | 2.3188 | 161
G05 | 2846 | 1588 | 1258 | 0 | 0.55798 | 0.45203 | 2.2122 | 185
G06 | 2778 | 1863 | 915 | 0 | 0.67063 | 0.44116 | 2.2664 | 241
G07 | 2393 | 1680 | 713 | 0 | 0.70205 | 0.37573 | 2.6623 | 335
R01 | 811 | 587 | 224 | 0 | 0.7238 | 0.084948 | 11.73 | 588
R02 | 812 | 623 | 189 | 0 | 0.76724 | 0.085537 | 11.691 | 585
R03 | 860 | 646 | 214 | 0 | 0.75116 | 0.090584 | 11.037 | 586
R04 | 789 | 586 | 203 | 0 | 0.74271 | 0.082393 | 12.143 | 577
R05 | 825 | 620 | 205 | 0 | 0.75152 | 0.086378 | 11.576 | 575
R06 | 815 | 606 | 209 | 0 | 0.74356 | 0.085627 | 11.682 | 569
R07 | 801 | 602 | 199 | 0 | 0.75156 | 0.083655 | 11.939 | 568
R08 | 812 | 602 | 210 | 0 | 0.74138 | 0.085339 | 11.713 | 581

C length distribution (moves: episodes): 1: 103, 2: 50, 3: 51, 4: 52, 5: 61, 6: 40, 7: 39, 8: 33, 9: 33, 10: 38, 11: 26, 12: 23, 13: 23, 14: 25, 15: 21, 16: 17, 17: 17, 18: 14, 19: 9, 20: 19, 21: 21, 22: 15, 23: 8, 24: 5, 25: 7, 26: 7, 27: 5, 28: 10, 29: 5, 30: 9, 31: 4, 32: 5, 33: 3, 34: 6, 35: 6, 36: 2, 37: 3, 38: 2, 39: 4, 41: 1, 42: 2, 43: 3, 44: 1, 45: 2, 46: 1, 48: 1, 49: 1, 51: 1, 53: 1, 54: 1, 56: 1, 57: 1.
C unfinished episode at week end: {"length": 1, "entry": 8, "episode_class": "traversal"}.

C frequent typed routes:
- 38 occurrences, entry 5: 5→6 (Gt-15)
- 37 occurrences, entry 2: 2→3 (Gt-03)
- 28 occurrences, entry 8: 8→9 (Gt-36)
- 17 occurrences, entry 2: 2→5 (Hold); 5→6 (Gt-15)
- 12 occurrences, entry 7: 7→5 (Hold); 5→6 (Gt-15)
- 11 occurrences, entry 4: 4→5 (syzygy); 5→6 (Gt-15)
- 9 occurrences, entry 7: 7→2 (syzygy); 2→5 (Hold); 5→6 (Gt-15)
- 7 occurrences, entry 2: 2→7 (syzygy); 7→5 (Hold); 5→6 (Gt-15)
- 6 occurrences, entry 1: 1→8 (syzygy); 8→9 (Gt-36)
- 6 occurrences, entry 4: 4→1 (Sink); 1→7 (Surge); 7→5 (Hold); 5→6 (Gt-15)

### boundary entry

Arm | Completed | Warp | Plex | Cap | Warp fraction | Boundary endings / class tick | Mean length | Distinct routes
---|---:|---:|---:|---:|---:|---:|---:|---:
C | 592 | 291 | 301 | 0 | 0.49155 | 1 | 1 | 12
M | 590 | 298 | 292 | 0 | 0.50508 | 1 | 1 | 12
G00 | 1080 | 558 | 522 | 0 | 0.51667 | 0.35248 | 2.837 | 196
G01 | 1501 | 799 | 702 | 0 | 0.53231 | 0.47068 | 2.1266 | 167
G02 | 1467 | 768 | 699 | 0 | 0.52352 | 0.41926 | 2.3824 | 221
G03 | 1513 | 711 | 802 | 0 | 0.46993 | 0.50066 | 1.9993 | 161
G04 | 1888 | 840 | 1048 | 0 | 0.44492 | 0.51542 | 1.9401 | 117
G05 | 1863 | 905 | 958 | 0 | 0.48578 | 0.49234 | 2.0311 | 143
G06 | 1949 | 738 | 1211 | 0 | 0.37866 | 0.5152 | 1.9425 | 135
G07 | 1620 | 816 | 804 | 0 | 0.5037 | 0.43654 | 2.2907 | 180
R01 | 533 | 258 | 275 | 0 | 0.48405 | 1 | 1 | 12
R02 | 587 | 275 | 312 | 0 | 0.46848 | 1 | 1 | 12
R03 | 586 | 284 | 302 | 0 | 0.48464 | 1 | 1 | 12
R04 | 504 | 247 | 257 | 0 | 0.49008 | 1 | 1 | 12
R05 | 529 | 263 | 266 | 0 | 0.49716 | 1 | 1 | 12
R06 | 562 | 285 | 277 | 0 | 0.50712 | 1 | 1 | 12
R07 | 505 | 259 | 246 | 0 | 0.51287 | 1 | 1 | 12
R08 | 565 | 290 | 275 | 0 | 0.51327 | 1 | 1 | 12

C length distribution (moves: episodes): 1: 592.
C unfinished episode at week end: null.

C frequent typed routes:
- 72 occurrences, entry 6: 6→3 (Warp)
- 72 occurrences, entry 9: 9→9 (Plex)
- 70 occurrences, entry 0: 0→9 (Plex)
- 68 occurrences, entry 3: 3→3 (Warp)
- 51 occurrences, entry 9: 9→9 (Gt-45)
- 47 occurrences, entry 0: 0→0 (Gt-00)
- 46 occurrences, entry 3: 3→6 (Gt-06)
- 36 occurrences, entry 6: 6→3 (Gt-21)
- 36 occurrences, entry 6: 6→3 (syzygy)
- 33 occurrences, entry 0: 0→9 (syzygy)

### Canonical boundary-entry diagnostic
Every completed canonical boundary-entry episode must have length 1 and the outcome fixed by entry: 0/9 → Plex; 3/6 → Warp. G arms are not subject to this diagnostic.
- C: PASS; checked 592; failures 0. Unfinished: {"length": 1, "entry": 8, "episode_class": "traversal"}.
- M: PASS; checked 590; failures 0. Unfinished: {"length": 1, "entry": 8, "episode_class": "traversal"}.
- G00: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 1, "entry": 8, "episode_class": "traversal"}.
- G01: NOT_APPLICABLE; checked 0; failures 0. Unfinished: null.
- G02: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 4, "entry": 3, "episode_class": "boundary_entry"}.
- G03: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 1, "entry": 8, "episode_class": "traversal"}.
- G04: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 1, "entry": 8, "episode_class": "traversal"}.
- G05: NOT_APPLICABLE; checked 0; failures 0. Unfinished: null.
- G06: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 1, "entry": 8, "episode_class": "traversal"}.
- G07: NOT_APPLICABLE; checked 0; failures 0. Unfinished: null.
- R01: PASS; checked 533; failures 0. Unfinished: {"length": 34, "entry": 7, "episode_class": "traversal"}.
- R02: PASS; checked 587; failures 0. Unfinished: {"length": 2, "entry": 8, "episode_class": "traversal"}.
- R03: PASS; checked 586; failures 0. Unfinished: {"length": 19, "entry": 8, "episode_class": "traversal"}.
- R04: PASS; checked 504; failures 0. Unfinished: null.
- R05: PASS; checked 529; failures 0. Unfinished: {"length": 2, "entry": 5, "episode_class": "traversal"}.
- R06: PASS; checked 562; failures 0. Unfinished: null.
- R07: PASS; checked 505; failures 0. Unfinished: {"length": 25, "entry": 5, "episode_class": "traversal"}.
- R08: PASS; checked 565; failures 0. Unfinished: {"length": 10, "entry": 1, "episode_class": "traversal"}.

### Outcome predictability
This quantity is within-episode forward association, not evidence of external anticipation. Traversal boundary endings are primary; all boundary endings are secondary. Miller–Madow estimates are signed and are not clipped to zero. A lag with n < 50 is insufficient. Values within the permutation null are reported as indistinguishable from zero.
B = 200; null 95th percentile uses nearest rank; ≥ proportion is the number of permuted plug-in values at least as large as observed divided by 200. The JSON contains every arm’s values and exact seed.

### traversal series: C and M

Arm | Lag | n | Plug-in bits | MM bits | Null 95% bits | ≥ proportion | Interpretation
---|---:|---:|---:|---:|---:|---:|---
C | 1 | 838 | 0.84273 | 0.84359 | 0.0055286 | 0 | above permutation 95th percentile (exploratory)
C | 2 | 735 | 0.84254 | 0.84352 | 0.0079983 | 0 | above permutation 95th percentile (exploratory)
C | 3 | 685 | 0.14203 | 0.13887 | 0.011487 | 0 | above permutation 95th percentile (exploratory)
C | 4 | 634 | 0.017666 | 0.011977 | 0.011944 | 0.005 | above permutation 95th percentile (exploratory)
C | 5 | 582 | 0.0065436 | 0.00034645 | 0.012601 | 0.375 | indistinguishable from zero
C | 6 | 521 | 0.011001 | 0.0040783 | 0.0154 | 0.18 | indistinguishable from zero
C | 7 | 481 | 0.0043041 | -0.0031943 | 0.019283 | 0.79 | indistinguishable from zero
C | 8 | 442 | 0.0063079 | -0.0018522 | 0.018087 | 0.605 | indistinguishable from zero
M | 1 | 858 | 0.85347 | 0.85431 | 0.0051994 | 0 | above permutation 95th percentile (exploratory)
M | 2 | 751 | 0.84569 | 0.84665 | 0.0078709 | 0 | above permutation 95th percentile (exploratory)
M | 3 | 696 | 0.19502 | 0.19191 | 0.010862 | 0 | above permutation 95th percentile (exploratory)
M | 4 | 646 | 0.033261 | 0.027678 | 0.012812 | 0 | above permutation 95th percentile (exploratory)
M | 5 | 591 | 0.0060778 | -2.4991e-05 | 0.014103 | 0.455 | indistinguishable from zero
M | 6 | 534 | 0.012561 | 0.0058072 | 0.015833 | 0.11 | indistinguishable from zero
M | 7 | 486 | 0.0052485 | -0.0021728 | 0.017327 | 0.66 | indistinguishable from zero
M | 8 | 444 | 0.0073345 | -0.00078879 | 0.018139 | 0.505 | indistinguishable from zero

### all series: C and M

Arm | Lag | n | Plug-in bits | MM bits | Null 95% bits | ≥ proportion | Interpretation
---|---:|---:|---:|---:|---:|---:|---
C | 1 | 1430 | 0.95008 | 0.95058 | 0.0065453 | 0 | above permutation 95th percentile (exploratory)
C | 2 | 735 | 0.84254 | 0.84352 | 0.0079983 | 0 | above permutation 95th percentile (exploratory)
C | 3 | 685 | 0.14203 | 0.13887 | 0.011487 | 0 | above permutation 95th percentile (exploratory)
C | 4 | 634 | 0.017666 | 0.011977 | 0.011944 | 0.005 | above permutation 95th percentile (exploratory)
C | 5 | 582 | 0.0065436 | 0.00034645 | 0.012601 | 0.375 | indistinguishable from zero
C | 6 | 521 | 0.011001 | 0.0040783 | 0.0154 | 0.18 | indistinguishable from zero
C | 7 | 481 | 0.0043041 | -0.0031943 | 0.019283 | 0.79 | indistinguishable from zero
C | 8 | 442 | 0.0063079 | -0.0018522 | 0.018087 | 0.605 | indistinguishable from zero
M | 1 | 1448 | 0.94811 | 0.94861 | 0.0074237 | 0 | above permutation 95th percentile (exploratory)
M | 2 | 751 | 0.84569 | 0.84665 | 0.0078709 | 0 | above permutation 95th percentile (exploratory)
M | 3 | 696 | 0.19502 | 0.19191 | 0.010862 | 0 | above permutation 95th percentile (exploratory)
M | 4 | 646 | 0.033261 | 0.027678 | 0.012812 | 0 | above permutation 95th percentile (exploratory)
M | 5 | 591 | 0.0060778 | -2.4991e-05 | 0.014103 | 0.455 | indistinguishable from zero
M | 6 | 534 | 0.012561 | 0.0058072 | 0.015833 | 0.11 | indistinguishable from zero
M | 7 | 486 | 0.0052485 | -0.0021728 | 0.017327 | 0.66 | indistinguishable from zero
M | 8 | 444 | 0.0073345 | -0.00078879 | 0.018139 | 0.505 | indistinguishable from zero

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
warp_fraction | 0.72912 | 0.7238–0.76724 | 2–2 | — | 0/2 | 0.444
boundary_ending_rate_all | 0.14187 | 0.12827–0.14345 | 8–8 | — | 0/2 | 0.444
mean_completed_length | 11.323 | 11.037–12.143 | 2–2 | — | 0/2 | 0.444
distinct_routes_per_100_episodes | 71.002 | 68.14–73.131 | 5–5 | — | 1/2 | 0.444
zone_occupancy_1 | 0.3399 | 0.33201–0.35833 | 2–2 | — | 1/2 | 0.444
zone_occupancy_2 | 0.057652 | 0.05483–0.061145 | 5–5 | — | 0/2 | 0.444
zone_occupancy_3 | 0.017074 | 0.0165–0.018959 | 4–4 | — | 0/2 | 0.444
zone_occupancy_4 | 0.046374 | 0.041079–0.048895 | 6–6 | — | 1/2 | 0.444
zone_occupancy_5 | 0.16979 | 0.16506–0.17202 | 6–6 | — | 1/2 | 0.444
zone_occupancy_6 | 0.047323 | 0.043783–0.049084 | 7–7 | — | 0/2 | 0.444
zone_occupancy_7 | 0.21944 | 0.21535–0.22625 | 6–6 | — | 0/2 | 0.444
zone_occupancy_8 | 0.07852 | 0.069574–0.079113 | 8–8 | — | 0/2 | 0.444
zone_occupancy_9 | 0.023925 | 0.019909–0.023463 | 9–9 | YES | 1/2 | 0.444
self_loops_0 | 47 | 25–38 | 9–9 | YES | 2/2 | 0.444
self_loops_1 | 1167 | 1081–1393 | 3–3 | — | 0/2 | 0.444
self_loops_3 | 68 | 52–69 | 8–8 | — | 1/2 | 0.444
self_loops_9 | 123 | 99–136 | 7–8 | — | 0/2 | 0.444
commitment_changed | 1517 | 984–3313 | 3–3 | — | 1/2 | 0.444
governor_changed | 3352 | 3317–3557 | 2–2 | — | 1/2 | 0.444
retention_changed | 2094 | 1796–2888 | 2–2 | — | 0/2 | 0.444
remembered_exit_ratio | 1.0236 | 0.96987–1.0421 | 8–8 | — | 0/1 | 0.222
outcome_mm_lag_1 | 0.84359 | 0.78368–0.85111 | 8–8 | — | 0/2 | 0.444
outcome_mm_lag_2 | 0.84352 | 0.76914–0.83161 | 9–9 | YES | 1/2 | 0.444
outcome_mm_lag_3 | 0.13887 | 0.11374–0.20984 | 4–4 | — | 0/2 | 0.444
outcome_mm_lag_4 | 0.011977 | -0.0014984–0.030942 | 6–6 | — | 0/2 | 0.444
outcome_mm_lag_5 | 0.00034645 | -0.0033245–0.0030266 | 7–7 | — | 0/2 | 0.444
outcome_mm_lag_6 | 0.0040783 | -0.0059859–0.0060028 | 8–8 | — | 0/2 | 0.444
outcome_mm_lag_7 | -0.0031943 | -0.0048317–0.010312 | 2–2 | — | 0/2 | 0.444
outcome_mm_lag_8 | -0.0018522 | -0.0069317–0.012627 | 4–4 | — | 0/2 | 0.444

Leave-one-out flag counts (each arm against the other eight; descriptive empirical comparison, not an independent null sample):

Arm | F | Comparable
---|---:|---:
C | 3 | 29
R01 | 9 | 29
R02 | 6 | 29
R03 | 6 | 29
R04 | 4 | 29
R05 | 8 | 29
R06 | 5 | 29
R07 | 10 | 29
R08 | 6 | 29

All other values, including eligible counts, visit sums and route novelty/rarity ranks, are derived descriptions and are never flagged.

### Traversal route novelty, rarity and recurrence
Counts are distinct typed routes; rates are per 100 completed traversal episodes. Reference rarity is leave-one-out among C and R01–R08, with occurrence in at most one of the other eight arms. It is not defined for M or G. Recurring rare routes were rare at first appearance, not merely rare now.

Arm | Novel | Novel / 100 | Reference-rare | Rare / 100 | Recurring rare this week
---|---:|---:|---:|---:|---:
C | 575 | 68.616 | 493 | 58.831 | 5
M | 584 | 68.065 | undefined | undefined | 0
G00 | 485 | 31.453 | undefined | undefined | 0
G01 | 352 | 15.665 | undefined | undefined | 0
G02 | 325 | 15.323 | undefined | undefined | 0
G03 | 340 | 15.406 | undefined | undefined | 0
G04 | 74 | 2.6744 | undefined | undefined | 0
G05 | 118 | 4.1462 | undefined | undefined | 0
G06 | 159 | 5.7235 | undefined | undefined | 0
G07 | 260 | 10.865 | undefined | undefined | 0
R01 | 571 | 70.407 | 495 | 61.036 | 4
R02 | 563 | 69.335 | 491 | 60.468 | 7
R03 | 562 | 65.349 | 493 | 57.326 | 7
R04 | 554 | 70.215 | 481 | 60.963 | 9
R05 | 553 | 67.03 | 475 | 57.576 | 8
R06 | 553 | 67.853 | 473 | 58.037 | 4
R07 | 550 | 68.664 | 474 | 59.176 | 8
R08 | 559 | 68.842 | 482 | 59.36 | 9

C descriptive ranks among nine canonical memory-carrying arms:
- novel_count: 9–9.
- novel_per_100_episodes: 4–4.
- reference_rare_count: 7–8.
- reference_rare_per_100_episodes: 4–4.
- recurring_rare_this_week: 3–3.

C traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.78234 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

C recurring rare routes:
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

M traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.78267 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

G00 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.35906 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

G01 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.25116 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

G02 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.25654 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

G03 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.23829 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

G04 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.091168 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

G05 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.097808 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

G06 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.11298 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

G07 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.17129 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R01 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.76932 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R01 recurring rare routes:
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R02 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.76192 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R02 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R03 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.73442 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R03 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R04 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.77273 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R04 recurring rare routes:
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R05 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.74535 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R05 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R06 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.7654 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R06 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R07 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.76486 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R07 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R08 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.74144 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R08 recurring rare routes:
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

Full class-specific length distributions, routes, memory activity, occupancy and lag statistics for every arm are retained in JSON.

## Timing
Priority begins only at the verified seal timestamp in seal/receipt.json. No priority is claimed over inputs already available before that time.
Exploratory; no hypothesis test or calibrated anomaly claim.
References are deterministic transformations of the same inflow, not independent sources.
2/9 is conditional on exchangeability and no ties; many weekly flags are expected.
Outcome predictability is within-episode forward association, not evidence of external anticipation.
