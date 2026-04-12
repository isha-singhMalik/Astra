# ASTRA-AUTHZ-002 — Broken Function Level Authorization (BFLA)

## Overview

Broken Function Level Authorization occurs when an API exposes privileged functions — admin operations, bulk data exports, user deletion, role changes — without adequately verifying that the caller has permission to invoke them. Unlike BOLA (which is about accessing another user's data), BFLA is about accessing functionality above your privilege level. Regular users can call admin endpoints. Junior staff can invoke executive functions. External APIs can trigger internal-only operations.

BFLA is particularly dangerous because these endpoints often perform destructive, irreversible, or highly sensitive operations — and they're frequently overlooked in access control reviews because developers assume "no one will know this endpoint exists."

## Tactic
Authorization Failure

## Protocols
REST · GraphQL

## Severity Score

| Dimension | Score (1–5) | Rationale |
|-----------|-------------|-----------|
| Exploitability | 4 | Requires knowing endpoint exists; often discoverable |
| Prevalence | 4 | Common in APIs with role-based access |
| Data sensitivity | 4 | Enables privilege escalation, bulk operations |
| Business impact | 5 | Account takeover, data destruction, fraud |
| **Composite** | **4.25 / 5** | |

**Rating:** Critical

---

## Attack Scenario

An attacker with a regular user account discovers admin-level API endpoints by reading JavaScript bundles, OpenAPI specs, or mobile app binaries — and calls them directly.

1. Attacker reverse-engineers the mobile app's JavaScript bundle or intercepts traffic
2. Discovers undocumented endpoint: `POST /api/v1/admin/users/{id}/role`
3. Calls it with their own authenticated token: `{"role": "admin"}`
4. API checks that the request is authenticated (valid token) — but does not check that the token holder has admin role
5. Attacker is now an admin

### Variant: Horizontal privilege escalation via function

1. Regular user calls `POST /api/v1/users/{victim_id}/password-reset` (intended for admins only)
2. API sends a password reset to the victim's email, which the attacker intercepts (if they control that email) or uses to lock the victim out

## Example Request / Payload

```http
POST /api/v1/admin/users/99/role HTTP/1.1
Host: target.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...[regular user token]
Content-Type: application/json

{"role": "admin"}
```

**Expected (secure) response:** `403 Forbidden — insufficient permissions`  
**Vulnerable response:** `200 OK — role updated`

### GraphQL mutation variant

```graphql
mutation {
  updateUserRole(userId: "99", role: ADMIN) {
    id
    role
    email
  }
}
```

---

## Real-World Breach Mapping

| Field | Detail |
|-------|--------|
| Incident | Coinbase Advanced Trade API BFLA |
| Year | 2021 |
| Organisation | Coinbase |
| What happened | A vulnerability in Coinbase's Advanced Trade API allowed authenticated regular users to invoke trading functions they were not authorized to use, including placing orders on behalf of other users. Researchers demonstrated manipulation of other users' trading activity. |
| ASTRA technique | ASTRA-AUTHZ-002 |
| Source | https://hackerone.com/reports/1369820 |

---

## Detection

### Sigma Rule
See [detection-rules/sigma/ASTRA-AUTHZ-002.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-AUTHZ-002.yml)

### What to look for

- Non-admin authenticated tokens calling endpoints in `/admin/`, `/internal/`, `/manage/`, `/ops/` path segments
- Regular user tokens calling HTTP verbs (DELETE, PUT, PATCH) on resource endpoints they would normally only GET
- Requests to endpoints that match admin endpoint naming conventions from user-role tokens
- Unusual mutations in GraphQL from non-privileged sessions (`deleteUser`, `updateRole`, `resetPassword` for other users)

### WAF / Gateway rule hint

Maintain a list of admin/privileged endpoint patterns (`/admin/*`, `/internal/*`, `/manage/*`). Any request matching these patterns should be routed through a role-validation middleware before reaching the handler. Flag and block requests where the JWT role claim is not in the allowed roles list for the endpoint.

---

## Remediation

1. **Implement function-level authorization middleware** — every route should declare its required role(s); a central middleware enforces this before the handler runs
2. **Deny by default** — if an endpoint doesn't have an explicit authorization rule, it should return 403
3. **Don't rely on obscurity** — hiding admin endpoints is not authorization; assume attackers can discover every endpoint
4. **Separate admin API surfaces** — consider deploying admin APIs on a separate internal service not accessible from the public internet
5. **Test with a lower-privilege token** — for every admin endpoint, add an automated test that verifies it returns 403 when called with a regular user token

---

## References

- [OWASP API Security — API5:2023 Broken Function Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/)
- [HackerOne — Coinbase BFLA report](https://hackerone.com/reports/1369820)
- [CWE-285: Improper Authorization](https://cwe.mitre.org/data/definitions/285.html)
- [PortSwigger — Access control vulnerabilities](https://portswigger.net/web-security/access-control)
