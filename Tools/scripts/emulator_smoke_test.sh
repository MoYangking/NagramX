#!/usr/bin/env bash
# Install the real x86_64 APK in Android 15; verify it stays alive and in the foreground.
# Save diagnostic evidence even when the app dies from a native signal.
set -Eeuo pipefail

PACKAGE=nu.gpu.nagram
OUT="${GITHUB_WORKSPACE:-$(pwd)}/emulator-diagnostics"
mkdir -p "$OUT"

collect_diagnostics() {
  set +e
  adb logcat -d -v threadtime > "$OUT/logcat.txt" 2>&1
  adb shell dumpsys activity activities > "$OUT/activities.txt" 2>&1
  adb shell dumpsys window windows > "$OUT/windows.txt" 2>&1
  adb shell dumpsys package "$PACKAGE" > "$OUT/package.txt" 2>&1
  adb shell dumpsys dropbox --print data_app_native_crash > "$OUT/native-crashes.txt" 2>&1
  adb exec-out screencap -p > "$OUT/screenshot.png" 2>/dev/null
  adb shell uiautomator dump /sdcard/nagramx-window.xml > "$OUT/uiautomator.txt" 2>&1
  adb pull /sdcard/nagramx-window.xml "$OUT/window.xml" >/dev/null 2>&1
  echo '--- NagramX app crash traces ---'
  grep -n -E -A 22 'FATAL EXCEPTION|Fatal signal|JNI DETECTED ERROR|UnsatisfiedLinkError|NoClassDefFoundError|Process: nu\.gpu\.nagram' "$OUT/logcat.txt" | tail -n 160 || true
  echo '--- Foreground window ---'
  grep -E 'mCurrentFocus|mFocusedApp' "$OUT/windows.txt" | tail -n 8 || true
}
trap collect_diagnostics EXIT

echo 'Generated APKs:'
find TMessagesProj/build/outputs/apk -type f -name '*.apk' -print
APK=$(find TMessagesProj/build/outputs/apk/debug -type f -name '*x86_64*.apk' -print -quit)
if [ -z "$APK" ]; then
  echo '::error::No x86_64 Debug APK was produced'
  exit 1
fi
if ! unzip -Z1 "$APK" | grep -q '^lib/x86_64/'; then
  echo '::error::Debug APK lacks the x86_64 native libraries'
  exit 1
fi

APKSIGNER="${ANDROID_HOME}/build-tools/36.0.0/apksigner"
"$APKSIGNER" verify --print-certs "$APK" | tee "$OUT/apk-signing-certificate.txt"

echo "Installing $APK"
adb devices -l
adb install -r "$APK"
adb shell pm list packages | grep -Fx "package:$PACKAGE"
adb shell am force-stop "$PACKAGE"
adb logcat -c
echo 'Launching default NagramX activity'
adb shell monkey -p "$PACKAGE" -c android.intent.category.LAUNCHER 1 | tee "$OUT/launch.txt"

initial_pid=''
for seconds in 12 12 16; do
  sleep "$seconds"
  pid=$(adb shell pidof "$PACKAGE" | tr -d '\r' || true)
  echo "After startup observation: pid=$pid"
  if [ -z "$pid" ]; then
    echo '::error::NagramX main process terminated during the 40-second startup test'
    exit 1
  fi
  if [ -n "$initial_pid" ] && [ "$pid" != "$initial_pid" ]; then
    echo '::error::NagramX restarted during the startup test'
    exit 1
  fi
  initial_pid="$pid"
done

FOCUS=$(adb shell dumpsys window | grep -E 'mCurrentFocus|mFocusedApp' || true)
echo "$FOCUS"
if ! echo "$FOCUS" | grep -Fq "$PACKAGE"; then
  echo '::error::NagramX Activity is not in the foreground'
  exit 1
fi

adb logcat -d -v threadtime > "$OUT/startup-logcat.txt"
python3 - "$OUT/startup-logcat.txt" "$PACKAGE" <<'PY'
import pathlib
import re
import sys

text = pathlib.Path(sys.argv[1]).read_text(errors="replace")
package = sys.argv[2]
for match in re.finditer(r"FATAL EXCEPTION:", text):
    block = text[match.start():match.start() + 3000]
    if "Process: " + package in block:
        print("::error::AndroidRuntime fatal exception in " + package)
        print(block[:2000])
        sys.exit(1)
for line in text.splitlines():
    if ("Fatal signal" in line or "JNI DETECTED ERROR" in line) and package in line:
        print("::error::Native crash: " + line)
        sys.exit(1)
print("PASS: package installed; launcher alive for 40s; foreground; no detected Java/JNI/native crash")
PY
adb exec-out screencap -p > "$OUT/launcher-after-40s.png"
