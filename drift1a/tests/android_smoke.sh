#!/usr/bin/env bash
set -euo pipefail
adb install -r drift1a/app/build/outputs/apk/debug/app-debug.apk
adb logcat -c
adb shell am start -n com.amelia.driftg1/.MainActivity --ez g1_smoke true
for i in $(seq 1 120); do
  adb logcat -d -s DRIFT_G1:V AndroidRuntime:E > drift1a/android-smoke.log
  if grep -q 'G1_SMOKE_PASS' drift1a/android-smoke.log; then
    cat drift1a/android-smoke.log
    exit 0
  fi
  if grep -q 'FATAL EXCEPTION\|Operation failed' drift1a/android-smoke.log; then
    cat drift1a/android-smoke.log
    exit 1
  fi
  sleep 2
done
cat drift1a/android-smoke.log
exit 1
