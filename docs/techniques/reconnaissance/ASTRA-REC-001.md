# ASTRA-REC-001 — API Endpoint Enumeration via JavaScript Scraping

## Overview

Modern single-page applications bundle their API call patterns directly into JavaScript files served to every browser. Attackers scrape these bundles to extract every `fetch()`, `axios()`, `$.ajax()`, or `HttpClient` call, building a complete list of API endpoints without ever sending a request to the server. This technique requires no authentication and leaves no footprint on the target API.

## Tactic
Reconnaissance

## Protocols
REST · GraphQL

## Severity Score

| Dimension | Score (1–5) | Rationale |
|-----------|-------------|-----------|
| Exploitability | 5 | Fully passive — no server requests needed |
| Prevalence | 5 | Universal in SPA-based applications |
| Data sensitivity | 2 | Reveals endpoints, not data |
| Business impact | 2 | Enables follow-on attacks |
| **Composite** | **3.5 / 5** | |

**Rating:** Medium

---

## Attack Scenario

1. Attacker visits the target web application and loads it in a browser
2. Opens DevTools → Sources, or downloads all `.js` bundle files via `wget` / `curl`
3. Runs a regex over bundles to extract all API paths: `grep -oE '"/api/[^"]*"' *.js`
4. Deduplicates and sorts results — full endpoint list obtained
5. Proceeds to probe discovered endpoints for authentication gaps, BOLA, or BFLA

## Example Request / Payload

```bash
# Download and scrape JS bundles
curl -s https://target.example.com | grep -oE 'src="[^"]*\.js"' | \
  xargs -I{} curl -s https://target.example.com/{} | \
  grep -oE '"(/api/v[0-9]/[^"]*)"' | sort -u
```

**Typical finds:** `/api/v1/users/{id}`, `/api/v1/admin/export`, `/api/v2/payments/{id}/refund`

---

## Real-World Breach Mapping

| Field | Detail |
|-------|--------|
| Incident | T-Mobile 2021 API breach |
| Year | 2021 |
| Organisation | T-Mobile |
| What happened | Attacker reportedly discovered an unprotected API endpoint via external reconnaissance including JS analysis, enabling access to a database containing 50M+ customer records |
| ASTRA technique | ASTRA-REC-001 |
| Source | https://www.wsj.com/articles/t-mobile-investigating-possible-data-breach-11629208791 |

---

## Detection

### Sigma Rule
See [detection-rules/sigma/ASTRA-REC-001.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-REC-001.yml)

### What to look for
- Single IP downloading all JS bundle files in rapid succession (< 10 seconds total load time)
- Automated user agents scraping static assets without corresponding page navigation events
- Subsequent probing of endpoints only discoverable via JS bundle review

### WAF / Gateway rule hint
Flag IPs that download 5+ unique `.js` bundle files within 30 seconds with no corresponding HTML page request.

---

## Remediation

1. **Minimise endpoint information in client-side code** — keep sensitive or admin API paths server-side only; don't embed them in frontend bundles
2. **Use API gateway route discovery controls** — don't rely on obscurity alone; ensure every discovered endpoint has proper authentication
3. **Implement subresource integrity** — helps detect bundle tampering, not enumeration, but part of a broader frontend security posture
4. **Remove dead / legacy endpoints** — if an endpoint is in a JS bundle but no longer supported, remove it from the router entirely

---

## References

- [OWASP Testing Guide — API Discovery](https://owasp.org/www-project-web-security-testing-guide/)
- [TruffleHog — Secrets in JS bundles](https://github.com/trufflesecurity/trufflehog)
