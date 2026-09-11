---
name: content-extractability-audit
description: Audit HTML content extractability, token density, facts locked in non-text graphics, heading hierarchy, and atomic quotable proposition density for AI summarizers and RAG retrieval pipelines.
license: Apache-2.0
allowed-tools:
  - run_command
  - view_file
---

# Content Extractability & Machine-Readability AI-Readiness Audit

## When to use
Use this skill when evaluating whether an AI assistant can parse, chunk, and quote facts from a website's pages, or diagnosing why an assistant drops key brand capabilities from summaries.

## Inputs
- **`target_url`** (string, required): The URL or domain to audit.
- **`--mock`** (boolean, optional): Run with simulated payloads for testing.

## Procedure
1. **Text-to-HTML Density Ratio Calculation**:
   - Strip scripts, styles, SVG paths, and comments.
   - Measure pure visible character count against total raw HTML byte size. Flag pages with text density < 10% as high-boilerplate noise.
2. **Heading Hierarchy & Chunking Boundaries**:
   - Extract all `<h1>`, `<h2>`, and `<h3>` tags.
   - Verify that exactly one primary `<h1>` defines the topical centroid.
   - Check for logical heading hierarchy to guarantee clean RAG chunking boundaries.
3. **Non-Text Fact Trapping (Image Alt Text Analysis)**:
   - Extract all `<img>` tags and inspect `alt` attribute completeness.
   - Flag images missing `alt` attributes, particularly infographics, comparison tables, or feature diagrams that lock facts away from text-based LLMs.
4. **Semantic DOM Structural Verification**:
   - Check for HTML5 structural elements (`<main>`, `<article>`, `<section>`).
   - Flag pages that rely entirely on non-semantic generic `<div>` soup.
5. **Atomic Quotable Proposition Density**:
   - Scan body text for high-information-density definitional sentences (e.g., "[Brand] is an X that provides Y").
   - Flag content that relies heavily on vague buzzwords without explicit, quotable factual claims.

## Output
Emits structured findings complying with the marketplace audit format:
```json
{
  "findings": [
    {
      "id": "CE-001",
      "title": "Low Text-to-HTML Density Ratio",
      "severity": "medium",
      "evidence": "Visible text makes up only 6.2% of raw HTML bytes (threshold 10%). Heavy DOM markup dilutes LLM context windows.",
      "suggested_action": {
        "summary": "Prune bloated inline styles/scripts and elevate core factual copy into semantic HTML tags.",
        "priority": "medium"
      }
    }
  ]
}
```

## Progressive Disclosure & References
- Quotable Proposition Guidelines: [citation_anchors.md](./references/citation_anchors.md)
- DOM Noise & Token Economics: [text_density_standards.md](./references/text_density_standards.md)
- Executable Python Checker: [extractability_check.py](./scripts/extractability_check.py)
