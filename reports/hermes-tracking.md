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
