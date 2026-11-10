# Method evidence ledger

Analyzed only the supplied base APK, package `com.ownly.customer`, version 2.0.7 (358), min SDK 24, target SDK 36. SHA-256: `5495bcf9cf03a7b956e253a2747c10f0222454b1e2106fa53213cd53dc708a05`. REA/JADX headless 0.7.1 reports 16885 classes and 2055 resources. Manifest evidence: `ev_25c9cfa3d80fcfda38c832fe4d5cb009c9b9103ad9dd7c5a94d2943f7697af6f`.

All findings are static artifact observations or reconstructions from decompiled bodies, not runtime observations. No application execution, production requests, or APK modifications were performed. Evidence IDs resolve to records in [rea-evidence.json](rea-evidence.json); [method-evidence.md](method-evidence.md) preserves inspected method bodies, prototypes and limitations. Decompiled display names can be aliases; obfuscated names below are preserved rather than renamed. Dynamic/reflective/JS calls are outside JADX reference coverage. Signatures and split APK contents were not verified.

Every section below is a REA result for the exact APK. Bodies are decompiler output (or marked smali), not original source.

## com.facebook.react.modules.network.NetworkingModule.sendRequestInternalReal (overload 0)

Evidence: `ev_037e7e55d9404382e22725cf6a634906f9a47d1c7045d5f18bb5ae5e797623b7`; DEX prototype `(Ljava/lang/String;Ljava/lang/String;ILcom/facebook/react/bridge/ReadableArray;Lcom/facebook/react/bridge/ReadableMap;Ljava/lang/String;ZIZLjava/lang/String;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    /* JADX WARN: Code duplicated, block: B:135:0x029f  */
    /* JADX WARN: Code duplicated, block: B:136:0x02a8  */
    /* JADX WARN: Code duplicated, block: B:139:0x02af  */
    /* JADX WARN: Code duplicated, block: B:141:0x02b8  */
    private final void sendRequestInternalReal(String str, String str2, int i, ReadableArray readableArray, ReadableMap readableMap, String str3, boolean z, int i2, boolean z2, String str4) throws IOException {
        String str5;
        ReactApplicationContext reactApplicationContext;
        int i3;
        b next;
        String str6;
        C cG;
        B b2;
        String strA;
        C cA;
        long jContentLength;
        Charset charsetC;
        String str7;
        ReactApplicationContext reactApplicationContextIfActiveOrWarn = getReactApplicationContextIfActiveOrWarn();
        try {
            Uri uri = Uri.parse(str2);
            for (d dVar : this.uriHandlers) {
                try {
                    Intrinsics.checkNotNull(uri);
                    if (dVar.b(uri, str3)) {
                        Pair pairA = dVar.a(uri);
                        WritableMap writableMap = (WritableMap) pairA.a();
                        byte[] bArr = (byte[]) pairA.b();
                        byte[] bytes = writableMap.toString().getBytes(Charsets.UTF_8);
                        Intrinsics.checkNotNullExpressionValue(bytes, "getBytes(...)");
                        long length = bytes.length;
                        str5 = str4;
                        try {
                            com.facebook.react.modules.network.f.k(reactApplicationContextIfActiveOrWarn, i, str5, str2, 200, M.i(), length);
                            reactApplicationContext = reactApplicationContextIfActiveOrWarn;
                            i3 = i;
                            str7 = str5;
                            try {
                                com.facebook.react.modules.network.f.d(reactApplicationContext, i3, str7, writableMap, bArr);
                                com.facebook.react.modules.network.f.j(reactApplicationContext, i3, str7, length);
                                return;
                            } catch (IOException e2) {
                                e = e2;
                            }
                        } catch (IOException e3) {
                            e = e3;
                            reactApplicationContext = reactApplicationContextIfActiveOrWarn;
                            i3 = i;
                        }
                    } else {
                        reactApplicationContextIfActiveOrWarn = reactApplicationContextIfActiveOrWarn;
                    }
                } catch (IOException e4) {
                    e = e4;
                    str7 = str4;
                    reactApplicationContext = reactApplicationContextIfActiveOrWarn;
                    i3 = i;
                }
                str5 = str7;
                com.facebook.react.modules.network.f.i(reactApplicationContext, i3, str5, e.getMessage(), e);
                return;
            }
            ReactApplicationContext reactApplicationContext2 = reactApplicationContextIfActiveOrWarn;
            try {
                B.a aVarL = new B.a().l(str2 == null ? "" : str2);
                if (i != 0) {
                    aVarL.k(Integer.valueOf(i));
                }
                z.a aVarG = this.client.G();
                Companion.c(aVarG);
                if (!z2) {
                    aVarG.h(n.b);
                }
                if (z) {
                    aVarG.b(new e(str3, reactApplicationContext2, i));
                }
                if (i2 != this.client.b()) {
                    aVarG.e(i2, TimeUnit.MILLISECONDS);
                }
                z zVarC = aVarG.c();
                t tVarExtractHeaders = extractHeaders(readableArray, readableMap);
                if (tVarExtractHeaders == null) {
                    com.facebook.react.modules.network.f.i(reactApplicationContext2, i, str4, "Unrecognized headers format", null);
                    return;
                }
                String strD = tVarExtractHeaders.d(CONTENT_TYPE_HEADER_NAME);
                String strD2 = tVarExtractHeaders.d(CONTENT_ENCODING_HEADER_NAME);
                aVarL.f(tVarExtractHeaders);
                if (readableMap == null) {
                    next = null;
                    break;
                }
                Iterator<b> it = this.requestBodyHandlers.iterator();
                do {
                    if (!it.hasNext()) {
                        next = null;
                        break;
                    }
                    next = it.next();
                } while (!next.a(readableMap));
                if (readableMap != null) {
                    Locale locale = Locale.ROOT;
                    String lowerCase = str.toLowerCase(locale);
                    Intrinsics.checkNotNullExpressionValue(lowerCase, "toLowerCase(...)");
                    if (!Intrinsics.areEqual(lowerCase, "get")) {
                        String lowerCase2 = str.toLowerCase(locale);
                        Intrinsics.checkNotNullExpressionValue(lowerCase2, "toLowerCase(...)");
                        if (!Intrinsics.areEqual(lowerCase2, "head")) {
                            if (next != null) {
                                cG = next.b(readableMap, strD);
                            } else if (readableMap.hasKey(REQUEST_BODY_KEY_STRING)) {
                                if (strD == null) {
                                    com.facebook.react.modules.network.f.i(reactApplicationContext2, i, str4, "Payload is set but no content-type header specified", null);
                                    return;
                                }
                                String string = readableMap.getString(REQUEST_BODY_KEY_STRING);
                                x xVarA = x.e.a(strD);
                                if (m.i(strD2)) {
                                    cG = (xVarA == null || string == null) ? null : m.d(xVarA, string);
                                    if (cG == null) {
                                        com.facebook.react.modules.network.f.i(reactApplicationContext2, i, str4, "Failed to gzip request body", null);
                                        return;
                                    }
                                } else {
                                    if (xVarA == null) {
                                        charsetC = StandardCharsets.UTF_8;
                                    } else {
                                        charsetC = xVarA.c(StandardCharsets.UTF_8);
                                        if (charsetC == null) {
                                            throw new IllegalStateException("Required value was null.");
                                        }
                                    }
                                    if (string == null) {
                                        com.facebook.react.modules.network.f.i(reactApplicationContext2, i, str4, "Received request but body was empty", null);
                                        return;
                                    }
                                    C.a aVar = C.Companion;
                                    Intrinsics.checkNotNull(charsetC);
                                    byte[] bytes2 = string.getBytes(charsetC);
                                    Intrinsics.checkNotNullExpressionValue(bytes2, "getBytes(...)");
                                    cG = C.a.n(aVar, xVarA, bytes2, 0, 0, 12, null);
                                }
                            } else if (readableMap.hasKey("base64")) {
                                if (strD == null) {
                                    com.facebook.react.modules.network.f.i(reactApplicationContext2, i, str4, "Payload is set but no content-type header specified", null);
                                    return;
                                }
                                String string2 = readableMap.getString("base64");
                                if (string2 == null) {
                                    throw new IllegalStateException("Required value was null.");
                                }
                                x xVarA2 = x.e.a(strD);
                                if (xVarA2 == null) {
                                    com.facebook.react.modules.network.f.i(reactApplicationContext2, i, str4, "Invalid content type specified: " + strD, null);
                                    return;
                                }
                                okio.k kVarA = okio.k.d.a(string2);
                                if (kVarA == null) {
                                    com.facebook.react.modules.network.f.i(reactApplicationContext2, i, str4, "Request body base64 string was invalid", null);
                                    return;
                                }
                                cG = C.Companion.e(xVarA2, kVarA);
                            } else if (readableMap.hasKey(REQUEST_BODY_KEY_URI)) {
                                if (strD == null) {
                                    com.facebook.react.modules.network.f.i(reactApplicationContext2, i, str4, "Payload is set but no content-type header specified", null);
                                    return;
                                }
                                String string3 = readableMap.getString(REQUEST_BODY_KEY_URI);
                                if (string3 == null) {
                                    com.facebook.react.modules.network.f.i(reactApplicationContext2, i, str4, "Request body URI field was set but null", null);
                                    return;
                                }
                                ReactApplicationContext reactApplicationContext3 = getReactApplicationContext();
                                Intrinsics.checkNotNullExpressionValue(reactApplicationContext3, "getReactApplicationContext(...)");
                                InputStream inputStreamH = m.h(reactApplicationContext3, string3);
                                if (inputStreamH == null) {
                                    com.facebook.react.modules.network.f.i(reactApplicationContext2, i, str4, "Could not retrieve file for uri " + string3, null);
                                    return;
                                }
                                cG = m.c(x.e.a(strD), inputStreamH);
                            } else if (readableMap.hasKey(REQUEST_BODY_KEY_FORMDATA)) {
                                if (strD == null) {
                                    strD = "multipart/form-data";
                                }
                                ReadableArray array = readableMap.getArray(REQUEST_BODY_KEY_FORMDATA);
                                if (array == null) {
                                    com.facebook.react.modules.network.f.i(reactApplicationContext2, i, str4, "Received request but form data was empty", null);
                                    return;
                                }
                                str6 = null;
                                y.a aVarConstructMultipartBody = constructMultipartBody(array, strD, i, str4);
                                if (aVarConstructMultipartBody == null) {
                                    return;
                                } else {
                                    cG = aVarConstructMultipartBody.c();
                                }
                            } else {
                                str6 = null;
                                cG = m.g(str);
                            }
                            str6 = null;
                        }
                        aVarL.g(str, wrapRequestBodyWithProgressEmitter(cG, i));
                        addRequest(i);
                        b2 = aVarL.b();
                        String string4 = b2.d().toString();
                        String strC = b2.c();
                        Map mapB = com.facebook.react.modules.network.f.b(b2.b());
                        if (com.facebook.react.common.build.a.b) {
                            strA = com.facebook.react.modules.network.f.a(b2.a());
                        } else {
                            strA = str6;
                        }
                        cA = b2.a();
                        if (cA != null) {
                            jContentLength = cA.contentLength();
                        } else {
                            jContentLength = 0;
                        }
                        com.facebook.react.modules.network.f.c(str4, string4, strC, mapB, strA, jContentLength);
                        zVarC.a(b2).z(new g(i, reactApplicationContext2, str4, str3, z));
                    }
                    str6 = null;
                } else {
                    str6 = null;
                }
                cG = m.g(str);
                aVarL.g(str, wrapRequestBodyWithProgressEmitter(cG, i));
                addRequest(i);
                b2 = aVarL.b();
                String string5 = b2.d().toString();
                String strC2 = b2.c();
                Map mapB2 = com.facebook.react.modules.network.f.b(b2.b());
                if (com.facebook.react.common.build.a.b) {
                    strA = com.facebook.react.modules.network.f.a(b2.a());
                } else {
                    strA = str6;
                }
                cA = b2.a();
                if (cA != null) {
                    jContentLength = cA.contentLength();
                } else {
                    jContentLength = 0;
                }
                com.facebook.react.modules.network.f.c(str4, string5, strC2, mapB2, strA, jContentLength);
                zVarC.a(b2).z(new g(i, reactApplicationContext2, str4, str3, z));
            } catch (Exception e5) {
                com.facebook.react.modules.network.f.i(reactApplicationContext2, i, str4, e5.getMessage(), e5);
            }
        } catch (IOException e6) {
            e = e6;
            str5 = str4;
            reactApplicationContext = reactApplicationContextIfActiveOrWarn;
            i3 = i;
        }
    }
```

