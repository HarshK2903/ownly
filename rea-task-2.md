# Task: Deep TLS Certificate Failure and HTTP Payload Visibility Investigation — Ownly Android

Continue the existing Ownly Android reverse-engineering investigation. Do not restart the analysis from scratch.

**Project directory:** `/home/bugulnoz/research/ownly/`

**Target application:** `com.ownly.customer`

**Physical test device:** Redmi Note 7 Pro, Android 10, connected through USB/ADB.

**Available tools:** REA MCP, JADX, Hermes bytecode analysis tools, ADB, Wireshark/tshark, and Linux command-line utilities.

## Existing evidence

PCAPdroid intercepted a connection:

- Application: Ownly
- SNI: `eu1-spiky.clevertap-prod.com`
- Destination: `18.161.216.67:443`
- Protocol: HTTPS over TCP
- Status: Error
- Decryption: Failed
- Error: `The client does not trust the proxy's certificate`
- TLS alert: `certificate unknown`

The application has previously been identified as React Native with Hermes bytecode v98 and a Pairip wrapper.

Network captures have now been added to:

`/home/bugulnoz/research/ownly/network/`

Previously generated analysis reports are stored in:

`/home/bugulnoz/research/ownly/reports/`

## Primary objectives

Determine the most precise, evidence-supported root cause of the TLS certificate verification failure.

Investigate why PCAPdroid's certificate is rejected, whether the problem arises from Android's CA trust configuration, certificate pinning, an SDK-specific trust manager, or another TLS implementation.

Then determine what is technically required to observe readable request URLs, HTTP methods, headers, JSON payloads and responses in an appropriately authorized test environment.

Do not assume certificate pinning merely because the TLS handshake failed.

## Phase 1 — Examine all existing captures

1. Inventory every file in `network/`, including PCAP, PCAPNG, HAR, keylog and existing reports.
2. Identify the actual captures and inspect their timestamps, packet counts, protocol distribution and available TLS evidence.
3. Use tshark or REA's PCAP tools to inspect the connection to `eu1-spiky.clevertap-prod.com`.
4. Examine available ClientHello, ServerHello, certificate, and TLS alert evidence.
5. Establish which TLS handshake events are actually visible, including their timestamps and endpoints.
6. Determine whether the capture contains encrypted application records, successfully decrypted HTTP data, or only an incomplete handshake.
7. Check whether other Ownly HTTPS connections succeed, fail or were not intercepted.
8. Distinguish evidence from the PCAP itself from information provided by the PCAPdroid screenshot.
9. Explain why an ordinary encrypted PCAP cannot automatically reveal HTTP request and response bodies without applicable TLS secrets or successful interception.

Create a technical timeline of the failed connection.

## Phase 2 — Investigate Android certificate trust

Use REA/JADX to inspect the application's actual installed APK.

Determine:

- Declared target SDK version.
- Whether `android:networkSecurityConfig` exists.
- The effective Network Security Configuration, where recoverable.
- Whether system CAs or user-installed CAs are trusted.
- Whether custom trust anchors are declared.
- Whether certificate pins or pin sets are declared.
- Whether the app is debuggable.
- Whether relevant settings are inherited from platform defaults.

Explain how Android 10 and the application's target SDK influence trust of a user-installed CA.

Inspect the specific evidence before determining whether Android's default trust rules alone explain the failure.

## Phase 3 — Investigate certificate pinning and custom TLS validation

Search the decompiled code and native libraries for relevant implementations, including:

- `CertificatePinner`
- `X509TrustManager`
- `TrustManagerFactory`
- `SSLContext`
- `HostnameVerifier`
- `network_security_config`
- OkHttp and related network clients
- React Native networking bridges
- CleverTap Android SDK networking
- Native TLS implementations, if present

Search for relevant certificate-validation configuration and call paths.

For each candidate, identify:

1. Actual class and method.
2. Implementation or configuration evidence.
3. Relevant callers and dependencies.
4. Whether it is used by the observed CleverTap connection.
5. Whether it plausibly explains the rejection.
6. What is still unknown.

Do not conclude that a library is responsible simply because its classes exist in the APK.

## Phase 4 — Investigate CleverTap

Identify the CleverTap SDK version if possible.

Analyze its client-side initialization, configuration and network implementation.

Determine whether CleverTap uses Android's default trust manager, a third-party networking client or custom certificate validation.

Trace the client-side origin of analytics events, their serialization and their handoff to the networking layer, where recoverable.

Investigate whether Hermes/React Native code creates events that are ultimately processed by the native CleverTap SDK.

Distinguish application-defined analytics data from automatically generated SDK data.

Do not infer actual transmitted request bodies from event names alone.

## Phase 5 — Identify the root cause

Create an evidence-based comparison of these hypotheses:

A. Android user CA is not trusted by Ownly.

B. Certificate pinning rejects PCAPdroid's generated certificate.

C. CleverTap or its HTTP client uses a custom trust store or certificate validator.

D. The proxy's certificate chain or configuration is invalid for another reason.

E. Multiple mechanisms contribute to the failure.

For each hypothesis, provide supporting evidence, contradictory evidence, missing evidence and a confidence rating.

Identify the strongest supported explanation.

If the evidence cannot distinguish two explanations, state that explicitly rather than guessing.

## Phase 6 — Determine how readable payloads could be obtained

The investigation goal is to understand the preconditions for observing authorized HTTP requests and responses.

Evaluate these environments separately:

1. The current non-rooted Android 10 phone.
2. A rooted research device used with appropriate authorization.
3. A developer-controlled debuggable Android build.
4. A developer-controlled React Native build with explicit networking diagnostics.

For each environment, explain:

- Whether the proxy CA can be trusted.
- Whether certificate pinning could still prevent interception.
- Whether the existing capture can be decrypted.
- Whether a new capture would be necessary.
- Whether request bodies may use additional encoding or application-level encryption.
- The limitations and risks.

Give a recommended diagnostic and remediation workflow for an authorized test build.

Do not patch the protected production APK, defeat Pairip, disable production certificate validation, extract credentials or replay authenticated production requests.

If readable production traffic cannot be obtained with the existing configuration, clearly explain the technical blocker and identify what additional authorized access would be required.

## Phase 7 — Correlate with the previous Hermes investigation

Read the existing architecture and Hermes reports.

Determine whether the recovered code reveals:

- API hostnames and endpoints.
- Request-building methods.
- Headers and body serialization.
- Network-client configuration.
- Analytics SDK event construction.
- React Native to native networking paths.

Map these findings to the observed network destinations where possible.

Do not fabricate endpoints, schemas or payload values.

## Required reports

Create or update:

- `reports/tls-root-cause.md`
- `reports/certificate-validation-analysis.md`
- `reports/clevertap-tls-analysis.md`
- `reports/network-capture-findings.md`
- `reports/payload-visibility-plan.md`

Each report must include actual evidence, relevant class/method names, commands used, and limitations.

## Final answer requirements

Give me a detailed final explanation covering:

1. What exactly failed in the TLS handshake.
2. Why PCAPdroid's certificate was rejected.
3. Whether Android CA trust or pinning is the demonstrated cause.
4. What the APK and Hermes analysis reveal.
5. Whether my existing PCAP contains any decryptable HTTP data.
6. Whether full payload visibility is possible on my current phone.
7. What additional access or configuration is required for authorized decrypted traffic analysis.
8. The next safest practical steps.

**Do not merely explain SSL certificate verification in general. Investigate this specific Ownly build, the actual capture files and the relevant code.**

Prioritize verifiable findings over speculation, and preserve all previously generated reports and APK files.
