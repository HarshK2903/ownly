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
