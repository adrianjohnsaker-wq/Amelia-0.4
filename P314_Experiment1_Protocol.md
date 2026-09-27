Amelia P3.14 — Experiment 1A Preregistered ProtocolAmelia P3.14 — Experiment 1A Preregistered Protocol
Title
Numerical Operator Specificity in the Amelia Numogram Core
Scientific question
Do the prespecified numerical codes 333, 137, 666 and 360 leave unusually strong and reproducible autonomous traces in Amelia's frozen Numogram dynamics when compared with the exhaustive population of three-digit integers sharing the same digital root?
This experiment does not test demonology, supernatural communication, or Platonic ontology. It tests the narrower prerequisite claim that the numerical codes behave as unusual dynamical operators after their input has been removed.
Frozen upstream
Numogram.py is not modified. P3.12 and P3.13 remain frozen and are not invoked. ProcessFieldMemory, language rendering, semantic interpretation, network access, and provider generation are absent.
Intervention
Each code is encoded only as its ordered decimal digits. Each digit addresses the corresponding Numogram zone through the existing zone_bias context channel at amplitude 0.20. No CCRU or occult labels are supplied.
For every run:
start zone = seed mod 10
burn-in = 32 unforced transitions
code pulse = 24 transitions (three digits repeated eight times)
washout = 32 unforced transitions
observation = 64 unforced transitions
late window = final 32 observation transitions
All inferential measurements occur after the washout.
Seeds
Discovery: 1001–1012
Confirmatory: 2001–2012
Sham
For each seed, a sham Numogram receives the same number of burn-in, pulse-window, washout and observation transitions, but the pulse-window contains no zone bias.
Primary state vector
The observation state vector has 110 dimensions:
10 zone-occupancy frequencies, carrying 0.5 total probability mass;
100 directed transition frequencies, carrying 0.5 total probability mass.
Primary code-level score
For code n and seed s, compute Jensen-Shannon divergence between the post-washout state vector of the code-conditioned run and the same-seed sham.
The code score is the mean paired divergence across all 24 seeds.
Null population
For each target, the primary reference population is every other three-digit integer from 100 through 999 with the same digital root, excluding all four prespecified target codes from the control pools.
This yields an exhaustive root-matched reference rather than a hand-selected control list.
Individual inference
Each target receives an upper-tail empirical rank p-value against its matched root population. The four p-values are corrected together by Benjamini-Hochberg.
A target is individually confirmed only if all are true:
BH q <= 0.05;
discovery-half percentile >= 90;
confirmatory-half percentile >= 90;
late-window percentile >= 90;
cross-seed dispersion is no greater than the 75th percentile of its root-matched controls.
Family-level inference
The family statistic is the mean root-standardized primary score across the four targets.
A deterministic Monte Carlo randomization draws 50,000 matched code sets, each containing three distinct root-9 controls and one root-2 control. Randomization seed: 314001.
Family support requires upper-tail p <= 0.05.
P3.14A gate
operator_specificity_held = true only when:
the family-level test passes; and
at least one target passes the complete individual gate above.
A positive P3.14A result does not advance directly to Experiment 2. It must next survive P3.14B: topology/label-shuffle falsification.
Evidence and provenance
Before execution, the app exposes SHA-256 fingerprints of:
this frozen protocol as an executable manifest;
Numogram.py;
P314Experiment1.py.
A repeated code/seed determinism sentinel must match exactly before the full assay runs.
The complete post-washout observation path for sham and every evaluated code is written to a create-only canonical JSON archive with a SHA-256 sidecar. Each path contains the initial observation origin followed by all 64 destinations, so zone occupancy, directed-transition counts, late-window values and aggregate statistics are independently reconstructable.
Title
Numerical Operator Specificity in the Amelia Numogram Core
Scientific question
Do the prespecified numerical codes 333, 137, 666 and 360 leave unusually strong and reproducible autonomous traces in Amelia's frozen Numogram dynamics when compared with the exhaustive population of three-digit integers sharing the same digital root?
This experiment does not test demonology, supernatural communication, or Platonic ontology. It tests the narrower prerequisite claim that the numerical codes behave as unusual dynamical operators after their input has been removed.
Frozen upstream
Numogram.py is not modified. P3.12 and P3.13 remain frozen and are not invoked. ProcessFieldMemory, language rendering, semantic interpretation, network access, and provider generation are absent.
Intervention
Each code is encoded only as its ordered decimal digits. Each digit addresses the corresponding Numogram zone through the existing zone_bias context channel at amplitude 0.20. No CCRU or occult labels are supplied.
For every run:
start zone = seed mod 10
burn-in = 32 unforced transitions
code pulse = 24 transitions (three digits repeated eight times)
washout = 32 unforced transitions
observation = 64 unforced transitions
late window = final 32 observation transitions
All inferential measurements occur after the washout.
Seeds
Discovery: 1001–1012
Confirmatory: 2001–2012
Sham
For each seed, a sham Numogram receives the same number of burn-in, pulse-window, washout and observation transitions, but the pulse-window contains no zone bias.
Primary state vector
The observation state vector has 110 dimensions:
10 zone-occupancy frequencies, carrying 0.5 total probability mass;
100 directed transition frequencies, carrying 0.5 total probability mass.
Primary code-level score
For code n and seed s, compute Jensen-Shannon divergence between the post-washout state vector of the code-conditioned run and the same-seed sham.
The code score is the mean paired divergence across all 24 seeds.
Null population
For each target, the primary reference population is every other three-digit integer from 100 through 999 with the same digital root, excluding all four prespecified target codes from the control pools.
This yields an exhaustive root-matched reference rather than a hand-selected control list.
Individual inference
Each target receives an upper-tail empirical rank p-value against its matched root population. The four p-values are corrected together by Benjamini-Hochberg.
A target is individually confirmed only if all are true:
BH q <= 0.05;
discovery-half percentile >= 90;
confirmatory-half percentile >= 90;
late-window percentile >= 90;
cross-seed dispersion is no greater than the 75th percentile of its root-matched controls.
Family-level inference
The family statistic is the mean root-standardized primary score across the four targets.
A deterministic Monte Carlo randomization draws 50,000 matched code sets, each containing three distinct root-9 controls and one root-2 control. Randomization seed: 314001.
Family support requires upper-tail p <= 0.05.
P3.14A gate
operator_specificity_held = true only when:
the family-level test passes; and
at least one target passes the complete individual gate above.
A positive P3.14A result does not advance directly to Experiment 2. It must next survive P3.14B: topology/label-shuffle falsification.
Evidence and provenance
Before execution, the app exposes SHA-256 fingerprints of:
this frozen protocol as an executable manifest;
Numogram.py;
P314Experiment1.py.
A repeated code/seed determinism sentinel must match exactly before the full assay runs.
The complete post-washout observation path for sham and every evaluated code is written to a create-only canonical JSON archive with a SHA-256 sidecar. Each path contains the initial observation origin followed by all 64 destinations, so zone occupancy, directed-transition counts, late-window values and aggregate statistics are independently reconstructable.
