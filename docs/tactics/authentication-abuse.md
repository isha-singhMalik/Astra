# Authentication Abuse

## Overview

Authentication abuse tactics cover all methods by which an attacker circumvents, bypasses, forges, or steals the credentials and tokens that identify a user to an API. Where authorization failure assumes a valid identity and tests what it can access, authentication abuse attacks the identity mechanism itself — the goal is to be seen as someone you're not, or to skip identity verification entirely.

APIs are particularly vulnerable because they rely heavily on stateless token-based authentication (JWTs, API keys, OAuth tokens) that carry no server-side session state — making token integrity the only barrier to impersonation.

## Techniques

| ID | Technique | Severity |
|----|-----------|----------|
| [ASTRA-AUTH-001](../techniques/authentication-abuse/ASTRA-AUTH-001.md) | JWT none algorithm bypass | Critical |
| [ASTRA-AUTH-002](../techniques/authentication-abuse/ASTRA-AUTH-002.md) | OAuth token leakage via referrer | High |
| [ASTRA-AUTH-003](../techniques/authentication-abuse/ASTRA-AUTH-003.md) | API key stuffing / brute force | High |

## Common root causes

- JWT libraries that accept unsigned tokens (`alg: none`)
- API keys transmitted in URLs (leaked in referrer headers and server logs)
- No rate limiting on authentication endpoints
- Long-lived tokens with no rotation or expiry
- OAuth `redirect_uri` validation too permissive

## Detection priority

Authentication abuse is often detectable through anomalous token patterns, login velocity, and geographic impossibilities. JWT none algorithm attacks have zero false positives and should be blocked immediately at the gateway.
