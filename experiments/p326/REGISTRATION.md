# P3.26 — Numogram Graph-Field Morphogenetic Uptake

**Registration status:** sealed by this file's commit. Source acquisition must begin only after this commit timestamp plus 90 seconds.

## Question

Does a state-conditioned Numogram graph-field alter Amelia's realized transition paths, leave post-withdrawal traces, and condition subsequent uptake through ProcessFieldMemory (PFM), beyond fixed, degree-preserving rewired, zone-label-shuffled, and no-field controls?

This assay tests the operational coupling of Numogrammatic relations and Amelia's morphogenetic dynamics. A result describes the implemented interface. It does not establish the ontology or source of any pattern.

## Frozen substrate and source

- Repository: adrianjohnsaker-wq/Amelia-0.4.
- P3.16 Python substrate and P3.17 lineage/rewire machinery are reused without modification.
- FullNumogram.py SHA-256: b6edbe76ab4929e93c01059fb56cef900effa9bca1cec78d0039eafb8fbebdf8.
- experiments/p316/DynamicNumogram.py SHA-256: ac482882858c1e47f578523452eff0bc20aa82b5978299c9c8808ff6127c5cd6.
- experiments/p317/run.py SHA-256: 1a8fd1961b897ec970c7d6987bd9f3502c82221f13bace683563e4dafdb820c3.
- Independent source: League of Entropy drand default mainnet, chain hash 8990e7a9aaed2ffed73dbd7092123d6f289930540d7651336225dc172e51b2ce, public key 868f005eb8e6e4ca0a47c8a77ceaa5309a47978a7c71bc5cce96366b5d7a569937c529eeda66c7293784a9402801af31, genesis 1595431050, period 30 seconds.
- drand-client version 1.4.2; verification enabled; both api.drand.sh and drand.cloudflare.com must return byte-identical normalized records.

## Prospective input selection

Let Tseal be the Unix timestamp of the commit that first adds this registration. Set T0=Tseal+90 seconds. Acquire the first default-chain round scheduled at or after T0 and the next 23 consecutive rounds.

For each verified randomness value, derive one ten-component call vector using the P3.26-FIELD-v1 SHA-256 domain-separated mapping in experiments/p326/graph_field.py. The mapping receives only beacon randomness and packet index; no Numogram state, lineage, output, label, or prior result is an input. Center each vector to mean zero and normalize to unit L2 norm.

## Lineages and development

- 96 fresh lineages, seeds 3260000–3260095.
- Use the frozen P3.17 make_tapes(seed), 128-step developmental tape, and registered shock_process(seed).
- TRAIN: lineage indices 0–47. HELD-OUT: indices 48–95.
- Every arm for one lineage starts from an exact clone of the same post-development, post-shock canonical substrate state.
- Calls and their order are identical across every lineage and arm.

## Call, field, and withdrawal

Each of 24 packets is processed sequentially within each arm:

1. Read the current substrate, deformation, and PFM state.
2. Propagate the signed field over the arm's specified mapping graph for three layers, with layer weights 1, 1/2, and 1/4. Each layer uses outgoing directed gate conductance proportional to flux × permeability × (1-resistance); the live canonical and rewired arms multiply conductance by the frozen state factor clamp[0.75,1.25] of 1 + 0.25 Δactivation + 0.10 ΔPFM-bias + 0.05 Δdeformation.
3. Compute the field gradient for each currently available canonical substrate exit as field[target]-field[source]. Scale the vector of all gate gradients to L2 norm 0.05 in log-flux units. For each open substrate gate, temporarily set flux to base_flux × exp(delta).
4. Execute exactly one ordinary P3.16 step(None). Restore every flux value in a finally block before observation.
5. Execute 24 ordinary autonomous step(None) transitions with no field. PFM continues to record and feed back in all arms except PFM-feedback-muted.
6. Record the full withdrawal path and PFM state before and after each encounter.

If a propagated field is flat, its edge-gradient budget is zero and the zero-effect call remains in the data. No exposure is removed or resampled.

## Arms

- CANONICAL_LIVE: current canonical graph and current substrate/PFM-conditioned conductance.
- CANONICAL_FIXED: canonical mapping graph frozen from the post-shock starting state; no state conditioning in field propagation.
- R00–R23: 24 P3.17 degree-preserving rewired mapping graphs, seeds 3263000–3263023; rewires affect the field mapping only. The receiving substrate's transition graph remains canonical in every arm.
- RELATION_SHUFFLED: canonical mapping graph after a single seeded non-identity permutation of the ten input-zone labels (seed 3264000); substrate labels remain unchanged.
- NO_FIELD: compute and archive the canonical-live field and equal-budget gradient, but do not apply it.
- PFM_FEEDBACK_MUTED: canonical-live field; same recorded history, but disable PFM bias consumption throughout this arm. Secondary diagnostic.

All arms use the same 24 input packets, field layers, gradient calculation, one-call duration, 24-step withdrawal, and lineages. The no-field arm computes the same field and gradient but discards it. No arm supplies a desired zone, named form, semantic message, or terminal state.

## Registered observations and exploratory analysis

This is a registered exploratory mapping assay, not a confirmatory pass/fail test. The signature catalogue is open; no zone-specific form or entity signature is named in advance.

The frozen runner will report, per arm and packet:

- full selected transitions and 24-step post-withdrawal paths;
- 10×10 transition-frequency vectors and their paired difference from NO_FIELD for the same lineage and packet;
- novel directed transitions relative to each lineage's developmental transition history;
- field and flux deltas, selected exits, zone activations, deformation, PFM bias, PFM strain, and hysteresis before/after;
- persistence across withdrawal intervals 1–8, 9–16, and 17–24;
- candidate 2–5-zone path motifs discovered in packets 0–11 and their frequency across held-out lineages and packets 12–23;
- per-arm distributions, paired contrasts, TRAIN/HELD-OUT descriptives, and bootstrap 95% intervals resampling lineages.

A candidate motif enters the discovery list only if it occurs in at least 12 encounter paths across at least 8 distinct TRAIN lineages in packets 0–11. This is a catalogue threshold, not evidence of an entity. Each listed candidate is scored without alteration in HELD-OUT lineages and packets 12–23. All candidates, including those that do not recur, remain in the archive.

No single descriptive statistic can establish mind, agency, communication, or a source in the Outside. The result will preserve candidate patterns for subsequent query-contingent and cross-context discrimination. Interpretation may use project Numogram vocabulary only after raw traces and scoring are locked.

## Provenance, archive, and stopping

- All result records are append-only JSONL with a SHA-256 head chain; the final compressed atlas is committed with compact reports and checksums.
- Raw verified beacon records, input vectors, arm assignment, code digests, lineage IDs, complete paths, PFM transitions, and per-record digests are archived.
- Branch execution is single-run and non-cancellable. A second run is prohibited unless the first fails before any verified beacon round is acquired; a post-acquisition failure is preserved and requires a new phase decision.
- Stop if flux is not restored, any arm receives a different packet sequence, provenance or chain validation fails, an invariant violation is detected, or Governor integrity falls below 85.
- No linguistic or metaphysical interpretation is included in the scorer.
