# Ownly reverse-engineering investigation progress

Saved on 2026-11-05 as a continuation handoff. This document consolidates existing findings; no APK analysis was rerun to produce it. Existing files were preserved.

## Resume status

The manifest, native startup chain, generated React Native package registration, selected native bridges, archive inventory and extraction are complete within their documented static scope. The overall investigation is **partially complete**: business workflows in Hermes bytecode have not been reconstructed. Resume at the Hermes decoding boundary, not at manifest inspection or native package discovery.

Original instructions: `rea-task.md`. Project: `/home/bugulnoz/research/ownly`. Target: `/home/bugulnoz/research/ownly/apk/com.ownly.customer/base.apk`, package `com.ownly.customer`, version 2.0.7 (358), min SDK 24, target SDK 36. APK SHA-256: `5495bcf9cf03a7b956e253a2747c10f0222454b1e2106fa53213cd53dc708a05`.

Use REA MCP for the investigation. Do not modify the APK or production services, invent class names/endpoints, or describe static observations as runtime behavior. Preserve existing reports and evidence. Runtime execution, service requests, app installation, live traffic capture and production interactions were not performed in this investigation.

## Saved files and provenance

| Path | Purpose / completed work |
|---|---|
| `rea-task.md` | User-authorized task and requested report scope |
| `apk/com.ownly.customer/base.apk` | Only application APK analyzed; split contents and signatures not verified |
| `jadx-headless-mcp-0.7.1-all.jar` | Existing supplied JADX provider JAR, not an application artifact |
| `reports/AndroidManifest.xml` | Complete decoded manifest from saved REA package evidence |
| `reports/architecture.md` | Framework, entry points, component inventory and coverage limits |
| `reports/startup-flow.md` | Pairip wrapper, provider declarations, MainApplication, activity and host chain |
| `reports/tracking-inventory.md` | Analytics/risk bridges and manifest collection defaults |
| `reports/workflows.md` | Per-workflow partial/unresolved status and Hermes blocker |
| `reports/method-evidence.md` | All inspected method bodies, DEX prototypes, overloads, representation and fallback markers |
| `reports/evidence-index.md` | Exact evidence ID → operation → selector index |
| `reports/rea-evidence.json` | Canonical portable REA bundle: 93 records; use instead of relying on server retention |
| `reports/package-overview.txt` | Pre-existing report, preserved; not used as independent proof in this pass |
| `reports/progress.md` | This complete handoff |

REA extracted the APK to `/tmp/rea-extracted-2b8cff02-ec20-459a-a730-ff8af5693d7d`. This temporary tree is not a durable handoff artifact and may disappear; extraction provenance is preserved in the canonical bundle. `assets/index.android.bundle` is 20,053,204 bytes; SHA-256 `b6f904c723cf894e03bf2e6bb0400015c288b78ad855f1eb825965d1654511a3`. Header bytes `c61fbc03c103191f62000000` identify Hermes bytecode version 98 (supplementary local byte inspection). Bundle hash was verified locally against REA extraction evidence. No APK filename ending `.map` was found in the local ZIP filename check; external maps remain possible.

Additional asset filenames observed: `assets/defaultArcusConfig.json`, `assets/juspay/app/config.json`, `pkg.json`, `release_config.json`, `resources.json`, and `assets/juspay/config.json`, `hyper_asset_metadata.json`, `juspay_assets.json`, `manifest.json`, `sdk_config.json`, `unified_config.json`, `payments/in.juspay.hyperpay/ownly.json`. These were inventoried, not semantically analyzed. Native-library and resource inventory does not establish their behavior.

REA archive inventory: 2,056 occurrences (root included), 2,055 edges, 1,839 nodes, no recorded integrity contradictions; inventory covers ZIP central-directory entries, not signing-block/non-entry bytes. Android/JADX reports 16,885 classes and 2,055 resources.

## Tool and session state

REA MCP was available and used directly. JADX headless provider version 0.7.1; bridge version 7; Java reported 21.0.12.1; worker_count 1; heap_limit_mib 1820. Provider JAR SHA-256 `6e5eacf500b64292bfb73c49797c1958f6ee44646e43e868039ae7feb573ff75`; bridge SHA-256 `e5044a8312dd0731f53af3f095508b3e5cff54df6b971c95d4305e2f39b4fa30`. Exact provenance and limitations are in each record.

Operations completed: inspect_android_package, search_android_classes, inspect_android_class, inspect_android_method, trace_android_references; archive open_binary, inspect_artifact/inventory_artifact, extract_artifact; evidence export. REA `close_binary({})` returned successfully at the end. No native analysis session remains intentionally open. Do not assume same-session retained IDs survive a client restart; use the saved JSON.

Host shell sandbox startup failed with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; approved escalated shell commands were used for local reads/writes and report verification. This was a host sandbox issue, not a REA provider failure. No REA configuration repair or software installation was performed.

Input-contract lessons already resolved: get_evidence_bundle filters require `detail: "summary"`; complete returns the full canonical bundle. Host method `getPackages` was not found: actual obfuscated selector is `com.ownly.customer.MainApplication.a.l`. Do not repeat these invalid calls. Broad tool replies can be duplicated/truncated by the client; full records are saved in JSON. Select method overload indices from existing class metadata (HyperSdkReactModule.process: 0 private HyperServices/String overload, 1 public String bridge).

## Exact next steps — pending work only

1. Read this handoff, `workflows.md` and the saved evidence index. Reuse all completed results below. Do not rerun the manifest, archive inventory, package searches, or already inspected methods unless the target changes or a specific evidence defect is found.
2. Resolve a **Hermes v98-compatible decoder** or matching original source/source map. The connected REA catalog had no Hermes decoder, and local commands `hbc-disassembler`, `hermes-dec`, `hbcdump`, `hermes`, `hbc-decompiler` were absent. Do not feed binary bytecode to REA's UTF-8 JavaScript graph analyzer. Before acquiring tooling, check whether a newly available REA capability or existing compatible local decoder/source has been supplied; record decoder version and compatibility. Do not install unrelated providers or rerun setup to fix a format limitation.
3. Decode the exact hash-bound packaged bundle into a new analysis directory. Reuse the existing extraction if present. If it is gone, recover only the required asset into a new path from the original APK, preserve its digest and record the extraction. Keep input bytes untouched. Record function IDs, bytecode offsets, module IDs and original symbols where present; label reconstructed names explicitly and never substitute invented Java class names for JS functions.
4. Trace root registration for `consumerapp` and navigation setup. Resolve concrete auth/home/search/restaurant/cart/checkout/tracking/address screens and their callers. Record registration-to-handler call relationships with decoder/source evidence.
5. Trace login: input validation → OTP request → OTP verification → response handling → session/token storage → authenticated navigation, plus refresh/logout. Distinguish the already known SMS-retrieval bridge from server authentication. Recover endpoints, HTTP methods and headers only from actual call sites; do not contact endpoints.
6. Trace discovery/search: selected location/address → serviceability → restaurant queries, pagination/sorting/filtering → restaurant/menu view; search input/debounce → request → results → navigation. Determine state ownership and error handling.
7. Trace cart/checkout: add/remove/change quantity/options → totals/persistence/restaurant switch → cart validation/order creation → payment JSON construction → Juspay/Cashfree/UPI selection → result callback → server confirmation/order success. Distinguish successful intent launch from confirmed payment. Establish retry/idempotency behavior only from code.
8. Trace order tracking: order ID acquisition → actual polling/socket/push subscription mechanism → status mapping → screen updates → terminal-state cleanup. Registered Firebase/Notifee components alone do not answer this.
9. Trace location/address handling and analytics at business call sites. Resolve geocoding, address persistence, serviceability payloads and consent. For each event record exact name, trigger, fields, identity linkage and SDK destination only where established; keep Incognia risk events separate from authentication success.
10. Continue native code only where a specific unresolved edge requires it: `com.hotupdater.H.o()` and its returned object's `a()` for final bundle selection; unresolved unqualified helper owners `f0`, `h`, `k`, `w0` and host-added package aliases; manager/callback implementations for location; payment result callbacks/launch delegates; OTP task listeners. Use existing class metadata and targeted REA inspect_android_class/method or trace_android_references, not broad repeat searches. A downloaded update may differ from this packaged version; never infer installed state from the APK alone.
11. If static decoding cannot resolve a question, record the precise residual unknown. Any future runtime plan must respect the existing no-production-modification constraint and use an appropriately isolated, explicitly scoped environment; no runtime setup or execution was done or requested by this save-progress turn.
12. Append new evidence and update reports without destroying the current canonical bundle: export a new versioned evidence file first, preserve old IDs, link new conclusions to exact methods/offsets, and keep observed/derived/inferred distinctions. Validate referenced IDs, hashes and coverage. Mark unresolved workflow rows complete only when their business call chains have actually been traced.

## Confirmed findings and unresolved issues, consolidated verbatim

The following saved report contents make this handoff self-contained. They are prior results, not newly repeated analysis. All embedded report links are relative to `reports/`.

---

## Saved report: architecture.md

# Ownly Android architecture

Analyzed only the supplied base APK, package `com.ownly.customer`, version 2.0.7 (358), min SDK 24, target SDK 36. SHA-256: `5495bcf9cf03a7b956e253a2747c10f0222454b1e2106fa53213cd53dc708a05`. REA/JADX headless 0.7.1 reports 16885 classes and 2055 resources. Manifest evidence: `ev_25c9cfa3d80fcfda38c832fe4d5cb009c9b9103ad9dd7c5a94d2943f7697af6f`.

All findings are static artifact observations or reconstructions from decompiled bodies, not runtime observations. No application execution, production requests, or APK modifications were performed. Evidence IDs resolve to records in [rea-evidence.json](rea-evidence.json); [method-evidence.md](method-evidence.md) preserves inspected method bodies, prototypes and limitations. Decompiled display names can be aliases; obfuscated names below are preserved rather than renamed. Dynamic/reflective/JS calls are outside JADX reference coverage. Signatures and split APK contents were not verified.

## Framework and entry points — answered

Observed: manifest application is `com.pairip.application.Application`, not MainApplication directly. Its constructor invokes `com.ownly.customer.MainApplication.<init>` and its declaration extends that class. `ev_7ec903b5debf5aec762bc6f00199bf417e7806a4f4eccfe33a1b7fa501692021` `ev_4aaebc6ed8bca4789e06f062599975668c117132b89cc30e81887d693dc8a6f0`

Default launcher is enabled alias `com.ownly.customer.MainActivityDefaultIcon`, targeting `com.ownly.customer.MainActivity`. Diwali and Staging icon aliases are declared disabled. MainActivity extends ReactActivity, returns React component `consumerapp` from `b0()`, and host `i()` returns Metro entry `index`. `ev_25c9cfa3d80fcfda38c832fe4d5cb009c9b9103ad9dd7c5a94d2943f7697af6f` `ev_b0b721bc80f6352bcba4616ff4046fe77c8184f537ca1e6ff80e6ce58c0e6a72` `ev_3274c189887357f0804a6bede9aa0ae0170696b006a19dbff219106ad7e2d45c` `ev_47521fae078ab6d16f593981947c908da3633fb1c4cbaebbcbb666404a78c582`

React Native is directly established by ReactActivity, React hosts and package registration. `com.ownly.customer.MainApplication.onCreate()` calls `DefaultNewArchitectureEntryPoint.load()` after SoLoader initialization. Hermes bytecode is packaged in `assets/index.android.bundle` (see workflow report for header identity). This is not a native Android screen-per-workflow app. `ev_43f0d6293fbbeb1af5195240ae91d19c673015bdf0082030e8d82650b8755e6a`

## Component inventory

| Area | Exact class and method | Reconstructed behavior / relationship | Evidence boundary |
|---|---|---|---|
| Networking | `com.facebook.react.modules.network.NetworkingModule.sendRequest` → `sendRequestInternalReal` | Receives caller-provided URL, HTTP method, headers, body and response options; builds requests using OkHttp types. Errors return through RN network response helpers. | `ev_1a1757f3295e0109f971027b04df648377a0c787b7a2995275feb5c5032ac48e` `ev_037e7e55d9404382e22725cf6a634906f9a47d1c7045d5f18bb5ae5e797623b7`; no Ownly endpoints or auth-header policy recovered |
| Authentication support | `com.faizal.OtpVerify.OtpVerifyModule.getOtp` → `requestOtp` | Delegates to Google Play phone API task and attaches completion/failure listeners. | `ev_afea8348aa5617024c29447762c5aac501c11719b9c621672f23673923a5d867` `ev_7383605032d6083277edc6e218fc31188a5719999a29b81c3d573554b33c7002`; OTP retrieval is not backend verification |
| Local relational storage | `com.nozbe.watermelondb.WMDatabaseBridge.initialize` → `WMDatabaseDriver` | Tagged connections; reports ok, schema_needed or migrations_needed; rejects other errors. Class also declares query/batch/schema/migration methods. | `ev_fbfc2b14a75737ae9edee7a67f68e50fcac59a5ef35801bc931bf826d7580d47` `ev_58b79aacf3372e477a57a2ea413673a232f9a019bdd796e6cf186a9f95ee244f`; app database names and tables unresolved |
| Key/value storage | `com.margelo.nitro.mmkv.HybridMMKVPlatformContext.getBaseDirectory` | Resolves app files directory plus `/mmkv`; throws without React context. | `ev_2dbaac96844f780d110f305d5fbe8089496efbb418c014fd3b7fed499cf36b50`; no token/cart keys or encryption settings established |
| Navigation | `com.ownly.customer.MainActivity.onNewIntent` | Forwards intent to superclass then updates activity intent. RN screens/gesture packages are registered by generated package list. | `ev_55dd3c02665953b74b208ede8037630fd7fa9a16e04be9f20abe97dbb92a2de8` `ev_c687cd1c9935ea85e2d4ffd9efa3131b57f9b47160379144d0861a8f11354402`; actual JS route graph unresolved |
| Location | `com.reactnativecommunity.geolocation.GeolocationModule.getCurrentPosition`, `startObserving`, `requestAuthorization` | Permission-aware location manager delegation and observation. | `ev_b1fb39db89da9414d46fd5e24c4b72e56077b2c4df6a859653aea75d6c0a90f9` `ev_f28983344a8dfe3024aeafb3286c9c8df109ecc1216edd6a328081121229fc94` `ev_32888ab7fde6438d23be47918f984aecfceb62189eaddc88deb5de18399619d6` |
| Payments | `in.juspay.hypersdkreact.HyperSdkReactModule.process(String)` → private `process(HyperServices,String)` | Parses JSON and delegates to HyperServices with current activity and launch/permission delegates. | `ev_acc75f13be87eb67e1e83694e66ade43896e31f3b5d7366083a2ba24f99a5664`; both overloads in method evidence |
| External UPI | `com.ownly.customer.UPIUrlHandlerModule.openUPIUrl` | Resolves VIEW intent handlers, launches supplied URI, resolves boolean; rejects unavailable activity/handler. | `ev_2c0bf5e0f07b94683e8d9159c7d224d8bbab949d0434b168ef55673d19d48156`; launch success is not payment confirmation |
| Analytics | `com.clevertap.react.CleverTapModule.recordEvent`, `com.appsflyer.reactnative.RNAppsFlyerModule.logEvent`, `io.invertase.firebase.analytics.ReactNativeFirebaseAnalyticsModule.logEvent` | Native bridges for named events and caller-provided parameters. | See tracking inventory |
| Risk signals | `com.incognia.reactnative.IncogniaModule.sendLoginEvent`, `sendPaymentEvent` | Builds SDK event objects from optional identity/location/payment fields. | `ev_abb5282c8fd4ea23585c492378d785c846b448bbb05d34669a75925d0d58d262` `ev_b923fe68a570c854d671b080f759bf6595eb6a422a36e4c3138066e900100d81`; business call sites unresolved |
| Bundle updates | `com.hotupdater.C.a.d` → `c(context).k()` → `com.hotupdater.H.k` | Host bundle path passes through cached HotUpdater object. | `ev_87d81435c0813ea7d1979d699c01fef9c49d8103408d08a8d93e331b6b1d5e75` `ev_3ef2b235127c346e02262e6df0746733f73fc0a5f358887933602b21aa40c1ed` `ev_48d64110b292c52b9b8be088c9ca762b51f2a6300e2374346b3268a514c5e6e9` `ev_e38f64ef8d84c6216b07de8f73b57d1c095efc5d8518ce758883231d48ef3405`; installed update choice unknown |

Generated package registration is observed in `com.facebook.react.i.a()` and `com.ownly.customer.MainApplication.a.l()`: AppsFlyer, HotUpdater, Notifee, WatermelonDB, geolocation, NetInfo, Firebase analytics/app/crashlytics/messaging/config, CleverTap, HyperSDK, Cashfree, Incognia, OTP Verify, MMKV, RN screens and WebView are among registered adapters. Registration establishes availability, not use in every workflow. `ev_c687cd1c9935ea85e2d4ffd9efa3131b57f9b47160379144d0861a8f11354402` `ev_6e806600d87aa25f4aa105513fbe4ef8fdeae62400799606949b7fdff14eef43`

## Remaining architecture gaps

Authentication protocol, business API catalog, JS route ownership, app schemas, cart persistence, order state machine and event trigger catalog remain unresolved. The main bundle is Hermes bytecode, and no Hermes decoder is exposed by the connected REA tool catalog or found among checked local decoder commands. UTF-8 JavaScript graph tools do not decode this bytecode. Static native bridge results must not be presented as complete business workflow traces. See [workflows.md](workflows.md).

---

## Saved report: startup-flow.md

# Startup flow

Analyzed only the supplied base APK, package `com.ownly.customer`, version 2.0.7 (358), min SDK 24, target SDK 36. SHA-256: `5495bcf9cf03a7b956e253a2747c10f0222454b1e2106fa53213cd53dc708a05`. REA/JADX headless 0.7.1 reports 16885 classes and 2055 resources. Manifest evidence: `ev_25c9cfa3d80fcfda38c832fe4d5cb009c9b9103ad9dd7c5a94d2943f7697af6f`.

All findings are static artifact observations or reconstructions from decompiled bodies, not runtime observations. No application execution, production requests, or APK modifications were performed. Evidence IDs resolve to records in [rea-evidence.json](rea-evidence.json); [method-evidence.md](method-evidence.md) preserves inspected method bodies, prototypes and limitations. Decompiled display names can be aliases; obfuscated names below are preserved rather than renamed. Dynamic/reflective/JS calls are outside JADX reference coverage. Signatures and split APK contents were not verified.

## Reconstructed startup chain

