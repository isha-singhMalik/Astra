# ASTRA-EXFIL-001 — Excessive Data Exposure

## Overview

Excessive Data Exposure occurs when an API returns far more data than the client needs for its stated purpose, relying on the frontend to filter what is actually displayed to the user. The full object — including sensitive fields — is returned in the API response and visible to anyone intercepting or inspecting the traffic. An attacker who calls the API directly (bypassing the frontend) receives all unexposed fields: internal user flags, hashed passwords, PII, financial data, admin metadata, or relationship data.

This is one of the most common API vulnerabilities because it stems from a development convenience: returning the full model object is easier than crafting a response tailored to each use case.

## Tactic
Exfiltration

## Protocols
REST · GraphQL

## Severity Score

| Dimension | Score (1–5) | Rationale |
|-----------|-------------|-----------|
| Exploitability | 5 | Just call the API directly and read the response |
| Prevalence | 5 | Extremely common — default ORM serialization pattern |
| Data sensitivity | 4 | Often exposes PII, tokens, hashed credentials |
| Business impact | 4 | Mass data exposure, regulatory penalties |
| **Composite** | **4.5 / 5** | |

**Rating:** Critical

---

## Attack Scenario

An attacker uses a mobile API or web app's developer tools to observe API calls and then replays them directly, inspecting the raw response rather than what the app renders.

1. Attacker opens a ride-sharing app and loads their own profile page
2. Using a proxy (Burp Suite / mitmproxy), attacker captures: `GET /api/v1/users/me`
3. App displays: name, profile photo, star rating
4. Raw API response contains: name, email, phone, hashed password, internal user flags (`is_banned: false`, `fraud_score: 12`), exact GPS coordinates from last 20 rides, payment method tokens, and admin notes
5. Attacker extracts all hidden fields — none of which were displayed in the app but all were transmitted

### Scale amplification via enumeration

Combine with ASTRA-AUTHZ-001 (BOLA): once excessive data exposure is confirmed on `/users/{id}`, an attacker can enumerate all user IDs and harvest the full dataset for every user.

## Example Request / Payload

```http
GET /api/v1/users/me HTTP/1.1
Host: target.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
```

**What the app shows:**
```json
{
  "name": "Alice Smith",
  "avatar": "https://cdn.example.com/avatars/alice.jpg",
  "rating": 4.8
}
```

**What the API actually returns:**
```json
{
  "id": 10482,
  "name": "Alice Smith",
  "email": "alice@example.com",
  "phone": "+44 7911 123456",
  "password_hash": "$2b$12$LQv3c1yqBWVHxkd...",
  "avatar": "https://cdn.example.com/avatars/alice.jpg",
  "rating": 4.8,
  "is_banned": false,
  "fraud_score": 12,
  "admin_notes": "VIP customer — escalate complaints",
  "stripe_customer_id": "cus_NffrFeUfNV2Hib",
  "last_location": {"lat": 51.5074, "lng": -0.1278},
  "created_at": "2021-03-14T09:22:11Z",
  "internal_flags": ["beta_tester", "legacy_account"]
}
```

---

## Real-World Breach Mapping

| Field | Detail |
|-------|--------|
| Incident | Optus Australia data breach |
| Year | 2022 |
| Organisation | Optus (Singtel subsidiary) |
| What happened | An unauthenticated API endpoint returned full customer records including names, dates of birth, phone numbers, email addresses, and identity document numbers. The API required no authentication and exposed the complete customer object rather than a filtered response. |
| ASTRA technique | ASTRA-EXFIL-001 |
| Source | https://www.itnews.com.au/news/optus-breach-an-api-with-no-authentication-591019 |

---

## Detection

### Sigma Rule
See [detection-rules/sigma/ASTRA-EXFIL-001.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-EXFIL-001.yml)

### What to look for

- API responses significantly larger than the UI would require (e.g. `/users/me` returning >2KB when the displayed profile is minimal)
- Sensitive field names in response bodies: `password`, `hash`, `token`, `secret`, `ssn`, `dob`, `internal`, `admin`, `fraud`
- High-frequency calls to user/profile endpoints from a single client, especially if cross-user (correlate with BOLA detection)
- Requests from non-browser clients (missing or unusual user agents) to endpoints typically called by the frontend app

### WAF / Gateway rule hint

Implement response scanning at the API gateway layer. Flag responses containing keywords like `password_hash`, `ssn`, `tax_id`, `internal_`, `_secret`, `admin_note` in JSON keys. This is a data loss prevention (DLP) pattern applied to API responses.

---

## Remediation

1. **Define explicit response schemas** — never return a full ORM model object; define a dedicated response DTO/serializer for each endpoint that includes only required fields
2. **Adopt an API specification-first approach** — use OpenAPI to define exactly what each endpoint returns, then validate responses against that spec in tests
3. **Implement response validation in CI** — add automated tests that call each endpoint and assert the response does not contain sensitive field names
4. **Use field-level access control for GraphQL** — don't rely on the frontend to skip fields; implement resolver-level field permissions
5. **Conduct regular API response audits** — periodically spider your own API and analyse response payloads for unexpected sensitive data

---

## References

- [OWASP API Security — API3:2023 Broken Object Property Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/)
- [ITNews — Optus breach analysis](https://www.itnews.com.au/news/optus-breach-an-api-with-no-authentication-591019)
- [CWE-213: Exposure of Sensitive Information Due to Incompatible Policies](https://cwe.mitre.org/data/definitions/213.html)
