---
name: freshness-authority-audit
description: Audit temporal freshness markers, dateModified/datePublished metadata, copyright staleness, organizational transparency (About, Contact, Privacy, Terms), and E-E-A-T authority signals needed for AI trust and consensus.
license: Apache-2.0
allowed-tools:
  - run_command
  - view_file
---

# Freshness & Authority AI-Readiness Audit

## When to use
Use this skill when diagnosing why AI assistants treat a website's facts as stale or uncorroborated, or when verifying that content timestamps and organizational trust signals satisfy modern LLM retrieval thresholds.

## Inputs
- **`target_url`** (string, required): The URL or domain to audit.
- **`--mock`** (boolean, optional): Run with simulated payloads for testing.

## Procedure
1. **Temporal Freshness & Timestamp Inspection**:
   - Extract `dateModified`, `datePublished`, `article:modified_time`, and `lastmod` tags from meta and JSON-LD.
   - Flag documents lacking explicit machine-readable last-modified dates.
2. **Copyright & Maintenance Recency Check**:
   - Scan footer and body text for copyright notices (e.g., `© 2020-2024`).
   - Flag sites displaying stale copyright years (> 2 years behind current year) as potential abandoned content signals.
3. **Organizational Transparency & E-E-A-T Footprint**:
   - Inspect internal navigation for essential trust anchors: About Us, Contact, Privacy Policy, Terms of Service.
   - Verify that organizational identity is clearly disclosed.
4. **Findings Generation**:
   - Return structured findings with clear evidence, severity, and remediation steps.

## Output
Emits structured findings conforming to the marketplace audit format:
```json
{
  "findings": [
    {
      "id": "FA-001",
      "title": "Stale Copyright Year Indicates Unmaintained Content",
      "severity": "medium",
      "evidence": "Footer contains 'Copyright 2022 Acme Inc'. Lacks current calendar year verification.",
      "suggested_action": {
        "summary": "Update copyright year dynamically and establish explicit content review cycles.",
        "priority": "medium"
      }
    }
  ]
}
```

## Progressive Disclosure & References
- Multi-Source Consensus & Authority Mechanics: [corroboration_signals.md](./references/corroboration_signals.md)
- Executable Python Checker: [freshness_check.py](./scripts/freshness_check.py)
