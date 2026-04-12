# Exfiltration

## Overview

Exfiltration tactics cover how attackers extract data at scale through API responses. Unlike a traditional database breach, API exfiltration uses the API's own legitimate response mechanisms — the attacker simply calls the API many times, collects the responses, and aggregates the data. No SQL injection, no file system access, no privilege escalation required.

APIs are ideal exfiltration channels because they return structured, machine-parseable data. A script that calls an endpoint 100,000 times is functionally identical to a legitimate high-volume client — making exfiltration difficult to distinguish from normal usage.

## Techniques

| ID | Technique | Severity |
|----|-----------|----------|
| [ASTRA-EXFIL-001](../techniques/exfiltration/ASTRA-EXFIL-001.md) | Excessive data exposure | Critical |
| [ASTRA-EXFIL-002](../techniques/exfiltration/ASTRA-EXFIL-002.md) | Bulk data harvesting via pagination abuse | High |

## What makes API exfiltration difficult to stop

- Legitimate clients make the same calls at high volume (analytics pipelines, mobile apps syncing data)
- Rate limiting is often based on IP, not user or data sensitivity
- APIs return more data than needed — filtering is done client-side
- Paginated endpoints are designed for bulk access; abusing them looks identical to using them

## Detection priority

Focus on volume anomalies per authenticated identity, not per IP. An attacker using a valid token calling 50,000 endpoints in 6 hours looks like a bot — but distributed across residential proxies it looks like 50,000 users. Fingerprint access patterns, not just source addresses.