## com.facebook.react.modules.network.NetworkingModule.sendRequest (overload 0)

Evidence: `ev_1a1757f3295e0109f971027b04df648377a0c787b7a2995275feb5c5032ac48e`; DEX prototype `(Ljava/lang/String;Ljava/lang/String;DLcom/facebook/react/bridge/ReadableArray;Lcom/facebook/react/bridge/ReadableMap;Ljava/lang/String;ZDZ)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    @Override // com.facebook.fbreact.specs.NativeNetworkingAndroidSpec
    public void sendRequest(String method, String url, double d2, ReadableArray readableArray, ReadableMap readableMap, String responseType, boolean z, double d3, boolean z2) {
        Intrinsics.checkNotNullParameter(method, "method");
        Intrinsics.checkNotNullParameter(url, "url");
        Intrinsics.checkNotNullParameter(responseType, "responseType");
        int i = (int) d2;
        int i2 = (int) d3;
        String strExtractOrGenerateDevToolsRequestId = extractOrGenerateDevToolsRequestId(readableMap);
        try {
            sendRequestInternalReal(method, url, i, readableArray, readableMap, responseType, z, i2, z2, strExtractOrGenerateDevToolsRequestId);
        } catch (Throwable th) {
            com.facebook.common.logging.a.k("Networking", "Failed to send url request: " + url, th);
            com.facebook.react.modules.network.f.i(getReactApplicationContextIfActiveOrWarn(), i, strExtractOrGenerateDevToolsRequestId, th.getMessage(), th);
        }
    }
```

