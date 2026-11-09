# Amelia C1 — 2026-W45 — amendments 7–12 (report layout)
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
C | 1395 | 920 | 475 | 0 | 0.6595 | 0.13839 | 7.238 | 610
M | 1414 | 920 | 494 | 0 | 0.65064 | 0.14028 | 7.1605 | 602
G00 | 2541 | 1540 | 1001 | 0 | 0.60606 | 0.25208 | 3.9658 | 719
G01 | 3580 | 2583 | 997 | 0 | 0.72151 | 0.35516 | 2.8148 | 607
G02 | 3595 | 1905 | 1690 | 0 | 0.5299 | 0.35665 | 2.8061 | 605
G03 | 3751 | 2127 | 1624 | 0 | 0.56705 | 0.37212 | 2.6875 | 582
G04 | 4704 | 2931 | 1773 | 0 | 0.62309 | 0.46667 | 2.1431 | 276
G05 | 4668 | 2573 | 2095 | 0 | 0.5512 | 0.4631 | 2.1594 | 337
G06 | 4712 | 2570 | 2142 | 0 | 0.54542 | 0.46746 | 2.1388 | 389
G07 | 4004 | 2491 | 1513 | 0 | 0.62213 | 0.39722 | 2.5177 | 531
R01 | 1399 | 898 | 501 | 0 | 0.64189 | 0.13879 | 7.1465 | 586
R02 | 1334 | 877 | 457 | 0 | 0.65742 | 0.13234 | 7.5555 | 609
R03 | 1358 | 852 | 506 | 0 | 0.62739 | 0.13472 | 7.4219 | 600
R04 | 1333 | 854 | 479 | 0 | 0.64066 | 0.13224 | 7.5859 | 590
R05 | 1368 | 882 | 486 | 0 | 0.64474 | 0.13571 | 7.375 | 613
R06 | 1351 | 881 | 470 | 0 | 0.65211 | 0.13403 | 7.4693 | 601
R07 | 1378 | 899 | 479 | 0 | 0.65239 | 0.13671 | 7.3099 | 615
R08 | 1323 | 858 | 465 | 0 | 0.64853 | 0.13125 | 7.6364 | 585

C length distribution (moves: episodes): 1: 637, 2: 58, 3: 61, 4: 63, 5: 53, 6: 54, 7: 35, 8: 37, 9: 42, 10: 30, 11: 33, 12: 28, 13: 26, 14: 19, 15: 14, 16: 16, 17: 19, 18: 16, 19: 14, 20: 8, 21: 13, 22: 8, 23: 12, 24: 6, 25: 6, 26: 8, 27: 10, 28: 2, 29: 8, 30: 5, 31: 4, 32: 2, 33: 5, 35: 3, 36: 3, 37: 5, 38: 1, 39: 1, 40: 1, 41: 5, 42: 3, 43: 1, 44: 1, 47: 3, 48: 1, 49: 1, 50: 3, 52: 2, 54: 1, 56: 2, 57: 1, 59: 1, 64: 1, 70: 2, 96: 1.
C unfinished episode at week end: null.

C frequent typed routes:
- 69 occurrences, entry 6: 6→3 (Warp)
- 65 occurrences, entry 9: 9→9 (Plex)
- 64 occurrences, entry 3: 3→3 (Warp)
- 60 occurrences, entry 0: 0→9 (Plex)
- 47 occurrences, entry 3: 3→6 (syzygy)
- 42 occurrences, entry 6: 6→3 (Gt-21)
- 36 occurrences, entry 6: 6→3 (syzygy)
- 35 occurrences, entry 0: 0→9 (syzygy)
- 34 occurrences, entry 2: 2→3 (Gt-03)
- 34 occurrences, entry 9: 9→0 (syzygy)

### traversal