1. Android selects manifest application `com.pairip.application.Application`; constructor invokes MainApplication constructor. `ev_7ec903b5debf5aec762bc6f00199bf417e7806a4f4eccfe33a1b7fa501692021`
2. Wrapper `attachBaseContext(Context)` calls `LicenseClient.checkLicense(context)` before `super.attachBaseContext(context)`. This observes a license-check call, not its runtime outcome. `ev_4aaebc6ed8bca4789e06f062599975668c117132b89cc30e81887d693dc8a6f0`
3. Manifest declares initialization providers, including FirebaseInitProvider (initOrder 100), ReactNativeFirebaseAppInitProvider (99), ReactNativeFirebaseCrashlyticsInitProvider (98), NotifeeInitProvider (-100), AndroidX InitializationProvider, CashfreeCoreContentProvider and PicassoProvider. Android lifecycle ordering before Application.onCreate is an inference from the component lifecycle; no provider execution was captured. Exact declarations are in [AndroidManifest.xml](AndroidManifest.xml). `ev_25c9cfa3d80fcfda38c832fe4d5cb009c9b9103ad9dd7c5a94d2943f7697af6f`
4. Inherited `com.ownly.customer.MainApplication.onCreate()` calls `com.clevertap.android.sdk.e.b(this)`, `f0.b2(f0.b.VERBOSE)`, `super.onCreate()`, `SoLoader.l(this, OpenSourceMergedSoMapping.a)`, then `DefaultNewArchitectureEntryPoint.load()`, in that order. `f0` is an unqualified decompiler display type here; its fully qualified owner was not resolved. `ev_43f0d6293fbbeb1af5195240ae91d19c673015bdf0082030e8d82650b8755e6a`
5. DefaultIcon alias launches MainActivity. Its onCreate initializes a timestamp via `h` when zero, applies theme `k.a`, calls `super.onCreate(null)`, invokes `w0.b(getWindow(),true)` and `h.o(this)`. Unqualified helper owners are not expanded without evidence. It intentionally passes null rather than the received saved-state bundle. `ev_b0b721bc80f6352bcba4616ff4046fe77c8184f537ca1e6ff80e6ce58c0e6a72` `ev_25c9cfa3d80fcfda38c832fe4d5cb009c9b9103ad9dd7c5a94d2943f7697af6f`
6. React component name is `consumerapp`; host entry name is `index`. Generated RN packages are obtained by `new com.facebook.react.i(this).a()` and extended by the host `l()` method. `ev_3274c189887357f0804a6bede9aa0ae0170696b006a19dbff219106ad7e2d45c` `ev_47521fae078ab6d16f593981947c908da3633fb1c4cbaebbcbb666404a78c582` `ev_6e806600d87aa25f4aa105513fbe4ef8fdeae62400799606949b7fdff14eef43` `ev_c687cd1c9935ea85e2d4ffd9efa3131b57f9b47160379144d0861a8f11354402`
7. Host `g()` delegates to HotUpdater `C.a.d(context)`; that obtains/caches an H instance and calls `H.k()` → `o().a()`. Final path-selection branch is not decoded, so no claim that the packaged bundle always wins over a downloaded update. `ev_87d81435c0813ea7d1979d699c01fef9c49d8103408d08a8d93e331b6b1d5e75` `ev_3ef2b235127c346e02262e6df0746733f73fc0a5f358887933602b21aa40c1ed` `ev_48d64110b292c52b9b8be088c9ca762b51f2a6300e2374346b3268a514c5e6e9` `ev_e38f64ef8d84c6216b07de8f73b57d1c095efc5d8518ce758883231d48ef3405`

## Intent entry paths

MainActivity is exported, singleTask, portrait. Manifest includes `ownlyapp:` and verified-link declarations for `https://ownly.food/app` and `https://ownly.onelink.me/tMlo`. These are declared URI matching rules, not verified server association or API endpoints. `onNewIntent` calls the superclass then `setIntent(intent)`; JS destination resolution remains unknown. `ev_25c9cfa3d80fcfda38c832fe4d5cb009c9b9103ad9dd7c5a94d2943f7697af6f` `ev_55dd3c02665953b74b208ede8037630fd7fa9a16e04be9f20abe97dbb92a2de8`

## Call-graph limits

JADX incoming references to MainApplication.onCreate are zero (`ev_60e2c279d12469e2fb5ec0b35e9be8c93872b3985507a570281bfc3d0fe999da`). This does not negate Android framework invocation. Likewise zero DEX users of a ReactMethod does not prove it is unused: JS calls cross a bridge.

---

## Saved report: tracking-inventory.md

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

---

## Saved report: workflows.md

# Client workflow traces and unresolved boundaries

Analyzed only the supplied base APK, package `com.ownly.customer`, version 2.0.7 (358), min SDK 24, target SDK 36. SHA-256: `5495bcf9cf03a7b956e253a2747c10f0222454b1e2106fa53213cd53dc708a05`. REA/JADX headless 0.7.1 reports 16885 classes and 2055 resources. Manifest evidence: `ev_25c9cfa3d80fcfda38c832fe4d5cb009c9b9103ad9dd7c5a94d2943f7697af6f`.

All findings are static artifact observations or reconstructions from decompiled bodies, not runtime observations. No application execution, production requests, or APK modifications were performed. Evidence IDs resolve to records in [rea-evidence.json](rea-evidence.json); [method-evidence.md](method-evidence.md) preserves inspected method bodies, prototypes and limitations. Decompiled display names can be aliases; obfuscated names below are preserved rather than renamed. Dynamic/reflective/JS calls are outside JADX reference coverage. Signatures and split APK contents were not verified.

## Coverage checklist

| Requested workflow | Status | Verified path | Unresolved business logic |
|---|---|---|---|
| Login | Partial | `com.faizal.OtpVerify.OtpVerifyModule.getOtp` → requestOtp → Google phone API task; Incognia login event and CleverTap identity bridges exist | Phone validation, send/verify OTP endpoints, session tokens, refresh/logout and screen transitions |
| Restaurant discovery | Unresolved | Geolocation and HTTP transport capabilities are present | Restaurant query, pagination, availability, sorting, recommendations and serviceability |
| Search | Unresolved | RN networking and RN screens are packaged | Search method, debounce, filters, endpoint and result navigation |
| Cart | Unresolved | WatermelonDB and MMKV adapters are registered | Cart state owner, add/remove/update, pricing, persistence and restaurant-change rules |
| Checkout | Partial | HyperSDK process and custom UPI intent bridge reconstructed | Cart validation, order creation, payment payload source, backend confirmation and retry/idempotency |
| Order tracking | Unresolved | Messaging/Notifee adapters packaged | Order state machine, polling/socket/push mechanism, status endpoint and update handlers |
| Location | Partial | Permission checks/requests and current/continuous position delegation | Address selection, geocoding, server payloads, serviceability and retention |
| Analytics | Partial | Named event, profile and Incognia risk bridges reconstructed | Business triggers and concrete event names/payloads |

## Login support

`com.faizal.OtpVerify.OtpVerifyModule.getOtp` (`ev_afea8348aa5617024c29447762c5aac501c11719b9c621672f23673923a5d867`) calls requestOtp; `com.faizal.OtpVerify.OtpVerifyModule.requestOtp` (`ev_7383605032d6083277edc6e218fc31188a5719999a29b81c3d573554b33c7002`) obtains a Google phone API Task and registers listeners. This is local SMS retrieval support, not a call to an Ownly login API. SDK method naming alone must not be used to invent a login service or successful authentication chain.

## Checkout support

`in.juspay.hypersdkreact.HyperSdkReactModule.process(String)` delegates to its private overload, which synchronizes on lock, parses a JSONObject, checks current activity and HyperServices, installs ReactLaunchDelegate and ReactRequestDelegate and invokes HyperServices.process(activity,json). Missing objects/invalid JSON produce SDK logging paths. Both overloads are recorded in method-evidence.md. `ev_acc75f13be87eb67e1e83694e66ade43896e31f3b5d7366083a2ba24f99a5664`

`com.ownly.customer.UPIUrlHandlerModule.openUPIUrl` (`ev_2c0bf5e0f07b94683e8d9159c7d224d8bbab949d0434b168ef55673d19d48156`) constructs ACTION_VIEW for a caller-provided URI; checks handlers; starts activity; resolves true. It rejects when no activity/handler exists or an exception occurs. This cannot establish payment success or order placement. The source does not validate the URI scheme in this method; any separate isUPIUrl check or JS caller precondition was not traced.

## Location support

`RNCGeolocationModule.getCurrentPosition` invokes `com.reactnativecommunity.geolocation.GeolocationModule.getCurrentPosition` at DEX code-unit offset 2, classes4.dex, method index 14498 (static reference evidence `ev_4e25690856d491e222b85ebf414c05dd1c37e0e69d4169b229c7e2bebaffbf96`). The implementation either calls mLocationManager.b directly when configuration.b is true or requests authorization then dispatches through a callback. SecurityException invokes emitLocationPermissionMissing. `ev_b1fb39db89da9414d46fd5e24c4b72e56077b2c4df6a859653aea75d6c0a90f9`

requestAuthorization obtains PermissionsModule, constructs coarse/fine permissions and checks fine permission, with coarse check on the rejection callback and additional grant/request logic delegated to callbacks. startObserving similarly dispatches to manager.e or asks authorization. No background tracking schedule is established. `ev_32888ab7fde6438d23be47918f984aecfceb62189eaddc88deb5de18399619d6` `ev_f28983344a8dfe3024aeafb3286c9c8df109ecc1216edd6a328081121229fc94`

## Hermes boundary and next evidence needed

REA extraction evidence `ev_8463fb70716a384111e107f07042a68fe9408f0e235e4a0a514928265f9a40c5` records `assets/index.android.bundle`, 20,053,204 bytes, SHA-256 `b6f904c723cf894e03bf2e6bb0400015c288b78ad855f1eb825965d1654511a3`. Supplementary local byte inspection found header bytes `c61fbc03c103191f62000000`: Hermes magic and little-endian bytecode version 98. This is binary bytecode, not UTF-8 source suitable for REA's JavaScript graph analyzer. No source map was found among APK filenames ending `.map` in the local ZIP inspection. This bounded filename check does not prove no external map exists.

The connected REA catalog advertises Android/JADX and UTF-8 JavaScript analysis, but no Hermes disassembly/decompilation tool. Checked local decoder commands hbc-disassembler, hermes-dec, hbcdump, hermes and hbc-decompiler were absent. Remaining business workflows require a compatible Hermes v98 decoder or matching source/source map, followed by source-linked call-site tracing. A downloaded HotUpdater bundle could additionally differ from the packaged build. No raw string candidate is promoted to an API endpoint or business method here.

The requested business workflow investigation is therefore incomplete at this boundary; native capabilities are not substitutes for the missing JS call graph.

---

## Exact completed class inspections

These class/member inventories are saved; do not inspect them again just to rediscover method names.

| Class | Evidence |
|---|---|
| `com.margelo.nitro.mmkv.HybridMMKVPlatformContext` | `ev_0946270d861b5aadb4f7c36c8d8d95863539ec4a3d34a245b4c3866b672df328` |
| `com.ownly.customer.AndroidInstalledAppsCheckerModule` | `ev_1552d014ac31705698fc0f8e5017852b3da76aac6e4b42fc9d883615951b4de3` |
| `com.hotupdater.C` | `ev_1fdb6ccbe8412869d9d3ed4e4639e5418faa32cdfe6d73571c88f9e7b31f1db9` |
| `com.clevertap.react.CleverTapModule` | `ev_4e5600b86603d4e6bfe929e781b808af21aa97b65aefcd428d5529ac7429a134` |
| `com.nozbe.watermelondb.WMDatabaseBridge` | `ev_58b79aacf3372e477a57a2ea413673a232f9a019bdd796e6cf186a9f95ee244f` |
| `com.ownly.customer.UPIUrlHandlerModule` | `ev_5e33258d8f32ec9ab0e96c57ea1f30e74168c9d2e67bad50bf9dc8fa12fa861d` |
| `com.reactnativecommunity.geolocation.GeolocationModule` | `ev_616855078c191e56bb3992d8fdf04e489959f7835040ebed78dffb3205eb15e5` |
| `com.pairip.application.Application` | `ev_71c2cc501e0e029f234a9f7c9aa5f990c3de006aff24577e897e6176d255ce27` |
| `com.facebook.react.modules.network.NetworkingModule` | `ev_7f5c2ad4cfd43ade2e0951ea2176cbb54afdded4fef0e3b0f559ae0b368fd875` |
| `com.facebook.react.i` | `ev_838870654cf5f0aa961581058f50b128045f4e183a3bf72edbe0c59bc32e3d81` |
| `com.ownly.customer.MainApplication` | `ev_88f2ec4bf386efcae4efd8a7f4abf874335b609e3716f584a8a9fb2f5baf11b6` |
| `com.ownly.customer.MainActivity` | `ev_890e9933d346c61a058a5834d3ad368fea54d019072c890dfc3dff47da29e36c` |
| `com.faizal.OtpVerify.OtpVerifyModule` | `ev_b85eb4e22e19e226be2142c76ad9f4e2995b09eee17ec4dcf2bbb6fdcba13c18` |
| `com.appsflyer.reactnative.RNAppsFlyerModule` | `ev_c759a676e3758483bb427333b146cfdc24adb484614063108614e5f019042834` |
| `com.incognia.reactnative.IncogniaModule` | `ev_e95d5ee55cdb645455fc74f205b06faeca88b471740d635cab5ab90aab9cb80d` |
| `in.juspay.hypersdkreact.HyperSdkReactModule` | `ev_f72d3c3b3106a5789de00b9c23687c6e7ef3a85b6d6afd0553108a61a017e199` |
| `io.invertase.firebase.analytics.ReactNativeFirebaseAnalyticsModule` | `ev_ff6ce5cd19434451bfcc04f5bd39ceda37dbf03586698e969365713d004910b8` |

## Exact completed method inspections

Full bodies are in method-evidence.md and the canonical bundle.

| Class and method | Overload | DEX prototype | Evidence |
|---|---|---|---|
| `com.facebook.react.modules.network.NetworkingModule.sendRequestInternalReal` | 0 | `(Ljava/lang/String;Ljava/lang/String;ILcom/facebook/react/bridge/ReadableArray;Lcom/facebook/react/bridge/ReadableMap;Ljava/lang/String;ZIZLjava/lang/String;)V` | `ev_037e7e55d9404382e22725cf6a634906f9a47d1c7045d5f18bb5ae5e797623b7` |
| `com.facebook.react.modules.network.NetworkingModule.sendRequest` | 0 | `(Ljava/lang/String;Ljava/lang/String;DLcom/facebook/react/bridge/ReadableArray;Lcom/facebook/react/bridge/ReadableMap;Ljava/lang/String;ZDZ)V` | `ev_1a1757f3295e0109f971027b04df648377a0c787b7a2995275feb5c5032ac48e` |
| `com.ownly.customer.UPIUrlHandlerModule.openUPIUrl` | 0 | `(Ljava/lang/String;Lcom/facebook/react/bridge/Promise;)V` | `ev_2c0bf5e0f07b94683e8d9159c7d224d8bbab949d0434b168ef55673d19d48156` |
| `com.margelo.nitro.mmkv.HybridMMKVPlatformContext.getBaseDirectory` | 0 | `()Ljava/lang/String;` | `ev_2dbaac96844f780d110f305d5fbe8089496efbb418c014fd3b7fed499cf36b50` |
| `com.ownly.customer.MainActivity.b0` | 0 | `()Ljava/lang/String;` | `ev_3274c189887357f0804a6bede9aa0ae0170696b006a19dbff219106ad7e2d45c` |
| `com.reactnativecommunity.geolocation.GeolocationModule.requestAuthorization` | 0 | `(Lcom/facebook/react/bridge/Callback;Lcom/facebook/react/bridge/Callback;)V` | `ev_32888ab7fde6438d23be47918f984aecfceb62189eaddc88deb5de18399619d6` |
| `com.hotupdater.C.a.d` | 0 | `(Landroid/content/Context;)Ljava/lang/String;` | `ev_3ef2b235127c346e02262e6df0746733f73fc0a5f358887933602b21aa40c1ed` |
| `com.ownly.customer.MainApplication.onCreate` | 0 | `()V` | `ev_43f0d6293fbbeb1af5195240ae91d19c673015bdf0082030e8d82650b8755e6a` |
| `com.ownly.customer.MainApplication.a.i` | 0 | `()Ljava/lang/String;` | `ev_47521fae078ab6d16f593981947c908da3633fb1c4cbaebbcbb666404a78c582` |
| `com.hotupdater.C.a.c` | 0 | `(Landroid/content/Context;)Lcom/hotupdater/H;` | `ev_48d64110b292c52b9b8be088c9ca762b51f2a6300e2374346b3268a514c5e6e9` |
| `com.pairip.application.Application.attachBaseContext` | 0 | `(Landroid/content/Context;)V` | `ev_4aaebc6ed8bca4789e06f062599975668c117132b89cc30e81887d693dc8a6f0` |
| `com.ownly.customer.MainApplication.a.<init>` | 0 | `(Lcom/ownly/customer/MainApplication;)V` | `ev_4ab16e314f3ae798884886371b88e5a5d84649593f19e955bf6eff1e87e461dc` |
| `com.ownly.customer.MainActivity.onNewIntent` | 0 | `(Landroid/content/Intent;)V` | `ev_55dd3c02665953b74b208ede8037630fd7fa9a16e04be9f20abe97dbb92a2de8` |
| `com.ownly.customer.MainApplication.a.l` | 0 | `()Ljava/util/List;` | `ev_6e806600d87aa25f4aa105513fbe4ef8fdeae62400799606949b7fdff14eef43` |
| `com.clevertap.react.CleverTapModule.onUserLogin` | 0 | `(Lcom/facebook/react/bridge/ReadableMap;)V` | `ev_70e66967e73bac45452e1cd345231c70763579dc232024cb1f78d0503faad259` |
| `com.faizal.OtpVerify.OtpVerifyModule.requestOtp` | 0 | `(Lcom/facebook/react/bridge/Promise;)V` | `ev_7383605032d6083277edc6e218fc31188a5719999a29b81c3d573554b33c7002` |
| `com.pairip.application.Application.<init>` | 0 | `()V` | `ev_7ec903b5debf5aec762bc6f00199bf417e7806a4f4eccfe33a1b7fa501692021` |
| `com.ownly.customer.MainApplication.a.g` | 0 | `()Ljava/lang/String;` | `ev_87d81435c0813ea7d1979d699c01fef9c49d8103408d08a8d93e331b6b1d5e75` |
| `com.ownly.customer.MainApplication.a.x` | 0 | `()Z` | `ev_93d0051638f7937960cfb174d1c9c1c95748c5d2df3244ea9d170390b030f8f5` |
| `com.appsflyer.reactnative.RNAppsFlyerModule.logEvent` | 0 | `(Ljava/lang/String;Lcom/facebook/react/bridge/ReadableMap;Lcom/facebook/react/bridge/Callback;Lcom/facebook/react/bridge/Callback;)V` | `ev_a60d8bc32d5e8fe0f905a0f8ff39c9eed545bd7528772dc53c28f74939e06fb9` |
| `com.incognia.reactnative.IncogniaModule.sendLoginEvent` | 0 | `(Lcom/facebook/react/bridge/ReadableMap;)V` | `ev_abb5282c8fd4ea23585c492378d785c846b448bbb05d34669a75925d0d58d262` |
| `in.juspay.hypersdkreact.HyperSdkReactModule.process` | 1 | `(Ljava/lang/String;)V` | `ev_acc75f13be87eb67e1e83694e66ade43896e31f3b5d7366083a2ba24f99a5664` |
| `com.faizal.OtpVerify.OtpVerifyModule.getOtp` | 0 | `(Lcom/facebook/react/bridge/Promise;)V` | `ev_afea8348aa5617024c29447762c5aac501c11719b9c621672f23673923a5d867` |
| `com.ownly.customer.MainActivity.onCreate` | 0 | `(Landroid/os/Bundle;)V` | `ev_b0b721bc80f6352bcba4616ff4046fe77c8184f537ca1e6ff80e6ce58c0e6a72` |
| `io.invertase.firebase.analytics.ReactNativeFirebaseAnalyticsModule.logEvent` | 0 | `(Ljava/lang/String;Lcom/facebook/react/bridge/ReadableMap;Lcom/facebook/react/bridge/Promise;)V` | `ev_b152f9c18b2d94f3a9fe005d19aaca6cb837d07f661292c46698d9f3106cc1a9` |
| `com.reactnativecommunity.geolocation.GeolocationModule.getCurrentPosition` | 0 | `(Lcom/facebook/react/bridge/ReadableMap;Lcom/facebook/react/bridge/Callback;Lcom/facebook/react/bridge/Callback;)V` | `ev_b1fb39db89da9414d46fd5e24c4b72e56077b2c4df6a859653aea75d6c0a90f9` |
| `com.incognia.reactnative.IncogniaModule.sendPaymentEvent` | 0 | `(Lcom/facebook/react/bridge/ReadableMap;)V` | `ev_b923fe68a570c854d671b080f759bf6595eb6a422a36e4c3138066e900100d81` |
| `com.ownly.customer.AndroidInstalledAppsCheckerModule.checkLaunchablePackages` | 0 | `(Lcom/facebook/react/bridge/ReadableArray;Lcom/facebook/react/bridge/Promise;)V` | `ev_bc2c3cb8614cec694f3dbb8ed1d7aa6fa2cb1426ffac7476a9cb3d924efd1fe3` |
| `com.facebook.react.i.a` | 0 | `()Ljava/util/ArrayList;` | `ev_c687cd1c9935ea85e2d4ffd9efa3131b57f9b47160379144d0861a8f11354402` |
| `com.clevertap.react.CleverTapModule.recordEvent` | 0 | `(Ljava/lang/String;Lcom/facebook/react/bridge/ReadableMap;)V` | `ev_d032b72b5e05525d8e79f14420eb4e04ca1804ed06c1251e1b6c020f0fb1516c` |
| `com.ownly.customer.MainApplication.a.t` | 0 | `()Z` | `ev_dc1b14459e0f258be17a3f9f54f6c84ffd5d5d8b4bac60bd4b6d522c73f3859f` |
| `com.hotupdater.H.k` | 0 | `()Ljava/lang/String;` | `ev_e38f64ef8d84c6216b07de8f73b57d1c095efc5d8518ce758883231d48ef3405` |
| `in.juspay.hypersdkreact.HyperSdkReactModule.process` | 0 | `(Lin/juspay/services/HyperServices;Ljava/lang/String;)V` | `ev_ec7ac1e5afd3c47c7d0524c653a13c7838a5111b0a36f93790537522316fc1aa` |
| `com.reactnativecommunity.geolocation.GeolocationModule.startObserving` | 0 | `(Lcom/facebook/react/bridge/ReadableMap;)V` | `ev_f28983344a8dfe3024aeafb3286c9c8df109ecc1216edd6a328081121229fc94` |
| `com.nozbe.watermelondb.WMDatabaseBridge.initialize` | 0 | `(Ljava/lang/Integer;Ljava/lang/String;IZLcom/facebook/react/bridge/Promise;)V` | `ev_fbfc2b14a75737ae9edee7a67f68e50fcac59a5ef35801bc931bf826d7580d47` |

