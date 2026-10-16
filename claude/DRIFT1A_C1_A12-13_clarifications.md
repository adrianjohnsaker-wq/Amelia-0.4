# DRIFT-1A-C1 — A12/A13 pre-genesis clarifications

Status: approved specification; implementation and validation pending. Genesis disabled.

1. Channel B: one G1.1 tick per admitted NIST chain-2 pulse in pulse-index order. Missing indices are gap events, not ticks. Use unchanged variates(input_hex, tick).
2. Encoding: decode outputValue as exactly 64 bytes of case-insensitive hexadecimal. input_hex = lowercase SHA-256 of those bytes. Reference k = lowercase SHA-256 of UTF-8 "DRIFT-1A-C1-NIST-REF-k|" concatenated with the 32 input digest bytes.
3. Genesis B: all A fields plus chain index, P0 (first pulse at least ten minutes after genesis), certificateId, SHA-256 of pinned certificate, cipherSuite, specification version, measured freshness and gap rate. RFC 3161 seal before P0 timestamp, otherwise fail.
4. B genesis gates: latest pulse no older than 10 minutes; at least 95% of expected pulses present over prior seven days. Record both measurements even if failed. These are operator-chosen engineering reliability gates, not statistical thresholds.
5. CertificateId change: record incident and halt B pending operator amendment; do not halt A.
6. Channel B uses identical 29 declared statistics and definitions; validate that none is constant across its canonical memory-carrying arms.
7. G ensemble and Form contrast exist on A only.
8. Sealed anticipation: specify statistic(s), channel, direction, k future whole weeks, and fixed decision rule (default C outside reference range in stated direction in at least m of k weeks, with m fixed in note). RFC 3161 seal before window opens. Evaluate once and publish two separate outcomes: (a) whether the sealed rule passed and (b) C rank against eight leave-one-out reference results over the same window, including disagreement and failures. Nine-arm minimum attainable one-sided rank p = 1/9 (approximately 0.111); passing only promotes a hypothesis to a new registered experiment with separate genesis and enough reference arms, not confirmation.

Required before genesis: unchanged A11 simulation measurements, A12 Form/Memory/Signal report, NIST cryptographic positive and negative tests, gaps, certificate changes, deterministic replay, channel independence, operator review. No live activation authorised.
