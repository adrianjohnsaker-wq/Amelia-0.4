# P3.18 — Developmental Competence Decomposition + Warp Developmental Gain

## Primary competence result

- PFM-mediated developmental competence gate: **PASS**
- FULL_OWN sentinel prevalence: 25/192
- BLANK sentinel prevalence: 1/192
- PFM_ONLY sentinel prevalence: 25/192
- DONOR_PFM sentinel prevalence: 26/192
- TENSOR_ONLY sentinel prevalence: 1/192
- FULL_OWN > BLANK paired sign p: 0.00000040
- PFM_ONLY > BLANK paired sign p: 0.00000040
- DONOR_PFM > BLANK paired sign p: 0.00000021

## Developmental transformation

- classification: **GLOBAL_HYSTERETIC_MATURITY**

| arm | sentinel lineages | raw p vs BLANK | Holm p | sufficient |
|---|---:|---:|---:|---:|
| STRAIN_HYSTERESIS | 32 | 0.00000000 | 0.00000000 | True |
| STRAIN_ONLY | 2 | 0.50000000 | 1.00000000 | False |
| HYSTERESIS_ONLY | 40 | 0.00000000 | 0.00000000 | True |
| RECENT_EVENTS_ONLY | 2 | 0.50000000 | 1.00000000 | False |
| FLAT_MAGNITUDE | 42 | 0.00000000 | 0.00000000 | True |
| SHUFFLED_STRAIN | 43 | 0.00000000 | 0.00000000 | True |

## Warp developmental gain

- promising for further development: **NO**
- canonical sentinel prevalence: 25/192
- Warp-gain sentinel prevalence: 23/192
- Warp-gain > canonical paired sign p: 1.00000000
- canonical mean developmental Warp transitions: 100.9740
- Warp-gain mean developmental Warp transitions: 100.9740
- absolute traffic difference: 0.0000
- mean bounded gain uses: 7.3854 of 8
- canonical mean frozen-panel breadth: 1.4896
- Warp-gain mean frozen-panel breadth: 1.4271

## Arm diagnostics

| arm | sentinel | panel breadth | hysteresis | strain mass | strain entropy | |bias| | tensor norm | dev Warp occupancy | post Warp occupancy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FULL_OWN | 25 | 1.4896 | 0.9263 | 3.1012 | 2.0603 | 0.0364 | 0.6051 | 0.7889 | 0.7812 |
| BLANK | 1 | 0.3073 | 0.0500 | 0.0000 | 0.0000 | 0.0000 | 0.3162 | 0.7889 | 0.7463 |
| PFM_ONLY | 25 | 1.4896 | 0.9263 | 3.1012 | 2.0603 | 0.0364 | 0.3162 | 0.7889 | 0.7812 |
| TENSOR_ONLY | 1 | 0.3073 | 0.0500 | 0.0000 | 0.0000 | 0.0000 | 0.6051 | 0.7889 | 0.7463 |
| DONOR_PFM | 26 | 1.4688 | 0.9263 | 3.1012 | 2.0603 | 0.0364 | 0.3162 | 0.7889 | 0.7951 |
| STRAIN_HYSTERESIS | 32 | 1.4427 | 0.9263 | 3.1012 | 2.0603 | 0.0248 | 0.3162 | 0.7889 | 0.7642 |
| STRAIN_ONLY | 2 | 0.7917 | 0.0500 | 3.1012 | 2.0603 | 0.0248 | 0.3162 | 0.7889 | 0.7642 |
| HYSTERESIS_ONLY | 40 | 1.0469 | 0.9263 | 0.0000 | 0.0000 | 0.0000 | 0.3162 | 0.7889 | 0.7463 |
| RECENT_EVENTS_ONLY | 2 | 0.6146 | 0.0500 | 0.0000 | 0.0000 | 0.0116 | 0.3162 | 0.7889 | 0.7640 |
| FLAT_MAGNITUDE | 42 | 1.0729 | 0.9263 | 3.1012 | 3.3219 | 0.0248 | 0.3162 | 0.7889 | 0.7520 |
| SHUFFLED_STRAIN | 43 | 1.1094 | 0.9263 | 3.1012 | 2.0603 | 0.0248 | 0.3162 | 0.7889 | 0.7445 |
| WARP_DEVELOPMENT_GAIN | 23 | 1.4271 | 0.9287 | 3.1050 | 2.0606 | 0.0365 | 0.6066 | 0.7889 | 0.7812 |

## Interpretation

P3.18 confirms that the P3.17 competence phenotype is substantially PFM-mediated and does not require lineage-specific memory content: own mature PFM and donor mature PFM both outperform a blank PFM while retaining at least 75% of full-process prevalence. The registered component classification is GLOBAL_HYSTERETIC_MATURITY. The bounded Warp-development gain does not meet its registered promotion criterion, so it remains experimental and the canonical Warp is unchanged.

## Provenance

- registration SHA-256: d7f0b62729ca8ee5ef68e177c6d729ab1b032ead380a38f698490ea48393b19e
- runner SHA-256: 752b174140b2c6d3c2e12030a89404bb255a1ad8da3fa244cb37aae98133390e
- Warp operator SHA-256: 7915789170f97819a8742c5f8cebdbed825cac6f92d9b343943b31a8b9fffa90
- frozen dynamic engine SHA-256: ac482882858c1e47f578523452eff0bc20aa82b5978299c9c8808ff6127c5cd6
- lineage archive SHA-256: 05ddc15e51b965655f29b4058e1b065a22fb6201d901b3bbbbe5d735ea095dae

The Warp implementation remains experimental unless the registered Warp endpoint is satisfied.