## Completed search boundaries and discovered class names

These are case-sensitive top-level class-name substring searches, not semantic searches. An empty result does not prove absence of a feature. Exact complete match arrays (including large Incognia and RN screens inventories) remain in rea-evidence.json.

- Query `NetworkingModule`: 1 matches; evidence `ev_02153da0411759deea02d5baf75e0564a8dd221617f21cddc5bcaf732a6b558b`. `com.facebook.react.modules.network.NetworkingModule`

- Query `AppsFlyer`: 14 matches; evidence `ev_059deab2f3791514b1a1a58de1d00fb53036ead6882b4eb3420de235c7898e2a`. `com.appsflyer.AppsFlyer2dXConversionCallback`, `com.appsflyer.AppsFlyerAdNetworkEventType`, `com.appsflyer.AppsFlyerConsent`, `com.appsflyer.AppsFlyerConversionListener`, `com.appsflyer.AppsFlyerInAppPurchaseValidationCallback`, `com.appsflyer.AppsFlyerInAppPurchaseValidatorListener`, `com.appsflyer.AppsFlyerLib`, `com.appsflyer.AppsFlyerProperties`, `com.appsflyer.attribution.AppsFlyerRequestListener`, `com.appsflyer.reactnative.PCAppsFlyerModule`, `com.appsflyer.reactnative.PCAppsFlyerPackage`, `com.appsflyer.reactnative.RNAppsFlyerConstants`, `com.appsflyer.reactnative.RNAppsFlyerModule`, `com.appsflyer.reactnative.RNAppsFlyerPackage`

- Query `Truecaller`: 0 matches; evidence `ev_08148e66c5143d37a3a5ebc0695b2e29826c24678f00550be35ce6e099e2c1f6`. No matches.

- Query `HyperSdk`: 2 matches; evidence `ev_0b8b748f5efdd76955075ec0b2035cc515e6d7145da872ae6e82ccdc2f7ebdb0`. `in.juspay.hypersdkreact.HyperSdkReactModule`, `in.juspay.hypersdkreact.HyperSdkReactPackage`

- Query `com.facebook.react.i`: 26 matches; evidence `ev_0fd464a5e3fcc1f3d578dfc1f90480780a190fd93478095317b8cd938a185da8`. `com.facebook.react.i`, `com.facebook.react.interfaces.a`, `com.facebook.react.interfaces.exceptionmanager.ReactJsExceptionHandler`, `com.facebook.react.interfaces.fabric.a`, `com.facebook.react.internal.a`, `com.facebook.react.internal.b`, `com.facebook.react.internal.c`, `com.facebook.react.internal.featureflags.ReactNativeFeatureFlagsCxxInterop`, `com.facebook.react.internal.featureflags.ReactNativeFeatureFlagsProvider`, `com.facebook.react.internal.featureflags.b`, `com.facebook.react.internal.featureflags.c`, `com.facebook.react.internal.featureflags.d`, `com.facebook.react.internal.featureflags.e`, `com.facebook.react.internal.featureflags.f`, `com.facebook.react.internal.featureflags.g`, `com.facebook.react.internal.featureflags.h`, `com.facebook.react.internal.featureflags.i`, `com.facebook.react.internal.featureflags.j`, `com.facebook.react.internal.interop.InteropEventEmitter`, `com.facebook.react.internal.interop.a`, `com.facebook.react.internal.tracing.PerformanceTracer`, `com.facebook.react.internal.turbomodule.core.TurboModuleInteropUtils`, `com.facebook.react.internal.turbomodule.core.TurboModuleManager`, `com.facebook.react.internal.turbomodule.core.TurboModuleManagerDelegate`, `com.facebook.react.internal.turbomodule.core.TurboModulePerfLogger`, `com.facebook.react.internal.turbomodule.core.interfaces.TurboModuleRegistry`

- Query `com.faizal.OtpVerify`: 5 matches; evidence `ev_14f29919c3fa43be414cc8d053963669e077ea627eed4c55082478ee945fc47b`. `com.faizal.OtpVerify.OtpVerifyModule`, `com.faizal.OtpVerify.a`, `com.faizal.OtpVerify.b`, `com.faizal.OtpVerify.c`, `com.faizal.OtpVerify.f`

- Query `com.incognia`: 2283 matches; evidence `ev_19099152b7f17da296604899bc8f50afd43f95ebb7d0f4fd550730c504237f25`. Full names preserved in the canonical match array; avoid copying this large vendor inventory into working context. Relevant inspected classes are listed above.

- Query `CleverTapModule`: 2 matches; evidence `ev_2aefc66539ae0bc8a21eca8a4f47415d0abd48bc0006fc7fddb1cf54f5c3a37f`. `com.clevertap.react.CleverTapModule`, `com.clevertap.react.NativeCleverTapModuleSpec`

- Query `com.nozbe`: 16 matches; evidence `ev_328bd983304366ae4478946d5a8dd80e61d930fe8f6152567dcc6c93861edff9`. `com.nozbe.watermelondb.BuildConfig`, `com.nozbe.watermelondb.Connection`, `com.nozbe.watermelondb.DatabaseUtils`, `com.nozbe.watermelondb.MigrationNeededError`, `com.nozbe.watermelondb.Queries`, `com.nozbe.watermelondb.R`, `com.nozbe.watermelondb.SchemaNeededError`, `com.nozbe.watermelondb.WMDatabase`, `com.nozbe.watermelondb.WMDatabaseBridge`, `com.nozbe.watermelondb.WMDatabaseDriver`, `com.nozbe.watermelondb.WatermelonDBPackage`, `com.nozbe.watermelondb.d`, `com.nozbe.watermelondb.s`, `com.nozbe.watermelondb.utils.MigrationSet`, `com.nozbe.watermelondb.utils.Pair`, `com.nozbe.watermelondb.utils.Schema`

- Query `AsyncStorage`: 0 matches; evidence `ev_363b7456ecfa619fc90fe0e58bbf88612d4c6a78aaa47a6adcb768e98b67da8c`. No matches.

- Query `MMKV`: 3 matches; evidence `ev_59199364bb52b6076b65ee6d4e0ee70a625d6e3bccce7f663f7174162f7ad37f`. `com.margelo.nitro.mmkv.HybridMMKVPlatformContext`, `com.margelo.nitro.mmkv.HybridMMKVPlatformContextSpec`, `com.tencent.mmkv.MMKV`

- Query `com.ownly`: 21 matches; evidence `ev_737a5cf451bfc2e32aa7753b7e28149f4e5cf5bad71c85007289e79fefda1ea7`. `com.ownly.customer.AndroidInstalledAppsCheckerModule`, `com.ownly.customer.AppIconSwitcherModule`, `com.ownly.customer.BuildConfig`, `com.ownly.customer.LaunchSplashModule`, `com.ownly.customer.MainActivity`, `com.ownly.customer.MainApplication`, `com.ownly.customer.R`, `com.ownly.customer.UPIUrlHandlerModule`, `com.ownly.customer.a`, `com.ownly.customer.b`, `com.ownly.customer.h`, `com.ownly.customer.i`, `com.ownly.customer.j`, `com.ownly.customer.k`, `com.ownly.customer.l`, `com.ownly.customer.phoneinput.PhoneTextInputManager`, `com.ownly.customer.phoneinput.a`, `com.ownly.customer.phoneinput.d`, `com.ownly.customer.phoneinput.e`, `com.ownly.customer.phoneinput.f`, `com.ownly.customer.phoneinput.j`

- Query `com.swmansion.rnscreens`: 207 matches; evidence `ev_760a1075d18ab77161ebade02ca58d703bfba1774f95eba6bc6175edd1b350a1`. Full names preserved in the canonical match array; avoid copying this large vendor inventory into working context. Relevant inspected classes are listed above.

- Query `Geolocation`: 3 matches; evidence `ev_77bc277d7d218a8ed174c2a83de41d6a337dc75b9a5221796ef07e405fa73b12`. `com.reactnativecommunity.geolocation.GeolocationModule`, `com.reactnativecommunity.geolocation.NativeRNCGeolocationSpec`, `com.reactnativecommunity.geolocation.RNCGeolocationModule`

- Query `io.invertase.firebase.analytics`: 3 matches; evidence `ev_a615f5b4572d1118ba2153fe1fcc4570cae1911076325ac83448391152019a50`. `io.invertase.firebase.analytics.ReactNativeFirebaseAnalyticsModule`, `io.invertase.firebase.analytics.l`, `io.invertase.firebase.analytics.v`

- Query `com.hotupdater`: 68 matches; evidence `ev_dafabe68c9054e54f856e278889fb6ca51fd72831d4669917b9a11d8a8e13c32`. Full names preserved in the canonical match array; avoid copying this large vendor inventory into working context. Relevant inspected classes are listed above.

## Completed static reference queries

| Target | Using-node count | Result / evidence |
|---|---|---|
| `com.clevertap.react.CleverTapModule.recordEvent` | 0 | No DEX using nodes; framework/JS callers remain possible; `ev_297f49deda5bd306e3d6a8855b0d8d1c1f4830263083bfc78cd5b0568feb137f` |
| `com.ownly.customer.UPIUrlHandlerModule.openUPIUrl` | 0 | No DEX using nodes; framework/JS callers remain possible; `ev_30cdcd94332c18b3b5227ae887d8b0c10b50724fb6dc6e4ddf1e93d4061214c9` |
| `com.reactnativecommunity.geolocation.GeolocationModule.getCurrentPosition` | 1 | com.reactnativecommunity.geolocation.RNCGeolocationModule.getCurrentPosition; `ev_4e25690856d491e222b85ebf414c05dd1c37e0e69d4169b229c7e2bebaffbf96` |
| `com.ownly.customer.MainApplication.onCreate` | 0 | No DEX using nodes; framework/JS callers remain possible; `ev_60e2c279d12469e2fb5ec0b35e9be8c93872b3985507a570281bfc3d0fe999da` |

## Verification already completed

All five generated analytical/method reports were checked for evidence IDs absent from the 93-record canonical bundle; none were missing. Required report files were checked nonempty. Packaged Hermes bundle SHA-256 was checked against extraction evidence. No application execution was used as validation.

The evidence bundle has zero formal REA unknown records; this does **not** mean the investigation has no unknowns. Remaining questions are explicitly recorded in the narrative reports and checklist above. No endpoint catalog, runtime network capture, complete business JS graph, application database dump, or recovered source tree was produced.

This save operation only creates reports/progress.md; all previously existing files remain unchanged. The full evidence index follows for offline lookup.

# REA evidence index

Full canonical records: [rea-evidence.json](rea-evidence.json). See [architecture.md](architecture.md), [startup-flow.md](startup-flow.md), [tracking-inventory.md](tracking-inventory.md), [workflows.md](workflows.md).

