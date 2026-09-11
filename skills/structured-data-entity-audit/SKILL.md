---
name: structured-data-entity-audit
description: Audit Schema.org JSON-LD and Microdata structured data for syntax validity, required properties, entity disambiguation via @id and sameAs links, and critical types (Organization, Product, FAQPage) needed for AI knowledge graph grounding.
license: Apache-2.0
allowed-tools:
  - run_command
  - view_file
---

# Structured Data & Entity Disambiguation AI-Readiness Audit

## When to use
Use this skill when auditing whether a website provides explicit, machine-readable structured data to AI search engines, or diagnosing why an AI assistant confuses a brand with homonyms or fails to display rich product and FAQ summaries.

## Inputs
- **`target_url`** (string, required): The URL or domain to audit.
- **`--mock`** (boolean, optional): Run with simulated payloads for testing.

## Procedure
1. **JSON-LD Script Tag Extraction**:
   - Locate and extract all `<script type="application/ld+json">` elements in the HTML document.
   - Validate strict JSON syntax; flag parsing errors or unescaped characters.
2. **Schema Type Hierarchy Inspection**:
   - Flatten top-level objects and nested `@graph` arrays.
   - Detect presence of core entity types: `Organization`, `Brand`, `Product`, `SoftwareApplication`, `WebSite`, `Article`, `FAQPage`.
3. **Entity Disambiguation & Knowledge Graph Linking Analysis**:
   - Check if `Organization` / `Brand` schemas specify an unambiguous `@id` URI.
   - Inspect `sameAs` array for authoritative external entity references (Wikidata, Crunchbase, Wikipedia, official LinkedIn, GitHub, X profiles).
4. **Conversational Answer Readiness (FAQPage & Offer)**:
   - Check for `FAQPage` structured data with question/answer pairs, which LLM retrieval models prioritize for direct answer generation.
   - For commerce/SaaS sites, verify `Offer`, `priceCurrency`, and `availability` completeness.
5. **Findings Formulation**:
   - Map defects to findings schema with clear evidence, severity, and copy-paste JSON-LD remediation blueprints.

## Output
Emits structured findings complying with the marketplace audit format:
```json
{
  "findings": [
    {
      "id": "SD-001",
      "title": "Missing Schema.org JSON-LD structured data",
      "severity": "high",
      "evidence": "Crawled page contains 0 application/ld+json script tags.",
      "suggested_action": {
        "summary": "Implement Organization and WebSite JSON-LD markup on all primary pages.",
        "priority": "high"
      }
    }
  ]
}
```

## Progressive Disclosure & References
- Ready-to-use JSON-LD Templates: [schema_blueprints.md](./references/schema_blueprints.md)
- Knowledge Graph Disambiguation Guide: [entity_disambiguation.md](./references/entity_disambiguation.md)
- Executable Python Checker: [structured_data_check.py](./scripts/structured_data_check.py)
