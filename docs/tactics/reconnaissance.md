# Reconnaissance

## Overview

Reconnaissance tactics cover the methods attackers use to discover and map an API's attack surface before attempting exploitation. Unlike traditional web app recon, API reconnaissance is often highly structured — APIs are designed to be machine-readable, and that same property makes them trivially enumerable.

A single successful recon step can hand an attacker a complete blueprint: every endpoint, every parameter, every data type, and every operation the API supports.

## Why API recon is uniquely dangerous

REST APIs leak endpoints via JavaScript bundles, mobile binaries, Swagger/OpenAPI specs, and error messages. GraphQL APIs can expose their *entire schema* in a single request. Even well-secured APIs often expose versioning paths (`/v1/`, `/v2/`), debug endpoints (`/health`, `/status`, `/metrics`), and internal-use routes that were never intended to be public.

## Techniques

| ID | Technique | Severity |
|----|-----------|----------|
| [ASTRA-REC-001](../techniques/reconnaissance/ASTRA-REC-001.md) | API endpoint enumeration via JS scraping | Medium |
| [ASTRA-REC-002](../techniques/reconnaissance/ASTRA-REC-002.md) | OpenAPI / Swagger spec discovery | High |
| [ASTRA-REC-003](../techniques/reconnaissance/ASTRA-REC-003.md) | GraphQL introspection leak | High |

## Common recon targets

- `/swagger.json`, `/openapi.json`, `/api-docs`, `/swagger-ui.html`
- `/graphql` with introspection enabled
- JavaScript bundle files containing `fetch()` or `axios()` calls
- Mobile app binaries (decompiled with `apktool` or `frida`)
- Error messages containing stack traces, framework names, or route lists
- `robots.txt` and sitemap files referencing API paths

## Detection priority

Recon attempts often look like normal browsing. Focus on: requests to known spec paths, introspection query patterns, and unusually high counts of 404 responses from a single IP (indicating path fuzzing).
