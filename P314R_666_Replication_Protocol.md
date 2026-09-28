Amelia P3.14R — Prospective 666 Fresh-Seed Replication
Antecedent result
P3.14A failed its preregistered four-code operator-specificity gate.
Within that failed family test, 666 nevertheless produced an exploratory candidate signal:
overall percentile: 100.0
upper rank p: 0.0102
BH q: 0.0408
original discovery-half percentile: 100.0
original confirmatory-half percentile: 41.2
late-window percentile: 94.8
stability criterion: held
The sealed P3.14A evidence digest is:
fda4127884f25d679fe563a7a70d56b63d5e33ff295fd53c38ef241bb002a391
Because the original split replication failed, 666 is treated here only as a newly generated hypothesis. No original seed is reused.
Primary question
Does code 666 produce an unusually strong, persistent, and cross-cohort replicable post-washout Numogram trace relative to the same exhaustive root-9 control universe used in P3.14A?
Secondary mechanistic question
Is the effect of 666 unusually dependent on the Numogram's seeded regime?
Two prespecified secondary tests address this:
code×seed interaction dispersion — whether the seed-specific 666 effect varies more than expected from the root-9 control population after removal of additive code and seed effects;
start-zone structure — whether mean effect varies unusually strongly across the ten predeclared starting zones (seed mod 10).
The two secondary p-values are Holm-corrected. These endpoints cannot rescue a failed primary replication.
Frozen Numogram intervention
No change is made to Numogram.py.
Each three-digit code is encoded as its ordered decimal digits. Each digit addresses the corresponding Numogram zone through the existing zone_bias channel with amplitude 0.20.
Per run:
start zone: seed mod 10
burn-in: 32 unforced transitions
pulse: 24 transitions (three digits repeated eight times)
washout: 32 unforced transitions
observation: 64 unforced transitions
late window: final 32 observation transitions
All inferential measurements occur after pulse removal and washout.
Fresh seeds
Forty new seeds are locked:
3001–3040
Two confirmatory cohorts are fixed before execution:
Cohort A: 3001–3020
Cohort B: 3021–3040
Each cohort contains every seed mod 10 start-zone exactly twice.
Sham
For every seed, a same-seed sham Numogram executes the same number of transitions without a numerical zone-bias pulse.
Root-9 reference population
The reference population exactly preserves the P3.14A root-9 null pool:
all three-digit integers with digital root 9, excluding 333, 360 and 666.
This yields 97 control codes. The replication therefore evaluates 98 codes in total: 97 controls plus target 666.
Primary state vector and score
The 110-dimensional state vector assigns:
0.5 probability mass to 10-zone occupancy frequencies;
0.5 probability mass to 100 directed transition frequencies.
For each seed, the effect is the Jensen–Shannon divergence between the post-washout code-conditioned state vector and its same-seed sham.
The primary code score is the mean effect over all 40 seeds.
Primary replication gate
666 replicates only if all conditions hold:
overall upper-tail empirical rank p <= 0.05 against the 97 controls;
Cohort A percentile >= 90;
Cohort B percentile >= 90;
late-window percentile >= 90;
cross-seed state dispersion is no greater than the 75th percentile of the control-code dispersion distribution.
No BH correction is needed for the primary endpoint because 666 is the single prespecified replication target.
A successful primary replication proceeds only to P3.14B, a separate Numogram topology/label-shuffle falsification. It does not proceed directly to Experiment 2.
Secondary seed-regime analysis
For every code and seed, let E[c,s] be the same-seed JSD effect.
Code×seed interaction dispersion
Using the 97 controls to estimate the additive seed baseline, compute:
R[c,s] = E[c,s] - mean_s(E[c,*]) - mean_control(E[*,s]) + grand_control_mean
The standard deviation of R[c,*] is the code×seed interaction dispersion.
666 is rank-tested against the 97 control interaction dispersions.
Start-zone structure
For each code, group its 40 seed effects by seed mod 10, producing ten group means. The variance of those ten means is compared with the same statistic for the 97 controls.
The interaction and start-zone p-values are Holm-corrected as a two-test secondary family.
Execution discipline
The run is checkpointed, but intermediate inferential statistics are never displayed.
Progress may show only:
sham count;
code count;
percentage complete;
checkpoint state.
The code evaluation order is deterministically shuffled with schedule seed 666314.
A resumed run is permitted only when the protocol digest, Numogram source hash, experiment source hash, protocol-file hash, and build revision all match the checkpoint.
Evidence
The final create-only evidence archive contains:
locked protocol and digest;
antecedent P3.14A evidence digest;
build-time Numogram and experiment source hashes;
all 40 sham observation paths;
all 98 × 40 code-conditioned observation paths;
primary replication statistics;
seed-specific effects;
secondary seed-regime statistics;
final evidence SHA-256.
No result from this stage should be described as evidence for an external, Platonic, or supernatural communication channel. The present stage tests only Numogram operator replication and seed-conditioned dynamics.