Arm | Completed | Warp | Plex | Cap | Warp fraction | Boundary endings / class tick | Mean length | Distinct routes
---|---:|---:|---:|---:|---:|---:|---:|---:
C | 855 | 637 | 218 | 0 | 0.74503 | 0.089623 | 11.178 | 598
M | 858 | 630 | 228 | 0 | 0.73427 | 0.090088 | 11.153 | 590
G00 | 1521 | 1001 | 520 | 0 | 0.65812 | 0.21335 | 4.687 | 529
G01 | 2198 | 1863 | 335 | 0 | 0.84759 | 0.30638 | 3.2639 | 444
G02 | 2156 | 1164 | 992 | 0 | 0.53989 | 0.31641 | 3.1605 | 408
G03 | 2254 | 1395 | 859 | 0 | 0.6189 | 0.32058 | 3.1207 | 418
G04 | 2816 | 2046 | 770 | 0 | 0.72656 | 0.42875 | 2.3327 | 165
G05 | 2822 | 1629 | 1193 | 0 | 0.57725 | 0.44595 | 2.2424 | 197
G06 | 2850 | 1850 | 1000 | 0 | 0.64912 | 0.44503 | 2.247 | 253
G07 | 2422 | 1664 | 758 | 0 | 0.68704 | 0.37062 | 2.6986 | 353
R01 | 826 | 630 | 196 | 0 | 0.76271 | 0.086883 | 11.41 | 574
R02 | 834 | 637 | 197 | 0 | 0.76379 | 0.087056 | 11.486 | 597
R03 | 788 | 576 | 212 | 0 | 0.73096 | 0.08286 | 12.067 | 588
R04 | 781 | 566 | 215 | 0 | 0.72471 | 0.081969 | 12.241 | 578
R05 | 826 | 598 | 228 | 0 | 0.72397 | 0.086601 | 11.558 | 601
R06 | 810 | 603 | 207 | 0 | 0.74444 | 0.084915 | 11.79 | 589
R07 | 837 | 640 | 197 | 0 | 0.76464 | 0.087745 | 11.388 | 603
R08 | 805 | 611 | 194 | 0 | 0.75901 | 0.084187 | 11.907 | 573

C length distribution (moves: episodes): 1: 97, 2: 58, 3: 61, 4: 63, 5: 53, 6: 54, 7: 35, 8: 37, 9: 42, 10: 30, 11: 33, 12: 28, 13: 26, 14: 19, 15: 14, 16: 16, 17: 19, 18: 16, 19: 14, 20: 8, 21: 13, 22: 8, 23: 12, 24: 6, 25: 6, 26: 8, 27: 10, 28: 2, 29: 8, 30: 5, 31: 4, 32: 2, 33: 5, 35: 3, 36: 3, 37: 5, 38: 1, 39: 1, 40: 1, 41: 5, 42: 3, 43: 1, 44: 1, 47: 3, 48: 1, 49: 1, 50: 3, 52: 2, 54: 1, 56: 2, 57: 1, 59: 1, 64: 1, 70: 2, 96: 1.
C unfinished episode at week end: null.

C frequent typed routes:
- 34 occurrences, entry 2: 2→3 (Gt-03)
- 32 occurrences, entry 5: 5→6 (Gt-15)
- 31 occurrences, entry 8: 8→9 (Gt-36)
- 19 occurrences, entry 7: 7→5 (Hold); 5→6 (Gt-15)
- 14 occurrences, entry 2: 2→5 (Hold); 5→6 (Gt-15)
- 11 occurrences, entry 4: 4→5 (syzygy); 5→6 (Gt-15)
- 10 occurrences, entry 8: 8→7 (Surge); 7→5 (Hold); 5→6 (Gt-15)
- 9 occurrences, entry 1: 1→7 (Surge); 7→5 (Hold); 5→6 (Gt-15)
- 9 occurrences, entry 1: 1→8 (syzygy); 8→9 (Gt-36)
- 6 occurrences, entry 5: 5→1 (Sink); 1→8 (syzygy); 8→9 (Gt-36)

### boundary entry

