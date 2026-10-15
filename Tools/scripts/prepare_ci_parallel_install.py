#!/usr/bin/env python3
"""Prepare a separate, CI-only NagramX APK that can be installed alongside NagramX.

The original repository's Gradle properties, manifest and Firebase config are
NOT changed in Git. This script is run only inside the isolated CI checkout.

Firebase config is duplicated solely to supply Google Services build resources.
It does not register this test package in Firebase; push and Google-linked
features require their own real Firebase client before production distribution.
"""
import copy
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL = "nu.gpu.nagram"
STANDALONE = "nu.gpu.nagram.moyangtest"

properties_path = ROOT / "gradle.properties"
properties = properties_path.read_text(encoding="utf-8")
regex = r"(?m)^APP_PACKAGE=([^\r\n]+)$"
matches = re.findall(regex, properties)
if matches != [ORIGINAL]:
    raise SystemExit(f"Expected exactly one original APP_PACKAGE={ORIGINAL}; found {matches}")
properties_path.write_text(
    re.sub(regex, "APP_PACKAGE=" + STANDALONE, properties, count=1),
    encoding="utf-8",
)

google_path = ROOT / "TMessagesProj/google-services.json"
google = json.loads(google_path.read_text(encoding="utf-8"))
clients = google.get("client", [])
source_clients = [
    c for c in clients
    if c.get("client_info", {}).get("android_client_info", {}).get("package_name") == ORIGINAL
]
if len(source_clients) != 1:
    raise SystemExit("Expected exactly one original NagramX Firebase client")
if any(
    c.get("client_info", {}).get("android_client_info", {}).get("package_name") == STANDALONE
    for c in clients
):
    raise SystemExit("CI-only package already exists in google-services.json")
clone = copy.deepcopy(source_clients[0])
clone["client_info"]["android_client_info"]["package_name"] = STANDALONE
clients.append(clone)
google_path.write_text(json.dumps(google, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

manifest_path = ROOT / "TMessagesProj/src/main/AndroidManifest.xml"
manifest = manifest_path.read_text(encoding="utf-8")
old_label = 'android:label="@string/NagramX"'
if manifest.count(old_label) != 1:
    raise SystemExit("Expected exactly one NagramX application label")
manifest_path.write_text(
    manifest.replace(old_label, 'android:label="NagramX Test"'),
    encoding="utf-8",
)

print(f"PASS: CI-only package: {STANDALONE}; release package remains {ORIGINAL}")
print("PASS: dedicated visible launcher label: NagramX Test")
print("INFO: cloned Firebase build config is NOT a separately registered Firebase app")
