# Contributing to ASTRA

First — thank you. ASTRA is only as useful as its community makes it.

Every technique you add, every breach you map, every detection rule you improve makes ASTRA more valuable for every security engineer, pentester, and developer who uses it.

---

## What You Can Contribute

- **New technique** — an API attack technique not yet in the matrix
- **New breach mapping** — a public breach that maps to an existing technique
- **New / improved detection rule** — a better Sigma rule for an existing technique
- **Correction** — fix an error in a technique description, severity score, or example
- **Translation** — translate technique pages to other languages

---

## Before You Start

1. Check existing techniques in the [matrix](README.md#the-matrix) — don't duplicate
2. Check open issues and PRs — someone may already be working on it
3. Open an issue first for new techniques using the [New Technique template](https://github.com/isha-singhMalik/Astra/issues/new?template=new-technique.md) — get a thumbs-up before writing

---

## Quick Links

- [New technique issue](https://github.com/isha-singhMalik/Astra/issues/new?template=new-technique.md)
- [New breach mapping issue](https://github.com/isha-singhMalik/Astra/issues/new?template=new-breach-mapping.md)
- [Update detection rule issue](https://github.com/isha-singhMalik/Astra/issues/new?template=update-detection-rule.md)
- [All open issues](https://github.com/isha-singhMalik/Astra/issues)
- [All open PRs](https://github.com/isha-singhMalik/Astra/pulls)

---

## Technique File Format

Every technique lives at:
```
docs/techniques/{tactic-slug}/ASTRA-{TACTIC}-{NUM}.md
```

Copy this template exactly:

```markdown
# ASTRA-XXX-000 — Technique Name

## Overview
One paragraph. What the attack is, why it works, what the attacker gains.

## Tactic
{Reconnaissance | Authentication Abuse | Authorization Failure | Exfiltration | Impact}

## Protocols
{REST} {GraphQL} {gRPC} {WebSocket} {SOAP}

## Severity Score

| Dimension | Score (1–5) | Rationale |
|-----------|-------------|-----------|
| Exploitability | X | How easy is it to execute? |
| Prevalence | X | How common is this in the wild? |
| Data sensitivity | X | How sensitive is what's exposed? |
| Business impact | X | Financial / reputational damage? |
| **Composite** | **X.X / 5** | Average of above |

**Rating:** Critical / High / Medium / Low

## Attack Scenario

1. Step one
2. Step two
3. Step three

## Example Request / Payload

\`\`\`http
GET /api/v1/example HTTP/1.1
Host: target.example.com
\`\`\`

## Real-World Breach Mapping

| Field | Detail |
|-------|--------|
| Incident | Name of breach |
| Year | YYYY |
| Organisation | Company name |
| What happened | One sentence |
| ASTRA technique | ASTRA-XXX-000 |
| Source | https://reference-url.com |

## Detection

### Sigma Rule
See [detection-rules/sigma/ASTRA-XXX-000.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-XXX-000.yml)

### What to look for
- Behavioural indicator one
- Behavioural indicator two

### WAF / Gateway rule hint
What pattern a WAF should flag.

## Remediation

1. Step one
2. Step two

## References

- [OWASP API Security Top 10](https://owasp.org/API-Security/)
- [CWE Reference](https://cwe.mitre.org/)
```

---

## Sigma Rule Format

Each technique gets one Sigma rule file at:
```
detection-rules/sigma/ASTRA-{TACTIC}-{NUM}.yml
```

The `tags` field must include the ASTRA technique ID prefixed with `astra.` — for example `astra.ASTRA-REC-001`.

---

## Severity Scoring Guide

Score each dimension 1–5:

| Score | Exploitability | Prevalence | Data sensitivity | Business impact |
|-------|----------------|------------|------------------|-----------------|
| 1 | Requires insider access | Rare / theoretical | Public data only | Cosmetic |
| 2 | Requires authenticated user | Occasional | Low-sensitivity PII | Minor |
| 3 | Requires valid API key | Common | Standard PII | Moderate disruption |
| 4 | Unauthenticated, some skill | Very common | Financial / health data | Significant breach |
| 5 | Unauthenticated, trivial | Ubiquitous | Critical credentials | Catastrophic |

Composite = average of all four dimensions, rounded to 1 decimal.

**Rating thresholds:** Critical ≥ 4.0 · High ≥ 3.0 · Medium ≥ 2.0 · Low < 2.0

---

## PR Checklist

- [ ] Technique file uses the exact template format
- [ ] All required sections present
- [ ] Sigma rule file present and named correctly
- [ ] ASTRA technique ID follows the format `ASTRA-{TACTIC}-{NNN}`
- [ ] Real-world breach mapping included (use "TBD" if none known)
- [ ] Matrix table in README.md updated with the new technique row

---

## Code of Conduct

Be excellent to each other. Technical project focused on defence and education. No glorifying attackers, no celebrating breaches.

---

## Questions?

Open a [Discussion](https://github.com/isha-singhMalik/Astra/discussions) or reach out on [LinkedIn](https://www.linkedin.com/in/ishasinghmalik/).
