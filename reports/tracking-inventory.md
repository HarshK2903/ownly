> **Hermes continuation (2026-11-05):** The decoder blocker described in this original native report is resolved. The byte-identical HBC has been analyzed through local Hermes MCP under REA process captures. Read [feature-flow-hermes.md](feature-flow-hermes.md), [hermes-tracking.md](hermes-tracking.md), and [hermes-evidence-index.md](hermes-evidence-index.md) for the new module/function findings, confidence levels and remaining gaps. The original native findings below remain preserved; statements about unavailable decoding describe the earlier pass.

# Tracking and telemetry inventory

Analyzed only the supplied base APK, package `com.ownly.customer`, version 2.0.7 (358), min SDK 24, target SDK 36. SHA-256: `5495bcf9cf03a7b956e253a2747c10f0222454b1e2106fa53213cd53dc708a05`. REA/JADX headless 0.7.1 reports 16885 classes and 2055 resources. Manifest evidence: `ev_25c9cfa3d80fcfda38c832fe4d5cb009c9b9103ad9dd7c5a94d2943f7697af6f`.

All findings are static artifact observations or reconstructions from decompiled bodies, not runtime observations. No application execution, production requests, or APK modifications were performed. Evidence IDs resolve to records in [rea-evidence.json](rea-evidence.json); [method-evidence.md](method-evidence.md) preserves inspected method bodies, prototypes and limitations. Decompiled display names can be aliases; obfuscated names below are preserved rather than renamed. Dynamic/reflective/JS calls are outside JADX reference coverage. Signatures and split APK contents were not verified.

## Verified native paths

| Exact bridge method | Observed call relationship and accepted data | What remains unknown |
|---|---|---|
| `com.clevertap.react.CleverTapModule.recordEvent(String,ReadableMap)` | `cleverTapModuleImpl.G1(name, map)`; `ev_d032b72b5e05525d8e79f14420eb4e04ca1804ed06c1251e1b6c020f0fb1516c` | Actual business event names, properties and triggers |
| `com.clevertap.react.CleverTapModule.onUserLogin(ReadableMap)` | `cleverTapModuleImpl.d1(map)`; `ev_70e66967e73bac45452e1cd345231c70763579dc232024cb1f78d0503faad259` | Actual profile fields; this is a telemetry identity bridge, not proof of Ownly authentication |
| `com.appsflyer.reactnative.RNAppsFlyerModule.logEvent` | Trims/rejects empty event name; RNUtil.toMap; requires current activity to call `AppsFlyerLib.getInstance().logEvent`; listener returns success/error callback. `ev_a60d8bc32d5e8fe0f905a0f8ff39c9eed545bd7528772dc53c28f74939e06fb9` | App event schedule, attribution identity and outbound requests |
| `io.invertase.firebase.analytics.ReactNativeFirebaseAnalyticsModule.logEvent` | Converts map to Bundle; calls module.z and settles promise on task completion. `ev_b152f9c18b2d94f3a9fe005d19aaca6cb837d07f661292c46698d9f3106cc1a9` | Actual named events and subsequent SDK transport |
| `com.incognia.reactnative.IncogniaModule.sendLoginEvent` | Builds LoginEvent with optional accountId, externalId, location, tag, properties and status; calls Incognia.sendLoginEvent. `ev_abb5282c8fd4ea23585c492378d785c846b448bbb05d34669a75925d0d58d262` | Whether/when Ownly invokes it and actual field values |
| `com.incognia.reactnative.IncogniaModule.sendPaymentEvent` | Builds PaymentEvent with optional identity, location, addresses, paymentValue, coupon, paymentMethods, storeId, tag, properties and status; calls Incognia.sendPaymentEvent. `ev_b923fe68a570c854d671b080f759bf6595eb6a422a36e4c3138066e900100d81` | Whether/when any checkout supplies these fields |
| `MainApplication.onCreate` | Calls CleverTap SDK helper before superclass; enables VERBOSE on displayed f0 logger. `ev_43f0d6293fbbeb1af5195240ae91d19c673015bdf0082030e8d82650b8755e6a` | Exact helper internals and runtime collection outcome |

These components are registered by `com.facebook.react.i.a()`. `ev_c687cd1c9935ea85e2d4ffd9efa3131b57f9b47160379144d0861a8f11354402`

## Manifest collection declarations

Direct manifest evidence `ev_25c9cfa3d80fcfda38c832fe4d5cb009c9b9103ad9dd7c5a94d2943f7697af6f`: CleverTap region `eu1`; default notification channels `CtRNS` and `transactional`; `firebase_analytics_collection_enabled=true`; `firebase_analytics_collection_deactivated=false`; `google_analytics_adid_collection_enabled=true`; `google_analytics_default_allow_ad_personalization_signals=true`; `firebase_crashlytics_collection_enabled=false`; `app_data_collection_default_enabled=true`; `firebase_messaging_auto_init_enabled=true`; `delivery_metrics_exported_to_big_query_enabled=false`; `firebase_messaging_notification_delegation_enabled=false`. These are packaged defaults, not observations of runtime overrides or consent.

Firebase measurement receiver/service/job service, Firebase messaging receiver/service, session lifecycle service and initialization providers are declared. CleverTapFileProvider is a file-sharing component, not evidence of an analytics upload. Manifest permission declarations include coarse/fine location, contacts, camera, microphone and notifications; permission presence alone establishes neither access nor exfiltration.

## Installed-package visibility

`com.ownly.customer.AndroidInstalledAppsCheckerModule.checkLaunchablePackages` (`ev_bc2c3cb8614cec694f3dbb8ed1d7aa6fa2cb1426ffac7476a9cb3d924efd1fe3`) accepts a caller-supplied list, filters nonempty strings, resolves launcher intents and returns launchablePackages, totalCount and launchableCount. Exceptions return an empty result. It does not itself transmit the list. Manifest queries include payment apps and other packages; they do not prove which JS callers ask to enumerate them or why.

## Coverage

SDK bridge capabilities and manifest defaults are answered. Event-trigger inventory, actual payloads, consent transitions, SDK destinations, transmission frequency and order-tracking telemetry are unresolved. No network traffic was generated or captured. Zero DEX references to CleverTapModule.recordEvent (`ev_297f49deda5bd306e3d6a8855b0d8d1c1f4830263083bfc78cd5b0568feb137f`) cannot establish absence of JS callers.