| Evidence ID | Operation | Selector |
|---|---|---|
| `ev_02153da0411759deea02d5baf75e0564a8dd221617f21cddc5bcaf732a6b558b` | search_android_classes | NetworkingModule |
| `ev_037e7e55d9404382e22725cf6a634906f9a47d1c7045d5f18bb5ae5e797623b7` | inspect_android_method | com.facebook.react.modules.network.NetworkingModule / sendRequestInternalReal |
| `ev_059deab2f3791514b1a1a58de1d00fb53036ead6882b4eb3420de235c7898e2a` | search_android_classes | AppsFlyer |
| `ev_08148e66c5143d37a3a5ebc0695b2e29826c24678f00550be35ce6e099e2c1f6` | search_android_classes | Truecaller |
| `ev_0946270d861b5aadb4f7c36c8d8d95863539ec4a3d34a245b4c3866b672df328` | inspect_android_class | com.margelo.nitro.mmkv.HybridMMKVPlatformContext |
| `ev_0b8b748f5efdd76955075ec0b2035cc515e6d7145da872ae6e82ccdc2f7ebdb0` | search_android_classes | HyperSdk |
| `ev_0fd464a5e3fcc1f3d578dfc1f90480780a190fd93478095317b8cd938a185da8` | search_android_classes | com.facebook.react.i |
| `ev_14f29919c3fa43be414cc8d053963669e077ea627eed4c55082478ee945fc47b` | search_android_classes | com.faizal.OtpVerify |
| `ev_1552d014ac31705698fc0f8e5017852b3da76aac6e4b42fc9d883615951b4de3` | inspect_android_class | com.ownly.customer.AndroidInstalledAppsCheckerModule |
| `ev_19099152b7f17da296604899bc8f50afd43f95ebb7d0f4fd550730c504237f25` | search_android_classes | com.incognia |
| `ev_1a1757f3295e0109f971027b04df648377a0c787b7a2995275feb5c5032ac48e` | inspect_android_method | com.facebook.react.modules.network.NetworkingModule / sendRequest |
| `ev_1bda774161748d774747b3997baf10a7bba00cd783a03ce8bdf8b111d36284e4` | search_android_classes | NetworkingModule |
| `ev_1c2b7aff4cf4d57e10c414871a751ab4532a94492a8dc3a66814601c66636fc3` | inspect_analysis_view |  |
| `ev_1fb3161ec10911ebf34f283535003f884c6a69fba48640d4fe9fc15cd101cae2` | search_android_classes | com.incognia |
| `ev_1fdb6ccbe8412869d9d3ed4e4639e5418faa32cdfe6d73571c88f9e7b31f1db9` | inspect_android_class | com.hotupdater.C |
| `ev_25c9cfa3d80fcfda38c832fe4d5cb009c9b9103ad9dd7c5a94d2943f7697af6f` | inspect_android_package |  |
| `ev_297f49deda5bd306e3d6a8855b0d8d1c1f4830263083bfc78cd5b0568feb137f` | trace_android_references | com.clevertap.react.CleverTapModule / recordEvent |
| `ev_2aefc66539ae0bc8a21eca8a4f47415d0abd48bc0006fc7fddb1cf54f5c3a37f` | search_android_classes | CleverTapModule |
| `ev_2c0bf5e0f07b94683e8d9159c7d224d8bbab949d0434b168ef55673d19d48156` | inspect_android_method | com.ownly.customer.UPIUrlHandlerModule / openUPIUrl |
| `ev_2dbaac96844f780d110f305d5fbe8089496efbb418c014fd3b7fed499cf36b50` | inspect_android_method | com.margelo.nitro.mmkv.HybridMMKVPlatformContext / getBaseDirectory |
| `ev_30cdcd94332c18b3b5227ae887d8b0c10b50724fb6dc6e4ddf1e93d4061214c9` | trace_android_references | com.ownly.customer.UPIUrlHandlerModule / openUPIUrl |
| `ev_3274c189887357f0804a6bede9aa0ae0170696b006a19dbff219106ad7e2d45c` | inspect_android_method | com.ownly.customer.MainActivity / b0 |
| `ev_32888ab7fde6438d23be47918f984aecfceb62189eaddc88deb5de18399619d6` | inspect_android_method | com.reactnativecommunity.geolocation.GeolocationModule / requestAuthorization |
| `ev_328bd983304366ae4478946d5a8dd80e61d930fe8f6152567dcc6c93861edff9` | search_android_classes | com.nozbe |
| `ev_363b7456ecfa619fc90fe0e58bbf88612d4c6a78aaa47a6adcb768e98b67da8c` | search_android_classes | AsyncStorage |
| `ev_3ef2b235127c346e02262e6df0746733f73fc0a5f358887933602b21aa40c1ed` | inspect_android_method | com.hotupdater.C.a / d |
| `ev_43f0d6293fbbeb1af5195240ae91d19c673015bdf0082030e8d82650b8755e6a` | inspect_android_method | com.ownly.customer.MainApplication / onCreate |
| `ev_47521fae078ab6d16f593981947c908da3633fb1c4cbaebbcbb666404a78c582` | inspect_android_method | com.ownly.customer.MainApplication.a / i |
| `ev_48d64110b292c52b9b8be088c9ca762b51f2a6300e2374346b3268a514c5e6e9` | inspect_android_method | com.hotupdater.C.a / c |
| `ev_4aaebc6ed8bca4789e06f062599975668c117132b89cc30e81887d693dc8a6f0` | inspect_android_method | com.pairip.application.Application / attachBaseContext |
| `ev_4ab16e314f3ae798884886371b88e5a5d84649593f19e955bf6eff1e87e461dc` | inspect_android_method | com.ownly.customer.MainApplication.a / <init> |
| `ev_4cd29282ca340bc7f62c817aff293beaea772e71b178a34cc6f89011b948e28c` | search_android_classes | com.nozbe |
| `ev_4e25690856d491e222b85ebf414c05dd1c37e0e69d4169b229c7e2bebaffbf96` | trace_android_references | com.reactnativecommunity.geolocation.GeolocationModule / getCurrentPosition |
| `ev_4e5600b86603d4e6bfe929e781b808af21aa97b65aefcd428d5529ac7429a134` | inspect_android_class | com.clevertap.react.CleverTapModule |
| `ev_55dd3c02665953b74b208ede8037630fd7fa9a16e04be9f20abe97dbb92a2de8` | inspect_android_method | com.ownly.customer.MainActivity / onNewIntent |
| `ev_58b79aacf3372e477a57a2ea413673a232f9a019bdd796e6cf186a9f95ee244f` | inspect_android_class | com.nozbe.watermelondb.WMDatabaseBridge |
| `ev_59199364bb52b6076b65ee6d4e0ee70a625d6e3bccce7f663f7174162f7ad37f` | search_android_classes | MMKV |
| `ev_5e33258d8f32ec9ab0e96c57ea1f30e74168c9d2e67bad50bf9dc8fa12fa861d` | inspect_android_class | com.ownly.customer.UPIUrlHandlerModule |
| `ev_60e2c279d12469e2fb5ec0b35e9be8c93872b3985507a570281bfc3d0fe999da` | trace_android_references | com.ownly.customer.MainApplication / onCreate |
| `ev_616855078c191e56bb3992d8fdf04e489959f7835040ebed78dffb3205eb15e5` | inspect_android_class | com.reactnativecommunity.geolocation.GeolocationModule |
| `ev_6b6f512aab5f508befa06a69e108928750734bd39a31984c90bf6e0de4b91000` | search_android_classes | AsyncStorage |
| `ev_6b931bfcef34c73ddd6dc363aa59a6e3aaa9d926af6823932162d10675c76b48` | search_android_classes | AppsFlyer |
| `ev_6e806600d87aa25f4aa105513fbe4ef8fdeae62400799606949b7fdff14eef43` | inspect_android_method | com.ownly.customer.MainApplication.a / l |
| `ev_6f2f0c7ae95a32ae5dda070391cd70675108a20d6233671e05bdfb4505c4b198` | search_android_classes | MMKV |
| `ev_70e66967e73bac45452e1cd345231c70763579dc232024cb1f78d0503faad259` | inspect_android_method | com.clevertap.react.CleverTapModule / onUserLogin |
| `ev_71c2cc501e0e029f234a9f7c9aa5f990c3de006aff24577e897e6176d255ce27` | inspect_android_class | com.pairip.application.Application |
| `ev_737a5cf451bfc2e32aa7753b7e28149f4e5cf5bad71c85007289e79fefda1ea7` | search_android_classes | com.ownly |
| `ev_7383605032d6083277edc6e218fc31188a5719999a29b81c3d573554b33c7002` | inspect_android_method | com.faizal.OtpVerify.OtpVerifyModule / requestOtp |
| `ev_760a1075d18ab77161ebade02ca58d703bfba1774f95eba6bc6175edd1b350a1` | search_android_classes | com.swmansion.rnscreens |
| `ev_77bc277d7d218a8ed174c2a83de41d6a337dc75b9a5221796ef07e405fa73b12` | search_android_classes | Geolocation |
| `ev_7ca32b1e2806b8c5f8b3137467fceff8c31d342ca800becec6b7db6be46c5853` | inspect_artifact |  |
| `ev_7ec903b5debf5aec762bc6f00199bf417e7806a4f4eccfe33a1b7fa501692021` | inspect_android_method | com.pairip.application.Application / <init> |
| `ev_7f5c2ad4cfd43ade2e0951ea2176cbb54afdded4fef0e3b0f559ae0b368fd875` | inspect_android_class | com.facebook.react.modules.network.NetworkingModule |
| `ev_838870654cf5f0aa961581058f50b128045f4e183a3bf72edbe0c59bc32e3d81` | inspect_android_class | com.facebook.react.i |
| `ev_8463fb70716a384111e107f07042a68fe9408f0e235e4a0a514928265f9a40c5` | extract_artifact |  |
| `ev_87d81435c0813ea7d1979d699c01fef9c49d8103408d08a8d93e331b6b1d5e75` | inspect_android_method | com.ownly.customer.MainApplication.a / g |
| `ev_88f2ec4bf386efcae4efd8a7f4abf874335b609e3716f584a8a9fb2f5baf11b6` | inspect_android_class | com.ownly.customer.MainApplication |
| `ev_890e9933d346c61a058a5834d3ad368fea54d019072c890dfc3dff47da29e36c` | inspect_android_class | com.ownly.customer.MainActivity |
| `ev_8db6357de5dbc27b90906962edf2c59c3b61f0dace0d068b71c3d004edf5751f` | search_android_classes | com.swmansion.rnscreens |
| `ev_93d0051638f7937960cfb174d1c9c1c95748c5d2df3244ea9d170390b030f8f5` | inspect_android_method | com.ownly.customer.MainApplication.a / x |
| `ev_a60d8bc32d5e8fe0f905a0f8ff39c9eed545bd7528772dc53c28f74939e06fb9` | inspect_android_method | com.appsflyer.reactnative.RNAppsFlyerModule / logEvent |
| `ev_a615f5b4572d1118ba2153fe1fcc4570cae1911076325ac83448391152019a50` | search_android_classes | io.invertase.firebase.analytics |
| `ev_abb5282c8fd4ea23585c492378d785c846b448bbb05d34669a75925d0d58d262` | inspect_android_method | com.incognia.reactnative.IncogniaModule / sendLoginEvent |
| `ev_acc75f13be87eb67e1e83694e66ade43896e31f3b5d7366083a2ba24f99a5664` | inspect_android_method | in.juspay.hypersdkreact.HyperSdkReactModule / process / 1 |
| `ev_afea8348aa5617024c29447762c5aac501c11719b9c621672f23673923a5d867` | inspect_android_method | com.faizal.OtpVerify.OtpVerifyModule / getOtp |
| `ev_b0b721bc80f6352bcba4616ff4046fe77c8184f537ca1e6ff80e6ce58c0e6a72` | inspect_android_method | com.ownly.customer.MainActivity / onCreate |
| `ev_b152f9c18b2d94f3a9fe005d19aaca6cb837d07f661292c46698d9f3106cc1a9` | inspect_android_method | io.invertase.firebase.analytics.ReactNativeFirebaseAnalyticsModule / logEvent |
| `ev_b1fb39db89da9414d46fd5e24c4b72e56077b2c4df6a859653aea75d6c0a90f9` | inspect_android_method | com.reactnativecommunity.geolocation.GeolocationModule / getCurrentPosition |
| `ev_b4a6508567f0803fb2265e03034ad056b53cfa98302ce3a1db2cedf4abc0bd98` | search_android_classes | CleverTapModule |
| `ev_b85eb4e22e19e226be2142c76ad9f4e2995b09eee17ec4dcf2bbb6fdcba13c18` | inspect_android_class | com.faizal.OtpVerify.OtpVerifyModule |
| `ev_b923fe68a570c854d671b080f759bf6595eb6a422a36e4c3138066e900100d81` | inspect_android_method | com.incognia.reactnative.IncogniaModule / sendPaymentEvent |
| `ev_bc2c3cb8614cec694f3dbb8ed1d7aa6fa2cb1426ffac7476a9cb3d924efd1fe3` | inspect_android_method | com.ownly.customer.AndroidInstalledAppsCheckerModule / checkLaunchablePackages |
| `ev_c31ed7fb62a5383d3b628e7e234a7cf173270aac62632779ec30190d7a741385` | search_android_classes | Geolocation |
| `ev_c561fa9fe8dc50f34149555429b08f38ab5eff469124a622f7db9e075cac9278` | search_android_classes | Truecaller |
| `ev_c687cd1c9935ea85e2d4ffd9efa3131b57f9b47160379144d0861a8f11354402` | inspect_android_method | com.facebook.react.i / a |
| `ev_c759a676e3758483bb427333b146cfdc24adb484614063108614e5f019042834` | inspect_android_class | com.appsflyer.reactnative.RNAppsFlyerModule |
| `ev_cc649031d53a5905330643eded59073c41dfcb8e7b3adeaa37ca286896a0a60d` | search_android_classes | io.invertase.firebase.analytics |
| `ev_d032b72b5e05525d8e79f14420eb4e04ca1804ed06c1251e1b6c020f0fb1516c` | inspect_android_method | com.clevertap.react.CleverTapModule / recordEvent |
| `ev_d48c00392ee04235ada479e75dd4f667d6945acbee3840d827ee4d0e56ec6128` | search_android_classes | com.facebook.react.i |
| `ev_d5d4fd3fe70a2ca6c11719571f9d8a5f55a517cdac5a7982322215c9ca1567b5` | search_android_classes | com.ownly |
| `ev_dafabe68c9054e54f856e278889fb6ca51fd72831d4669917b9a11d8a8e13c32` | search_android_classes | com.hotupdater |
| `ev_dc1b14459e0f258be17a3f9f54f6c84ffd5d5d8b4bac60bd4b6d522c73f3859f` | inspect_android_method | com.ownly.customer.MainApplication.a / t |
| `ev_dd0939f6f3becba196365015124b24e7e8206f433c7248fefe81085b1513b8d9` | search_android_classes | com.faizal.OtpVerify |
| `ev_dff2a9816e2f7b65850a3e5ab089082618b2c8edbb79b9feab0d985e5117ee16` | inventory_artifact |  |
| `ev_e38f64ef8d84c6216b07de8f73b57d1c095efc5d8518ce758883231d48ef3405` | inspect_android_method | com.hotupdater.H / k |
| `ev_e95d5ee55cdb645455fc74f205b06faeca88b471740d635cab5ab90aab9cb80d` | inspect_android_class | com.incognia.reactnative.IncogniaModule |
| `ev_ec7ac1e5afd3c47c7d0524c653a13c7838a5111b0a36f93790537522316fc1aa` | inspect_android_method | in.juspay.hypersdkreact.HyperSdkReactModule / process / 0 |
| `ev_efa35f73c5c30dc2eda269396bdd181e04594fd51d87fbeb23e7a4b2e7300c68` | search_android_classes | com.hotupdater |
| `ev_f28983344a8dfe3024aeafb3286c9c8df109ecc1216edd6a328081121229fc94` | inspect_android_method | com.reactnativecommunity.geolocation.GeolocationModule / startObserving |
| `ev_f72d3c3b3106a5789de00b9c23687c6e7ef3a85b6d6afd0553108a61a017e199` | inspect_android_class | in.juspay.hypersdkreact.HyperSdkReactModule |
| `ev_fbfc2b14a75737ae9edee7a67f68e50fcac59a5ef35801bc931bf826d7580d47` | inspect_android_method | com.nozbe.watermelondb.WMDatabaseBridge / initialize |
| `ev_ff5fd95cd4240fb96a0bcb46448aa88168e2243c037805e8a6519c56d6746536` | search_android_classes | HyperSdk |
| `ev_ff6ce5cd19434451bfcc04f5bd39ceda37dbf03586698e969365713d004910b8` | inspect_android_class | io.invertase.firebase.analytics.ReactNativeFirebaseAnalyticsModule |


---

## Task 2 continuation — Hermes decoded, 2026-11-05

The earlier Hermes tooling blocker is resolved. Newly installed local Hermes MCP was queried through a Python stdio adapter under REA process captures. Verified the HBC matches the packaged digest; recovered Metro inventory (4,638 modules), function metadata (42,307 functions), targeted modules and request-builder assembly. No full-bundle decompile or production interaction. See feature-flow-hermes.md, hermes-tracking.md and hermes-evidence-index.md for the current results and exact remaining work; the earlier resume checklist above is historical. Native reports were backed up as *-native-v1.md before adding continuation links; original rea-evidence.json is unchanged. New evidence is exported separately to rea-evidence-hermes.json. Reuse analysis/hermes/mcp cached selectors to avoid repeating completed tool operations. Decompiler variable-recovery errors remain; validate missing async edges with targeted assembly/IR.

Task 2 final validation: separate analytics REA session exported to `rea-evidence-hermes-analytics.json`; capture IDs in hermes-tracking.md validated against that file plus the preserved native bundle. Export counts: {"rea-evidence.json": {"records": 93, "unknowns": 0}, "rea-evidence-hermes.json": {"records": 50, "unknowns": 40}, "rea-evidence-hermes-analytics.json": {"records": 20, "unknowns": 16}}. Process residual unknowns describe tool-run/environment/network-observation limits, not a claim that business workflows executed. `hermes-artifacts.json` records exact saved module/function response hashes and four credential-redacted derived files. Prior native report bodies verified preserved in backups and current report suffixes. Remaining work is listed in feature-flow-hermes.md and hermes-tracking.md.


---

# Complete continuation handoff after Task 2 — 2026-11-05

This appended checkpoint is the current resume point. Earlier native-only findings and the earlier decoder-blocked checklist remain preserved above as historical progress. This save operation read existing artifacts only; no REA, JADX or Hermes analysis was rerun. The investigation remains a static, partially reconstructed client investigation, not a verified runtime/backend implementation.

## Current state and constraints

- Original scope: `rea-task.md`; continuation scope: `rea-task-2.md`.
- APK: `apk/com.ownly.customer/base.apk`, com.ownly.customer 2.0.7 (358), SHA-256 `5495bcf9cf03a7b956e253a2747c10f0222454b1e2106fa53213cd53dc708a05`.
- HBC: `analysis/hermes/ownly.hbc`, 20,053,204 bytes; SHA-256 `b6f904c723cf894e03bf2e6bb0400015c288b78ad855f1eb825965d1654511a3`; Hermes v98, byte-identical to `assets/index.android.bundle` previously extracted from the APK.
- Native identity and startup were already established: Pairip Application wrapper → Ownly MainApplication; enabled DefaultIcon launcher alias → MainActivity; React component name consumerapp; RN new-architecture loader; host bundle selection passes through HotUpdater. Exact Java class/method inventories and evidence are preserved above and in native reports.
- The newly installed Hermes MCP resolved the old format blocker. It reports 4,638 Metro modules, 42,307 functions and 55,800 strings. Targeted module/function analysis and selected raw assembly checks were completed; no full-bundle decompilation was attempted.
- All claims are static or derived from decompiler output. Module labels can be reconstructed; Java class names are separate from Metro/function IDs. Recovered source contains incorrect variable reuse, unresolved closures and empty helper bodies; never execute it as original application source.
- Do not modify the APK, bypass Pairip, collect credential values, or invoke production APIs to validate a hypothesis. No app execution, production API call, secret scan, credential harvesting, payment/order placement or runtime capture was performed. An embedded credential literal encountered incidentally in a targeted result was redacted from four derived files; no literal is reproduced in reports.

## Current coverage

| Area | Completed evidence | Remaining scope |
|---|---|---|
| Framework/startup | Manifest, aliases, Pairip inheritance, RN hosts, package registration, native initialization, JS App/navigation composition | Final HotUpdater path-selection branch and exact installed bundle state |
| Navigation | M2073/F2075 native-stack setup, F13640 route registry, F13638 state-change analytics | Full deep-link resolver, final login/onboarding transition and every lazy-screen edge |
| Networking | BaseApiService M1152, headers M1206, fetch port M2618, environment M2620, retry M1618/M1619 | Runtime hostname/config values and all middleware branches; no server behavior established |
| Authentication | OTP builders F11284/F11288, selectors/reducer, verify flow M1652, customer details, MMKV session adapter M2625 and service M1127 | Refresh protocol, full logout ordering, alternate Rapido sign-in/UI path |
| Discovery/menu | Home M3347 → M3775 → M2637, feed/pagination/curated-list request builders, restaurant-page M1758/M1780 | Exhaustive query/cache/filter variants and backend ranking/serviceability implementation |
| Search | Recommendations/grouped-food/menu/similar-restaurant call sites, F18073 assembly, navigation/history modules identified | Complete debounce, cancellation, ranking and history lifecycle |
| Cart | Reducer F11133, totals helpers, restaurant conflict state, M1815 cart API, M1833 MMKV persistence, preflight builders | All price equations, action edge cases, complete persistence scheduling/middleware |
| Checkout | Order/status/payment verification builders checked in assembly; PaymentService, gateway selection, Juspay callbacks/backend checks, completion polling | All terminal status memberships and callback edges; server idempotency; custom UPI JS caller |
| Location | Selected location service, geolocation/native correlation, geocoding/places/serviceability call sites and caching/deduplication | Full accuracy/provider/fallback policy, retention, address lifecycle and consent |
| Order tracking | GET order/rider builders F17071/F17078, usePollingManager F18662 and PollingService; remote-config intervals, cleanup/final-state branches | Actual runtime intervals, all terminal states, additional push paths |
| Analytics | Naming F18921, materialization F18918, CleverTap sink F31972 checked in assembly; login/cart/checkout/search/location helpers and native correlations | Complete schema/consent validation, runtime selection per caller, SDK fan-out and Incognia business reachability |

