# Detection Rules

ASTRA ships a Sigma detection rule with every technique. Sigma is an open, vendor-neutral rule format compatible with Splunk, Elastic SIEM, Microsoft Sentinel, Sumo Logic, IBM QRadar, and any other Sigma-supported backend.

All rules live in [`detection-rules/sigma/`](https://github.com/isha-singhMalik/Astra/tree/main/detection-rules/sigma) in the repository.

---

## Rule index

| Rule file | Technique | Severity | Status |
|-----------|-----------|----------|--------|
| [ASTRA-REC-001.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-REC-001.yml) | JS bundle scraping | Medium | experimental |
| [ASTRA-REC-002.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-REC-002.yml) | OpenAPI spec discovery | High | stable |
| [ASTRA-REC-003.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-REC-003.yml) | GraphQL introspection | High | stable |
| [ASTRA-AUTH-001.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-AUTH-001.yml) | JWT none algorithm | Critical | stable |
| [ASTRA-AUTH-002.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-AUTH-002.yml) | OAuth token leakage | High | experimental |
| [ASTRA-AUTH-003.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-AUTH-003.yml) | API key stuffing | High | experimental |
| [ASTRA-AUTHZ-001.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-AUTHZ-001.yml) | BOLA / IDOR | Critical | experimental |
| [ASTRA-AUTHZ-002.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-AUTHZ-002.yml) | BFLA | Critical | stable |
| [ASTRA-AUTHZ-003.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-AUTHZ-003.yml) | Mass assignment | High | experimental |
| [ASTRA-EXFIL-001.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-EXFIL-001.yml) | Excessive data exposure | Critical | experimental |
| [ASTRA-EXFIL-002.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-EXFIL-002.yml) | Pagination abuse | High | experimental |
| [ASTRA-IMPACT-001.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-IMPACT-001.yml) | Resource exhaustion | High | experimental |
| [ASTRA-IMPACT-002.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-IMPACT-002.yml) | Injection | Critical | stable |
| [ASTRA-IMPACT-003.yml](https://github.com/isha-singhMalik/Astra/blob/main/detection-rules/sigma/ASTRA-IMPACT-003.yml) | Business logic abuse | High | experimental |

---

## Using ASTRA Sigma rules

### Convert to your SIEM

Use [sigma-cli](https://github.com/SigmaHQ/sigma-cli) to convert rules to your platform's query language:

```bash
# Install sigma-cli
pip install sigma-cli

# Convert to Splunk SPL
sigma convert -t splunk detection-rules/sigma/ASTRA-AUTH-001.yml

# Convert to Elastic Query DSL
sigma convert -t elasticsearch detection-rules/sigma/ASTRA-AUTHZ-001.yml

# Convert all rules at once
sigma convert -t splunk detection-rules/sigma/*.yml
```

### Rule status meanings

- `stable` — tested, low false positive rate, safe to use in production alerting
- `experimental` — functional but may need tuning for your environment
- `deprecated` — superseded by a newer rule; kept for reference

---

## Improve a rule

Found a false positive or know a better detection pattern?

[Open a detection rule issue](https://github.com/isha-singhMalik/Astra/issues/new?template=update-detection-rule.md)
