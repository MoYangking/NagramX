#!/usr/bin/env python3
"""Source-level regression guard for NagramX functionality during Telegram sync.

This is deliberately a *static* gate, not a substitute for compiling and
testing on Android devices. Keep it on the staging PR until runtime QA passes.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
CHECKS = {
    "TMessagesProj/src/main/java/org/telegram/tgnet/ConnectionsManager.java": [
        "NekoXConfig.currentAppId()", "RequestFlagDownloadByteBudget",
        "native_sendRequest(currentAccount, buffer.address",
    ],
    "TMessagesProj/jni/TgNetWrapper.cpp": [
        "native_moveToDatacenter", "native_onHostNameResolved",
        '"(IJIIIZII)V"',
    ],
    "TMessagesProj/jni/tgnet/Defines.h": [
        "#define MAX_ACCOUNT_COUNT 10", "#define PROXY_CONNECTIONS_COUNT 10",
    ],
    "TMessagesProj/jni/tgnet/ConnectionSocket.cpp": [
        "AF_INET6", "isProxyIpv6", "onHostNameResolved(",
    ],
    "TMessagesProj/src/main/java/org/telegram/ui/ActionBar/ActionBar.java": [
        "NekoConfig.actionBarDecoration", "NaConfig.INSTANCE.getCustomTitleUserName",
    ],
    "TMessagesProj/src/main/java/org/telegram/ui/Components/FilterTabsView.java": [
        "NekoConfig.hideAllTab.Bool()", "if (defaultTab != null)",
    ],
    "TMessagesProj/src/main/java/org/telegram/ui/Components/TranscribeButton.java": [
        "TranscribeHelper.useTranscribeAI", "TranscribeHelper.sendRequest",
    ],
    "TMessagesProj/src/main/java/org/telegram/ui/Components/RLottieDrawable.java": [
        "NekoConfig.",
    ],
    "TMessagesProj/src/main/java/org/telegram/messenger/TelegramQRCodeWriter.java": [
        "ic_launcher_nagram_blue",
    ],
    "TMessagesProj/src/main/java/org/telegram/ui/Components/ItemOptions.java": [
        "onLongClickListener", "CharSequence subtext",
    ],
    "TMessagesProj/src/main/java/org/telegram/ui/Components/ChatAvatarContainer.java": [
        "LastSeenHelper", "avatarOptionsMenuItem", "isCentered()",
    ],
    "TMessagesProj/build.gradle": [
        "APP_PACKAGE", "NagramX", "signingConfigs.release",
    ],
}
errors = []
for relative, markers in CHECKS.items():
    file = ROOT / relative
    if not file.is_file():
        errors.append("Missing file: " + relative)
        continue
    text = file.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            errors.append(f"Missing expected customization in {relative}: {marker}")
if errors:
    print("\n".join("FAIL: " + msg for msg in errors), file=sys.stderr)
    sys.exit(1)
print(f"PASS: {sum(map(len, CHECKS.values()))} NagramX integration markers found in {len(CHECKS)} files")