## Durable artifacts and tool state

Installed tools: `tools/hermes/hermes-mcp`, `tools/hermes/hermes-decomp` (CLI advertises HBC 40–99). Local MCP initialize reported rmcp version 2.1.0. The live tool catalog did not expose direct Hermes connector methods; the installed server was queried over stdio via `analysis/hermes/query_mcp.py` under REA `capture_process_scenario`. REA evidence observes the analysis-tool run, not execution of the Android target. Input/tool hashes are in `reports/hermes-artifacts.json`.

The query adapter caches exact tool/argument pairs in `analysis/hermes/mcp/<tool>-<argument-hash>.json` and companion `.txt`. Reuse these results before making any new query. It initializes and loads the selected HBC per invocation and terminates the owned Hermes server on exit. No persistent Hermes process is intentionally left running. The earlier archive/native REA session was closed. Saved exports are the portable source of evidence; do not assume retained server state survives restart.

Useful read-only MCP operations already used: file_info, list_modules, dump(functions metadata only), xref_search, module_exports, decompile_module, decompile_function, disassemble and function_info. No patch/inject/create/frida/secrets tools were used. Function IDs and module IDs must not be interchanged; selected Metro factories follow M+2, but nested functions do not.

`reports/hermes-artifacts.json` lists retained response paths, byte sizes, current SHA-256 hashes, tool hashes and credential-redaction provenance. REA captured response hashes can predate redaction; use that manifest for the retained sanitized file digest. Do not regenerate sanitized outputs simply to recreate the unredacted bytes.

## Evidence exports and reports

| File | Bytes at checkpoint | Records | Formal residual unknowns |
|---|---|---|---|
| [rea-evidence.json](rea-evidence.json) | 6517300 | 93 | 0 |
| [rea-evidence-hermes.json](rea-evidence-hermes.json) | 761810 | 50 | 40 |
| [rea-evidence-hermes-analytics.json](rea-evidence-hermes-analytics.json) | 209411 | 20 | 16 |

Exports originate from separate sessions and record counts must not be summed as unique observations without deduplicating evidence IDs. Native bundle remains the original 93-record artifact. Process residual unknowns describe sampled process trees, environment/identity and unobserved network/filesystem effects; they are not a runtime finding about Ownly. Narrative business unknowns remain even where a bundle has no formal unknown records.

Existing reports: architecture.md, startup-flow.md, tracking-inventory.md, workflows.md, method-evidence.md, evidence-index.md, AndroidManifest.xml, package-overview.txt, feature-flow-hermes.md, hermes-tracking.md, hermes-evidence-index.md and hermes-artifacts.json. `architecture-native-v1.md`, `workflows-native-v1.md`, `tracking-inventory-native-v1.md` preserve the original native reports; current versions add continuation notices. `package-overview.txt` predates this investigation pass and was preserved, not treated as new proof.

The following three complete saved report snapshots retain the actual findings, modules/functions, dependencies, request paths, native correlations, snippets, evidence IDs, confidence levels and analysis boundaries. Their original files remain unchanged. Relative links resolve from reports/.

---

## Checkpoint snapshot: feature-flow-hermes.md

# Hermes feature-flow reconstruction — Ownly 2.0.7

The HBC is byte-identical to the prior APK asset: SHA-256 `b6f904c723cf894e03bf2e6bb0400015c288b78ad855f1eb825965d1654511a3`, 20,053,204 bytes, Hermes magic `c61fbc03c103191f`, version 98. Local Hermes MCP (`rmcp` server version 2.1.0) reports 42,307 functions, 55,800 strings, 4,638 Metro modules and global F0. Metro module IDs and function IDs are different namespaces; for the inventoried factories M0=F2 and the selected factories follow M+2. Nested functions have independent IDs recorded below. Module labels are decoder reconstructions, not original file paths or Java class names.

This pass used the installed Hermes MCP over stdio, launched by `analysis/hermes/query_mcp.py` under REA `capture_process_scenario`. No direct Hermes connector was exposed in this chat, so local stdio was used instead. Saved JSON contains exact tool selectors/responses; TXT contains reconstructed JavaScript, assembly or metadata. REA captures record the analysis tools running, not the Android application. Provenance: [rea-evidence-hermes.json](rea-evidence-hermes.json), [hermes-evidence-index.md](hermes-evidence-index.md), [hermes-artifacts.json](hermes-artifacts.json). Prior 93-record JADX bundle remains untouched.

Confidence: **high-static** = explicit bytecode instructions/metadata or simple unambiguous reconstructed calls; **medium-derived** = full-module reconstruction with async/closure uncertainty; **unresolved** = no adequate supporting chain. No runtime, backend behavior, credentials, environment values or production API responses were acquired. Source-like output has wrong register-variable reuse, empty helper bodies and unresolved closures; it is not executable recovered original JavaScript. Important request builders were checked against raw assembly. In particular, apparent `path.phoneNumber`, `endpoint.headers` and `type.type` after reassignment are decoder defects; original parameter access is preserved by the assembly.

## Root, navigation and API architecture

[M0/F2](../analysis/hermes/mcp/decompile_module-0bf214602666.txt) imports App M732/F734 and uses AppRegistry registration; [M732/F734](../analysis/hermes/mcp/decompile_module-ce0b2a9b1644.txt) imports Navigation M2073/F2075, CartInitializer M2020, auth/store M1127, CleverTap M1669, HotUpdater M1696 and other initialization modules. Earlier JADX MainActivity.b0 returns `consumerapp`; no consumerapp xref was found by the decoder search, so do not claim the literal registration-name edge was independently proved by that query. App's reconstructed initialization schedules SDK/setup work through InteractionManager and includes explicit Firebase analytics enablement, CleverTap/Incognia initialization and Juspay prefetch. Exact callback timing is not runtime-observed.

[M2073/F2075](../analysis/hermes/mcp/decompile_module-de60c5160b42.txt) creates a native stack navigator and Navigation function F13640. Route declarations include SplashScreen, LoginScreen (M2495), OnboardingScreen (M2598), Home (M3341), Search, SearchResults, RestaurantListing/RestaurantListingNova, RestaurantPage (M3924), RestaurantSearchPage (M4068), CartPage (M4074), OrderPlaceStatus, OrderTrackingScreen (M3846), PaymentFailedScreen, AddressesScreen, LocationScreen, LocationSearchScreen and MapScreen. MainActivity.onNewIntent forwards to RN; the precise JS deep-link resolver is still not reconstructed. Navigation state change F13638 records screen breadcrumbs and forwards navigationAnalytics. **High-static** route membership; **medium-derived** root composition.

Two network layers coexist:

- [M1152/F1154](../analysis/hermes/mcp/decompile_module-2e965c8a984f.txt) BaseApiService exposes request/requestViaXhr, builds URL from runtime base URL plus endpoint, assembles headers and invokes fetch/XHR. [M1206/F1208](../analysis/hermes/mcp/decompile_module-d2ad90e40f73.txt) builds auth/device/location/cart/session headers. Header construction includes symbolic API key, Bearer token, appid/appversion, X-Version-ID, X-Device-Channel, deviceid and Content-Type; keys/values were not harvested.
- [M2618/F2620](../analysis/hermes/mcp/decompile_module-ed99bc9888ea.txt) createFetchHttpPort plus [M2620/F2622](../analysis/hermes/mcp/decompile_module-17fb9209860a.txt) createRnEnv and M2615 bind the portable request context M2614. [M1619/F1621](../analysis/hermes/mcp/decompile_module-90809e417d01.txt) requestWithRetry executes `context.http.request(request)` and normalizes results/errors. [M1618/F1620](../analysis/hermes/mcp/decompile_module-618bd3767ef2.txt) defaults to maxAttempts=1, baseDelayMs=250, maxDelayMs=5000, jitterRatio=0.2, retry statuses 408/429/500/502/503/504 and safeMethodsOnly=true. These defaults do not prove repeated POST attempts; individual calls can override policy.
- [M1154/F1156](../analysis/hermes/mcp/decompile_module-98d41c5219bb.txt) resolves environment from runtime override/config or bundle ID; com.ownly.customer is recognized as prod. API base URL comes from `OWNLY_API_BASE_URL`; credential-bearing settings remain symbolic. Runtime override/config means no hostname is inferred merely from package name.

Native correlation: RN NetworkingModule.sendRequest → sendRequestInternalReal, previously inspected through JADX, supplies the underlying HTTP bridge. The JS transport uses fetch/XHR APIs, but this pass does not prove every request crosses that class (native SDK traffic is separate).

## Login and authentication

Modules: [M1635/F1637](../analysis/hermes/mcp/decompile_module-ebe0ab07cfac.txt) authFlowReducer (F11264), [M1639/F1641](../analysis/hermes/mcp/decompile_module-dc2f7d28c07e.txt) selectors, [M1644/F1646](../analysis/hermes/mcp/decompile_module-efb79fc8f643.txt) request OTP, [M1647/F1649](../analysis/hermes/mcp/decompile_module-9912400322d8.txt) verify OTP, [M1652/F1654](../analysis/hermes/mcp/decompile_module-15dadc5250a6.txt) verify flow, [M2625/F2627](../analysis/hermes/mcp/decompile_module-da3ed9de961f.txt) runtime session adapter, [M1127/F1129](../analysis/hermes/mcp/decompile_module-98e1a0b2d216.txt) native RN auth/store service.

**High-static** request-builder reconstruction (assembly checked):

```js
// M1644 F11284, analyst reconstruction from bytecode
request = {method: 'POST', url: input.path ?? '/api/v1/otp',
  body: {phoneNumber: input.phoneNumber, smsType: input.smsType ?? 'otp',
    ...(input.channel ? {channel: input.channel} : {})},
  timeoutMs: input.timeoutMs, credentials: input.credentials};
// M1647 F11288
request = {method: 'POST', url: input.path ?? '/api/v1/otp/verify',
  body: {phoneNumber: input.phoneNumber, otp: input.otp},
  timeoutMs: input.timeoutMs, credentials: input.credentials};
```

F11284 accesses phoneNumber at 0x2d, smsType 0x37, optional channel 0x49; F11288 accesses phoneNumber at 0x2d and otp at 0x37. Request runner delegates to requestWithRetry. Selectors use ten-digit phone regex and a four-digit normalized OTP; request/verify loading flags gate submissions. Reducer actions include requestOtpStart/Success/Failure, verifyOtpStart/Success/Failure, backToPhone and profile submission. Action creators sanitize phone digits to ten and OTP digits individually.

**Medium-derived** verification flow F25454: runVerifyOtp → require returned token → storeAuthSession(token,user) → runFetchCustomerDetails (M1643; GET `/api/v1/customer/details`) → store customer details → return token/user/customerDetails/isNewUser. `Wrong OTP. Please try again.` is a packaged fallback error. M2625.storeAuthSession (F15248) writes `authToken` and serialized `user`; storeCustomerDetails writes serialized `customerDetails`. M1127 initializes `createMMKV()` from M1133 and provides getStoredToken/getStoredUser/getStoredCustomerDetails/logout/OTP callback methods. This now ties auth state to the earlier native MMKV directory bridge. No token values were retrieved. Native OTP Verify.getOtp/requestOtp is SMS autofill support; it is not the verification API itself.

Additional auth alternatives are packaged: M1641 runExchangeRapidoToken and M1649 runSignInWithRapidoFlow. Their presence is recorded, but the full alternate UI branch and exchange contract are not claimed verified. Token refresh remains unresolved; the earlier zero `refreshToken` substring xref does not establish absence of refresh behavior. Logout callback ordering and final login/onboarding navigation remain partially traced.

## Restaurant discovery and menu loading

[M3347/F3349](../analysis/hermes/mcp/decompile_module-5f3a77d7bb3d.txt) useHomeViewModel → [M3775/F3777](../analysis/hermes/mcp/decompile_module-d4a261dc6fe4.txt) fetchHomeNovaApiPage (F31233) → [M2637/F2639](../analysis/hermes/mcp/decompile_module-cefa97758282.txt) fetchHomePageFeed (F28672) → requestWithRetry. Adapter forwards lat/lng, initial/serviceability mode, offset/pageSize, filters and veg-mode request headers, then adapts the server feed response. Home view model has loading/ready/error states, refresh/serviceability checks and pagination merges. Backend ranking, serviceability determination and feed composition are server-side unknowns.

**Medium-derived** call-site contract: POST `/api/v1/home-page-feed`; body fields lat,lng,isInitialCall,serviceability, optional pagination and sanitized filters; headers X-Selected-Lat/X-Selected-Lng. [M2636/F2638](../analysis/hermes/mcp/decompile_module-d324fb120845.txt) fetchPaginatedRestaurantFeed targets POST `/api/v1/feed/getPaginatedRestaurantFeed`, with location/filters/page/size and conditional offset/sort. [M2639/F2641](../analysis/hermes/mcp/decompile_module-2235243a6d54.txt) fetchCuratedListBff targets POST `/api/v1/feed/bff/curated-list`, forwards curatedListId and location/initial-call metadata. These are source-linked request candidates, not observed live endpoints. Async reconstruction is imperfect; exact fallback-variable assignments should be checked in assembly before implementation reuse.

Restaurant detail path: [M1780/F1782](../analysis/hermes/mcp/decompile_module-aca9dea644b4.txt) fetchRestaurantPageRaw/response mapper → [M1758/F1760](../analysis/hermes/mcp/decompile_module-58ec3c60df34.txt) createFetchRestaurantPageRequest → requestWithRetry. POST `/api/v1/restaurant-page` uses query `brand-id` or `restaurant-id`, optional curatedListId; initial payload menu=true/details=true/outlets=false with lat/lng; outlet payload reverses those flags. Optional search filters/location/page/size and X-Search-Id occur in reconstruction. Server response is mapped into domain data. Brand/outlet prioritization, malformed-response behavior and all component query variants are not exhaustively verified.

## Search

[M3914/F3916](../analysis/hermes/mcp/decompile_module-bd22671ae957.txt) SearchService contains getSearchRecommendations, restaurant-grouped food lookup, menu-items lookup and similar-restaurant lookup. Portable counterparts: M3580 recommendations, M3578 grouped results, M3579 menu items, M3583 similar restaurants. Their default paths are listed below. M3917 SearchNavigationService and navigation registry connect search results to entity destinations; full debounce/cancellation/filter-ranking implementation remains partial.

**High-static**, M3580 F18073 (assembly 0x2d searchString, 0x37 location, 0x40 cityId):

```js
request = {method: 'POST', url: input.path ?? '/api/v1/search/get-search-recommendations',
  body: {searchString: input.searchString, location: input.location, cityId: input.cityId},
  timeoutMs: input.timeoutMs, credentials: input.credentials};
```

M3914 response code inspects success/data.EntityResults, returns suggestions/searchId, caps suggestions with MAX_SUGGESTIONS and handles the server message `search string length should be greater than 3`. This message is a client error-handling branch, not independently confirmed server validation. Recent searches/history service M3896 and analytics M3893 are identified but persistence policy and complete history lifecycle are not exhaustively traced.

## Cart

[M1611/F1613](../analysis/hermes/mcp/decompile_module-55664534f7b4.txt) cartReducer F11133 and [M1609/F1611](../analysis/hermes/mcp/decompile_module-c7c54a0044cb.txt) calculateCartTotals F11123, F11898 supply pure state/totals functions. Reducer inspects restaurant conflicts, keeps pending attempted item/quantity, applies customizations and finalizes totals. The conflict state has current/new restaurant IDs and names, attempted item and needsCustomization. Exact action cases and price equations should be read from saved code/assembly before asserting all edge cases; reconstruction contains faulty Object.assign variable recovery.

[M1815/F1817](../analysis/hermes/mcp/decompile_module-647a89aa8499.txt) cartApiService.processCart calls POST `/api/v1/cart`; [M1833/F1835](../analysis/hermes/mcp/decompile_module-d145acad85a3.txt) CartStorageService implements save/load/clear (batched and legacy paths), item/restaurant/address/instruction/totals/API-response storage, JSON parsing and cleanDataForStorage. It depends on MMKV M1133. Thus MMKV usage is established for this JS cart service, while WatermelonDB registration from the prior pass still does not prove it owns cart state. M1832 persistence queue/debounce helpers and M2010 middleware were inventoried; their full call schedule was not decoded.

Checkout preflight [M1622/F1624](../analysis/hermes/mcp/decompile_module-d128930ef2a2.txt) F11167 builds active-restaurant cart payload and groups items by foodId with quantity/customizations. F11168 dispatches a request body returned by that builder; default path `/api/v1/cart`, credentials default include. Failures for empty restaurant/cart input are represented. Keep local totals distinct from returned server pricing/availability validation.

## Checkout and payment

Request builders checked against assembly:

```js
// M1616 F11145
if (!input.checkoutPayload || typeof input.checkoutPayload !== 'object' ||
    !('cart' in input.checkoutPayload)) throw Error('Invalid checkout payload: missing cart data');
request = {method:'POST', url:input.endpoint ?? '/api/v1/orders',
  body:input.checkoutPayload, headers:input.headers, credentials:input.credentials ?? 'include'};
// M1620 F11163
url = input.endpoint ?? ('/api/v1/orders/' + input.orderId);
// M1621 F11165
url = input.endpoint ?? ('/api/v1/get-payment-details/' + input.orderId);
// Both status/verification request objects use GET and credentials default 'include'.
```

F11145 validates cart membership around 0x4a–0x52, chooses endpoint at 0x72, copies payload at 0x90 and headers at 0x9a. F11163/F11165 read orderId at 0x16 and concatenate default path at 0x39/0x3d. **High-static** builder fields, **medium-derived** full orchestration.

