# ASTRA-AUTHZ-001 — Broken Object Level Authorization (BOLA / IDOR)

## Overview

Broken Object Level Authorization (BOLA), also known as Insecure Direct Object Reference (IDOR), occurs when an API exposes object identifiers (user IDs, account numbers, document IDs) in requests without verifying that the requesting user is authorized to access that specific object. An attacker who can enumerate or predict these identifiers can access any user's data by simply substituting their own ID for another's — without needing elevated privileges.

BOLA is the single most prevalent critical API vulnerability. It was ranked #1 in the OWASP API Security Top 10 in both 2019 and 2023.

## Tactic
Authorization Failure

## Protocols
REST · GraphQL · WebSocket

## Severity Score

| Dimension | Score (1–5) | Rationale |
|-----------|-------------|-----------|
| Exploitability | 5 | Trivial — change one parameter value |
| Prevalence | 5 | Most common critical API flaw |
| Data sensitivity | 4 | Typically exposes PII, account data |
| Business impact | 4 | Regulatory exposure, mass data breach |
| **Composite** | **4.5 / 5** | |

**Rating:** Critical

---

## Attack Scenario

An attacker registers a legitimate account on a platform and observes the API request pattern when accessing their own profile.

1. Attacker logs in and fetches their own profile: `GET /api/v1/users/10482`
2. Attacker observes the numeric user ID `10482` in the URL path
3. Attacker iterates: `GET /api/v1/users/10481`, `GET /api/v1/users/10480`, etc.
4. API returns full profile data for each user — name, email, phone, address — without checking if the token holder is user `10481`
5. Attacker scripts this across the full user ID range, harvesting the entire user base

The attack requires no special tooling — `curl` and a `for` loop is sufficient.

## Example Request / Payload

```http
GET /api/v1/users/10481 HTTP/1.1
Host: target.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...[token for user 10482]
Content-Type: application/json
```

**Expected (secure) response:** `403 Forbidden`  
**Vulnerable response:** Full user object returned for user `10481`

### GraphQL variant

```graphql
query {
  user(id: "10481") {
    id
    email
    phoneNumber
    address
    paymentMethods {
      cardLastFour
    }
  }
}
```

---

## Real-World Breach Mapping

| Field | Detail |
|-------|--------|
| Incident | Twitter / X API breach |
| Year | 2022 |
| Organisation | Twitter / X Corp |
| What happened | An unauthenticated API endpoint allowed enumeration of Twitter accounts by phone number or email, exposing whether specific numbers were linked to accounts — affecting 5.4M users |
| ASTRA technique | ASTRA-AUTHZ-001 |
| Source | https://www.bleepingcomputer.com/news/security/twitter-confirms-zero-day-used-to-expose-data-of-54-million-accounts/ |

| Field | Detail |
|-------|--------|
| Incident | Peloton API BOLA |
| Year | 2021 |
| Organisation | Peloton |
| What happened | Unauthenticated requests to `/api/ride/{id}/details` and user profile endpoints returned full private profile data for any user ID — even when accounts were set to private |
| ASTRA technique | ASTRA-AUTHZ-001 |
| Source | https://www.tenable.com/blog/peloton-api-security-flaw |

---

## Detection

### Sigma Rule
See [detection-rules/sigma/ASTRA-AUTHZ-001.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-AUTHZ-001.yml)

### What to look for

- A single authenticated session accessing > N different object IDs in a short window (e.g. >50 unique user IDs in 60 seconds)
- Sequential or near-sequential numeric IDs in URL paths across requests
- High volume of `200 OK` responses to parameterised object endpoints from a single token
- Access to object IDs that don't belong to the authenticated user (requires server-side correlation)
- User ID values in URL paths that differ from the `sub` claim in the presented JWT

### WAF / Gateway rule hint

Rate-limit and flag requests where a single client IP or API token accesses more than 30 unique numeric path parameters on user/account/resource endpoints within a 60-second window.

---

## Remediation

1. **Implement object-level authorization on every endpoint** — before returning any object, verify that the requesting user's identity (from the validated auth token) matches the owner of the requested object
2. **Never trust client-supplied IDs alone** — always re-derive the user's identity from the server-side session or token, not from a parameter
3. **Use non-enumerable, random identifiers** — replace sequential integer IDs with UUIDs (v4) to eliminate trivial enumeration (note: obscurity alone is not authorization — both are needed)
4. **Add authorization unit tests** — for every object-level endpoint, write a test that verifies user A cannot access user B's resource
5. **Log and alert on cross-user access patterns** — build detection into your platform, not just your WAF

---

## References

- [OWASP API Security Top 10 — API1:2023 BOLA](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)
- [PortSwigger — IDOR](https://portswigger.net/web-security/access-control/idor)
- [Salt Security — BOLA in the Wild](https://salt.security/blog/what-is-broken-object-level-authorization-bola)
- [CWE-639: Authorization Bypass Through User-Controlled Key](https://cwe.mitre.org/data/definitions/639.html)