Arm | Completed | Warp | Plex | Cap | Warp fraction | Boundary endings / class tick | Mean length | Distinct routes
---|---:|---:|---:|---:|---:|---:|---:|---:
C | 540 | 283 | 257 | 0 | 0.52407 | 1 | 1 | 12
M | 556 | 290 | 266 | 0 | 0.52158 | 1 | 1 | 12
G00 | 1020 | 539 | 481 | 0 | 0.52843 | 0.34565 | 2.8902 | 190
G01 | 1382 | 720 | 662 | 0 | 0.52098 | 0.47557 | 2.1006 | 163
G02 | 1439 | 741 | 698 | 0 | 0.51494 | 0.4406 | 2.2752 | 197
G03 | 1497 | 732 | 765 | 0 | 0.48898 | 0.49098 | 2.0354 | 164
G04 | 1888 | 885 | 1003 | 0 | 0.46875 | 0.53759 | 1.8602 | 111
G05 | 1846 | 944 | 902 | 0 | 0.51138 | 0.492 | 2.0325 | 140
G06 | 1862 | 720 | 1142 | 0 | 0.38668 | 0.50653 | 1.9731 | 136
G07 | 1582 | 827 | 755 | 0 | 0.52276 | 0.44626 | 2.2408 | 178
R01 | 573 | 268 | 305 | 0 | 0.46771 | 1 | 1 | 12
R02 | 500 | 240 | 260 | 0 | 0.48 | 1 | 1 | 12
R03 | 570 | 276 | 294 | 0 | 0.48421 | 1 | 1 | 12
R04 | 552 | 288 | 264 | 0 | 0.52174 | 1 | 1 | 12
R05 | 542 | 284 | 258 | 0 | 0.52399 | 1 | 1 | 12
R06 | 541 | 278 | 263 | 0 | 0.51386 | 1 | 1 | 12
R07 | 541 | 259 | 282 | 0 | 0.47874 | 1 | 1 | 12
R08 | 518 | 247 | 271 | 0 | 0.47683 | 1 | 1 | 12

C length distribution (moves: episodes): 1: 540.
C unfinished episode at week end: null.

C frequent typed routes:
- 69 occurrences, entry 6: 6→3 (Warp)
- 65 occurrences, entry 9: 9→9 (Plex)
- 64 occurrences, entry 3: 3→3 (Warp)
- 60 occurrences, entry 0: 0→9 (Plex)
- 47 occurrences, entry 3: 3→6 (syzygy)
- 42 occurrences, entry 6: 6→3 (Gt-21)
- 36 occurrences, entry 6: 6→3 (syzygy)
- 35 occurrences, entry 0: 0→9 (syzygy)
- 34 occurrences, entry 9: 9→0 (syzygy)
- 33 occurrences, entry 9: 9→9 (Gt-45)

### Canonical boundary-entry diagnostic
Every completed canonical boundary-entry episode must have length 1 and the outcome fixed by entry: 0/9 → Plex; 3/6 → Warp. G arms are not subject to this diagnostic.
- C: PASS; checked 540; failures 0. Unfinished: null.
- M: PASS; checked 556; failures 0. Unfinished: null.
- G00: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 3, "entry": 6, "episode_class": "boundary_entry"}.
- G01: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 3, "entry": 6, "episode_class": "boundary_entry"}.
- G02: NOT_APPLICABLE; checked 0; failures 0. Unfinished: null.
- G03: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 2, "entry": 6, "episode_class": "boundary_entry"}.
- G04: NOT_APPLICABLE; checked 0; failures 0. Unfinished: null.
- G05: NOT_APPLICABLE; checked 0; failures 0. Unfinished: null.
- G06: NOT_APPLICABLE; checked 0; failures 0. Unfinished: {"length": 2, "entry": 6, "episode_class": "boundary_entry"}.
- G07: NOT_APPLICABLE; checked 0; failures 0. Unfinished: null.
- R01: PASS; checked 573; failures 0. Unfinished: {"length": 90, "entry": 5, "episode_class": "traversal"}.
- R02: PASS; checked 500; failures 0. Unfinished: {"length": 9, "entry": 2, "episode_class": "traversal"}.
- R03: PASS; checked 570; failures 0. Unfinished: {"length": 8, "entry": 8, "episode_class": "traversal"}.
- R04: PASS; checked 552; failures 0. Unfinished: {"length": 1, "entry": 2, "episode_class": "traversal"}.
- R05: PASS; checked 542; failures 0. Unfinished: {"length": 2, "entry": 8, "episode_class": "traversal"}.
- R06: PASS; checked 541; failures 0. Unfinished: {"length": 2, "entry": 2, "episode_class": "traversal"}.
- R07: PASS; checked 541; failures 0. Unfinished: {"length": 9, "entry": 1, "episode_class": "traversal"}.
- R08: PASS; checked 518; failures 0. Unfinished: {"length": 2, "entry": 8, "episode_class": "traversal"}.