[M2030/F2032](../analysis/hermes/mcp/decompile_module-dfe4c074a492.txt) PaymentService processOrder/startPayment tracks paymentInProgress/currentOrderId and handles AppState return recovery. Its configured polling fields are retryDelayMs=5000, maxAttempts=60, maxConsecutiveFailures=8. [M2055/F2057](../analysis/hermes/mcp/decompile_module-caa9db87dbab.txt) resolves gateway aliases to Cashfree or Juspay, defaulting to Cashfree for unknown values. [M2049/F2051](../analysis/hermes/mcp/decompile_module-476f89522c19.txt) JuspayGateway.verifyWithBackend checks getPaymentDetails; [M2035/F2037](../analysis/hermes/mcp/decompile_module-a91a9ea30145.txt) PaymentHandlers.handleSuccess calls [M2036/F2038](../analysis/hermes/mcp/decompile_module-ee18bd8ea7ed.txt) waitForOrderCompletion, which queries order status and branches on status sets, cancellation and attempt/failure limits. Complete terminal status memberships remain to be corroborated separately; do not infer a server order state machine from names alone.

Juspay SDK path [M2050/F2052](../analysis/hermes/mcp/decompile_module-de4242d42148.txt) callProcess F13529 → wrapper M2051/native fallback `NativeModules.HyperSdkReact` → previously inspected Java `in.juspay.hypersdkreact.HyperSdkReactModule.process(String)` → private process → HyperServices.process(activity,json). HyperEvent listeners handle SDK callbacks; SDK completion is followed by backend verification/order polling. The custom UPIUrlHandlerModule.openUPIUrl previously analyzed is a separate available bridge; its precise JS checkout caller was not established in this pass.

[M2037/F2039](../analysis/hermes/mcp/decompile_module-d6091f488677.txt) contains createOrder, getOrderStatus, getPaymentDetails and a POST cancellation-status update path. These are client requests only; no payment/order action was performed. Client duplicate-success guards and cancelable polling exist; server idempotency is unresolved.

## Location and order tracking

[M2016/F2018](../analysis/hermes/mcp/decompile_module-05f406ee3c2a.txt) LocationService composes [M1661/F1663](../analysis/hermes/mcp/decompile_module-54941cfbd210.txt) LocationFetcher and [M1660/F1662](../analysis/hermes/mcp/decompile_module-35f042ba0c2d.txt) GeocodingService, selectedLocation state, update subscribers and manualSelectionVersion. GeocodingService caches/deduplicates requests and calls POST `/api/v2/geocoding` and `/api/v2/places/autocomplete`; M2063 ServiceabilityReasons calls POST `/api/v1/serviceability/check`. These call sites use symbolic serviceability credential headers. Address caching/selection is client-side; geocoding/serviceability results are backend data. Native geolocation correlation: GeolocationModule.getCurrentPosition/requestAuthorization/startObserving from the first pass; manager/provider policy and full accuracy/fallback semantics remain unverified.

Order data: [M3316/F3318](../analysis/hermes/mcp/decompile_module-a7932396fe43.txt) F17071 builds GET `/api/v1/orders/` + encodeURIComponent(orderId), trimming trailing slash from overridable path. Rider data: [M3317/F3319](../analysis/hermes/mcp/decompile_module-1c4f8b65d99a.txt) F17078 builds GET `/api/v1/order/` + encodeURIComponent(orderId) + `/track` (singular `order` is observed). F17071 reads orderId at 0x19 and encodes it at 0x6a–0x74; F17078 appends `/track` at 0x84. M3316/M3317 normalize result payloads and route through requestWithRetry. No data values or credentials were acquired.

[M3855/F3857](../analysis/hermes/mcp/decompile_module-8f1db563bc3e.txt) usePollingManager F18662 → [M3856/F3858](../analysis/hermes/mcp/decompile_module-eec27ccafc05.txt) pollingService.startPolling. Order intervals come from remoteConfig.orderPollingIntervals and rider intervals from remoteConfig.riderPollingInterval. Defaults in the polling layer include maxDuration=7,200,000ms, maxRetries=3, backoffMultiplier=1.5; it polls immediately then starts an interval, and exposes stop/restart/updateInterval methods. Hook reacts to status changes, starts rider polling when assigned, stops on final states and explicitly handles DELIVERED/ORDER_DELIVERED. Cleanup stops both pollers. This establishes a client polling implementation; it does not exclude additional push notifications or prove exact runtime intervals.

## Analytics and native evidence correlation

See [hermes-tracking.md](hermes-tracking.md) for bytecode-linked event-name generation, materialization, dispatch, login/cart/checkout and screen/location context. The earlier native reports remain authoritative for Java bridge mechanics: CleverTap recordEvent/onUserLogin, AppsFlyer.logEvent, Firebase.logEvent, Incognia login/payment events. This pass recovers actual JS event-generation functions and a CleverTap sink; Incognia business event reachability and consent must still be distinguished from mere native capability.

## Residual work

Coverage now includes all requested feature areas with concrete modules, request builders and dependencies, but is not an exhaustive behavioral reconstruction. Verify remaining async/closure edges using targeted disassembly/IR, especially final UI navigation, auth refresh/logout, menu cache integration, search debounce/cancellation, cart formula edge cases, all payment/order terminal statuses and configured polling intervals. Resolve actual runtime base host only if supplied nonsecret config evidence permits; never extract credential values. Check whether HotUpdater changes the installed JS version before applying packaged-code conclusions to a live installation. No full-bundle decompile, Pairip bypass, secret scanner, app execution or production API interaction was used.

---

## Checkpoint snapshot: hermes-tracking.md

# Hermes analytics and event-generation findings

Target: `analysis/hermes/ownly.hbc`, Hermes v98, SHA-256 `b6f904c723cf894e03bf2e6bb0400015c288b78ad855f1eb825965d1654511a3`. Read together with [native tracking inventory](tracking-inventory.md) and [method evidence](method-evidence.md). All findings are static client-side reconstructions. No SDK execution, secrets scan, credential collection, live payload capture or API request was performed.

Local Hermes MCP 2.1.0 was queried through `analysis/hermes/query_mcp.py` under REA `capture_process_scenario`. Complete MCP responses and text are saved in `analysis/hermes/mcp/`. REA process evidence observes the analysis command and response-file digests, not app behavior. Captures in this scope: `ev_9e1420f9554bcd040704b6eb8c680eb48cdf8e8e9be1014da5d5b049edf04570` (targeted module analysis), `ev_4c0bdf67e99a879b6ca58514c38db4ebc99d7efe1a77dec1aa91a861da5b4803` (exports and sink assembly), `ev_bb94f25d1aea91946ac8b03fe37be5c3e5afa73bdadd0053f50dbce561a8d105` (event assembly and helper analysis), `ev_10f97a5564953a3ecbc887612ad713d9351bc6b6f3c4df3db0adabbfb0600be7` (login/cart/checkout helpers). These four records are preserved in [rea-evidence-hermes-analytics.json](rea-evidence-hermes-analytics.json); they are not in the historical 93-record bundle or the parent session's separate Hermes export.

## Architecture and dependencies

There are parallel telemetry paths, rather than proof that every event goes to every SDK:

1. M1669 / factory F1671 (`CleverTapService`) exposes standard screen, navigation, interaction, business, system, error and impression operations, plus legacy named-event wrappers. Dependencies include CleverTap adapter M1671, AppsFlyer M1674, Firebase M1681, runtime session M1693, queue M1713, context M1714/M1715/M1718/M1719 and app store M2011.
2. M1976 standard emitters (F13179 screen view, F13181 navigation, F13183 interaction, F13185 business, F13187 system, F13189 impression batch) delegate to CleverTapService. Its `getCollectorsForStandardEvent` selects `[]` for navigation and `["clevertap"]` otherwise. This is a declared routing choice; whether all callers honor it requires complete call-site coverage.
3. M3939 / factory F3941 constructs an additional configurable analytics runtime via M3940 → M3946 `createAnalytics`, with console sink M3959 and CleverTap sink M3960. It exports `analytics`, `restaurantPageAnalytics` and `restaurantSearchAnalytics`. A background AppState callback calls `analytics.flush()`.
4. M1713 / factory F1715 implements an asynchronous analytics job queue. Export F11728 `enqueueAnalyticsJob` defaults priority to `high` and returns a Promise; F11729 flushes; F11731 returns stats; F11721 schedules low-priority work. Module contains low-priority eviction and queue-pressure logic, but exact capacity/timing guarantees were not validated against assembly.

M3939's global context reconstructs app platform/version/build/model/OS, HotUpdater bundle ID, device ID, runtime session ID, actor type `customer`, actor ID from stored customer/user data with anonymous fallback, selected city/area/address, current and selected coordinates, current/previous screen. These are *field definitions and access paths*, not collected values or proof of transmission. M1669 F25520 `buildGlobalFields` has overlapping fields and adds event ID/time/schema metadata.

## Event naming and payload materialization — assembly corroborated

M3953 factory F3955 exports **F18921 `generateEventName`**. Bytecode validates this reconstruction:

```js
// Analyst reconstruction from F18921; not original source.
if (config.type === "interaction") {
  return config.type + "_" + config.screen + "_" + config.entity
    + (config.element ? "_" + config.element : "") + "_" + config.action;
}
return config.type + "_" + config.entity;
```

At F18921 offsets 0x39–0x4a it loads type/screen/entity/element; 0x76 loads action; 0x88–0xa4 constructs the interaction name. Non-interaction concatenation is 0x10–0x30. Confidence: high for this formula. The full decompiler mutates its apparent `type` parameter during destructuring; use assembly to resolve that display artifact.

M3952 factory F3954 exports **F18918 `materializeAnalyticsEvent`**. Assembly shows pageContext, payload, then globalContext copied into the same object (loads at 0x0a, 0x4a, 0x85), using helper closure F31903. The module's predicate accepts null/string/boolean/finite-number property values; nested structures are not treated as generic event props by this helper. Interaction fields are then assigned from config: `ui_screen`, `ui_component`, optional `ui_element`, `action`; noninteraction entity/payloadAction assignment respects includeEntityInPayload. Finally event_name, event_type, schema_version, ts_ms and event_id are written at 0x17b–0x1b5. Confidence: high for merge order and metadata writes; predicate detail is derived from module output, not separately assembly-checked.

M3960 factory F3962 builds a CleverTap sink. **F31972 `track`** rejects non-string/empty event_name, copies the event properties, removes event_name, and invokes native adapter `recordEvent(name, props)`. F31972 0x28 is GetById `recordEvent`; 0x52 deletes event_name; 0x57 is Call3 with name and copied props. This assembly corrects decompiler output that displays incomplete temporary variables/Object.assign arguments. The same module supports identify → onUserLogin/profile, profile patch → profileSet, and finite, range-checked lat/lng → setLocation; those identities/property schemas are reconstruction, not observed real identities.

## Recovered named-event helpers

| Module/function | Client helper behavior | Concrete event names / field schema | Confidence |
|---|---|---|---|
| M1669 F25523 trackSignUp | Legacy CleverTap event plus Firebase and AppsFlyer wrappers | `sign_up`; Firebase `sign_up`; AppsFlyer `af_complete_registration` | Derived from module body; caller occurrence not independently verified |
| M1669 F25524 trackLogin | Calls incogniaService.trackLogin("AUTHORIZED", props), this.trackEvent("login", props), Firebase login and AppsFlyer login | `login`, `af_login` | High for helper call order, separately targeted function output; not proof of server-authorized login |
| M1669 F25529 trackAddToCart | Calls Firebase ADD_TO_CART and AppsFlyer ADD_TO_CART with the same props | Native names `add_to_cart`, `af_add_to_cart`; embedded payload event_name `food_item_added_to_cart`; food_item_name/id, cart_id, restaurant_id, price, quantity | High for helper; no direct this.trackEvent call in this function |
| M1669 F25530 trackViewCart | Firebase VIEW_CART and AppsFlyer VIEW_CART | `view_cart`, `af_view_cart`; payload page_open/cartpage and cart/order value fields | Derived from module body |
| M1669 F25531 trackBeginCheckout | Firebase BEGIN_CHECKOUT and AppsFlyer INITIATED_CHECKOUT; normalizes discount/delivery values for Firebase payload | `begin_checkout`, `af_initiated_checkout`; payload event_name `cart_proceedtopayment_button_pressed`, screen_name cartpage, cart_id, cart totals/counts, restaurant name/id, total_payable, gst; optional other_price_components | High for targeted helper; does not prove payment succeeds |
| M1674 F11484 trackAppsFlyerEvent | Calls AppsFlyer wrapper logEvent(name,props,success,failure), with default empty props | Constants also include `af_app_opened`, `af_onboarding_completed` | Derived; exact RN native bridge corroborated below |
| M1681 F11551 trackFirebaseEvent | Calls modular getAnalytics/logEvent; F11553 returns instance ID; F11555 sets user ID | Constants app_open, sign_up, login, add_to_cart, view_cart, begin_checkout | Derived; async decompiler retains imperfect state-machine variables |

## Search and location event generation

M3893 factory F3895 declares 13 targeted search helpers. Export mapping: F18768 query submitted, F18769 screen context loaded, F18770 recent-search tap, F18771 suggestion tap, F18772 popular-in-area tap, F18773 category-grid tap, F18774 restaurant tap, F18775 no results, F18776 suggestion impressions, F18777 result impressions, F18778 feedback prompt tap, F18779 feedback context loaded, F18780 feedback submitted.

F18768 prepares a standard interaction with SEARCH_PAGE / SEARCH_BAR / SEARCH_INPUT / action `submit`; includes `prop_search_query` from query, optional `prop_search_query_id`, and result-count properties derived from resultsByType; dispatches through M1976.emitStandardInteraction and catches failure. F18770 similarly uses RECENT_SEARCHES / RESULT_CARD / tap and query/query-id. These are helper-level trigger semantics; exact invocation from each UI callback remains unverified here. Optional merge destinations in the decompiler are imperfect, so do not treat all conditional props as exact wire payloads until assembly checked.

M2015 factory F2017 exports 20 location helpers: GPS enabling attempt/result, address save/delete, popup impression, location selection, manual-location-added, current-location tap, saved/recent/prediction taps, and permission-dialog actions. **F13388 trackLocationSelected** calls M1976.emitStandardBusiness with entity LOCATION and action `selected`, optional prop_cart_id, and ctx_screen from current route → getAnalyticsScreenForRoute, falling back to LOCATION_SELECTION_PAGE. F13391/F13392 are GPS enabling attempt/result, F13386 address saved, F13393 use-current-location tap. These expose how user actions are intended to be instrumented, not observed GPS or address values.

## Correlation to earlier native REA/JADX findings

| Hermes path | Earlier native endpoint | Native evidence ID |
|---|---|---|
| M3960 F31972 / M1669 legacy or queued emission → JS adapter M1671 recordEvent | com.clevertap.react.CleverTapModule.recordEvent → cleverTapModuleImpl.G1 | ev_d032b72b5e05525d8e79f14420eb4e04ca1804ed06c1251e1b6c020f0fb1516c |
| M3960 identify / CleverTapService identification | com.clevertap.react.CleverTapModule.onUserLogin → cleverTapModuleImpl.d1 | ev_70e66967e73bac45452e1cd345231c70763579dc232024cb1f78d0503faad259 |
| M1674 trackAppsFlyerEvent → logEvent | com.appsflyer.reactnative.RNAppsFlyerModule.logEvent → AppsFlyerLib.logEvent | ev_a60d8bc32d5e8fe0f905a0f8ff39c9eed545bd7528772dc53c28f74939e06fb9 |
| M1681 trackFirebaseEvent → modular analytics logEvent | io.invertase.firebase.analytics.ReactNativeFirebaseAnalyticsModule.logEvent | ev_b152f9c18b2d94f3a9fe005d19aaca6cb837d07f661292c46698d9f3106cc1a9 |
| M1669 F25524 → incogniaService.trackLogin | com.incognia.reactnative.IncogniaModule.sendLoginEvent | ev_abb5282c8fd4ea23585c492378d785c846b448bbb05d34669a75925d0d58d262; intervening JS service bridge not traced in this scope |

## Remaining limitations and next probes

Decompiled JS is not guaranteed executable original source: async state machines, object-spread destinations, temporary names and inlined empty helpers display artifacts. Confidence is explicitly reduced for unverified control/dataflow. The sampled event catalog is not exhaustive. Event helper existence is distinct from actual screen dispatch and SDK transport. No server behavior, analytics endpoint, runtime consent state, real device/user/coordinate value, actual sink delivery, timing, or event upload was observed.

Next work should trace selected event helpers to actual UI callbacks and decode individual uncertain field merges, audit M3946 scheduling/lane limits against assembly, connect incogniaService to its native module, and identify which runtime is selected by each restaurant/home/search flow. Native manifest collection defaults remain as documented previously; JS runtime configuration may override them. No need to repeat already captured modules/functions.

## Saved result links

- [M1669](../analysis/hermes/mcp/decompile_module-f83d601cad9d.txt); factory F1671.
- [M1674](../analysis/hermes/mcp/decompile_module-773deed94914.txt); factory F1676.
- [M1681](../analysis/hermes/mcp/decompile_module-cbb2822dc75a.txt); factory F1683.
- [M1713](../analysis/hermes/mcp/decompile_module-672b56722771.txt); factory F1715.
- [M1976](../analysis/hermes/mcp/decompile_module-2ef794eb7974.txt); factory F1978.
- [M1996](../analysis/hermes/mcp/decompile_module-c8333e36095d.txt); factory F1998.
- [M2015](../analysis/hermes/mcp/decompile_module-db7a741512f4.txt); factory F2017.
- [M3893](../analysis/hermes/mcp/decompile_module-35e178e88f53.txt); factory F3895.
- [M3939](../analysis/hermes/mcp/decompile_module-8e2bd617255f.txt); factory F3941.
- [M3940](../analysis/hermes/mcp/decompile_module-12be9d3e81bf.txt); factory F3942.
- [M3946](../analysis/hermes/mcp/decompile_module-e97bdcbc26dd.txt); factory F3948.
- [M3952](../analysis/hermes/mcp/decompile_module-c85ff859aea6.txt); factory F3954.
- [M3953](../analysis/hermes/mcp/decompile_module-5794c9e7b7d9.txt); factory F3955.
- [M3959](../analysis/hermes/mcp/decompile_module-828908722be1.txt); factory F3961.
- [M3960](../analysis/hermes/mcp/decompile_module-81e64b9204ee.txt); factory F3962.
- [decompile_function F1671](../analysis/hermes/mcp/decompile_function-f5168afd4b86.txt).
- [decompile_function F18768](../analysis/hermes/mcp/decompile_function-7a4b68a495a5.txt).
- [decompile_function F13388](../analysis/hermes/mcp/decompile_function-85b9ffa23e6b.txt).
- [decompile_function F25524](../analysis/hermes/mcp/decompile_function-1795f5df510c.txt).
- [decompile_function F25529](../analysis/hermes/mcp/decompile_function-f413adc9fb11.txt).
- [decompile_function F25531](../analysis/hermes/mcp/decompile_function-c4f7705f584c.txt).
- [decompile_function F11728](../analysis/hermes/mcp/decompile_function-7feef2e395a5.txt).
- [disassemble F31972](../analysis/hermes/mcp/disassemble-715968c0758d.txt).
- [disassemble F18921](../analysis/hermes/mcp/disassemble-b76f7a72f375.txt).
- [disassemble F18918](../analysis/hermes/mcp/disassemble-777a358fec5b.txt).

