#!/usr/bin/env bash
# Launch the real x86_64 Debug APK in an Android 15 emulator.
# No Telegram account credentials or login automation are required.
set -Eeuo pipefail

PACKAGE=nu.gpu.nagram
OUT="$GITHUB_WORKSPACE/emulator-diagnostics"
mkdir -p "$OUT"

collect_diagnostics() {
  set +e
  adb logcat -d -v threadtime > "$OUT/logcat.txt" 2>&1
  adb shell dumpsys activity activities > "$OUT/activities.txt" 2>&1
  adb shell dumpsys window windows > "$OUT/windows.txt" 2>&1
  adb shell dumpsys package "$PACKAGE" > "$OUT/package.txt" 2>&1
  adb exec-out screencap -p > "$OUT/screenshot.png" 2>/dev/null
  adb shell uiautomator dump /sdcard/nagramx-window.xml > "$OUT/uiautomator.txt" 2>&1
  adb pull /sdcard/nagramx-window.xml "$OUT/window.xml" >/dev/null 2>&1
  echo '--- App crash traces (when present) ---'
  grep -n -E -A 18 'FATAL EXCEPTION|Fatal signal|UnsatisfiedLinkError|NoClassDefFoundError|Process: nu\.gpu\.nagram' "$OUT/logcat.txt" | tail -n 180 || true
  echo '--- Foreground window ---'
  grep -E 'mCurrentFocus|mFocusedApp' "$OUT/windows.txt" | tail -n 8 || true
}
trap collect_diagnostics EXIT

APK=$(find TMessagesProj/build/outputs/apk -type f -name '*-x86_64.apk' -print -quit)
if [ -z "$APK" ]; then
  echo '::error::No x86_64 APK was produced'
  exit 1
fi

echo "Installing $APK"
adb devices -l
adb install -r "$APK"
adb shell pm list packages | grep -F "package:$PACKAGE"
adb shell am force-stop "$PACKAGE"
adb logcat -c
echo 'Launching the default NagramX launcher Activity'
adb shell monkey -p "$PACKAGE" -c android.intent.category.LAUNCHER 1 | tee "$OUT/launch.txt"
sleep 30

PID=$(adb shell pidof "$PACKAGE" | tr -d '\r' || true)
echo "App pid: $PID"
if [ -z "$PID" ]; then
  echo '::error::The NagramX main process terminated during startup'
  exit 1
fi

FOCUS=$(adb shell dumpsys window | grep -E 'mCurrentFocus|mFocusedApp' || true)
echo "$FOCUS"
if ! echo "$FOCUS" | grep -Fq "$PACKAGE"; then
  echo '::error::The NagramX Activity did not stay in the foreground'
  exit 1
fi

# Detect Java crashes even if the app restarted itself.
adb logcat -d -v threadtime > "$OUT/startup-logcat.txt"
python3 - "$OUT/startup-logcat.txt" "$PACKAGE" <<'PY'
import pathlib
import re
import sys

text = pathlib.Path(sys.argv[1]).read_text(errors="replace")
package = sys.argv[2]
for match in re.finditer(r"FATAL EXCEPTION:", text):
    block = text[match.start():match.start() + 2500]
    if "Process: " + package in block:
        print("::error::AndroidRuntime FATAL EXCEPTION in " + package)
        print(block[:2000])
        sys.exit(1)
# A native crash of the same package may be recorded by libc before Java dies.
for line in text.splitlines():
    if "Fatal signal" in line and package in line:
        print("::error::Native fatal signal: " + line)
        sys.exit(1)
print("PASS: launcher process alive, Activity foreground, no recorded app Java fatal exception")
PY