### Outcome predictability
This quantity is within-episode forward association, not evidence of external anticipation. Traversal boundary endings are primary; all boundary endings are secondary. Miller–Madow estimates are signed and are not clipped to zero. A lag with n < 50 is insufficient. Values within the permutation null are reported as indistinguishable from zero.
B = 200; null 95th percentile uses nearest rank; ≥ proportion is the number of permuted plug-in values at least as large as observed divided by 200. The JSON contains every arm’s values and exact seed.

### traversal series: C and M

Arm | Lag | n | Plug-in bits | MM bits | Null 95% bits | ≥ proportion | Interpretation
---|---:|---:|---:|---:|---:|---:|---
C | 1 | 855 | 0.81906 | 0.81991 | 0.0052146 | 0 | above permutation 95th percentile (exploratory)
C | 2 | 758 | 0.80601 | 0.80696 | 0.0069434 | 0 | above permutation 95th percentile (exploratory)
C | 3 | 700 | 0.19552 | 0.19243 | 0.011896 | 0 | above permutation 95th percentile (exploratory)
C | 4 | 639 | 0.025735 | 0.020091 | 0.011614 | 0.005 | above permutation 95th percentile (exploratory)
C | 5 | 576 | 0.0079783 | 0.0017166 | 0.013549 | 0.265 | indistinguishable from zero
C | 6 | 523 | 0.0098376 | 0.0029413 | 0.014489 | 0.23 | indistinguishable from zero
C | 7 | 469 | 0.0068871 | -0.00080315 | 0.016003 | 0.54 | indistinguishable from zero
C | 8 | 434 | 0.0044927 | -0.0038177 | 0.019296 | 0.73 | indistinguishable from zero
M | 1 | 858 | 0.83528 | 0.83612 | 0.0051334 | 0 | above permutation 95th percentile (exploratory)
M | 2 | 760 | 0.81951 | 0.82046 | 0.0080143 | 0 | above permutation 95th percentile (exploratory)
M | 3 | 706 | 0.21907 | 0.21601 | 0.01188 | 0 | above permutation 95th percentile (exploratory)
M | 4 | 643 | 0.02473 | 0.019121 | 0.013289 | 0 | above permutation 95th percentile (exploratory)
M | 5 | 576 | 0.0057423 | -0.00051937 | 0.0126 | 0.47 | indistinguishable from zero
M | 6 | 520 | 0.018965 | 0.012029 | 0.015281 | 0.015 | above permutation 95th percentile (exploratory)
M | 7 | 460 | 0.0067162 | -0.0011245 | 0.017103 | 0.49 | indistinguishable from zero
M | 8 | 427 | 0.0067618 | -0.0016849 | 0.021594 | 0.605 | indistinguishable from zero

### all series: C and M

