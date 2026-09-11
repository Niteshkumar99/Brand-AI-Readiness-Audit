---
name: crawl-render-audit
description: Audit a website's crawler access permissions, HTTP redirect chains, headers, robots.txt AI-bot policies, and Client-Side Rendering (CSR) traps that prevent AI assistants from indexing facts. Use when evaluating why AI crawlers fail to fetch or parse a site.
license: Apache-2.0
allowed-tools:
  - run_command
  - view_file
---

# Crawl & Render AI-Readiness Audit

## When to use
Use this skill when diagnosing why a website is invisible to AI crawlers, blocked by robots.txt, timing out due to redirect chains, or returning an empty JavaScript shell that AI scrapers cannot execute.

## Inputs
- **`target_url`** (string, required): The root URL or specific page URL to audit (e.g. `https://example.com`).
- **`--mock`** (boolean, optional): Run with simulated network responses for testing and offline evaluation.

## Procedure
1. **Network Connectivity & Latency Check**:
   - Issue an HTTP GET request with standard headers and standard AI crawler user agents.
   - Measure Time to First Byte (TTFB) and count redirect hops. Flag any chain exceeding 2 hops.
2. **Robots.txt AI Crawling Analysis**:
   - Fetch `/robots.txt` and parse directive blocks for modern AI bots: `GPTBot`, `PerplexityBot`, `ClaudeBot`, `Google-Extended`, `Amazonbot`, `Applebot-Extended`, `Bytespider`, `CCBot`, `Meta-ExternalAgent`.
   - Identify explicit `Disallow: /` directives and wildcard disallows affecting AI indexing.
3. **HTTP Header & Meta-Robots Verification**:
   - Inspect response headers for `X-Robots-Tag: noindex`, `noai`, or `unavailable_after`.
   - Verify presence of self-referential `<link rel="canonical">`.
4. **Client-Side Rendering (CSR) Trap Detection**:
   - Parse the raw HTML DOM.
   - Detect single container shells (e.g., `<div id="root"></div>`, `<div id="app"></div>`) where inner text is under 150 characters despite script payloads.
   - Identify `<noscript>` tags warning that JavaScript is mandatory.
5. **Findings Generation**:
   - Structure all detected issues with ID, Title, Severity (`critical`, `high`, `medium`, `low`), Evidence, and Suggested Action.

## Output
Emits an array of finding objects compliant with the audit schema:
```json
{
  "findings": [
    {
      "id": "CR-001",
      "title": "Robots.txt blocks AI search engine crawlers",
      "severity": "critical",
      "evidence": "Robots.txt Disallows GPTBot and PerplexityBot from accessing site root.",
      "suggested_action": {
        "summary": "Update robots.txt to explicitly allow AI crawlers needed for brand visibility.",
        "priority": "critical"
      }
    }
  ]
}
```

## Progressive Disclosure & References
- Comprehensive AI Crawler Registry: [ai_bot_user_agents.md](./references/ai_bot_user_agents.md)
- SSR/SSG vs CSR Architectural Fixes: [js_rendering_fallbacks.md](./references/js_rendering_fallbacks.md)
- Executable Python Checker: [crawl_render_check.py](./scripts/crawl_render_check.py)
