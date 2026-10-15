# NagramX test APK: installation and signing

The Telegram 13.0.2 integration is **work in progress** and should not be shipped as a release.

## Which APK should I install?

- The PR's `NagramX-Standalone-ARM64` GitHub Actions artifact contains an experimental `NagramX-Standalone-...-arm64-v8a-debug.apk`.
- Its application ID is `nu.gpu.nagram.moyangtest`; the Android launcher label is `NagramX Test`.
- The original NagramX ID is **unchanged in Git**: `nu.gpu.nagram`. The official Telegram Android ID is normally `org.telegram.messenger`.
- The standalone APK is intended to install alongside both applications without sharing their installation identity or data. You will need to sign in again; it does not restore previous local chats, secrets, or settings.

## Why did the original test APK say signature conflict?

Earlier PR CI steps stripped release signing from Debug builds, which made Android use a temporary Debug keystore. Different CI executions could therefore sign the same `nu.gpu.nagram` ID with different certificates. Android refuses to upgrade a package signed by a different key. The user-visible uninstall may also leave that package installed in another Android profile/user.

The new CI Debug signing cache helps keep *new* CI certificates consistent, but it cannot reconstruct a prior signing private key or fix a same-ID application installed under an unrelated certificate.

## Limitations

- The isolated application identity is applied by `Tools/scripts/prepare_ci_parallel_install.py` **only in CI checkouts**. Production/release sources and signing configurations are untouched.
- The script temporarily duplicates the original Google Services resource entry under the test ID so Gradle can build. This does **not** create an authentic Firebase Android application registration; push notifications, Google-linked services, and anything tied to the original package signature may not work. Production use requires registering the new package with the owner's Firebase project or choosing a proper release signing setup.
- Passing the x86_64 Android 15 launch smoke test checks only install, foreground, 40-second process survival, and observed startup crashes. It does not cover account login, message sync, calls, or complete NagramX features.

## If installation still fails

On Windows with Android platform-tools, the exact error can be obtained with:

```powershell
adb shell pm list users
adb shell pm list packages -u | findstr /i nagram
adb install -r "C:\path\to\NagramX-Standalone-arm64-v8a-debug.apk"
```

Report the exact `INSTALL_FAILED_*` code. `INSTALL_FAILED_UPDATE_INCOMPATIBLE` means a signature mismatch for the same install identity; a `CONFLICTING_PROVIDER`, `SHARED_USER_INCOMPATIBLE`, or other code requires a different fix. Don't clear application data or remove other Telegram apps before checking the error.
