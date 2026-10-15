#!/usr/bin/env python3
"""Check Java/C++ Lottie JNI signatures and required legacy VoIP classes.

A Java native method may link by its mangled symbol even if the C++ parameter
list is wrong; that shifts JNI arguments and causes native SIGSEGV on startup.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
java = (ROOT / "TMessagesProj/src/main/java/org/telegram/ui/Components/RLottieNative.java").read_text()
cpp = (ROOT / "TMessagesProj/jni/lottie.cpp").read_text()
java_methods = dict(re.findall(
    r"\bprivate\s+static\s+native\s+\w+\s+(n\w+)\s*\((.*?)\)\s*;",
    java, flags=re.S,
))
cpp_methods = dict(re.findall(
    r"\bJNIEXPORT\s+\w+\s+JNICALL\s+"
    r"Java_org_telegram_ui_Components_RLottieNative_(n\w+)\s*\((.*?)\)\s*\{",
    cpp, flags=re.S,
))
type_map = {
    "String": "jstring",
    "String[]": "jobjectArray",
    "int": "jint",
    "int[]": "jintArray",
    "long": "jlong",
    "boolean": "jboolean",
    "Bitmap": "jobject",
}
errors = []
for name, java_args in java_methods.items():
    native_args = cpp_methods.get(name)
    if native_args is None:
        errors.append("No C++ implementation for " + name)
        continue
    declared = [p.strip().rsplit(" ", 1)[0] for p in java_args.split(",") if p.strip()]
    try:
        expected = [type_map[t] for t in declared]
    except KeyError as exc:
        errors.append(f"Unsupported Java JNI type in {name}: {exc}")
        continue
    actual_all = [p.strip().split()[0] for p in native_args.split(",") if p.strip()]
    if len(actual_all) < 2 or actual_all[0] != "JNIEnv" or actual_all[1] != "jclass":
        errors.append(name + ": JNI environment and class arguments are missing")
        continue
    actual = actual_all[2:]
    if actual != expected:
        errors.append(f"{name}: Java expects {expected}; C++ declares {actual}")

for name in cpp_methods:
    if name not in java_methods:
        errors.append("Stale C++ JNI export without Java declaration: " + name)

voip_root = ROOT / "TMessagesProj/src/main/java/org/telegram/messenger/voip"
for classname in ("AudioRecordJNI", "AudioTrackJNI", "JNIUtilities", "Resampler"):
    path = voip_root / (classname + ".java")
    if not path.is_file() or "package org.telegram.messenger.voip;" not in path.read_text():
        errors.append(f"Native VoIP startup prerequisite missing: {path.relative_to(ROOT)}")

if errors:
    for error in errors:
        print("FAIL: " + error, file=sys.stderr)
    sys.exit(1)

print(f"PASS: {len(java_methods)} Lottie JNI signatures agree with C++")
print("PASS: all four required legacy VoIP helper classes are present")
