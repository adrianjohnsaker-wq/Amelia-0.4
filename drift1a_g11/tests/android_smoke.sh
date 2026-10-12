#!/usr/bin/env bash
set -euo pipefail
adb install -r drift1a_g11/app/build/outputs/apk/debug/app-debug.apk
adb logcat -c
adb shell am start -n com.amelia.driftg11/.MainActivity --ez g11_smoke true
for i in $(seq 1 120); do
  adb logcat -d -s DRIFT_G11:V AndroidRuntime:E > drift1a_g11/android-smoke.log
  if grep -q 'G11_SMOKE_PASS' drift1a_g11/android-smoke.log; then
    cat drift1a_g11/android-smoke.log
    adb exec-out run-as com.amelia.driftg11 cat files/g11-smoke-evidence.zip > drift1a_g11/g11-smoke-evidence.zip
    adb exec-out screencap -p > drift1a_g11/g11-smoke-screen.png
    exit 0
  fi
  if grep -q 'FATAL EXCEPTION\|Operation failed' drift1a_g11/android-smoke.log; then
    cat drift1a_g11/android-smoke.log
    exit 1
  fi
  sleep 2
done
cat drift1a_g11/android-smoke.log
exit 1