Arm | Lag | n | Plug-in bits | MM bits | Null 95% bits | ≥ proportion | Interpretation
---|---:|---:|---:|---:|---:|---:|---
C | 1 | 1395 | 0.9253 | 0.92582 | 0.0062556 | 0 | above permutation 95th percentile (exploratory)
C | 2 | 758 | 0.80601 | 0.80696 | 0.0069434 | 0 | above permutation 95th percentile (exploratory)
C | 3 | 700 | 0.19552 | 0.19243 | 0.011896 | 0 | above permutation 95th percentile (exploratory)
C | 4 | 639 | 0.025735 | 0.020091 | 0.011614 | 0.005 | above permutation 95th percentile (exploratory)
C | 5 | 576 | 0.0079783 | 0.0017166 | 0.013549 | 0.265 | indistinguishable from zero
C | 6 | 523 | 0.0098376 | 0.0029413 | 0.014489 | 0.23 | indistinguishable from zero
C | 7 | 469 | 0.0068871 | -0.00080315 | 0.016003 | 0.54 | indistinguishable from zero
C | 8 | 434 | 0.0044927 | -0.0038177 | 0.019296 | 0.73 | indistinguishable from zero
M | 1 | 1414 | 0.9335 | 0.93401 | 0.0065921 | 0 | above permutation 95th percentile (exploratory)
M | 2 | 760 | 0.81951 | 0.82046 | 0.0080143 | 0 | above permutation 95th percentile (exploratory)
M | 3 | 706 | 0.21907 | 0.21601 | 0.01188 | 0 | above permutation 95th percentile (exploratory)
M | 4 | 643 | 0.02473 | 0.019121 | 0.013289 | 0 | above permutation 95th percentile (exploratory)
M | 5 | 576 | 0.0057423 | -0.00051937 | 0.0126 | 0.47 | indistinguishable from zero
M | 6 | 520 | 0.018965 | 0.012029 | 0.015281 | 0.015 | above permutation 95th percentile (exploratory)
M | 7 | 460 | 0.0067162 | -0.0011245 | 0.017103 | 0.49 | indistinguishable from zero
M | 8 | 427 | 0.0067618 | -0.0016849 | 0.021594 | 0.605 | indistinguishable from zero

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
warp_fraction | 0.74503 | 0.72397–0.76464 | 5–5 | — | 0/4 | 0.889
boundary_ending_rate_all | 0.13839 | 0.13125–0.13879 | 8–8 | — | 0/4 | 0.889
mean_completed_length | 11.178 | 11.388–12.241 | 1–1 | YES | 1/4 | 0.889
distinct_routes_per_100_episodes | 69.942 | 69.492–74.619 | 2–2 | — | 1/4 | 0.889
zone_occupancy_1 | 0.34025 | 0.33455–0.36037 | 2–2 | — | 1/4 | 0.889
zone_occupancy_2 | 0.059539 | 0.054065–0.060593 | 6–6 | — | 0/4 | 0.889
zone_occupancy_3 | 0.018449 | 0.015983–0.020042 | 6–6 | — | 0/4 | 0.889
zone_occupancy_4 | 0.043082 | 0.043968–0.047809 | 1–1 | YES | 2/4 | 0.889
zone_occupancy_5 | 0.16751 | 0.16272–0.17223 | 6–6 | — | 1/4 | 0.889
zone_occupancy_6 | 0.048323 | 0.042926–0.049167 | 8–8 | — | 0/4 | 0.889
zone_occupancy_7 | 0.22327 | 0.21514–0.22808 | 8–8 | — | 0/4 | 0.889
zone_occupancy_8 | 0.07673 | 0.071391–0.07685 | 8–8 | — | 0/4 | 0.889
zone_occupancy_9 | 0.022851 | 0.020289–0.023904 | 8–8 | — | 1/4 | 0.889
self_loops_0 | 30 | 28–39 | 2–2 | — | 2/4 | 0.889
self_loops_1 | 1148 | 1072–1375 | 2–2 | — | 1/4 | 0.889
self_loops_3 | 64 | 53–73 | 7–7 | — | 1/4 | 0.889
self_loops_9 | 98 | 89–135 | 2–2 | — | 1/4 | 0.889
commitment_changed | 1200 | 1526–3230 | 1–1 | YES | 2/4 | 0.889
governor_changed | 3407 | 3355–3560 | 2–2 | — | 1/4 | 0.889
retention_changed | 1984 | 1784–2790 | 2–2 | — | 1/4 | 0.889
remembered_exit_ratio | 0.98815 | 0.96077–1.0317 | 3–3 | — | 0/3 | 0.667
outcome_mm_lag_1 | 0.81991 | 0.78811–0.85086 | 5–5 | — | 0/4 | 0.889
outcome_mm_lag_2 | 0.80696 | 0.7697–0.82978 | 6–6 | — | 1/4 | 0.889
outcome_mm_lag_3 | 0.19243 | 0.13307–0.19462 | 7–7 | — | 0/4 | 0.889
outcome_mm_lag_4 | 0.020091 | 0.0031405–0.035122 | 4–4 | — | 0/4 | 0.889
outcome_mm_lag_5 | 0.0017166 | -0.0017157–0.011824 | 4–4 | — | 0/4 | 0.889
outcome_mm_lag_6 | 0.0029413 | -0.0044947–0.016708 | 7–7 | — | 0/4 | 0.889
outcome_mm_lag_7 | -0.00080315 | -0.001584–0.0041976 | 2–2 | — | 0/4 | 0.889
outcome_mm_lag_8 | -0.0038177 | -0.0070993–0.0087913 | 2–2 | — | 0/4 | 0.889