---

## Checkpoint snapshot: hermes-evidence-index.md

# Hermes MCP evidence index

All outputs are derived from the verified HBC; source excerpts are reconstructed, not original JS. `hermes-artifacts.json` hashes current retained files. REA process captures in `rea-evidence-hermes.json` attest tool execution; they do not authenticate decompiler semantics. Selected captured hashes may predate credential-literal redaction; redacted files are marked in the artifact manifest.

| Module | Factory | Name (decoder label) | Dependencies | Saved source |
|---|---|---|---|---|
| 0 | F2 | unnamed | [1, 2, 3, 15, 38, 537, 732, 4462, 2092, 1160, 1158, 2583, 2592, 2594, 2589, 2590, 2573, 2593, 4635] | [decompile_module-0bf214602666.txt](../analysis/hermes/mcp/decompile_module-0bf214602666.txt) |
| 732 | F734 | App | [1, 2, 29, 74, 15, 733, 739, 768, 1127, 2020, 2060, 2073, 1669, 1673, 4339, 244, 1696, 538, 1153, 2581, 4599, 1813, 2430, 4601, 4161, 2416, 4603, 2050, 2012, 1682, 3207, 1158, 4520, 1157, 1225, 1587, 4604, 2612, 1719, 2011, 4607, 4608, 2572, 4609, 2442, 2770, 4629, 4630, 3686, 2512, 1799, 4634, 1117] | [decompile_module-ce0b2a9b1644.txt](../analysis/hermes/mcp/decompile_module-ce0b2a9b1644.txt) |
| 1127 | F1129 | unnamed | [1, 2, 5, 6, 15, 1128, 1130, 1131, 1133, 1206, 1152, 2004, 1225, 2018, 2019, 1850, 1851] | [decompile_module-98e1a0b2d216.txt](../analysis/hermes/mcp/decompile_module-98e1a0b2d216.txt) |
| 1133 | F1135 | unnamed | [1134, 1140, 1141, 1142, 1144, 1146, 1147, 1148, 1149, 1150, 1151] | [decompile_module-d957f98a5861.txt](../analysis/hermes/mcp/decompile_module-d957f98a5861.txt) |
| 1152 | F1154 | BaseApiService | [1, 2, 5, 6, 1127, 1153, 1157, 1205, 1206, 2017] | [decompile_module-2e965c8a984f.txt](../analysis/hermes/mcp/decompile_module-2e965c8a984f.txt) |
| 1153 | F1155 | API_CONFIGS | [1154] | [decompile_module-8caeab2c63f1.txt](../analysis/hermes/mcp/decompile_module-8caeab2c63f1.txt) |
| 1154 | F1156 | resolveRuntimeConfig | [1, 1155, 733] | [decompile_module-98d41c5219bb.txt](../analysis/hermes/mcp/decompile_module-98d41c5219bb.txt) |
| 1206 | F1208 | BaseHeadersService | [1, 29, 2, 5, 6, 15, 733, 1207, 1133, 1205, 1223, 1719, 1127, 1669, 1695] | [decompile_module-d2ad90e40f73.txt](../analysis/hermes/mcp/decompile_module-d2ad90e40f73.txt) |
| 1609 | F1611 | calculateCartTotals | [] | [decompile_module-c7c54a0044cb.txt](../analysis/hermes/mcp/decompile_module-c7c54a0044cb.txt) |
| 1611 | F1613 | cartReducer | [1, 71, 1609, 1612, 1598, 1607, 1613, 1614] | [decompile_module-55664534f7b4.txt](../analysis/hermes/mcp/decompile_module-55664534f7b4.txt) |
| 1616 | F1618 | runCheckoutOrder | [1, 2, 1617] | [decompile_module-b0485fd073cb.txt](../analysis/hermes/mcp/decompile_module-b0485fd073cb.txt) |
| 1617 | F1619 | unnamed | [1618, 1619] | [decompile_module-9fe25a7c356c.txt](../analysis/hermes/mcp/decompile_module-9fe25a7c356c.txt) |
| 1618 | F1620 | unnamed | [] | [decompile_module-618bd3767ef2.txt](../analysis/hermes/mcp/decompile_module-618bd3767ef2.txt) |
| 1619 | F1621 | requestWithRetry | [1, 2, 1618] | [decompile_module-90809e417d01.txt](../analysis/hermes/mcp/decompile_module-90809e417d01.txt) |
| 1620 | F1622 | runCheckoutOrderStatus | [1, 2, 1617] | [decompile_module-6c05bd4689f3.txt](../analysis/hermes/mcp/decompile_module-6c05bd4689f3.txt) |
| 1621 | F1623 | runCheckoutPaymentVerification | [1, 2, 1617] | [decompile_module-6dd1cc3f689b.txt](../analysis/hermes/mcp/decompile_module-6dd1cc3f689b.txt) |
| 1622 | F1624 | runCheckoutPreflight | [1, 2, 1623, 1617] | [decompile_module-d128930ef2a2.txt](../analysis/hermes/mcp/decompile_module-d128930ef2a2.txt) |
| 1635 | F1637 | authFlowReducer | [1636] | [decompile_module-ebe0ab07cfac.txt](../analysis/hermes/mcp/decompile_module-ebe0ab07cfac.txt) |
| 1638 | F1640 | selectCanRequestOtp | [1639] | [decompile_module-4bc7a2a5b768.txt](../analysis/hermes/mcp/decompile_module-4bc7a2a5b768.txt) |
| 1639 | F1641 | unnamed | [] | [decompile_module-dc2f7d28c07e.txt](../analysis/hermes/mcp/decompile_module-dc2f7d28c07e.txt) |
| 1641 | F1643 | runExchangeRapidoToken | [1, 2, 1617] | [decompile_module-9bd7edea0b59.txt](../analysis/hermes/mcp/decompile_module-9bd7edea0b59.txt) |
| 1643 | F1645 | runFetchCustomerDetails | [1, 2, 1617] | [decompile_module-fbc669687b57.txt](../analysis/hermes/mcp/decompile_module-fbc669687b57.txt) |
| 1644 | F1646 | runRequestOtp | [1, 2, 1617] | [decompile_module-efb79fc8f643.txt](../analysis/hermes/mcp/decompile_module-efb79fc8f643.txt) |
| 1647 | F1649 | runVerifyOtp | [1, 2, 1617] | [decompile_module-9912400322d8.txt](../analysis/hermes/mcp/decompile_module-9912400322d8.txt) |
| 1648 | F1650 | unnamed | [] | [decompile_module-f121c951e635.txt](../analysis/hermes/mcp/decompile_module-f121c951e635.txt) |
| 1649 | F1651 | runSignInWithRapidoFlow | [1, 2, 1641, 1643, 1648] | [decompile_module-bb1077130615.txt](../analysis/hermes/mcp/decompile_module-bb1077130615.txt) |
| 1652 | F1654 | runVerifyOtpFlow | [1, 2, 1647, 1643, 1648] | [decompile_module-15dadc5250a6.txt](../analysis/hermes/mcp/decompile_module-15dadc5250a6.txt) |
| 1659 | F1661 | safeError | [] | [decompile_module-55134a5380d1.txt](../analysis/hermes/mcp/decompile_module-55134a5380d1.txt) |
| 1660 | F1662 | GeocodingService | [1, 29, 2, 5, 6, 1205, 1152, 1153] | [decompile_module-35f042ba0c2d.txt](../analysis/hermes/mcp/decompile_module-35f042ba0c2d.txt) |
| 1661 | F1663 | LocationFetcher | [1, 2, 5, 6, 1662, 1205, 1667] | [decompile_module-54941cfbd210.txt](../analysis/hermes/mcp/decompile_module-54941cfbd210.txt) |
| 1662 | F1664 | unnamed | [1663] | [decompile_module-a06e32297851.txt](../analysis/hermes/mcp/decompile_module-a06e32297851.txt) |
| 1669 | F1671 | CleverTapService | [1, 1670, 71, 2, 5, 6, 1671, 15, 733, 1127, 1673, 1674, 1681, 1693, 1694, 1695, 1696, 1713, 1714, 1715, 1716, 1717, 1718, 1223, 1719, 2011, 2012, 2014] | [decompile_module-f83d601cad9d.txt](../analysis/hermes/mcp/decompile_module-f83d601cad9d.txt) |
| 1674 | F1676 | APPSFLYER_EVENTS | [1, 1675] | [decompile_module-773deed94914.txt](../analysis/hermes/mcp/decompile_module-773deed94914.txt) |
| 1681 | F1683 | FIREBASE_EVENTS | [1, 2, 1682] | [decompile_module-cbb2822dc75a.txt](../analysis/hermes/mcp/decompile_module-cbb2822dc75a.txt) |
| 1713 | F1715 | enqueueAnalyticsJob | [1, 2] | [decompile_module-672b56722771.txt](../analysis/hermes/mcp/decompile_module-672b56722771.txt) |
| 1758 | F1760 | RESTAURANT_PAGE_PATH | [] | [decompile_module-58ec3c60df34.txt](../analysis/hermes/mcp/decompile_module-58ec3c60df34.txt) |
| 1780 | F1782 | unnamed | [1, 2, 1617, 1758, 1781] | [decompile_module-aca9dea644b4.txt](../analysis/hermes/mcp/decompile_module-aca9dea644b4.txt) |
| 1815 | F1817 | cartApiService | [1, 2, 6, 5, 10, 12, 13, 143, 1816, 1817, 1812, 1152] | [decompile_module-647a89aa8499.txt](../analysis/hermes/mcp/decompile_module-647a89aa8499.txt) |
| 1833 | F1835 | CART_STORAGE_KEYS | [1, 29, 5, 6, 1133, 1659] | [decompile_module-d145acad85a3.txt](../analysis/hermes/mcp/decompile_module-d145acad85a3.txt) |
| 1976 | F1978 | emitStandardBusiness | [1, 2, 1669, 1977] | [decompile_module-2ef794eb7974.txt](../analysis/hermes/mcp/decompile_module-2ef794eb7974.txt) |
| 1996 | F1998 | unnamed | [1670] | [decompile_module-c8333e36095d.txt](../analysis/hermes/mcp/decompile_module-c8333e36095d.txt) |
| 2015 | F2017 | trackGpsEnablingAttempt | [1996, 1850, 1976, 1670] | [decompile_module-db7a741512f4.txt](../analysis/hermes/mcp/decompile_module-db7a741512f4.txt) |
| 2016 | F2018 | locationService | [1, 2, 5, 6, 1668, 1205, 1661, 1224, 2004, 1225, 1586, 1813, 1660, 1669, 1667] | [decompile_module-05f406ee3c2a.txt](../analysis/hermes/mcp/decompile_module-05f406ee3c2a.txt) |
| 2017 | F2019 | unnamed | [1, 29, 74, 1133] | [decompile_module-5f844a1e2429.txt](../analysis/hermes/mcp/decompile_module-5f844a1e2429.txt) |
| 2030 | F2032 | paymentService | [1, 2, 5, 6, 15, 2031, 2032, 2035, 2039, 2040, 2037, 2050, 2054, 2055, 2038] | [decompile_module-dfe4c074a492.txt](../analysis/hermes/mcp/decompile_module-dfe4c074a492.txt) |
| 2035 | F2037 | PaymentHandlers | [1, 2, 5, 6, 2036, 2037, 2038] | [decompile_module-a91a9ea30145.txt](../analysis/hermes/mcp/decompile_module-a91a9ea30145.txt) |
| 2036 | F2038 | waitForOrderCompletion | [1, 2, 2037] | [decompile_module-ee18bd8ea7ed.txt](../analysis/hermes/mcp/decompile_module-ee18bd8ea7ed.txt) |
| 2037 | F2039 | captureUserDroppedEvent | [1, 2, 1153, 1152] | [decompile_module-d6091f488677.txt](../analysis/hermes/mcp/decompile_module-d6091f488677.txt) |
| 2039 | F2041 | unnamed | [] | [decompile_module-b7e72c8a2e68.txt](../analysis/hermes/mcp/decompile_module-b7e72c8a2e68.txt) |
| 2049 | F2051 | JuspayGateway | [1, 2, 5, 6, 2039, 2050, 2037] | [decompile_module-476f89522c19.txt](../analysis/hermes/mcp/decompile_module-476f89522c19.txt) |
| 2050 | F2052 | JUSPAY_PROCESS_CANCELLED_CODE | [1, 2, 1155, 15, 2051, 1207, 1669, 1681, 2039, 1153] | [decompile_module-de4242d42148.txt](../analysis/hermes/mcp/decompile_module-de4242d42148.txt) |
| 2055 | F2057 | resolveGatewayType | [2041] | [decompile_module-caa9db87dbab.txt](../analysis/hermes/mcp/decompile_module-caa9db87dbab.txt) |
| 2062 | F2064 | BaseFeedConfigService | [1, 2, 6, 5, 10, 12, 13, 143, 2063, 1205, 1695, 2064, 2065, 1133, 1152] | [decompile_module-dd1682c3aeea.txt](../analysis/hermes/mcp/decompile_module-dd1682c3aeea.txt) |
| 2063 | F2065 | ServiceabilityReasons | [1, 2, 5, 6, 1152, 1153, 1714] | [decompile_module-63b6b25cc72c.txt](../analysis/hermes/mcp/decompile_module-63b6b25cc72c.txt) |
| 2073 | F2075 | Navigation | [1, 74, 15, 2074, 3206, 3207, 3209, 2495, 2598, 2605, 3341, 2694, 2712, 2988, 2989, 3835, 3846, 3890, 3924, 4068, 4074, 4093, 4148, 2430, 4159, 4161, 4162, 2416, 4163, 244, 4183, 1813, 4249, 4250, 4252, 4266, 4333, 4334, 4335, 4336, 4338, 4340, 4342, 4391, 4394, 4409, 4412, 1157, 3343, 1850, 2006, 1851, 4520, 4538] | [decompile_module-de60c5160b42.txt](../analysis/hermes/mcp/decompile_module-de60c5160b42.txt) |
| 2615 | F2617 | unnamed | [1, 2, 1153, 2616, 2622, 2633, 2685] | [decompile_module-4adda9065af7.txt](../analysis/hermes/mcp/decompile_module-4adda9065af7.txt) |
| 2618 | F2620 | unnamed | [1, 2] | [decompile_module-ed99bc9888ea.txt](../analysis/hermes/mcp/decompile_module-ed99bc9888ea.txt) |
| 2620 | F2622 | unnamed | [1, 2, 2621, 2617, 2619, 2618] | [decompile_module-17fb9209860a.txt](../analysis/hermes/mcp/decompile_module-17fb9209860a.txt) |
| 2625 | F2627 | authRuntimeContainer | [1, 1127] | [decompile_module-da3ed9de961f.txt](../analysis/hermes/mcp/decompile_module-da3ed9de961f.txt) |
| 2633 | F2635 | unnamed | [2634, 2635, 2636, 2637, 2639, 2638, 2640, 2649, 2651, 2655, 2658, 2659, 2660, 2661, 2666, 2667, 2668, 2671, 2672, 2657, 2656, 2673, 2674, 2675, 2677, 2678, 2676, 2654, 2652, 2653, 2650, 2669, 2670, 2679, 2680, 2681, 2682, 2683, 2684] | [decompile_module-553b15b01ab0.txt](../analysis/hermes/mcp/decompile_module-553b15b01ab0.txt) |
| 2636 | F2638 | unnamed | [1, 2, 2635, 1617] | [decompile_module-d324fb120845.txt](../analysis/hermes/mcp/decompile_module-d324fb120845.txt) |
| 2637 | F2639 | unnamed | [1, 2, 2638, 1617] | [decompile_module-cefa97758282.txt](../analysis/hermes/mcp/decompile_module-cefa97758282.txt) |
| 2639 | F2641 | unnamed | [1, 2, 2638, 1617] | [decompile_module-2235243a6d54.txt](../analysis/hermes/mcp/decompile_module-2235243a6d54.txt) |
| 2641 | F2643 | unnamed | [2642, 2643, 2644, 2645, 2646, 2647, 2648] | [decompile_module-fc10070932a3.txt](../analysis/hermes/mcp/decompile_module-fc10070932a3.txt) |
| 3316 | F3318 | runFetchOrderTrackingOrder | [1, 2, 1617] | [decompile_module-a7932396fe43.txt](../analysis/hermes/mcp/decompile_module-a7932396fe43.txt) |
| 3317 | F3319 | runFetchRiderTracking | [1, 2, 1617] | [decompile_module-1c4f8b65d99a.txt](../analysis/hermes/mcp/decompile_module-1c4f8b65d99a.txt) |
| 3320 | F3322 | orderTrackingScreenReducer | [3318] | [decompile_module-aa9842d5e4b9.txt](../analysis/hermes/mcp/decompile_module-aa9842d5e4b9.txt) |
| 3342 | F3344 | unnamed | [1, 74, 1127, 1799, 1851, 2011, 2608, 1831, 3343, 3344] | [decompile_module-534024f91bc6.txt](../analysis/hermes/mcp/decompile_module-534024f91bc6.txt) |
| 3347 | F3349 | unnamed | [1, 2, 29, 74, 2641, 3348, 3447, 3763, 3764, 3765, 1799, 2011, 2017, 3766, 3767, 3768, 3775, 3776] | [decompile_module-5f3a77d7bb3d.txt](../analysis/hermes/mcp/decompile_module-5f3a77d7bb3d.txt) |
| 3578 | F3580 | runSearchFoodItemsByRestaurant | [1, 2, 1617] | [decompile_module-6f97b96158ff.txt](../analysis/hermes/mcp/decompile_module-6f97b96158ff.txt) |
| 3579 | F3581 | runSearchMenuItems | [1, 2, 1617] | [decompile_module-d634d6480e46.txt](../analysis/hermes/mcp/decompile_module-d634d6480e46.txt) |
| 3580 | F3582 | runSearchRecommendations | [1, 2, 1617] | [decompile_module-30ecb090f536.txt](../analysis/hermes/mcp/decompile_module-30ecb090f536.txt) |
| 3583 | F3585 | runSearchSimilarRestaurants | [1, 2, 1617] | [decompile_module-960e612ac376.txt](../analysis/hermes/mcp/decompile_module-960e612ac376.txt) |
| 3767 | F3769 | HOME_BOTTOM_BAR_HEIGHT | [538] | [decompile_module-694d678b2ff4.txt](../analysis/hermes/mcp/decompile_module-694d678b2ff4.txt) |
| 3775 | F3777 | unnamed | [1, 2, 2633, 2614] | [decompile_module-d4a261dc6fe4.txt](../analysis/hermes/mcp/decompile_module-d4a261dc6fe4.txt) |
| 3776 | F3778 | unnamed | [1, 29, 74, 3777, 3755, 3778, 3779, 1851] | [decompile_module-d589c9bf4e45.txt](../analysis/hermes/mcp/decompile_module-d589c9bf4e45.txt) |
| 3847 | F3849 | unnamed | [3848, 3849, 3850, 3851, 3853, 3855, 3854, 3857] | [decompile_module-1e7900f9ce6a.txt](../analysis/hermes/mcp/decompile_module-1e7900f9ce6a.txt) |
| 3855 | F3857 | unnamed | [1, 2, 74, 2087, 3856, 3852, 3304, 3340] | [decompile_module-8f1db563bc3e.txt](../analysis/hermes/mcp/decompile_module-8f1db563bc3e.txt) |
| 3856 | F3858 | pollingService | [1, 2, 5, 6] | [decompile_module-eec27ccafc05.txt](../analysis/hermes/mcp/decompile_module-eec27ccafc05.txt) |
| 3893 | F3895 | trackRecentSearchTap | [1976, 1670, 1848] | [decompile_module-35e178e88f53.txt](../analysis/hermes/mcp/decompile_module-35e178e88f53.txt) |
| 3914 | F3916 | SearchService | [1, 2, 5, 6, 1152, 3567, 2614, 1153] | [decompile_module-bd22671ae957.txt](../analysis/hermes/mcp/decompile_module-bd22671ae957.txt) |
| 3937 | F3939 | unnamed | [74, 3938, 3961, 3994] | [decompile_module-3ca1d89926d8.txt](../analysis/hermes/mcp/decompile_module-3ca1d89926d8.txt) |
| 3938 | F3940 | unnamed | [3939, 3960, 3959] | [decompile_module-b00e23ca1b93.txt](../analysis/hermes/mcp/decompile_module-b00e23ca1b93.txt) |
| 3939 | F3941 | analytics | [1, 15, 733, 1673, 1127, 1695, 1693, 2011, 1719, 1714, 1223, 1715, 3940, 3959, 3960, 1696] | [decompile_module-8e2bd617255f.txt](../analysis/hermes/mcp/decompile_module-8e2bd617255f.txt) |
| 3940 | F3942 | unnamed | [3941, 3942, 3944, 3945, 3943, 3946, 3947, 3956, 3957, 3958, 3953, 3952] | [decompile_module-12be9d3e81bf.txt](../analysis/hermes/mcp/decompile_module-12be9d3e81bf.txt) |
| 3942 | F3944 | HomePageConfig | [3941, 3943] | [decompile_module-64acf77c36c4.txt](../analysis/hermes/mcp/decompile_module-64acf77c36c4.txt) |
| 3943 | F3945 | ScreenId | [] | [decompile_module-7aadf74d82a4.txt](../analysis/hermes/mcp/decompile_module-7aadf74d82a4.txt) |
| 3946 | F3948 | unnamed | [1, 2, 3947, 3948, 3949, 3950, 3952, 3953, 3954, 3955] | [decompile_module-e97bdcbc26dd.txt](../analysis/hermes/mcp/decompile_module-e97bdcbc26dd.txt) |
| 3952 | F3954 | materializeAnalyticsEvent | [] | [decompile_module-c85ff859aea6.txt](../analysis/hermes/mcp/decompile_module-c85ff859aea6.txt) |
| 3953 | F3955 | generateEventName | [] | [decompile_module-5794c9e7b7d9.txt](../analysis/hermes/mcp/decompile_module-5794c9e7b7d9.txt) |
| 3959 | F3961 | consoleSink | [] | [decompile_module-828908722be1.txt](../analysis/hermes/mcp/decompile_module-828908722be1.txt) |
| 3960 | F3962 | cleverTapSink | [1, 1671, 3940] | [decompile_module-81e64b9204ee.txt](../analysis/hermes/mcp/decompile_module-81e64b9204ee.txt) |
| 3961 | F3963 | unnamed | [1, 29, 74, 1728, 3087, 3962, 1851, 2017, 3989, 3992, 3993] | [decompile_module-b4ea2779c5bf.txt](../analysis/hermes/mcp/decompile_module-b4ea2779c5bf.txt) |
| 3994 | F3996 | unnamed | [74, 3995, 1851, 3940] | [decompile_module-a852b3e738fc.txt](../analysis/hermes/mcp/decompile_module-a852b3e738fc.txt) |

