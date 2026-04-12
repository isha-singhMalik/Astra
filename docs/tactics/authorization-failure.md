# Authorization Failure

## Overview

Authorization failure tactics cover all cases where an API allows a user to access resources or invoke functions beyond what they are legitimately permitted to do. Authentication confirms *who you are*. Authorization governs *what you can do*. These are separate concerns — an API can authenticate correctly and still fail entirely at authorization.

Authorization failures are the most impactful class of API vulnerabilities because they directly expose data and functionality to unauthorized parties, often at scale.

## Why APIs are especially vulnerable

Traditional web applications tend to enforce authorization in server-rendered views — if the view is hidden, the data is inaccessible. APIs are different: they expose raw data and functions directly. A developer can remove a button from the UI while leaving the underlying API endpoint completely unprotected. Mobile apps are decompilable, JavaScript bundles are readable, and proxy tools trivially expose every API call the frontend makes.

The result: authorization logic that was "enforced by the UI" is bypassed in seconds.

## Techniques

| ID | Technique | Severity |
|----|-----------|----------|
| [ASTRA-AUTHZ-001](../techniques/authorization-failure/ASTRA-AUTHZ-001.md) | Broken Object Level Authorization (BOLA / IDOR) | Critical |
| [ASTRA-AUTHZ-002](../techniques/authorization-failure/ASTRA-AUTHZ-002.md) | Broken Function Level Authorization (BFLA) | Critical |
| [ASTRA-AUTHZ-003](../techniques/authorization-failure/ASTRA-AUTHZ-003.md) | Mass Assignment / Property Injection | High |

## Key distinction from Authentication Abuse

- **Authentication Abuse** — the attacker forges or steals credentials to be seen as a legitimate user
- **Authorization Failure** — the attacker uses legitimate credentials but accesses things they shouldn't be able to

Most authorization failures require no credential theft. A regular user account is sufficient.

## Common root causes

- Object ownership not verified before returning data
- Role checks missing from admin endpoints assumed to be "hidden"
- ORM `.save()` methods accepting all client-supplied fields without filtering
- Copy-paste route handlers that inherit incorrect permission middleware
- Authorization logic implemented in the frontend, not the API

## Detection priority

Authorization failures are often silent — they return `200 OK` and look like normal traffic. Detection requires understanding what *should* be accessible, not just what *is* being accessed. Invest in:

- Object-ownership correlation (does this token's user ID match the requested resource's owner ID?)
- Cross-user access rate monitoring (one token accessing N different user IDs)
- Role-vs-endpoint mapping enforcement at the gateway layer
