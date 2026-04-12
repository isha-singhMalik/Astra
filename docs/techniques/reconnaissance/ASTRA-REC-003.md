# ASTRA-REC-003 — GraphQL Introspection Leak

## Overview

GraphQL's introspection system allows clients to query the API schema itself — discovering every type, query, mutation, field, and argument the API exposes. While invaluable in development, leaving introspection enabled in production gives any attacker a complete blueprint of your API surface in a single request. This dramatically accelerates reconnaissance, revealing hidden fields, admin mutations, internal types, and deprecated endpoints that were never meant to be public-facing.

Unlike REST APIs where endpoint discovery requires fuzzing, a single introspection query against a GraphQL API returns the entire attack surface in one response.

## Tactic
Reconnaissance

## Protocols
GraphQL

## Severity Score

| Dimension | Score (1–5) | Rationale |
|-----------|-------------|-----------|
| Exploitability | 5 | Single query, no auth required in many cases |
| Prevalence | 4 | Widely misconfigured in production |
| Data sensitivity | 3 | Exposes schema, not data directly |
| Business impact | 3 | Significantly accelerates follow-on attacks |
| **Composite** | **3.75 / 5** | |

**Rating:** High

---

## Attack Scenario

An attacker identifies a GraphQL endpoint (typically `/graphql`, `/api/graphql`, `/v1/graphql`) and runs a full introspection query.

1. Attacker sends a standard introspection query to `https://target.example.com/graphql`
2. API returns the full schema: all types, queries, mutations, subscriptions, and field names
3. Attacker identifies interesting targets: `adminMutation`, `deleteUser`, `internalUserData`, `legacyAccountTransfer`
4. Attacker maps field types and arguments: `deleteUser(userId: ID!, force: Boolean)`
5. Attacker proceeds to test BOLA, BFLA, and injection against the now-fully-documented surface

## Example Request / Payload

```graphql
{
  __schema {
    queryType { name }
    mutationType { name }
    subscriptionType { name }
    types {
      name
      kind
      description
      fields {
        name
        description
        args {
          name
          type { name kind }
          defaultValue
        }
        type { name kind }
      }
    }
    directives {
      name
      locations
      args { name }
    }
  }
}
```

```http
POST /graphql HTTP/1.1
Host: target.example.com
Content-Type: application/json

{"query": "{ __schema { types { name fields { name args { name } } } } }"}
```

**Tools that automate this:**
- `graphw00f` — fingerprints GraphQL engine then dumps schema
- `InQL` — Burp Suite extension for GraphQL recon
- `graphql-voyager` — visualises introspection output as an interactive graph

---

## Real-World Breach Mapping

| Field | Detail |
|-------|--------|
| Incident | HackerOne GraphQL introspection exposure |
| Year | 2020 |
| Organisation | HackerOne |
| What happened | A researcher found that HackerOne's GraphQL API had introspection enabled, exposing internal query types including fields related to undisclosed vulnerability reports. The schema revealed access patterns that could be further probed. |
| ASTRA technique | ASTRA-REC-003 |
| Source | https://hackerone.com/reports/291531 |

---

## Detection

### Sigma Rule
See [detection-rules/sigma/ASTRA-REC-003.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-REC-003.yml)

### What to look for

- HTTP POST requests to GraphQL endpoints containing `__schema` in the body
- Requests containing `__type` introspection queries
- High-volume single requests returning unusually large GraphQL responses (full schema dumps are typically >50KB)
- Tool-specific patterns: `graphw00f`, `InQL`, or `graphql-introspection-detector` user agent strings

### WAF / Gateway rule hint

Inspect POST body for GraphQL requests. Flag and optionally block requests where the body contains `__schema` or `__type(name:` outside of development environments. Consider returning a generic error rather than a `disabled` message (which confirms GraphQL is running).

---

## Remediation

1. **Disable introspection in production** — most GraphQL frameworks support a single config flag: `introspection: false`
2. **If introspection is required, require authentication** — authenticated introspection for internal tooling is acceptable; public introspection is not
3. **Disable field suggestions** — GraphQL error messages that suggest similar field names when you typo also leak schema information; disable these too
4. **Use query depth and complexity limiting** — even with introspection disabled, implement query depth limits to prevent abuse via nested query exploration
5. **Audit your schema for sensitive field names** — fields like `adminOverride`, `internalOnly`, `debug`, `_raw` are red flags

---

## References

- [OWASP GraphQL Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html)
- [HackerOne — GraphQL introspection report #291531](https://hackerone.com/reports/291531)
- [GraphQL — Introspection docs](https://graphql.org/learn/introspection/)
- [graphw00f — GraphQL fingerprinting tool](https://github.com/dolevf/graphw00f)