## Function metadata and request-builder assembly

| Tool | Exact arguments | Saved result |
|---|---|---|
| disassemble | `{"function_id": 11284, "show_offsets": true}` | [disassemble-17973bdeaf66.json](../analysis/hermes/mcp/disassemble-17973bdeaf66.json) |
| disassemble | `{"function_id": 17078, "show_offsets": true}` | [disassemble-2926ce255ce3.json](../analysis/hermes/mcp/disassemble-2926ce255ce3.json) |
| disassemble | `{"function_id": 18073, "show_offsets": true}` | [disassemble-4f0b92f8f97a.json](../analysis/hermes/mcp/disassemble-4f0b92f8f97a.json) |
| disassemble | `{"function_id": 11168, "show_offsets": true}` | [disassemble-5948388b92e6.json](../analysis/hermes/mcp/disassemble-5948388b92e6.json) |
| disassemble | `{"function_id": 17071, "show_offsets": true}` | [disassemble-5e6a49d2b7b6.json](../analysis/hermes/mcp/disassemble-5e6a49d2b7b6.json) |
| disassemble | `{"function_id": 31972, "show_offsets": true}` | [disassemble-715968c0758d.json](../analysis/hermes/mcp/disassemble-715968c0758d.json) |
| disassemble | `{"function_id": 11163, "show_offsets": true}` | [disassemble-75f7ef9ab127.json](../analysis/hermes/mcp/disassemble-75f7ef9ab127.json) |
| disassemble | `{"function_id": 18918, "show_offsets": true}` | [disassemble-777a358fec5b.json](../analysis/hermes/mcp/disassemble-777a358fec5b.json) |
| disassemble | `{"function_id": 11288, "show_offsets": true}` | [disassemble-79fb9020203a.json](../analysis/hermes/mcp/disassemble-79fb9020203a.json) |
| disassemble | `{"function_id": 11165, "show_offsets": true}` | [disassemble-b530bc4994f2.json](../analysis/hermes/mcp/disassemble-b530bc4994f2.json) |
| disassemble | `{"function_id": 18921, "show_offsets": true}` | [disassemble-b76f7a72f375.json](../analysis/hermes/mcp/disassemble-b76f7a72f375.json) |
| disassemble | `{"function_id": 11145, "show_offsets": true}` | [disassemble-feffd65feaa7.json](../analysis/hermes/mcp/disassemble-feffd65feaa7.json) |
| function_info | `{"function_id": 17071}` | [function_info-0ce57b883ac7.json](../analysis/hermes/mcp/function_info-0ce57b883ac7.json) |
| function_info | `{"function_id": 11284}` | [function_info-23b2f996efc4.json](../analysis/hermes/mcp/function_info-23b2f996efc4.json) |
| function_info | `{"function_id": 11288}` | [function_info-284875a09b4d.json](../analysis/hermes/mcp/function_info-284875a09b4d.json) |
| function_info | `{"function_id": 13529}` | [function_info-2ddbc937b425.json](../analysis/hermes/mcp/function_info-2ddbc937b425.json) |
| function_info | `{"function_id": 11133}` | [function_info-38e825389291.json](../analysis/hermes/mcp/function_info-38e825389291.json) |
| function_info | `{"function_id": 11165}` | [function_info-3b4f7402f570.json](../analysis/hermes/mcp/function_info-3b4f7402f570.json) |
| function_info | `{"function_id": 17078}` | [function_info-3debe565360c.json](../analysis/hermes/mcp/function_info-3debe565360c.json) |
| function_info | `{"function_id": 16923}` | [function_info-57d03ba83264.json](../analysis/hermes/mcp/function_info-57d03ba83264.json) |
| function_info | `{"function_id": 11273}` | [function_info-7eb0938eb14b.json](../analysis/hermes/mcp/function_info-7eb0938eb14b.json) |
| function_info | `{"function_id": 11277}` | [function_info-910e22cfb062.json](../analysis/hermes/mcp/function_info-910e22cfb062.json) |
| function_info | `{"function_id": 11163}` | [function_info-b222b21924ea.json](../analysis/hermes/mcp/function_info-b222b21924ea.json) |
| function_info | `{"function_id": 18073}` | [function_info-c2a24010d58d.json](../analysis/hermes/mcp/function_info-c2a24010d58d.json) |
| function_info | `{"function_id": 11145}` | [function_info-c7a0712845e8.json](../analysis/hermes/mcp/function_info-c7a0712845e8.json) |
| function_info | `{"function_id": 18662}` | [function_info-dd7bea1b6e79.json](../analysis/hermes/mcp/function_info-dd7bea1b6e79.json) |
| function_info | `{"function_id": 15248}` | [function_info-f04bcd778c3b.json](../analysis/hermes/mcp/function_info-f04bcd778c3b.json) |
| module_exports | `{"module_id": 1652}` | [module_exports-15dadc5250a6.json](../analysis/hermes/mcp/module_exports-15dadc5250a6.json) |
| module_exports | `{"module_id": 3317}` | [module_exports-1c4f8b65d99a.json](../analysis/hermes/mcp/module_exports-1c4f8b65d99a.json) |
| module_exports | `{"module_id": 1976}` | [module_exports-2ef794eb7974.json](../analysis/hermes/mcp/module_exports-2ef794eb7974.json) |
| module_exports | `{"module_id": 3580}` | [module_exports-30ecb090f536.json](../analysis/hermes/mcp/module_exports-30ecb090f536.json) |
| module_exports | `{"module_id": 3893}` | [module_exports-35e178e88f53.json](../analysis/hermes/mcp/module_exports-35e178e88f53.json) |
| module_exports | `{"module_id": 3953}` | [module_exports-5794c9e7b7d9.json](../analysis/hermes/mcp/module_exports-5794c9e7b7d9.json) |
| module_exports | `{"module_id": 1713}` | [module_exports-672b56722771.json](../analysis/hermes/mcp/module_exports-672b56722771.json) |
| module_exports | `{"module_id": 1674}` | [module_exports-773deed94914.json](../analysis/hermes/mcp/module_exports-773deed94914.json) |
| module_exports | `{"module_id": 3960}` | [module_exports-81e64b9204ee.json](../analysis/hermes/mcp/module_exports-81e64b9204ee.json) |
| module_exports | `{"module_id": 1647}` | [module_exports-9912400322d8.json](../analysis/hermes/mcp/module_exports-9912400322d8.json) |
| module_exports | `{"module_id": 1617}` | [module_exports-9fe25a7c356c.json](../analysis/hermes/mcp/module_exports-9fe25a7c356c.json) |
| module_exports | `{"module_id": 3316}` | [module_exports-a7932396fe43.json](../analysis/hermes/mcp/module_exports-a7932396fe43.json) |
| module_exports | `{"module_id": 1616}` | [module_exports-b0485fd073cb.json](../analysis/hermes/mcp/module_exports-b0485fd073cb.json) |
| module_exports | `{"module_id": 3952}` | [module_exports-c85ff859aea6.json](../analysis/hermes/mcp/module_exports-c85ff859aea6.json) |
| module_exports | `{"module_id": 1681}` | [module_exports-cbb2822dc75a.json](../analysis/hermes/mcp/module_exports-cbb2822dc75a.json) |
| module_exports | `{"module_id": 1622}` | [module_exports-d128930ef2a2.json](../analysis/hermes/mcp/module_exports-d128930ef2a2.json) |
| module_exports | `{"module_id": 2015}` | [module_exports-db7a741512f4.json](../analysis/hermes/mcp/module_exports-db7a741512f4.json) |
| module_exports | `{"module_id": 1644}` | [module_exports-efb79fc8f643.json](../analysis/hermes/mcp/module_exports-efb79fc8f643.json) |
| module_exports | `{"module_id": 1669}` | [module_exports-f83d601cad9d.json](../analysis/hermes/mcp/module_exports-f83d601cad9d.json) |
| xref_search | `{"query": "consumerapp"}` | [xref_search-172cf9ddf9cd.json](../analysis/hermes/mcp/xref_search-172cf9ddf9cd.json) |
| xref_search | `{"query": "restaurant"}` | [xref_search-28fd29be67cc.json](../analysis/hermes/mcp/xref_search-28fd29be67cc.json) |
| xref_search | `{"query": "verifyOtp"}` | [xref_search-466c612b6e0a.json](../analysis/hermes/mcp/xref_search-466c612b6e0a.json) |
| xref_search | `{"query": "/api/v1/restaurant"}` | [xref_search-65d9223de236.json](../analysis/hermes/mcp/xref_search-65d9223de236.json) |
| xref_search | `{"query": "refreshToken"}` | [xref_search-8241894272aa.json](../analysis/hermes/mcp/xref_search-8241894272aa.json) |
| xref_search | `{"query": "orderTracking"}` | [xref_search-ae8e34dcf44a.json](../analysis/hermes/mcp/xref_search-ae8e34dcf44a.json) |
| xref_search | `{"query": "checkout"}` | [xref_search-b0731339c81a.json](../analysis/hermes/mcp/xref_search-b0731339c81a.json) |
| xref_search | `{"query": "recordEvent"}` | [xref_search-b63b961833c4.json](../analysis/hermes/mcp/xref_search-b63b961833c4.json) |
| xref_search | `{"query": "baseURL"}` | [xref_search-d60ec0c54ff0.json](../analysis/hermes/mcp/xref_search-d60ec0c54ff0.json) |
| xref_search | `{"query": "createNativeStackNavigator"}` | [xref_search-dffa2a5445a3.json](../analysis/hermes/mcp/xref_search-dffa2a5445a3.json) |
| xref_search | `{"query": "cart"}` | [xref_search-e180440566c4.json](../analysis/hermes/mcp/xref_search-e180440566c4.json) |

Analytics process captures are exported separately in [rea-evidence-hermes-analytics.json](rea-evidence-hermes-analytics.json), from the independent analytics analysis session. See hermes-tracking.md for its four exact capture IDs.


---

## Exact next steps — do not repeat completed analysis

1. Read this latest checkpoint and consult `hermes-evidence-index.md` plus `hermes-artifacts.json`. Resolve requested module/function selectors against cached JSON/TXT first. Do not repeat manifest decoding, APK inventory/extraction, module inventory, function metadata dump or already cached decompilation/disassembly.
2. Select one unresolved business edge and inspect only its relevant Hermes function/closure/IR. The bulk output is syntactically source-like but has known variable recovery errors: e.g. path.phoneNumber, endpoint.headers, reassigned type.type and async-generator environment variables. Use saved disassembly for already checked builders; request new disassembly/closures/get_ir_json only for an unanswered edge.
3. Finish auth: M1652/F25454 verify-result → session/customer-details → final navigation; M1127 logout/callback ordering; refresh protocol; M1641/M1649 alternate sign-in. Trace actual caller reachability and reducers rather than inferring protocol from exported names. Keep credential values symbolic.
4. Finish discovery/menu: validate M3347/M3775/M2637 async argument binding in assembly; M1758/M1780 menu query/cache integration and all outlet/filter/pagination branches. Distinguish backend data/ranking/serviceability from client adaptation.
5. Finish search: locate the input debounce/cancellation handlers and bind them to M3914 or portable M3578/M3579/M3580/M3583 paths; trace filter/ranking and M3896 history persistence. Use the existing route registry, request builders and F18073 assembly.
6. Finish cart: check F11133 reducer branch semantics, M1609 totals formulas and customization/quantity limits; connect M1832 queue/M2010 middleware to M1833 writes and restoration. Do not equate registered WatermelonDB with cart ownership; verified cart persistence uses MMKV.
7. Finish checkout: follow M2030 processOrder/startPayment → M2049 backend verification → M2035/M2036 completion polling; decode all status-set memberships/cancellation/duplicate-result paths. M2050/F13529 bridges to HyperSdkReact and the prior Java HyperServices path. Find the custom UPIUrlHandlerModule's actual JS caller if present. Server idempotency remains unknown unless explicit client evidence supports a limited claim.
8. Finish order tracking: use existing F17071/F17078 request assembly and F18662 polling hook; decode isOrderInFinalState F16923/status sets and exact remote-config interval defaults. Do not infer sockets/push absence from confirmed polling. Trace notification-driven screen entry separately if needed.
9. Finish location: manager/provider selection, accuracy/fallback/timeout behavior, address persistence and serviceability use of selected coordinates. Reuse native GeolocationModule bodies and JS M2016/M1660/M1661 before drilling into new callbacks.
10. Finish analytics: follow F18921 event naming, F18918 payload construction and F31972 CleverTap sink; audit M3946 scheduling/lane limits; validate merges/field precedence and consent. Bind standard/legacy/new-runtime emitters to each screen/action. Trace incogniaService to the previously known native event methods without collecting payload values. Reuse all helpers and assembly already listed in hermes-tracking.md.
11. If installed-app behavior becomes relevant, first resolve the HotUpdater native chain `com.hotupdater.H.o()` → returned object's `a()` and identify the selected bundle without bypassing Pairip or modifying app/prod state. The packaged HBC findings cannot establish that a live installation uses the same update. Runtime execution was not part of this checkpoint or prior validation.
12. Save only new evidence to a new versioned export; preserve all three exports, prior reports and sanitized response files. Update report confidence/coverage explicitly and append progress. Validate hashes, local report links and cited IDs across the correct session bundles. Do not declare the investigation complete while the above edges remain unresolved.

## Checkpoint verification

The preceding analysis pass verified HBC identity, retained artifact hashes, report links, analytics capture IDs across the appropriate exports, preservation of native report bodies and the original 93-record bundle. This save turn only consolidates saved results. All existing report files other than this intentionally appended progress.md are hash-checked unchanged; the previous progress.md bytes are retained exactly as a prefix. No application or analysis tool was rerun.