Leave-one-out flag counts (each arm against the other eight; descriptive empirical comparison, not an independent null sample):

Arm | F | Comparable
---|---:|---:
C | 3 | 29
R01 | 11 | 29
R02 | 12 | 29
R03 | 7 | 29
R04 | 5 | 29
R05 | 6 | 29
R06 | 3 | 29
R07 | 5 | 29
R08 | 6 | 29

All other values, including eligible counts, visit sums and route novelty/rarity ranks, are derived descriptions and are never flagged.

### Traversal route novelty, rarity and recurrence
Counts are distinct typed routes; rates are per 100 completed traversal episodes. Reference rarity is leave-one-out among C and R01–R08, with occurrence in at most one of the other eight arms. It is not defined for M or G. Recurring rare routes were rare at first appearance, not merely rare now.

Arm | Novel | Novel / 100 | Reference-rare | Rare / 100 | Recurring rare this week
---|---:|---:|---:|---:|---:
C | 502 | 58.713 | 486 | 56.842 | 30
M | 486 | 56.643 | undefined | undefined | 0
G00 | 350 | 23.011 | undefined | undefined | 0
G01 | 224 | 10.191 | undefined | undefined | 0
G02 | 166 | 7.6994 | undefined | undefined | 0
G03 | 180 | 7.9858 | undefined | undefined | 0
G04 | 21 | 0.74574 | undefined | undefined | 0
G05 | 49 | 1.7364 | undefined | undefined | 0
G06 | 79 | 2.7719 | undefined | undefined | 0
G07 | 151 | 6.2345 | undefined | undefined | 0
R01 | 486 | 58.838 | 472 | 57.143 | 21
R02 | 505 | 60.552 | 501 | 60.072 | 28
R03 | 499 | 63.325 | 490 | 62.183 | 20
R04 | 496 | 63.508 | 477 | 61.076 | 18
R05 | 511 | 61.864 | 490 | 59.322 | 26
R06 | 497 | 61.358 | 479 | 59.136 | 21
R07 | 506 | 60.454 | 500 | 59.737 | 24
R08 | 478 | 59.379 | 472 | 58.634 | 28

C descriptive ranks among nine canonical memory-carrying arms:
- novel_count: 6–6.
- novel_per_100_episodes: 1–1.
- reference_rare_count: 5–5.
- reference_rare_per_100_episodes: 1–1.
- recurring_rare_this_week: 9–9.

C traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.7679 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.66794 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.67258 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

C recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44, 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[1,[[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44, 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[7,[[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

M traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.76572 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.6526 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.66248 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

G00 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.36735 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.29466 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.28857 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

G01 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.26385 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.1491 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.15341 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

G02 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.26734 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.13631 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.12812 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

G03 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.22423 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.13447 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.13044 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

G04 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.09715 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.029109 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.030459 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

G05 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.09481 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.039924 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.041047 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

G06 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.13133 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.060836 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.058817 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

G07 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.17253 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.094255 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.099946 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

R01 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.74775 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.66744 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.65232 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

R01 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44, 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44, 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R02 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.75558 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.66345 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.68402 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

R02 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44, 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44, 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44, 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44, 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R03 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.75099 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.67986 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.68196 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

R03 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.

R04 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.7696 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.68624 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.69204 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

R04 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44, 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44, 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44, 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R05 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.74297 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.67455 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.68123 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

R05 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R06 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.76825 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.65303 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.65824 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

R06 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44, 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44, 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44, 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

R07 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.7883 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.67691 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.65264 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

R07 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44, 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[7,[[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44, 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

R08 traversal-route Jensen–Shannon divergence:
- Against 2026-W42: 0.76561 bits; seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Against 2026-W43: 0.66073 bits; seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Against 2026-W44: 0.66892 bits; seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.

R08 recurring rare routes:
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[1,[[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[1,[[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44, 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[2,[[2,7,"syzygy","syzygy",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[4,[[4,5,"syzygy","syzygy",null,false],[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W42; recurrence weeks 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W45; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[5,[[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[5,[[5,4,"syzygy","syzygy",null,false],[4,5,"syzygy","syzygy",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[7,[[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,2,"syzygy","syzygy",null,false],[2,7,"syzygy","syzygy",null,false],[7,2,"syzygy","syzygy",null,false],[2,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"current","Sink",null,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,1,"current","Sink",null,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,2,"syzygy","syzygy",null,false],[2,3,"gate","Gt-03",3,false]]]`; first week 2026-W44; recurrence weeks 2026-W45; first seal `790e229a216dd584d85fe60557689e9827bb1e71702ba926764540457404cbf7`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[7,[[7,5,"current","Hold",null,false],[5,4,"syzygy","syzygy",null,false],[4,1,"gate","Gt-10",10,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,1,"syzygy","syzygy",null,false],[1,8,"syzygy","syzygy",null,false],[8,1,"syzygy","syzygy",null,false],[1,8,"syzygy","syzygy",null,false],[8,9,"gate","Gt-36",36,false]]]`; first week 2026-W43; recurrence weeks 2026-W45; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,1,"gate","Gt-01",1,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W43; recurrence weeks 2026-W44; first seal `c0d584503abc61978194701c86ca4a698fda1029ba287ca3ad30b0168a81adbe`.
- Typed route `[8,[[8,7,"current","Surge",null,false],[7,1,"gate","Gt-28",28,false],[1,7,"current","Surge",null,false],[7,5,"current","Hold",null,false],[5,6,"gate","Gt-15",15,false]]]`; first week 2026-W42; recurrence weeks 2026-W43, 2026-W44; first seal `d8139cc6022f57203eddea7d09727e6b62051f53b22fcbb78ce7d618682233ba`.

Full class-specific length distributions, routes, memory activity, occupancy and lag statistics for every arm are retained in JSON.

## Timing
Priority begins only at the verified seal timestamp in seal/receipt.json. No priority is claimed over inputs already available before that time.
Exploratory; no hypothesis test or calibrated anomaly claim.
References are deterministic transformations of the same inflow, not independent sources.
2/9 is conditional on exchangeability and no ties; many weekly flags are expected.
Outcome predictability is within-episode forward association, not evidence of external anticipation.
