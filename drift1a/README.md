# Amelia DRIFT-1A G1 — Android

Download the `Amelia-DRIFT1A-G1-Android` artifact from the successful
**Amelia DRIFT-1A G1 Android APK** GitHub Actions run. Extract the ZIP and install
`Amelia-DRIFT1A-G1.apk`. Android 7+; includes 32-bit ARM, 64-bit ARM and x86_64.
The app has its own package `com.amelia.driftg1` and installs beside existing Amelia.
It needs no account, network permission or API key.

On launch, wait for **G1 device parity: PASS**. This checks the original canonical
source bytes and compares a 64-tick three-arm run with the build-time reference
(exact edge paths, numerical state tolerance 1e-12). A failed check leaves run
controls disabled.

1. Keep seed **101**, start zone **1**, and tap **New run**.
2. Use **1 tick**, **32 ticks**, or **Finish 512**. C, G and M receive shared
   deterministic synthetic inputs. State is saved after each complete tick.
3. Tap **Verify run** to replay all saved ticks exactly.
4. Tap **Export evidence** to save a ZIP with the manifest and complete tick records.

The active run resumes after reopening the app. **New run** retains older runs in
app-private storage but makes the new run active; export the current run before
starting another if you want its evidence accessible through the UI. Closing or
rotating while a batch is working may leave fewer ticks completed; reopening loads
the last complete atomic tick. Export before uninstalling or clearing app storage.

This is the accepted offline G1 engineering architecture. No live beacon experiment,
forecast service, LLM chat or autonomy claim is added. Canonical memory, frozen
rewired graph, and full-history-reset arms are labelled C/G/M. Each pilot is 512
ticks. The Governor and corrected retention rules remain as in the accepted package.

The workflow verifies `ACCEPTED_CORE_SHA256SUMS.txt` before building, runs the 28 G1
tests plus Android-storage tests, and then exercises the actual APK on an Android 9
x86_64 emulator. ARM-device acceptance is checked by the same parity test at launch.
It does not modify `amelia-1/` or OUTSIDE-2 ledgers/workflows.

Existing AMELIA signing secrets are used when present. Otherwise each CI build uses
an ephemeral Android debug key: a later build may not install over an earlier one.
Export evidence before replacing such an installation. The initial side-by-side
installation is unaffected.

Build locally: Python 3.11, JDK 17, Gradle 8.9 and Android SDK 34:

```sh
python prepare.py
python -m unittest discover -s tests -v
gradle :app:assembleDebug
```

Assets contain byte-exact G1 Python sources. The app copies them to private storage
before importing so canonical integrity checks read real source bytes and JSON.
Only packaging, UI, storage and synthetic-run orchestration are new Android code.
