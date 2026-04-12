# Impact

## Overview

Impact tactics cover how attackers weaponize API access to cause direct harm: disrupting availability, corrupting or destroying data, injecting malicious payloads, or abusing business logic for financial gain. These are the end-stage attacks — they follow successful reconnaissance, authentication, and authorization steps, or exploit vulnerabilities that allow direct impact without prior access.

## Techniques

| ID | Technique | Severity |
|----|-----------|----------|
| [ASTRA-IMPACT-001](../techniques/impact/ASTRA-IMPACT-001.md) | Resource exhaustion / API DoS | High |
| [ASTRA-IMPACT-002](../techniques/impact/ASTRA-IMPACT-002.md) | SQL / NoSQL injection via API parameters | Critical |
| [ASTRA-IMPACT-003](../techniques/impact/ASTRA-IMPACT-003.md) | Business logic abuse | High |

## Why impact attacks are often underestimated

APIs introduce new impact vectors that don't exist in traditional web applications. A deeply nested GraphQL query can bring down a database. A single API endpoint with missing input validation can be a full SQL injection point. A payment API without idempotency checks can be exploited for double-spend attacks.

## Detection priority

Injection attacks produce distinctive patterns in query logs and error rates. Resource exhaustion attacks are visible in infrastructure metrics. Business logic abuse is the hardest to detect — it requires understanding what *should* happen in a transaction flow, not just what *is* happening.