## com.ownly.customer.UPIUrlHandlerModule.openUPIUrl (overload 0)

Evidence: `ev_2c0bf5e0f07b94683e8d9159c7d224d8bbab949d0434b168ef55673d19d48156`; DEX prototype `(Ljava/lang/String;Lcom/facebook/react/bridge/Promise;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    @ReactMethod
    public final void openUPIUrl(String url, Promise promise) {
        Intrinsics.checkNotNullParameter(url, "url");
        Intrinsics.checkNotNullParameter(promise, "promise");
        try {
            Activity currentActivity = getReactApplicationContext().getCurrentActivity();
            if (currentActivity == null) {
                promise.reject(MerchantConstants.ERROR, "No current activity available");
                return;
            }
            Intent intent = new Intent("android.intent.action.VIEW", Uri.parse(url));
            PackageManager packageManager = currentActivity.getPackageManager();
            Intrinsics.checkNotNullExpressionValue(packageManager, "getPackageManager(...)");
            List<ResolveInfo> listQueryIntentActivities = packageManager.queryIntentActivities(intent, 0);
            Intrinsics.checkNotNullExpressionValue(listQueryIntentActivities, "queryIntentActivities(...)");
            if (listQueryIntentActivities.isEmpty()) {
                promise.reject(MerchantConstants.ERROR, "No UPI app found to handle the URL");
            } else {
                currentActivity.startActivity(intent);
                promise.resolve(Boolean.TRUE);
            }
        } catch (Exception e) {
            promise.reject(MerchantConstants.ERROR, "Failed to open UPI URL: " + e.getMessage(), e);
        }
    }
```

## com.margelo.nitro.mmkv.HybridMMKVPlatformContext.getBaseDirectory (overload 0)

Evidence: `ev_2dbaac96844f780d110f305d5fbe8089496efbb418c014fd3b7fed499cf36b50`; DEX prototype `()Ljava/lang/String;`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    @Override // com.margelo.nitro.mmkv.HybridMMKVPlatformContextSpec
    public String getBaseDirectory() {
        ReactApplicationContext reactApplicationContextA = NitroModules.Companion.a();
        if (reactApplicationContextA == null) {
            throw new Error("Cannot get MMKV base directory - No Android Context available!");
        }
        return reactApplicationContextA.getFilesDir().getAbsolutePath() + "/mmkv";
    }
```

## com.ownly.customer.MainActivity.b0 (overload 0)

Evidence: `ev_3274c189887357f0804a6bede9aa0ae0170696b006a19dbff219106ad7e2d45c`; DEX prototype `()Ljava/lang/String;`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    protected String b0() {
        return "consumerapp";
    }
```

## com.reactnativecommunity.geolocation.GeolocationModule.requestAuthorization (overload 0)

