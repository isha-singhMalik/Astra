# Real-World Breach Mappings

Every technique in ASTRA is mapped to at least one publicly disclosed breach. This page collects all mappings in one place.

The goal: connect abstract attack techniques to real incidents so that the risk is concrete, not theoretical.

---

| Breach | Year | Organisation | Records / Impact | ASTRA Technique | Reference |
|--------|------|--------------|-----------------|-----------------|-----------|
| Twitter / X API | 2022 | Twitter / X Corp | 5.4M user records | [ASTRA-AUTHZ-001](techniques/authorization-failure/ASTRA-AUTHZ-001.md) | [BleepingComputer](https://www.bleepingcomputer.com/news/security/twitter-confirms-zero-day-used-to-expose-data-of-54-million-accounts/) |
| Optus Australia | 2022 | Optus (Singtel) | 10M customer records | [ASTRA-EXFIL-001](techniques/exfiltration/ASTRA-EXFIL-001.md) | [ITNews](https://www.itnews.com.au/news/optus-breach-an-api-with-no-authentication-591019) |
| Peloton | 2021 | Peloton Interactive | All user profiles publicly accessible | [ASTRA-AUTHZ-001](techniques/authorization-failure/ASTRA-AUTHZ-001.md) | [Tenable](https://www.tenable.com/blog/peloton-api-security-flaw) |
| Peloton API spec | 2021 | Peloton Interactive | Full API schema exposed | [ASTRA-REC-002](techniques/reconnaissance/ASTRA-REC-002.md) | [Tenable](https://www.tenable.com/blog/peloton-api-security-flaw) |
| T-Mobile | 2021 | T-Mobile | 50M+ records | [ASTRA-REC-001](techniques/reconnaissance/ASTRA-REC-001.md) | [WSJ](https://www.wsj.com/articles/t-mobile-investigating-possible-data-breach-11629208791) |
| Coinbase | 2021 | Coinbase | Trading manipulation | [ASTRA-AUTHZ-002](techniques/authorization-failure/ASTRA-AUTHZ-002.md) | [HackerOne #1369820](https://hackerone.com/reports/1369820) |
| Auth0 / jsonwebtoken | 2015 | Auth0 + downstream apps | Authentication bypass — all users | [ASTRA-AUTH-001](techniques/authentication-abuse/ASTRA-AUTH-001.md) | [Auth0 Blog](https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/) |
| HackerOne GraphQL | 2020 | HackerOne | Internal schema exposed | [ASTRA-REC-003](techniques/reconnaissance/ASTRA-REC-003.md) | [HackerOne #291531](https://hackerone.com/reports/291531) |

---

## Know a breach we should add?

[Open a breach mapping issue](https://github.com/isha-singhMalik/Astra/issues/new?template=new-breach-mapping.md)

We accept mappings to any publicly disclosed breach where the root cause is confirmed and maps to an ASTRA technique.
