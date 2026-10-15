# Telegram official 13.0.2 upstream port — staging report

**Status: INCOMPLETE — do not publish APKs or label this fork 13.0.2 yet.**

This is a machine-generated safe first pass, not a full Telegram release migration.
NagramX-specific files and customizations are preserved where changes conflict.

- Official baseline: [12.10.0](https://github.com/DrKLO/Telegram/commit/4e1a61eca6c9b6ee3aa9c35cf8c70554750f2439)
- Latest pinned upstream: [13.0.2](https://github.com/DrKLO/Telegram/commit/f32ffeec763f0bdbf4bec25b52d654f77bff733d)
- Ported scope: Telegram's Java sources, Android resources, and app assets
- Pending manual integration: all native/JNI, Gradle/build files, manifest, submodules, and any conflicts below
- The original NagramX application ID, version, and signing configuration are deliberately unchanged

## First-pass file results

- added: 174
- clean_merges: 116
- clean_replacements: 166
- outside_scope: 11428
- removed: 4820
- conflicts requiring manual review: 46

## Conflicting files (first 300)

- TMessagesProj/src/main/java/com/google/android/exoplayer2/BaseRenderer.java — NagramX changed or removed upstream-deleted file
- TMessagesProj/src/main/java/com/google/android/exoplayer2/NoSampleRenderer.java — NagramX changed or removed upstream-deleted file
- TMessagesProj/src/main/java/com/google/android/exoplayer2/Player.java — NagramX changed or removed upstream-deleted file
- TMessagesProj/src/main/java/com/google/android/exoplayer2/ext/ffmpeg/FfmpegLibrary.java — NagramX changed or removed upstream-deleted file
- TMessagesProj/src/main/java/com/google/android/exoplayer2/extractor/wav/WavExtractor.java — NagramX changed or removed upstream-deleted file
- TMessagesProj/src/main/java/com/google/android/exoplayer2/mediacodec/MediaCodecInfo.java — NagramX changed or removed upstream-deleted file
- TMessagesProj/src/main/java/com/google/android/exoplayer2/util/MimeTypes.java — NagramX changed or removed upstream-deleted file
- TMessagesProj/src/main/java/com/google/android/exoplayer2/util/UnknownNull.java — NagramX changed or removed upstream-deleted file
- TMessagesProj/src/main/java/org/telegram/messenger/ApplicationLoader.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/messenger/CodeHighlighting.java — NagramX changed or removed upstream-deleted file
- TMessagesProj/src/main/java/org/telegram/messenger/Emoji.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/messenger/FileLog.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/messenger/ImageLoader.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/messenger/LocaleController.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/messenger/MediaController.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/messenger/MusicBrowserService.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/messenger/SharedConfig.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/messenger/TelegramMediaSession.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/messenger/TelegramQRCodeWriter.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/messenger/voip/VoIPController.java — NagramX changed or removed upstream-deleted file
- TMessagesProj/src/main/java/org/telegram/messenger/voip/VoIPPreNotificationService.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/messenger/voip/VoipAudioManager.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/tgnet/ConnectionsManager.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/tgnet/TLParseException.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/ActionBar/ActionBar.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/ActionBar/BaseFragment.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/Cells/ChatActionCell.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/Cells/ChatMessageCell.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/ChatActivity.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/Components/ChatActivityEnterView.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/Components/ChatAttachAlert.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/Components/ChatAvatarContainer.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/Components/FilterTabsView.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/Components/ItemOptions.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/Components/PasscodeView.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/Components/RLottieDrawable.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/Components/TranscribeButton.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/Components/VideoPlayer.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/Components/spoilers/SpoilersTextView.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/DialogsActivity.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/LaunchActivity.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/LoginActivity.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/MainTabsActivity.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/PeerColorActivity.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/SettingsActivity.java — three-way content conflict or binary file
- TMessagesProj/src/main/java/org/telegram/ui/Stories/UploadingDotsSpannable.java — three-way content conflict or binary file

## Paths outside the automated scope (11428 files; first 100)

- .gitmodules
- Dockerfile
- README.md
- TMessagesProj/build.gradle
- TMessagesProj/emoji/FORMAT.md
- TMessagesProj/emoji/base_builder.py
- TMessagesProj/emoji/build_emoji_pack.py
- TMessagesProj/emoji/emoji.stats.json
- TMessagesProj/emoji/optimizer_core.py
- TMessagesProj/emoji/optimizer_visual.py
- TMessagesProj/emoji/quality_seams.py
- TMessagesProj/emoji/requirements.txt
- TMessagesProj/emoji/research_results.json
- TMessagesProj/emoji/test_java_loader.py
- TMessagesProj/emoji/verification.json
- TMessagesProj/emoji/verify_emoji_pack.py
- TMessagesProj/jni/CMakeLists.txt
- TMessagesProj/jni/TgNetWrapper.cpp
- TMessagesProj/jni/audio.c
- TMessagesProj/jni/boringssl/CMakeLists.txt
- TMessagesProj/jni/boringssl/LICENSE
- TMessagesProj/jni/boringssl/cmake/OpenSSLConfig.cmake
- TMessagesProj/jni/boringssl/cmake/go.cmake
- TMessagesProj/jni/boringssl/cmake/paths.cmake
- TMessagesProj/jni/boringssl/crypto/abi_self_test.cc
- TMessagesProj/jni/boringssl/crypto/aes/aes.cc
- TMessagesProj/jni/boringssl/crypto/asn1/a_bitstr.cc
- TMessagesProj/jni/boringssl/crypto/asn1/a_bool.cc
- TMessagesProj/jni/boringssl/crypto/asn1/a_d2i_fp.cc
- TMessagesProj/jni/boringssl/crypto/asn1/a_dup.cc
- TMessagesProj/jni/boringssl/crypto/asn1/a_gentm.cc
- TMessagesProj/jni/boringssl/crypto/asn1/a_i2d_fp.cc
- TMessagesProj/jni/boringssl/crypto/asn1/a_int.cc
- TMessagesProj/jni/boringssl/crypto/asn1/a_mbstr.cc
- TMessagesProj/jni/boringssl/crypto/asn1/a_object.cc
- TMessagesProj/jni/boringssl/crypto/asn1/a_octet.cc
- TMessagesProj/jni/boringssl/crypto/asn1/a_strex.cc
- TMessagesProj/jni/boringssl/crypto/asn1/a_strnid.cc
- TMessagesProj/jni/boringssl/crypto/asn1/a_time.cc
- TMessagesProj/jni/boringssl/crypto/asn1/a_type.cc
- TMessagesProj/jni/boringssl/crypto/asn1/a_utctm.cc
- TMessagesProj/jni/boringssl/crypto/asn1/asn1_lib.cc
- TMessagesProj/jni/boringssl/crypto/asn1/asn1_par.cc
- TMessagesProj/jni/boringssl/crypto/asn1/asn1_test.cc
- TMessagesProj/jni/boringssl/crypto/asn1/asn_pack.cc
- TMessagesProj/jni/boringssl/crypto/asn1/f_int.cc
- TMessagesProj/jni/boringssl/crypto/asn1/f_string.cc
- TMessagesProj/jni/boringssl/crypto/asn1/internal.h
- TMessagesProj/jni/boringssl/crypto/asn1/posix_time.cc
- TMessagesProj/jni/boringssl/crypto/asn1/tasn_dec.cc
- TMessagesProj/jni/boringssl/crypto/asn1/tasn_enc.cc
- TMessagesProj/jni/boringssl/crypto/asn1/tasn_fre.cc
- TMessagesProj/jni/boringssl/crypto/asn1/tasn_new.cc
- TMessagesProj/jni/boringssl/crypto/asn1/tasn_typ.cc
- TMessagesProj/jni/boringssl/crypto/asn1/tasn_utl.cc
- TMessagesProj/jni/boringssl/crypto/base64/base64.cc
- TMessagesProj/jni/boringssl/crypto/base64/base64_test.cc
- TMessagesProj/jni/boringssl/crypto/bcm_support.h
- TMessagesProj/jni/boringssl/crypto/bio/bio.cc
- TMessagesProj/jni/boringssl/crypto/bio/bio_mem.cc
- TMessagesProj/jni/boringssl/crypto/bio/bio_test.cc
- TMessagesProj/jni/boringssl/crypto/bio/connect.cc
- TMessagesProj/jni/boringssl/crypto/bio/errno.cc
- TMessagesProj/jni/boringssl/crypto/bio/fd.cc
- TMessagesProj/jni/boringssl/crypto/bio/file.cc
- TMessagesProj/jni/boringssl/crypto/bio/hexdump.cc
- TMessagesProj/jni/boringssl/crypto/bio/internal.h
- TMessagesProj/jni/boringssl/crypto/bio/pair.cc
- TMessagesProj/jni/boringssl/crypto/bio/printf.cc
- TMessagesProj/jni/boringssl/crypto/bio/socket.cc
- TMessagesProj/jni/boringssl/crypto/bio/socket_helper.cc
- TMessagesProj/jni/boringssl/crypto/blake2/blake2.cc
- TMessagesProj/jni/boringssl/crypto/blake2/blake2_test.cc
- TMessagesProj/jni/boringssl/crypto/blake2/blake2b256_tests.txt
- TMessagesProj/jni/boringssl/crypto/bn/bn_asn1.cc
- TMessagesProj/jni/boringssl/crypto/bn/convert.cc
- TMessagesProj/jni/boringssl/crypto/bn/exponentiation.cc
- TMessagesProj/jni/boringssl/crypto/buf/buf.cc
- TMessagesProj/jni/boringssl/crypto/buf/buf_test.cc
- TMessagesProj/jni/boringssl/crypto/bytestring/asn1_compat.cc
- TMessagesProj/jni/boringssl/crypto/bytestring/ber.cc
- TMessagesProj/jni/boringssl/crypto/bytestring/bytestring_test.cc
- TMessagesProj/jni/boringssl/crypto/bytestring/cbb.cc
- TMessagesProj/jni/boringssl/crypto/bytestring/cbs.cc
- TMessagesProj/jni/boringssl/crypto/bytestring/internal.h
- TMessagesProj/jni/boringssl/crypto/bytestring/unicode.cc
- TMessagesProj/jni/boringssl/crypto/chacha/asm/chacha-armv4.pl
- TMessagesProj/jni/boringssl/crypto/chacha/asm/chacha-armv8.pl
- TMessagesProj/jni/boringssl/crypto/chacha/asm/chacha-x86.pl
- TMessagesProj/jni/boringssl/crypto/chacha/asm/chacha-x86_64.pl
- TMessagesProj/jni/boringssl/crypto/chacha/chacha.cc
- TMessagesProj/jni/boringssl/crypto/chacha/chacha_test.cc
- TMessagesProj/jni/boringssl/crypto/chacha/internal.h
- TMessagesProj/jni/boringssl/crypto/cipher/aead_test.cc
- TMessagesProj/jni/boringssl/crypto/cipher/asm/aes128gcmsiv-x86_64.pl
- TMessagesProj/jni/boringssl/crypto/cipher/asm/chacha20_poly1305_armv8.pl
- TMessagesProj/jni/boringssl/crypto/cipher/asm/chacha20_poly1305_x86_64.pl
- TMessagesProj/jni/boringssl/crypto/cipher/cipher_test.cc
- TMessagesProj/jni/boringssl/crypto/cipher/derive_key.cc
- TMessagesProj/jni/boringssl/crypto/cipher/e_aesctrhmac.cc

## Validation gate

Before merging, manually resolve all conflicts, integrate JNI/Gradle/manifest
and establish that Gradle builds and the NagramX feature regression tests pass.
Keep this change in a draft pull request until those gates pass.

## Follow-up integration commits (after the first-pass report)

The first-pass statistics above are a snapshot, not the current totals.

- [2e8a611](https://github.com/MoYangking/NagramX/commit/2e8a61182685e2ce8a1641a30b793313ad530783): restore the NagramX legacy ExoPlayer source subtree, which its custom media classes still depend on.
- [a6a0932](https://github.com/MoYangking/NagramX/commit/a6a0932e95771c70c1e1547dfe12b4ff2a962bb3): manually resolve five conflicts while preserving NagramX custom QR codes, spoiler preferences, media-session behavior, and TL parse handling.
- [c38aeb8](https://github.com/MoYangking/NagramX/commit/c38aeb8051a2d984f89ea12cd35b4242b185455c): add the official pinned Telegram Android 13.0.2 Media3 git submodule (Arseny271/media), five Gradle module dependencies, and WebKit; remove the duplicate upstream ResLottieMeta source while preserving NagramX's existing Lottie metadata generator.
- [881d9f3](https://github.com/MoYangking/NagramX/commit/881d9f3fe6e6fb69daeabc9a12899e94cf540998): manually reconcile three more conflicts covering the official Bluetooth routing, vibration handling, and media browsing.
- [17707fe](https://github.com/MoYangking/NagramX/commit/17707fe7454c666c1fb1fb834b0e13dfdf66d1bc): create the Gradle 9.x intermediate Media3 project directory.

This reduces the 46 originally reported content conflicts to **38 yet to be reconciled**, before build-detected integration problems. The original deletion count of 4,820 also predates the legacy source restoration.

**Still incomplete:** source compatibility, 38 unresolved conflict files, official native/JNI/CMake and submodule changes beyond Media3, the Android manifest, APK builds, and real-device feature tests. Neither a successful first-pass GitHub Action nor the official upstream commit SHA is evidence of a working NagramX 13.0.2 APK. Do not merge/release until validated.
