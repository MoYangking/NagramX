#!/usr/bin/env python3
"""Apply an AGP 9 compatibility shim to a pinned Telegram Media3 git submodule.

Run after 'git submodule update --init --recursive', before Gradle. Changes are
only to the disposable submodule checkout; our base branch stays untouched.
This is intentionally explicit and strict rather than patching arbitrary code.
"""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
MEDIA = ROOT / "TMessagesProj_Modules" / "media"
EXPECTED_REV = "c430d207677071b1873f9f18266d55ec45722180"
ORIGINAL = "apply plugin: 'kotlin-android'"
REPLACEMENT = "// Kotlin is integrated in Android Gradle Plugin 9; do not apply kotlin-android again."

def main() -> None:
    if not (MEDIA / "core_settings.gradle").is_file():
        raise SystemExit("Telegram Media3 submodule missing: run git submodule update --init --recursive")
    actual = subprocess.check_output(
        ["git", "-C", str(MEDIA), "rev-parse", "HEAD"], text=True
    ).strip()
    if actual != EXPECTED_REV:
        raise SystemExit(f"Media3 gitlink mismatch: expected {EXPECTED_REV}, got {actual}")
    for relative in ("libraries/common_ktx/build.gradle", "libraries/ui_compose/build.gradle"):
        target = MEDIA / relative
        source = target.read_text(encoding="utf-8")
        count = source.count(ORIGINAL)
        if count == 1:
            target.write_text(source.replace(ORIGINAL, REPLACEMENT), encoding="utf-8")
            print("Patched AGP 9 Kotlin compatibility:", relative)
        elif count == 0 and REPLACEMENT in source:
            print("Already patched:", relative)
        else:
            raise SystemExit(f"Upstream file layout changed: {relative} (matches={count})")

if __name__ == "__main__":
    main()
