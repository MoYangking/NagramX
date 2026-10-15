#!/usr/bin/env python3
"""Safely port clean Telegram Android changes into the NagramX staging branch.

Run only in an isolated GitHub Actions checkout. This script intentionally does
not modify gradle.properties, JNI, Gradle build files, or the Android manifest.
An incomplete port must never be advertised as a released Telegram version.
"""
from __future__ import annotations

import os
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

BASE = os.environ["TELEGRAM_BASE_SHA"]
LATEST = os.environ["TELEGRAM_LATEST_SHA"]
REPORT_PATH = Path("docs/telegram-upstream-sync.md")
SCOPE = (
    "TMessagesProj/src/main/java/",
    "TMessagesProj/src/main/res/",
    "TMessagesProj/src/main/assets/",
)


def run_git(*args: str, missing_ok: bool = False) -> bytes | None:
    result = subprocess.run(["git", *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        return result.stdout
    if missing_ok:
        return None
    raise RuntimeError(f"git {' '.join(args[:4])}: {result.stderr.decode('utf-8', 'replace')[:1000]}")


def content_at(ref: str, path: str) -> bytes | None:
    return run_git("show", f"{ref}:{path}", missing_ok=True)


def safe_filename(name: str) -> bool:
    parts = Path(name).parts
    return bool(parts) and ".." not in parts and not name.startswith("/") and "\\" not in name


def merge_text(ours: bytes, ancestor: bytes, theirs: bytes) -> bytes | None:
    try:
        ours.decode("utf-8")
        ancestor.decode("utf-8")
        theirs.decode("utf-8")
    except UnicodeDecodeError:
        return None
    if any(b"\x00" in data for data in (ours, ancestor, theirs)):
        return None
    with tempfile.TemporaryDirectory(prefix="telegram-merge-") as tmp:
        a, b, c = (Path(tmp) / part for part in ("ours", "base", "theirs"))
        a.write_bytes(ours)
        b.write_bytes(ancestor)
        c.write_bytes(theirs)
        result = subprocess.run(
            ["git", "merge-file", "-p", "-L", "NagramX", "-L", "Telegram-base",
             "-L", "Telegram-13.0.2", str(a), str(b), str(c)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        return result.stdout if result.returncode == 0 else None


def main() -> None:
    raw = run_git("diff", "--name-status", "--no-renames", "-z", BASE, LATEST)
    assert raw is not None
    fields = raw.decode("utf-8", "surrogateescape").rstrip("\x00").split("\x00")
    if len(fields) % 2:
        raise RuntimeError("Unexpected git diff --name-status -z output")

    stats = Counter()
    conflicts: list[tuple[str, str]] = []
    skipped: list[str] = []

    for offset in range(0, len(fields), 2):
        status, filename = fields[offset : offset + 2]
        if not safe_filename(filename):
            raise RuntimeError(f"Unsafe path in upstream diff: {filename!r}")
        if not filename.startswith(SCOPE):
            skipped.append(filename)
            stats["outside_scope"] += 1
            continue
        if status not in ("M", "A", "D", "T"):
            conflicts.append((filename, f"unsupported change type: {status}"))
            continue

        base = content_at(BASE, filename)
        latest = content_at(LATEST, filename)
        ours = content_at("HEAD", filename)
        dest = Path(filename)

        # Git submodules and symlinks must be handled explicitly by a maintainer.
        mode = run_git("ls-tree", LATEST, "--", filename)
        if mode and (mode.startswith(b"160000 ") or mode.startswith(b"120000 ")):
            conflicts.append((filename, "submodule or symbolic link"))
            continue
        if ours == latest:
            stats["already_synced"] += 1
            continue
        if base is None and latest is not None:
            if ours is not None:
                conflicts.append((filename, "new upstream file collides with NagramX file"))
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(latest)
            stats["added"] += 1
        elif base is not None and latest is None:
            if ours == base:
                if dest.is_file():
                    dest.unlink()
                stats["removed"] += 1
            else:
                conflicts.append((filename, "NagramX changed or removed upstream-deleted file"))
        elif base is not None and latest is not None:
            if ours is None:
                conflicts.append((filename, "upstream update to file removed by NagramX"))
                continue
            if ours == base:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(latest)
                stats["clean_replacements"] += 1
            else:
                merged = merge_text(ours, base, latest)
                if merged is None:
                    conflicts.append((filename, "three-way content conflict or binary file"))
                    continue
                if merged != ours:
                    dest.write_bytes(merged)
                    stats["clean_merges"] += 1
                else:
                    stats["already_merged"] += 1
        else:
            conflicts.append((filename, "unsupported upstream diff state"))

    report = [
        "# Telegram official 13.0.2 upstream port — staging report",
        "",
        "**Status: INCOMPLETE — do not publish APKs or label this fork 13.0.2 yet.**",
        "",
        "This is a machine-generated safe first pass, not a full Telegram release migration.",
        "NagramX-specific files and customizations are preserved where changes conflict.",
        "",
        f"- Official baseline: [12.10.0](https://github.com/DrKLO/Telegram/commit/{BASE})",
        f"- Latest pinned upstream: [13.0.2](https://github.com/DrKLO/Telegram/commit/{LATEST})",
        "- Ported scope: Telegram's Java sources, Android resources, and app assets",
        "- Pending manual integration: all native/JNI, Gradle/build files, manifest, submodules, and any conflicts below",
        "- The original NagramX application ID, version, and signing configuration are deliberately unchanged",
        "",
        "## First-pass file results",
        "",
        *[f"- {k}: {v}" for k, v in sorted(stats.items())],
        f"- conflicts requiring manual review: {len(conflicts)}",
        "",
        "## Conflicting files (first 300)",
        "",
        *[f"- {p} — {reason}" for p, reason in conflicts[:300]],
    ]
    if len(conflicts) > 300:
        report.append(f"- ... and {len(conflicts) - 300} more conflicts")
    report.extend([
        "",
        f"## Paths outside the automated scope ({len(skipped)} files; first 100)",
        "",
        *[f"- {p}" for p in skipped[:100]],
        "",
        "## Validation gate",
        "",
        "Before merging, manually resolve all conflicts, integrate JNI/Gradle/manifest",
        "and establish that Gradle builds and the NagramX feature regression tests pass.",
        "Keep this change in a draft pull request until those gates pass.",
        "",
    ])
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report[:25]))


if __name__ == "__main__":
    main()