Evidence: `ev_32888ab7fde6438d23be47918f984aecfceb62189eaddc88deb5de18399619d6`; DEX prototype `(Lcom/facebook/react/bridge/Callback;Lcom/facebook/react/bridge/Callback;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    public void requestAuthorization(final Callback callback, final Callback callback2) {
        final PermissionsModule permissionsModule = (PermissionsModule) getReactApplicationContext().getNativeModule(PermissionsModule.class);
        ArrayList arrayList = new ArrayList();
        arrayList.add("android.permission.ACCESS_COARSE_LOCATION");
        arrayList.add("android.permission.ACCESS_FINE_LOCATION");
        final JavaOnlyArray javaOnlyArrayFrom = JavaOnlyArray.from(arrayList);
        final Callback callback3 = new Callback() { // from class: com.reactnativecommunity.geolocation.g
            @Override // com.facebook.react.bridge.Callback
            public final void invoke(Object[] objArr) {
                GeolocationModule.c(callback, callback2, objArr);
            }
        };
        final Callback callback4 = new Callback() { // from class: com.reactnativecommunity.geolocation.h
            @Override // com.facebook.react.bridge.Callback
            public final void invoke(Object[] objArr) {
                callback2.invoke(r.a(r.a, "Failed to request location permission."));
            }
        };
        final Callback callback5 = new Callback() { // from class: com.reactnativecommunity.geolocation.i
            @Override // com.facebook.react.bridge.Callback
            public final void invoke(Object[] objArr) {
                callback2.invoke(r.a(r.a, "Failed to check location permission."));
            }
        };
        final Callback callback6 = new Callback() { // from class: com.reactnativecommunity.geolocation.j
            @Override // com.facebook.react.bridge.Callback
            public final void invoke(Object[] objArr) {
                GeolocationModule.g(permissionsModule, javaOnlyArrayFrom, callback3, callback4, callback, objArr);
            }
        };
        permissionsModule.checkPermission("android.permission.ACCESS_FINE_LOCATION", new PromiseImpl(callback6, new Callback() { // from class: com.reactnativecommunity.geolocation.k
            @Override // com.facebook.react.bridge.Callback
            public final void invoke(Object[] objArr) {
                permissionsModule.checkPermission("android.permission.ACCESS_COARSE_LOCATION", new PromiseImpl(callback6, callback5));
            }
        }));
    }
```

## com.hotupdater.C.a.d (overload 0)

Evidence: `ev_3ef2b235127c346e02262e6df0746733f73fc0a5f358887933602b21aa40c1ed`; DEX prototype `(Landroid/content/Context;)Ljava/lang/String;`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
        public final String d(Context context) {
            Intrinsics.checkNotNullParameter(context, "context");
            return c(context).k();
        }
```

## com.ownly.customer.MainApplication.onCreate (overload 0)

Evidence: `ev_43f0d6293fbbeb1af5195240ae91d19c673015bdf0082030e8d82650b8755e6a`; DEX prototype `()V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    @Override // com.clevertap.react.a, com.clevertap.android.sdk.r, android.app.Application
    public void onCreate() throws IOException {
        com.clevertap.android.sdk.e.b(this);
        f0.b2(f0.b.VERBOSE);
        super.onCreate();
        SoLoader.l(this, OpenSourceMergedSoMapping.a);
        DefaultNewArchitectureEntryPoint.load();
    }
```

## com.ownly.customer.MainApplication.a.i (overload 0)

Evidence: `ev_47521fae078ab6d16f593981947c908da3633fb1c4cbaebbcbb666404a78c582`; DEX prototype `()Ljava/lang/String;`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
        @Override // com.facebook.react.I
        protected String i() {
            return "index";
        }
```

## com.hotupdater.C.a.c (overload 0)

Evidence: `ev_48d64110b292c52b9b8be088c9ca762b51f2a6300e2374346b3268a514c5e6e9`; DEX prototype `(Landroid/content/Context;)Lcom/hotupdater/H;`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
        public final H c(Context context) {
            H h;
            Intrinsics.checkNotNullParameter(context, "context");
            H h2 = C.b;
            if (h2 != null) {
                return h2;
            }
            synchronized (this) {
                h = C.b;
                if (h == null) {
                    Context applicationContext = context.getApplicationContext();
                    Intrinsics.checkNotNullExpressionValue(applicationContext, "getApplicationContext(...)");
                    h = new H(applicationContext);
                    C.b = h;
                }
            }
            return h;
        }
