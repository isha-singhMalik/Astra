# Changelog

All notable changes to ASTRA are documented here.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
ASTRA uses [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2026-04-10

### Added
- Initial release of the ASTRA framework
- 5 tactic categories: Reconnaissance, Authentication Abuse, Authorization Failure, Exfiltration, Impact
- 14 techniques (ASTRA-REC-001 through ASTRA-IMPACT-003)
- Sigma detection rules for all 14 techniques
- Real-world breach mappings: Twitter 2022, Optus 2022, Peloton 2021, T-Mobile 2021, Coinbase 2021
- GitHub Actions CI/CD pipeline for auto-deployment to GitHub Pages
- PR validation bot enforcing technique format
- Issue templates for community contributions
- MkDocs documentation site
- ASTRA White Paper v1.0

### Framework
- Composite severity scoring system (exploitability × prevalence × data sensitivity × business impact)
- Protocol-native tagging (REST, GraphQL, gRPC, WebSocket, SOAP)
- Contributing guide and technique template

---

## Roadmap

### [1.1.0] — Planned
- 10 additional techniques across existing tactics
- gRPC-specific tactic expansion
- WebSocket abuse techniques
- CI/CD pipeline attack techniques
- API gateway misconfiguration techniques

### [2.0.0] — Planned
- New tactic: Persistence (long-term API access maintenance)
- New tactic: Supply Chain (third-party API compromise)
- Interactive web matrix (filterable by protocol, severity, tactic)
- ASTRA scoring API (JSON endpoint for tool integration)
- Community statistics dashboard
