# ASTRA-REC-002 — OpenAPI / Swagger Specification Discovery

## Overview

Many APIs expose their OpenAPI (Swagger) specification at well-known paths by default. This document is a machine-readable blueprint of the entire API: every endpoint, every HTTP method, every parameter, every request body schema, every response schema, and every authentication requirement. For an attacker, finding this file is equivalent to receiving the API's full technical documentation — typically more detailed than anything the developer intentionally published.

## Tactic
Reconnaissance

## Protocols
REST

## Severity Score

| Dimension | Score (1–5) | Rationale |
|-----------|-------------|-----------|
| Exploitability | 5 | Wordlist-based; fully automated |
| Prevalence | 4 | Default in many frameworks (FastAPI, SpringDoc, NestJS) |
| Data sensitivity | 3 | Schema and auth requirements exposed, not user data |
| Business impact | 3 | Dramatically accelerates targeted attacks |
| **Composite** | **3.75 / 5** | |

**Rating:** High

---

## Attack Scenario

1. Attacker probes well-known spec paths using a wordlist or automated tool
2. Discovers `https://api.target.com/v2/api-docs` returns a full OpenAPI 3.0 JSON document
3. Imports the spec into Postman, Insomnia, or a purpose-built tool like `APIFuzzer`
4. Within minutes has a fully configured test environment with every endpoint, parameter type, and auth scheme documented
5. Begins systematic testing of each endpoint for BOLA, BFLA, injection, and business logic issues

## Example Request / Payload

```bash
# Common spec paths to probe
for path in swagger.json swagger.yaml openapi.json openapi.yaml \
            api-docs v1/api-docs v2/api-docs v3/api-docs \
            swagger/v1/swagger.json swagger-ui.html api/swagger.json; do
  curl -s -o /dev/null -w "%{http_code} $path\n" \
    https://target.example.com/$path
done
```

---

## Real-World Breach Mapping

| Field | Detail |
|-------|--------|
| Incident | Peloton API exposure |
| Year | 2021 |
| Organisation | Peloton |
| What happened | Researchers discovered Peloton's API had an exposed OpenAPI spec that revealed undocumented endpoints, combined with no authentication on user data endpoints — enabling full profile enumeration |
| ASTRA technique | ASTRA-REC-002 |
| Source | https://www.tenable.com/blog/peloton-api-security-flaw |

---

## Detection

### Sigma Rule
See [detection-rules/sigma/ASTRA-REC-002.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-REC-002.yml)

### What to look for
- Requests to known OpenAPI/Swagger paths from external IPs
- Large JSON/YAML responses (>50KB) from `/api-docs`, `/swagger`, `/openapi` paths
- Sequential probing of multiple spec paths from the same IP within 60 seconds

### WAF / Gateway rule hint
Block or require authentication for all paths matching: `*swagger*`, `*api-docs*`, `*openapi*`, `*redoc*`.

---

## Remediation

1. **Disable spec exposure in production** — most frameworks have a config flag; set it to off for production deployments
2. **If spec must be accessible, require authentication** — even basic auth protects against automated discovery
3. **Never expose internal-only endpoints in the public spec** — use separate spec files for public vs internal APIs
4. **Audit your spec for sensitive data** — example values in specs sometimes contain real credentials or internal hostnames

---

## References

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [OWASP API Security — Improper Assets Management](https://owasp.org/API-Security/editions/2023/en/0xa9-improper-inventory-management/)
