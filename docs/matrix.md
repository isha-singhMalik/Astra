# ASTRA Threat Matrix

Full matrix of all techniques across all tactics. Click any technique ID for the full entry.

---

## Reconnaissance

| ID | Technique | Protocols | Severity |
|----|-----------|-----------|----------|
| [ASTRA-REC-001](techniques/reconnaissance/ASTRA-REC-001.md) | API endpoint enumeration via JS scraping | REST, GraphQL | Medium |
| [ASTRA-REC-002](techniques/reconnaissance/ASTRA-REC-002.md) | OpenAPI / Swagger spec discovery | REST | High |
| [ASTRA-REC-003](techniques/reconnaissance/ASTRA-REC-003.md) | GraphQL introspection leak | GraphQL | High |

## Authentication Abuse

| ID | Technique | Protocols | Severity |
|----|-----------|-----------|----------|
| [ASTRA-AUTH-001](techniques/authentication-abuse/ASTRA-AUTH-001.md) | JWT none algorithm bypass | REST, GraphQL | Critical |
| [ASTRA-AUTH-002](techniques/authentication-abuse/ASTRA-AUTH-002.md) | OAuth token leakage via referrer | REST | High |
| [ASTRA-AUTH-003](techniques/authentication-abuse/ASTRA-AUTH-003.md) | API key stuffing / brute force | REST, gRPC | High |

## Authorization Failure

| ID | Technique | Protocols | Severity |
|----|-----------|-----------|----------|
| [ASTRA-AUTHZ-001](techniques/authorization-failure/ASTRA-AUTHZ-001.md) | Broken Object Level Authorization (BOLA) | REST, GraphQL, WebSocket | Critical |
| [ASTRA-AUTHZ-002](techniques/authorization-failure/ASTRA-AUTHZ-002.md) | Broken Function Level Authorization (BFLA) | REST, GraphQL | Critical |
| [ASTRA-AUTHZ-003](techniques/authorization-failure/ASTRA-AUTHZ-003.md) | Mass assignment / property injection | REST, GraphQL | High |

## Exfiltration

| ID | Technique | Protocols | Severity |
|----|-----------|-----------|----------|
| [ASTRA-EXFIL-001](techniques/exfiltration/ASTRA-EXFIL-001.md) | Excessive data exposure | REST, GraphQL | Critical |
| [ASTRA-EXFIL-002](techniques/exfiltration/ASTRA-EXFIL-002.md) | Bulk data harvesting via pagination abuse | REST | High |

## Impact

| ID | Technique | Protocols | Severity |
|----|-----------|-----------|----------|
| [ASTRA-IMPACT-001](techniques/impact/ASTRA-IMPACT-001.md) | Resource exhaustion / API DoS | REST, gRPC, WebSocket | High |
| [ASTRA-IMPACT-002](techniques/impact/ASTRA-IMPACT-002.md) | SQL / NoSQL injection via API parameters | REST, GraphQL | Critical |
| [ASTRA-IMPACT-003](techniques/impact/ASTRA-IMPACT-003.md) | Business logic abuse | REST, GraphQL | High |

---

## Severity legend

| Rating | Composite Score | Meaning |
|--------|----------------|---------|
| Critical | 4.0 – 5.0 | Immediate threat; exploitable by unauthenticated or low-privilege attacker with catastrophic impact |
| High | 3.0 – 3.9 | Significant threat; requires some access or skill; high data or business impact |
| Medium | 2.0 – 2.9 | Moderate threat; enables follow-on attacks or partial data exposure |
| Low | < 2.0 | Limited direct impact; typically an enabler technique |

---

*ASTRA v1.0 — [Contribute a technique →](contributing.md)*
