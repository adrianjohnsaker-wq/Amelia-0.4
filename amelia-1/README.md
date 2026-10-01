# Android Amelia 1.0

Build specification: the programme's "Android Amelia 1.0: Build Specification" document.

## Milestone M0 (this commit)
- Committed Gradle project (AGP 8.7.3, Kotlin 1.9.24, Chaquopy 17.0.0, Python 3.11, SDK 34/24).
- Canonical Numogram modules copied byte-for-byte from the sealed programme
  (CanonicalNumogram.py f7c4e9a7…, NumogramDynamics.py dbc034e4…, NumogramInterface.py e2091e17…).
- `amelia_core.startup_check()` refuses to proceed unless module digests match
  `canonical_manifest.json` and the Numogram carries canonical digest df164ce7… (30 edges: 10 syzygy, 10 current, 10 gate).
- CI (`.github/workflows/amelia1.yml`): unit tests, offline check, build manifest, APK artifact `Amelia-1.0-M0`.

## Signing
No private signing key is committed. For stable install-over builds, set repository secrets
`AMELIA_KEYSTORE_B64`, `AMELIA_KEYSTORE_PASSWORD` and `AMELIA_KEY_ALIAS`; CI reconstructs the key only
inside the runner. If those secrets are absent, the project falls back to Android debug signing so CI can still
produce an APK. Switching from the fallback key to the stable key requires one uninstall, so configure the
stable key before developmental memory accumulates (before M2).

## Milestone M1
- `amelia_substrate.py`: episodic walker on the canonical graph with trace layers L1 (habit field),
  L2 (episodic archive with reconsolidation) and L3 (canalisation field). Memory acts only through
  ingress and passage: p(e) proportional to p_law(e) * (1 + beta * s(e)).
- Present state P and trace H are serialised and digested separately; import verifies both digests.
- With zero modulation every episode is identical to the sealed `NumogramInterface.episode`
  (checked for D0, D1, D2a, D2b, D3).
- Determinism rule: only +, -, *, / and math.sqrt in the dynamics, so CI and the phone agree bit for bit.
- CI computes a reference lineage (seed 90701, 200 episodes) and ships its digests; the app reproduces
  it on the phone and shows MATCH or MISMATCH.
- All constants are provisional until the M3 characterisation.

## Not yet built
Persistence, export and the inactive language layer (M2), characterisation (M3), sealed acceptance run (M4).
