# Amelia DRIFT-1A G1.1 for Android

Install **Amelia-DRIFT1A-G11.apk** from the **Amelia-DRIFT1A-G11-Android**
GitHub Actions artifact. Android 7+; ARM32, ARM64 and x86_64. The separate app
**Amelia DRIFT-1A G1.1** leaves the accepted G1 installation and its evidence intact.

1. Launch and wait for **G1.1 device parity: PASS** (512-tick reference check).
2. Keep seed **101**, press **New run**, then **Finish 512**.
3. Press **Verify run**. Expect **PASS: 512 ticks replayed exactly**.
4. Press **Export evidence**, save **Amelia-DRIFT1A-G11-evidence.zip**, and
   return that archive with a screenshot for the physical-device audit.

Every tick contains one graph move. Uniform entry occurs at tick start whenever
an episode begins, including tick zero. C/G retain history; M resets it before
selection. All three arms share ingress proposals and transition variates.
The fixed boundary is {0,3,6,9}. The display includes episode counts and Warp/Plex
outcomes; the archive contains full routes, effects, snapshots and hash chain.

No network permission, live beacon, language model, or registered live assay.
Run data saves atomically after each tick. New run preserves old session folders;
export the active run before switching because the UI exports the current run.
Signing uses configured repository secrets when present, otherwise a debug key.

Local validation: `python prepare.py` then `python -m unittest discover -s tests -v`.
Read PROTOCOL_AMENDMENT.md for event order, pairing and measurement conventions.
The frozen reference is evidence/g11_reference.json.gz, with a human-readable
summary in evidence/g11_reference_summary.json. AUDIT_AND_DECISIONS.md describes
the inherited G1 selector; the G1.1 amendment governs the new embodiment.
