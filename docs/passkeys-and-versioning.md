# Telegram passkeys and upstream versioning

## Why an official Telegram passkey cannot be used in this fork

Android Credential Manager passkeys are scoped to a relying party (the website)
and authorized Android application identities, not just to the physical phone.
The app identity includes **both the application package and its signing
certificate**, which the relying party must recognize through Digital Asset
Links and any applicable server-side policy.

The standalone GitHub Actions APK uses `nu.gpu.nagram.moyangtest` and a Debug
certificate. The original NagramX package is `nu.gpu.nagram`. Neither identity
is the official Telegram app `org.telegram.messenger` signed with Telegram's
release certificate. Having a passkey available in the official app therefore
does **not** grant this fork access to that passkey. Changing only the package
name to `org.telegram.messenger`, or putting `https://...` in a WebAuthn
request's origin field, does not grant the required trust. It can also conflict
with an already-installed official Telegram app.

Telegram's upstream `BuildVars.java` explicitly says passkey support is for
official application identities. Consequently the fork does not advertise a
passkey login or creation action until an authorized identity is available.

The repository's `PasskeysController.java` was also modified to synthesize
WebAuthn `clientDataJSON`, supply an artificial `clientDataHash` and override
`origin`. Those fields must come from the credential provider rather than be
forged by the client. They have been returned to the normal upstream flow for
any *future* correctly authorized builds. **This does not make official keys
available to this fork.**

To support official Telegram passkeys legitimately, Telegram must explicitly
authorize the actual package name and signing certificate (and any applicable
API identity). This requires the relying party's cooperation; the Android
project or GitHub Actions alone cannot make it happen.

**Use another supported login flow** (phone verification or QR approval with
another already signed-in Telegram client). Logging into Telegram Web using a
passkey does not automatically log this separate Android app in.

## Versioning after Telegram 13.0.2 sync

Source metadata is `APP_VERSION_NAME=13.0.2` and
`APP_VERSION_CODE=7175`, matching Telegram 13.0.2's Android version
properties. `TMessagesProj/build.gradle` now derives the APK's `versionCode`
from `APP_VERSION_CODE` instead of retaining NagramX's older hardcoded
`1261`; the APK's `versionName` already uses `APP_VERSION_NAME`.

The PR build validates the actual output APK's application ID, versionCode,
and versionName with Android build tools before publishing, and records these
values in `apk-identity.txt`. After each future upstream sync, update both
properties to the version actually incorporated.

Version metadata does not mean all Telegram 13.0.2 features are fully ported;
the NagramX sync branch remains work in progress. Upgrading the installed APK
also requires an unchanged application ID and compatible signing certificate.
