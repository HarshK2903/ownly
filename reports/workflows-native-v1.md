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