```

## com.pairip.application.Application.attachBaseContext (overload 0)

Evidence: `ev_4aaebc6ed8bca4789e06f062599975668c117132b89cc30e81887d693dc8a6f0`; DEX prototype `(Landroid/content/Context;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
/* JADX INFO: loaded from: classes2.dex */
public class Application extends MainApplication {
    @Override // android.content.ContextWrapper
    protected void attachBaseContext(Context context) {
        LicenseClient.checkLicense(context);
        super.attachBaseContext(context);
    }
```

## com.ownly.customer.MainApplication.a.<init> (overload 0)

Evidence: `ev_4ab16e314f3ae798884886371b88e5a5d84649593f19e955bf6eff1e87e461dc`; DEX prototype `(Lcom/ownly/customer/MainApplication;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
        a() {
            super(MainApplication.this);
            this.c = true;
            this.d = true;
        }
```

## com.ownly.customer.MainActivity.onNewIntent (overload 0)

Evidence: `ev_55dd3c02665953b74b208ede8037630fd7fa9a16e04be9f20abe97dbb92a2de8`; DEX prototype `(Landroid/content/Intent;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    @Override // com.facebook.react.ReactActivity, androidx.activity.h, android.app.Activity
    public void onNewIntent(Intent intent) {
        Intrinsics.checkNotNullParameter(intent, "intent");
        super.onNewIntent(intent);
        setIntent(intent);
    }
```

## com.ownly.customer.MainApplication.a.l (overload 0)

Evidence: `ev_6e806600d87aa25f4aa105513fbe4ef8fdeae62400799606949b7fdff14eef43`; DEX prototype `()Ljava/util/List;`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
        @Override // com.facebook.react.I
        protected List l() {
            ArrayList arrayListA = new com.facebook.react.i(this).a();
            arrayListA.add(new t());
            arrayListA.add(new l());
            arrayListA.add(new com.ownly.customer.a());
            arrayListA.add(new b());
            arrayListA.add(new i());
            arrayListA.add(new com.ownly.customer.phoneinput.d());
            Intrinsics.checkNotNullExpressionValue(arrayListA, "apply(...)");
            return arrayListA;
        }
```

## com.clevertap.react.CleverTapModule.onUserLogin (overload 0)

Evidence: `ev_70e66967e73bac45452e1cd345231c70763579dc232024cb1f78d0503faad259`; DEX prototype `(Lcom/facebook/react/bridge/ReadableMap;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    @Override // com.clevertap.react.NativeCleverTapModuleSpec
    public void onUserLogin(ReadableMap readableMap) {
        this.cleverTapModuleImpl.d1(readableMap);
    }
```

## com.faizal.OtpVerify.OtpVerifyModule.requestOtp (overload 0)

Evidence: `ev_7383605032d6083277edc6e218fc31188a5719999a29b81c3d573554b33c7002`; DEX prototype `(Lcom/facebook/react/bridge/Promise;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    private void requestOtp(Promise promise) {
        Task taskX = com.google.android.gms.auth.api.phone.a.b(this.reactContext).x();
        taskX.a(new a());
        taskX.addOnCompleteListener(new b());
        taskX.g(new c(promise));
        taskX.d(new d(promise));
    }
```

## com.pairip.application.Application.<init> (overload 0)

Evidence: `ev_7ec903b5debf5aec762bc6f00199bf417e7806a4f4eccfe33a1b7fa501692021`; DEX prototype `()V`; confidence `derived`; representation `smali`; source `complete`; fallback `True`.

Markers: ['java_body_unavailable']

```smali
.method public constructor <init>()V
    .registers 1

    invoke-direct {p0}, Lcom/ownly/customer/MainApplication;-><init>()V

    return-void
.end method
```

## com.ownly.customer.MainApplication.a.g (overload 0)

Evidence: `ev_87d81435c0813ea7d1979d699c01fef9c49d8103408d08a8d93e331b6b1d5e75`; DEX prototype `()Ljava/lang/String;`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
        @Override // com.facebook.react.I
        protected String g() {
            C.a aVar = C.a;
            Context applicationContext = MainApplication.this.getApplicationContext();
            Intrinsics.checkNotNullExpressionValue(applicationContext, "getApplicationContext(...)");
            return aVar.d(applicationContext);
        }
```

## com.ownly.customer.MainApplication.a.x (overload 0)

Evidence: `ev_93d0051638f7937960cfb174d1c9c1c95748c5d2df3244ea9d170390b030f8f5`; DEX prototype `()Z`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
        @Override // com.facebook.react.defaults.e
        protected boolean x() {
            return this.c;
        }
```

## com.appsflyer.reactnative.RNAppsFlyerModule.logEvent (overload 0)

Evidence: `ev_a60d8bc32d5e8fe0f905a0f8ff39c9eed545bd7528772dc53c28f74939e06fb9`; DEX prototype `(Ljava/lang/String;Lcom/facebook/react/bridge/ReadableMap;Lcom/facebook/react/bridge/Callback;Lcom/facebook/react/bridge/Callback;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    @ReactMethod
    public void logEvent(String str, ReadableMap readableMap, Callback callback, Callback callback2) {
        final CallbackGuard callbackGuard = new CallbackGuard(callback);
        final CallbackGuard callbackGuard2 = new CallbackGuard(callback2);
        try {
            if (str.trim().equals("")) {
                callbackGuard2.invoke("No 'eventName' found or its empty");
                return;
            }
            Map<String, Object> map = RNUtil.toMap(readableMap);
            if (map == null) {
                map = new HashMap<>();
            }
            if (getCurrentActivity() != null) {
                AppsFlyerLib.getInstance().logEvent(getCurrentActivity(), str, map, new AppsFlyerRequestListener() { // from class: com.appsflyer.reactnative.RNAppsFlyerModule.3
                    @Override // com.appsflyer.attribution.AppsFlyerRequestListener
                    public void onError(int i, String str2) {
                        callbackGuard2.invoke(str2);
                    }

                    @Override // com.appsflyer.attribution.AppsFlyerRequestListener
                    public void onSuccess() {
                        callbackGuard.invoke("Success");
                    }
                });
            }
        } catch (Exception e) {
            callbackGuard2.invoke(e.getMessage());
        }
    }
```

## com.incognia.reactnative.IncogniaModule.sendLoginEvent (overload 0)

Evidence: `ev_abb5282c8fd4ea23585c492378d785c846b448bbb05d34669a75925d0d58d262`; DEX prototype `(Lcom/facebook/react/bridge/ReadableMap;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    @ReactMethod
    public void sendLoginEvent(ReadableMap readableMap) {
        String string = readableMap.hasKey(EVENT_ACCOUNT_ID) ? readableMap.getString(EVENT_ACCOUNT_ID) : null;
        String string2 = readableMap.hasKey(EVENT_EXTERNAL_ID) ? readableMap.getString(EVENT_EXTERNAL_ID) : null;
        Incognia.sendLoginEvent(new LoginEvent.Builder().accountId(string).externalId(string2).location(readableMap.hasKey(EVENT_LOCATION) ? convertToEventLocation(readableMap.getMap(EVENT_LOCATION)) : null).tag(readableMap.hasKey(EVENT_TAG) ? readableMap.getString(EVENT_TAG) : null).properties(readableMap.hasKey(EVENT_PROPERTIES) ? convertToEventProperties(readableMap.getMap(EVENT_PROPERTIES)) : null).status(readableMap.hasKey(EVENT_STATUS) ? readableMap.getString(EVENT_STATUS) : null).build());
    }
```

## in.juspay.hypersdkreact.HyperSdkReactModule.process (overload 1)

Evidence: `ev_acc75f13be87eb67e1e83694e66ade43896e31f3b5d7366083a2ba24f99a5664`; DEX prototype `(Ljava/lang/String;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    @ReactMethod
    public void process(String str) {
        process(this.hyperServices, str);
    }
```

## com.faizal.OtpVerify.OtpVerifyModule.getOtp (overload 0)

Evidence: `ev_afea8348aa5617024c29447762c5aac501c11719b9c621672f23673923a5d867`; DEX prototype `(Lcom/facebook/react/bridge/Promise;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    @ReactMethod
    public void getOtp(Promise promise) {
        requestOtp(promise);
    }
```

## com.ownly.customer.MainActivity.onCreate (overload 0)

Evidence: `ev_b0b721bc80f6352bcba4616ff4046fe77c8184f537ca1e6ff80e6ce58c0e6a72`; DEX prototype `(Landroid/os/Bundle;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    @Override // com.facebook.react.ReactActivity, androidx.fragment.app.s, androidx.activity.h, androidx.core.app.i, android.app.Activity
    protected void onCreate(Bundle bundle) {
        h hVar = h.a;
        if (hVar.i() == 0) {
            hVar.n(System.currentTimeMillis());
        }
        setTheme(k.a);
        super.onCreate(null);
        w0.b(getWindow(), true);
        hVar.o(this);
    }
```

## io.invertase.firebase.analytics.ReactNativeFirebaseAnalyticsModule.logEvent (overload 0)

Evidence: `ev_b152f9c18b2d94f3a9fe005d19aaca6cb837d07f661292c46698d9f3106cc1a9`; DEX prototype `(Ljava/lang/String;Lcom/facebook/react/bridge/ReadableMap;Lcom/facebook/react/bridge/Promise;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    @ReactMethod
    public void logEvent(String str, ReadableMap readableMap, final Promise promise) {
        this.module.z(str, toBundle(readableMap)).addOnCompleteListener(new OnCompleteListener() { // from class: io.invertase.firebase.analytics.e
            @Override // com.google.android.gms.tasks.OnCompleteListener
            public final void onComplete(Task task) {
                ReactNativeFirebaseAnalyticsModule.h(promise, task);
            }
        });
    }
```

## com.reactnativecommunity.geolocation.GeolocationModule.getCurrentPosition (overload 0)

Evidence: `ev_b1fb39db89da9414d46fd5e24c4b72e56077b2c4df6a859653aea75d6c0a90f9`; DEX prototype `(Lcom/facebook/react/bridge/ReadableMap;Lcom/facebook/react/bridge/Callback;Lcom/facebook/react/bridge/Callback;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    public void getCurrentPosition(final ReadableMap readableMap, final Callback callback, final Callback callback2) {
        try {
            if (this.mConfiguration.b.booleanValue()) {
                this.mLocationManager.b(readableMap, callback, callback2);
            } else {
                requestAuthorization(new Callback() { // from class: com.reactnativecommunity.geolocation.f
                    @Override // com.facebook.react.bridge.Callback
                    public final void invoke(Object[] objArr) {
                        this.a.lambda$getCurrentPosition$5(readableMap, callback, callback2, objArr);
                    }
                }, callback2);
            }
        } catch (SecurityException e) {
            emitLocationPermissionMissing(e);
        }
    }
```

## com.incognia.reactnative.IncogniaModule.sendPaymentEvent (overload 0)

Evidence: `ev_b923fe68a570c854d671b080f759bf6595eb6a422a36e4c3138066e900100d81`; DEX prototype `(Lcom/facebook/react/bridge/ReadableMap;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    @ReactMethod
    public void sendPaymentEvent(ReadableMap readableMap) {
        String string = readableMap.hasKey(EVENT_ACCOUNT_ID) ? readableMap.getString(EVENT_ACCOUNT_ID) : null;
        String string2 = readableMap.hasKey(EVENT_EXTERNAL_ID) ? readableMap.getString(EVENT_EXTERNAL_ID) : null;
        String string3 = readableMap.hasKey(EVENT_TAG) ? readableMap.getString(EVENT_TAG) : null;
        String string4 = readableMap.hasKey(EVENT_STATUS) ? readableMap.getString(EVENT_STATUS) : null;
        String string5 = readableMap.hasKey(EVENT_STORE_ID) ? readableMap.getString(EVENT_STORE_ID) : null;
        EventProperties eventPropertiesConvertToEventProperties = readableMap.hasKey(EVENT_PROPERTIES) ? convertToEventProperties(readableMap.getMap(EVENT_PROPERTIES)) : null;
        EventLocation eventLocationConvertToEventLocation = readableMap.hasKey(EVENT_LOCATION) ? convertToEventLocation(readableMap.getMap(EVENT_LOCATION)) : null;
        List<PaymentAddress> listConvertPaymentAddressesReadableArrayToList = readableMap.hasKey(PAYMENT_ADDRESSES) ? convertPaymentAddressesReadableArrayToList(readableMap.getArray(PAYMENT_ADDRESSES)) : null;
        PaymentValue paymentValueConvertToPaymentValue = readableMap.hasKey(PAYMENT_VALUE) ? convertToPaymentValue(readableMap.getMap(PAYMENT_VALUE)) : null;
        Incognia.sendPaymentEvent(new PaymentEvent.Builder().accountId(string).externalId(string2).location(eventLocationConvertToEventLocation).addresses(listConvertPaymentAddressesReadableArrayToList).paymentValue(paymentValueConvertToPaymentValue).paymentCoupon(readableMap.hasKey(PAYMENT_COUPON) ? convertToPaymentCoupon(readableMap.getMap(PAYMENT_COUPON)) : null).paymentMethods(readableMap.hasKey(PAYMENT_METHODS) ? convertPaymentMethodsReadableArrayToList(readableMap.getArray(PAYMENT_METHODS)) : null).storeId(string5).tag(string3).properties(eventPropertiesConvertToEventProperties).status(string4).build());
    }
```

## com.ownly.customer.AndroidInstalledAppsCheckerModule.checkLaunchablePackages (overload 0)

Evidence: `ev_bc2c3cb8614cec694f3dbb8ed1d7aa6fa2cb1426ffac7476a9cb3d924efd1fe3`; DEX prototype `(Lcom/facebook/react/bridge/ReadableArray;Lcom/facebook/react/bridge/Promise;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    @ReactMethod
    public final void checkLaunchablePackages(ReadableArray packageNames, Promise promise) {
        String string;
        Intrinsics.checkNotNullParameter(packageNames, "packageNames");
        Intrinsics.checkNotNullParameter(promise, "promise");
        try {
            PackageManager packageManager = getReactApplicationContext().getPackageManager();
            ArrayList arrayList = new ArrayList();
            ArrayList arrayList2 = new ArrayList();
            Iterator<Object> it = packageNames.toArrayList().iterator();
            Intrinsics.checkNotNullExpressionValue(it, "iterator(...)");
            while (it.hasNext()) {
                Object next = it.next();
                String str = next instanceof String ? (String) next : null;
                if (str != null && (string = StringsKt.Z0(str).toString()) != null && string.length() != 0) {
                    arrayList2.add(string);
                }
            }
            int size = arrayList2.size();
            int i = 0;
            while (i < size) {
                Object obj = arrayList2.get(i);
                i++;
                String str2 = (String) obj;
                Intent launchIntentForPackage = packageManager.getLaunchIntentForPackage(str2);
                if (launchIntentForPackage != null) {
                    launchIntentForPackage.addCategory("android.intent.category.LAUNCHER");
                } else {
                    launchIntentForPackage = new Intent("android.intent.action.MAIN");
                    launchIntentForPackage.addCategory("android.intent.category.LAUNCHER");
                    launchIntentForPackage.setPackage(str2);
                }
                try {
                    if (launchIntentForPackage.resolveActivity(packageManager) != null) {
                        arrayList.add(str2);
                    }
                } catch (Exception unused) {
                }
            }
            WritableArray writableArrayCreateArray = Arguments.createArray();
            int size2 = arrayList.size();
            int i2 = 0;
            while (i2 < size2) {
                Object obj2 = arrayList.get(i2);
                i2++;
                writableArrayCreateArray.pushString((String) obj2);
            }
            WritableMap writableMapCreateMap = Arguments.createMap();
            writableMapCreateMap.putArray("launchablePackages", writableArrayCreateArray);
            writableMapCreateMap.putInt("totalCount", arrayList2.size());
            writableMapCreateMap.putInt("launchableCount", arrayList.size());
            promise.resolve(writableMapCreateMap);
        } catch (Exception unused2) {
            WritableMap writableMapCreateMap2 = Arguments.createMap();
            writableMapCreateMap2.putArray("launchablePackages", Arguments.createArray());
            writableMapCreateMap2.putInt("totalCount", 0);
            writableMapCreateMap2.putInt("launchableCount", 0);
            promise.resolve(writableMapCreateMap2);
        }
    }
```

## com.facebook.react.i.a (overload 0)

Evidence: `ev_c687cd1c9935ea85e2d4ffd9efa3131b57f9b47160379144d0861a8f11354402`; DEX prototype `()Ljava/util/ArrayList;`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    public ArrayList a() {
        return new ArrayList(Arrays.asList(new com.facebook.react.shell.r(null), new com.ReactNativeBlobUtil.i(), new RNAppsFlyerPackage(), new FastImageViewPackage(), new com.hotupdater.L(), new com.lodev09.truesheet.B(), new NotifeePackage(), new WatermelonDBPackage(), new com.reactnativecommunity.clipboard.b(), new com.reactnativecommunity.geolocation.m(), new com.reactnativecommunity.netinfo.h(), new com.reactnativedocumentpicker.n(), new io.invertase.firebase.analytics.l(), new io.invertase.firebase.app.b(), new io.invertase.firebase.crashlytics.c(), new io.invertase.firebase.messaging.t(), new io.invertase.firebase.config.j(), new org.reactnative.maskedview.b(), new com.rive.f(), new com.sbaiahmed1.reactnativeblur.f(), new com.shopify.reactnative.skia.f(), new com.swmansion.reactnativebottomsheet.i(), new com.clevertap.react.t(), new HyperSdkReactPackage(), new com.airbnb.android.react.lottie.i(), new com.heanoria.library.reactnative.locationenabler.c(), new com.reactnativecashfreepgsdk.a(), new com.lugg.RNCConfig.c(), new com.rt2zz.reactnativecontacts.c(), new com.learnium.RNDeviceInfo.b(), new com.ease.k(), new com.zoontek.rnedgetoedge.j(), new com.alpha0010.fs.h(), new com.swmansion.gesturehandler.e(), new com.mkuczera.haptic.c(), new com.imagepicker.f(), new com.ibits.react_native_in_app_review.c(), new com.incognia.reactnative.c(), new com.reactnativekeyboardcontroller.b(), new com.BV.LinearGradient.a(), new h0(), new com.margelo.nitro.mmkv.c(), new com.navigationmode.b(), new com.margelo.nitro.c(), new com.faizal.OtpVerify.f(), new com.zoontek.rnpermissions.f(), new com.swmansion.pulsar.reactnative.b(), new ReanimatedPackage(), new com.reactnativerestart.b(), new com.th3rdwave.safeareacontext.e(), new com.swmansion.rnscreens.s(), new cl.json.c(), new com.zmxv.RNSound.c(), new SvgPackage(), new com.unistyles.l(), new com.oblador.vectoricons.c(), new com.reactnativecommunity.webview.o(), new WorkletsPackage(), new com.worklets.b(), new com.RNFetchBlob.e()));
    }
```

## com.clevertap.react.CleverTapModule.recordEvent (overload 0)

Evidence: `ev_d032b72b5e05525d8e79f14420eb4e04ca1804ed06c1251e1b6c020f0fb1516c`; DEX prototype `(Ljava/lang/String;Lcom/facebook/react/bridge/ReadableMap;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    @Override // com.clevertap.react.NativeCleverTapModuleSpec
    public void recordEvent(String str, ReadableMap readableMap) {
        this.cleverTapModuleImpl.G1(str, readableMap);
    }
```

## com.ownly.customer.MainApplication.a.t (overload 0)

Evidence: `ev_dc1b14459e0f258be17a3f9f54f6c84ffd5d5d8b4bac60bd4b6d522c73f3859f`; DEX prototype `()Z`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
        @Override // com.facebook.react.I
        public boolean t() {
            return false;
        }
```

## com.hotupdater.H.k (overload 0)

Evidence: `ev_e38f64ef8d84c6216b07de8f73b57d1c095efc5d8518ce758883231d48ef3405`; DEX prototype `()Ljava/lang/String;`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    public final String k() {
        return o().a();
    }
```

## in.juspay.hypersdkreact.HyperSdkReactModule.process (overload 0)

Evidence: `ev_ec7ac1e5afd3c47c7d0524c653a13c7838a5111b0a36f93790537522316fc1aa`; DEX prototype `(Lin/juspay/services/HyperServices;Ljava/lang/String;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    private void process(HyperServices hyperServices, String str) {
        synchronized (lock) {
            try {
                JSONObject jSONObject = new JSONObject(str);
                s sVar = (s) getCurrentActivity();
                if (sVar == null) {
                    Log.w(NAME, "process: activity is null");
                    SdkTracker.trackBootLifecycle(LogSubCategory.LifeCycle.HYPER_SDK, "error", "hyper_sdk_react", Labels.HyperSdk.INITIATE, "activity is null");
                } else if (hyperServices == null) {
                    Log.w(NAME, "process: hyperService is null");
                    SdkTracker.trackBootLifecycle(LogSubCategory.LifeCycle.HYPER_SDK, "error", "hyper_sdk_react", Labels.HyperSdk.INITIATE, "hyperServices is null");
                } else {
                    hyperServices.setActivityLaunchDelegate(new ReactLaunchDelegate(this.context));
                    hyperServices.setRequestPermissionDelegate(new ReactRequestDelegate(sVar));
                    hyperServices.process(sVar, jSONObject);
                }
            } catch (JSONException e) {
                SdkTracker.trackAndLogBootException(NAME, "lifecycle", LogSubCategory.LifeCycle.HYPER_SDK, "hyper_sdk_react", "Exception in process", e);
            }
        }
    }
```

## com.reactnativecommunity.geolocation.GeolocationModule.startObserving (overload 0)

Evidence: `ev_f28983344a8dfe3024aeafb3286c9c8df109ecc1216edd6a328081121229fc94`; DEX prototype `(Lcom/facebook/react/bridge/ReadableMap;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    public void startObserving(final ReadableMap readableMap) {
        try {
            if (this.mConfiguration.b.booleanValue()) {
                this.mLocationManager.e(readableMap);
            } else {
                requestAuthorization(new Callback() { // from class: com.reactnativecommunity.geolocation.d
                    @Override // com.facebook.react.bridge.Callback
                    public final void invoke(Object[] objArr) {
                        this.a.lambda$startObserving$6(readableMap, objArr);
                    }
                }, new Callback() { // from class: com.reactnativecommunity.geolocation.e
                    @Override // com.facebook.react.bridge.Callback
                    public final void invoke(Object[] objArr) {
                        this.a.lambda$startObserving$7(objArr);
                    }
                });
            }
        } catch (SecurityException e) {
            emitLocationPermissionMissing(e);
        }
    }
```

## com.nozbe.watermelondb.WMDatabaseBridge.initialize (overload 0)

Evidence: `ev_fbfc2b14a75737ae9edee7a67f68e50fcac59a5ef35801bc931bf826d7580d47`; DEX prototype `(Ljava/lang/Integer;Ljava/lang/String;IZLcom/facebook/react/bridge/Promise;)V`; confidence `derived`; representation `java`; source `complete`; fallback `False`.

Markers: []

```java
    @ReactMethod
    public void initialize(Integer num, String str, int i, boolean z, Promise promise) {
        if (this.connections.containsKey(num)) {
            throw new IllegalStateException("A driver with tag " + num + " already set up");
        }
        WritableMap writableMapCreateMap = Arguments.createMap();
        try {
            this.connections.put(num, new Connection.Connected(new WMDatabaseDriver(this.reactContext, str, i, z)));
            writableMapCreateMap.putString(AuthorizationResponseParser.CODE, "ok");
            promise.resolve(writableMapCreateMap);
        } catch (MigrationNeededError e) {
            this.connections.put(num, new Connection.Waiting(new ArrayList()));
            writableMapCreateMap.putString(AuthorizationResponseParser.CODE, "migrations_needed");
            writableMapCreateMap.putInt("databaseVersion", e.databaseVersion);
            promise.resolve(writableMapCreateMap);
        } catch (SchemaNeededError unused) {
            this.connections.put(num, new Connection.Waiting(new ArrayList()));
            writableMapCreateMap.putString(AuthorizationResponseParser.CODE, "schema_needed");
            promise.resolve(writableMapCreateMap);
        } catch (Exception e2) {
            promise.reject(e2);
        }
    }
```
