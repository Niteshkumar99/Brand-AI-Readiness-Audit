---
name: audit-orchestrator
description: Designated entrypoint skill for the Brand AI-Readiness Audit Marketplace. Audits any website for AI discoverability and on-site engagement readiness by orchestrating specialized domain skills, aggregating empirical findings, and producing a prioritized, actionable audit report.
license: Apache-2.0
allowed-tools:
  - run_command
  - view_file
---

# Brand AI-Readiness Audit Orchestrator (Entrypoint)

## When to use
Use this skill when receiving any request to audit, evaluate, or diagnose a website's readiness for AI search engines, answer engines (ChatGPT, Perplexity, Claude, Gemini), or post-click visitor retention.

## Inputs
- **`target_url`** (string, required): The target domain or URL (e.g. `https://example.com`).
- **`--json-out`** (string, optional): File path to save the resulting JSON report.
- **`--mock`** (boolean, optional): Run in simulated/offline mode for testing and air-gapped evaluation.
- **`--verbose`** (boolean, optional): Output step-by-step diagnostic logging.

## Procedure
1. **Target Normalization & Input Validation**:
   - Normalize target to canonical scheme (`https://`) and validate domain hostname syntax.
2. **Sub-Skill Execution & Domain Coordination**:
   - Execute **`crawl-render-audit`**: Evaluate HTTP response, robots.txt AI bot policies, and CSR rendering traps.
   - Execute **`structured-data-entity-audit`**: Evaluate Schema.org JSON-LD, entity disambiguation, and knowledge graph links.
   - Execute **`content-extractability-audit`**: Evaluate text-to-HTML ratio, heading hierarchy, image alt coverage, and atomic definitional propositions.
   - Execute **`freshness-authority-audit`**: Evaluate dateModified metadata, copyright staleness, and E-E-A-T transparency signals.
   - Execute **`engagement-orientation-audit`**: Evaluate mobile viewport configuration, hero value clarity, actionable next steps, and cognitive friction.
3. **Aggregation, Deduplication & Severity Normalization**:
   - Merge findings from all 5 domain audits.
   - Compute severity distribution: `critical`, `high`, `medium`, `low`.
   - Calculate composite **AI Readiness Score** (0-100) based on weighted penalties.
4. **Proactive Recommendations Synthesis**:
   - Formulate proactive recommendations (e.g., `llms.txt` deployment, conversational FAQ schema, Wikidata entity linking) that strengthen brand discoverability even where no defects exist.
5. **Output Generation & Validation**:
   - Emit a single, strictly formatted JSON report conforming to the required schema.

## Output
Emits the master audit report conforming to the marketplace schema:
```json
{
  "site": "example.com",
  "audited_at": "2026-09-09T14:32:00Z",
  "readiness_score": 74,
  "summary": {
    "total_findings": 5,
    "critical": 1,
    "high": 1,
    "medium": 2,
    "low": 1
  },
  "findings": [
    {
      "id": "CR-001",
      "title": "Robots.txt restricts AI crawler access",
      "severity": "critical",
      "evidence": "Robots.txt blocks GPTBot and PerplexityBot from accessing site root.",
      "suggested_action": {
        "summary": "Update robots.txt to explicitly allow AI search engines.",
        "priority": "critical"
      }
    }
  ],
  "proactive_recommendations": [
    {
      "title": "Publish llms.txt standard index",
      "impact": "high",
      "summary": "Deploy /llms.txt markdown overview for direct LLM agent indexing."
    }
  ]
}
```

## Progressive Disclosure & References
- JSON Schema Specification: [audit_schema.json](./references/audit_schema.json)
- Severity Scoring & Calibration Rubric: [scoring_rubric.md](./references/scoring_rubric.md)
- Executable Master CLI: [run_audit.py](./scripts/run_audit.py)
