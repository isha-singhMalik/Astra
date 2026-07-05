# ASTRA — API Security Threat & Risk Atlas

> A structured, community-driven threat matrix for API security.  
> Protocol-native. Detection-first. Breach-mapped.

[![Version](https://img.shields.io/badge/version-1.0.0-6C63FF?style=flat-square)](https://github.com/isha-singhMalik/Astra/releases)
[![License](https://img.shields.io/badge/license-CC%20BY%204.0-0F6E56?style=flat-square)](LICENSE)
[![OWASP Incubator](https://img.shields.io/badge/OWASP-Incubator-993C1D?style=flat-square)](https://owasp.org/projects/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-BA7517?style=flat-square)](CONTRIBUTING.md)
[![Deploy](https://img.shields.io/github/actions/workflow/status/isha-singhMalik/Astra/deploy.yml?label=site&style=flat-square)](https://isha-singhmalik.github.io/Astra)

---

## What is ASTRA?

ASTRA is a **MITRE ATT&CK-style threat matrix built specifically for API security**. Where MITRE covers the entire enterprise attack surface and OWASP API Top 10 gives you a ranked list, ASTRA gives you a structured, navigable, protocol-native knowledge base of how APIs are attacked — and exactly how to detect and stop it.

**Every technique in ASTRA includes:**
- A clear description and attack scenario
- Protocol applicability (REST / GraphQL / gRPC / WebSocket / SOAP)
- A severity score (exploitability × impact × prevalence)
- A ready-to-use Sigma detection rule
- A real-world breach mapped to the technique
- Remediation guidance

---

## The Matrix

| ID | Technique | Tactic | Protocols | Severity |
|----|-----------|--------|-----------|----------|
| [ASTRA-REC-001](docs/techniques/reconnaissance/ASTRA-REC-001.md) | API endpoint enumeration via JS scraping | Reconnaissance | REST, GraphQL | Medium |
| [ASTRA-REC-002](docs/techniques/reconnaissance/ASTRA-REC-002.md) | OpenAPI / Swagger spec discovery | Reconnaissance | REST | High |
| [ASTRA-REC-003](docs/techniques/reconnaissance/ASTRA-REC-003.md) | GraphQL introspection leak | Reconnaissance | GraphQL | High |
| [ASTRA-AUTH-001](docs/techniques/authentication-abuse/ASTRA-AUTH-001.md) | JWT none algorithm bypass | Auth Abuse | REST, GraphQL | Critical |
| [ASTRA-AUTH-002](docs/techniques/authentication-abuse/ASTRA-AUTH-002.md) | OAuth token leakage via referrer | Auth Abuse | REST | High |
| [ASTRA-AUTH-003](docs/techniques/authentication-abuse/ASTRA-AUTH-003.md) | API key stuffing / brute force | Auth Abuse | REST, gRPC | High |
| [ASTRA-AUTHZ-001](docs/techniques/authorization-failure/ASTRA-AUTHZ-001.md) | Broken Object Level Authorization (BOLA) | AuthZ Failure | REST, GraphQL | Critical |
| [ASTRA-AUTHZ-002](docs/techniques/authorization-failure/ASTRA-AUTHZ-002.md) | Broken Function Level Authorization (BFLA) | AuthZ Failure | REST | Critical |
| [ASTRA-AUTHZ-003](docs/techniques/authorization-failure/ASTRA-AUTHZ-003.md) | Mass assignment / property injection | AuthZ Failure | REST, GraphQL | High |
| [ASTRA-EXFIL-001](docs/techniques/exfiltration/ASTRA-EXFIL-001.md) | Excessive data exposure | Exfiltration | REST, GraphQL | Critical |
| [ASTRA-EXFIL-002](docs/techniques/exfiltration/ASTRA-EXFIL-002.md) | Bulk data harvesting via pagination abuse | Exfiltration | REST | High |
| [ASTRA-IMPACT-001](docs/techniques/impact/ASTRA-IMPACT-001.md) | Resource exhaustion / API DoS | Impact | REST, gRPC, WebSocket | High |
| [ASTRA-IMPACT-002](docs/techniques/impact/ASTRA-IMPACT-002.md) | SQL / NoSQL injection via API parameters | Impact | REST, GraphQL | Critical |
| [ASTRA-IMPACT-003](docs/techniques/impact/ASTRA-IMPACT-003.md) | Business logic abuse | Impact | REST, GraphQL | High |

> v1.0 ships 14 techniques across 5 tactics. v2.0 roadmap targets 40+ techniques. [Contribute a technique →](CONTRIBUTING.md)

---

## Tactic Categories

| Tactic | Goal | Techniques |
|--------|------|------------|
| [Reconnaissance](docs/tactics/reconnaissance.md) | Discover API surface, endpoints, and schemas | 3 |
| [Authentication Abuse](docs/tactics/authentication-abuse.md) | Bypass, steal, or forge authentication credentials | 3 |
| [Authorization Failure](docs/tactics/authorization-failure.md) | Access resources or functions beyond intended permissions | 3 |
| [Exfiltration](docs/tactics/exfiltration.md) | Extract data at scale through API responses | 2 |
| [Impact](docs/tactics/impact.md) | Disrupt, destroy, or weaponize API functionality | 3 |

---

## What Makes ASTRA Different

| Feature | MITRE ATT&CK | OWASP API Top 10 | **ASTRA** |
|---------|-------------|------------------|-----------|
| API-specific | Partial | Yes | Yes |
| Protocol-native tagging | No | No | **Yes** |
| Ready detection rules | No | No | **Yes (Sigma)** |
| Severity scoring | Partial | Rank only | **Yes (composite)** |
| Real breach mappings | Some | Some | **Yes — every technique** |
| Community PR workflow | No | No | **Yes** |
| Versioned releases | Yes | Yes | **Yes** |
| Free & open source | Yes | Yes | **Yes** |

---

## Real Breach Mappings

| Breach | Year | ASTRA Technique | Impact |
|--------|------|-----------------|--------|
| Twitter / X | 2022 | ASTRA-AUTHZ-001 (BOLA) | 5.4M user records |
| Optus Australia | 2022 | ASTRA-EXFIL-001 (Excessive data exposure) | 10M customer records |
| Peloton | 2021 | ASTRA-AUTHZ-001 (BOLA) | All user data publicly accessible |
| T-Mobile | 2021 | ASTRA-REC-002 (API spec discovery) | 50M+ records |
| Coinbase | 2021 | ASTRA-AUTHZ-002 (BFLA) | Trading manipulation |

---

## Quick Start

### Use ASTRA for threat modelling

1. List all your API endpoints and group by function
2. For each group, identify which ASTRA tactics apply
3. Check each relevant technique — does your API have this attack vector?
4. Use the bundled Sigma rules to add detection to your SIEM
5. Prioritise remediation by severity score

### Use ASTRA for penetration testing

Browse techniques by tactic or protocol. Each technique page includes an attack scenario walkthrough you can run against a target in scope.

### Contribute a technique

See [CONTRIBUTING.md](CONTRIBUTING.md). Takes about 20 minutes to write a complete technique entry. We have an issue template to guide you.

---

## Detection Rules

All Sigma rules live in [`detection-rules/sigma/`](detection-rules/sigma/). Each `.yml` file maps 1:1 to an ASTRA technique ID.

Compatible with: Splunk, Elastic SIEM, Microsoft Sentinel, Sumo Logic, QRadar, and any Sigma-compatible backend.

---

## Repository Structure

```
astra/
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── docs/
│   ├── tactics/
│   └── techniques/
│       ├── reconnaissance/
│       ├── authentication-abuse/
│       ├── authorization-failure/
│       ├── exfiltration/
│       └── impact/
├── detection-rules/
│   └── sigma/
├── .github/
│   ├── workflows/
│   │   ├── deploy.yml
│   │   └── validate.yml
│   └── ISSUE_TEMPLATE/
└── mkdocs.yml
```

---

## Versioning

ASTRA follows semantic versioning:
- **Major** (v2.0) — new tactic categories or structural changes
- **Minor** (v1.1) — new techniques added
- **Patch** (v1.0.1) — corrections, detection rule updates

---

## License

ASTRA is released under [Creative Commons Attribution 4.0 (CC BY 4.0)](LICENSE).  
ASTRA was created by Isha Singh Malik in April 2026.
If you use or reference ASTRA, attribution is required under CC BY 4.0.You may use, share, and adapt ASTRA freely — with attribution.

---

## Author

Built and maintained by **Isha Singh Malik**.

[Website](https://isha-singhmalik.github.io/Astra) · [White Paper](docs/whitepaper.md) · [LinkedIn](https://www.linkedin.com/in/ishasinghmalik/) · [Twitter / X](https://x.com/ishamalik2427)

---

*ASTRA is an independent open-source project. Not affiliated with MITRE Corporation.*

> 📄 **White Paper v1.pdf is live** —
> [Download the ASTRA White Paper](ASTRA_WhitePaper_v1.pdf)