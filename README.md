# Brand AI-Readiness Audit Marketplace
> **Adobe University Hackathon 2026 — Round 3 Submission (Advanced Enterprise Edition)**  
> Standard `agentskills.io` Multi-Skill Agent Marketplace for Automated AI Discoverability, On-Site Engagement, and Private/Secured Network Auditing.

---

## 1. Executive Overview

Modern discovery has undergone a paradigm shift: users no longer navigate the web solely through traditional search engines; they rely on **AI assistants** (ChatGPT, Claude, Perplexity, Gemini, Apple Intelligence, and Google AI Overviews) to find, summarize, and recommend brands.

If an AI crawler cannot access a website, cannot parse facts trapped behind Client-Side JavaScript, is blocked by a CDN/WAF firewall, or cannot disambiguate the brand entity in knowledge graphs, the brand is **functionally invisible** in AI answers. Furthermore, when visitors referred by an AI answer land on the website, vague messaging, intrusive popups, or missing context cause them to **bounce immediately**.

The **Brand AI-Readiness Audit Marketplace** encodes the foundational principles of LLM retrieval-augmented generation (RAG), crawler mechanics, edge CDN firewalls, and post-click visitor retention into a modular, production-ready agent skill marketplace.

### Enterprise & Secured Capabilities
- **Universal HTTPS & Modern TLS (1.2/1.3)** with SNI support.
- **Self-Signed & Internal Enterprise CA Support (`--insecure`)** for auditing private intranet sites, staging domains (`staging.brand.internal`), and localhost (`http://localhost:3000`).
- **Active Edge WAF / CDN AI-Bot Firewall Probing (`--probe-bots`)** to detect if Cloudflare, Akamai, or AWS WAF is silently dropping AI crawlers (`GPTBot`, `PerplexityBot`).
- **Authenticated Staging Audits**: Supports HTTP Basic Auth (`--auth user:pass`), Bearer tokens (`--header "Authorization: Bearer <token>"`), Cloudflare Zero Trust service tokens, and preview cookies (`--cookie`).
- **Corporate Proxy Tunneling (`--proxy http://proxy:8080`)**.

---

## 2. Marketplace Architecture & Separation of Concerns

The marketplace is strictly modular, separating concerns into **1 Entrypoint Orchestrator** and **5 Specialized Domain Skills**, unified by `marketplace.json`:

```text
brand-ai-readiness-audit/
├── marketplace.json                      # Master manifest declaring skills & entrypoint
├── README.md                             # Comprehensive enterprise manual
├── .vscode/                              # 1-Click execution profiles for VS Code
│   ├── launch.json                       # Debug configurations for live, mock, staging, & WAF
│   ├── tasks.json                        # Automated tasks (Ctrl+Shift+B)
│   └── settings.json                     # Clean workspace hygiene settings
└── skills/
    ├── audit-orchestrator/               # [ENTRYPOINT] Coordinates sub-skills & emits final report
    │   ├── SKILL.md                      # agentskills.io specification
    │   ├── scripts/
    │   │   ├── run_audit.py              # Master CLI orchestrator with security flags
    │   │   └── security_client.py        # Unified SSL/TLS, auth, proxy, and bot-probing engine
    │   └── references/
    │       ├── audit_schema.json         # Strict JSON Schema for output reports
    │       ├── scoring_rubric.md         # Severity ranking and readiness scoring formula
    │       └── private_secured_audits.md # Enterprise guide for staging/VPN/secured sites
    ├── crawl-render-audit/               # Crawlability, robots.txt AI bots, WAF firewall, CSR gaps
    │   ├── SKILL.md
    │   ├── scripts/
    │   │   ├── crawl_render_check.py     # Upgraded with WAF bot probe, HSTS, mixed content
    │   │   └── security_client.py
    │   └── references/                   # AI crawler registry & SSR/CSR architectural guide
    ├── structured-data-entity-audit/     # Schema.org JSON-LD, entity disambiguation, Wikidata
    │   ├── SKILL.md
    │   ├── scripts/structured_data_check.py
    │   └── references/                   # Schema blueprints & knowledge graph linking
    ├── content-extractability-audit/     # LLM token density, facts locked in non-text, atomic facts
    │   ├── SKILL.md
    │   ├── scripts/extractability_check.py
    │   └── references/                   # Quotable proposition patterns & DOM noise benchmarks
    ├── freshness-authority-audit/        # Temporal signals, multi-source corroboration, E-E-A-T
    │   ├── SKILL.md
    │   ├── scripts/freshness_check.py
    │   └── references/                   # Web consensus vectors & author authority standards
    └── engagement-orientation-audit/     # Above-the-fold value clarity, friction, referral retention
        ├── SKILL.md
        ├── scripts/engagement_check.py
        └── references/                   # AI referral UX & cognitive friction heuristics
```

---

## 3. What the Marketplace Detects (Round-2 Failure Modes)

### A. Off-Site Discoverability (Why AI Assistants Miss or Misrepresent the Brand)
1. **Robots.txt AI Crawling Restrictions (`CR-001`)**: Explicit or implicit blocks against `GPTBot`, `PerplexityBot`, `ClaudeBot`, `Google-Extended`, `Amazonbot`, `Applebot-Extended`.
2. **Active WAF / CDN AI-Bot Firewall Blocks (`CR-009`)**: Cloudflare / Akamai / AWS WAF returning HTTP 403 or CAPTCHAs to AI user-agents while regular browsers are permitted.
3. **Client-Side Rendering (CSR) Trap (`CR-002`)**: Factual content assembled dynamically by client-side JS (`<div id="root">`), invisible to HTTP-only AI retrieval pipelines.
4. **Missing HSTS & Insecure Mixed Content (`CR-010`, `CR-011`)**: Unencrypted HTTP assets on HTTPS pages or lack of transport security reducing citation confidence.
5. **Structured Data & Entity Ambiguity (`SD-001`, `SD-003`)**: Missing Schema.org JSON-LD (`Organization`, `Product`, `FAQPage`) and absence of `@id` / `sameAs` links (Wikidata, Crunchbase, Wikipedia).
6. **Facts Locked in Non-Text (`CE-004`)**: Pricing, feature matrices, and architecture trapped in non-textual images without descriptive `alt` tags.
7. **Absence of Quotable Atomic Propositions (`CE-006`)**: Missing definitive 1-sentence value definitions that LLM summarizers require to quote facts with high confidence.
8. **Stale Temporal Markers (`FA-001`, `FA-002`)**: Outdated copyright years and missing `dateModified` / `datePublished` tags.

### B. On-Site Engagement (Why Visitors Who Arrive Don't Stay)
1. **Hero Value Proposition Fog (`EO-002`)**: First 250 words and `<h1>` failing to state what the product is and who it is for within 5 seconds of arrival.
2. **Cognitive Friction & Interstitials (`EO-004`)**: Aggressive modal popups, cookie walls, or newsletter prompts that block immediate access to promised information.
3. **Missing Information Scent & Action Pathways (`EO-003`)**: Lack of clear CTAs (Docs, Pricing, Demo, Trial) matching the user's search intent.
4. **Mobile & Viewport Misconfigurations (`EO-001`)**: Missing viewport tags causing layout breakage on mobile devices.

---

## 4. Suggested Actions & Proactive Recommendations

The marketplace follows a **recommend-only** paradigm (no live site modifications, no authenticated actions, respects robots.txt).

Every finding includes:
- **`severity`**: `critical`, `high`, `medium`, or `low`.
- **`evidence`**: Concrete empirical evidence from the audit (exact counts, missing tags, HTTP response).
- **`suggested_action`**: Mechanism-sound, prioritized recommendations specifying what to change and why it works.

Beyond fixing detected bugs, the entrypoint synthesizes **Proactive Recommendations**:
- Adding `llms.txt` and `llms-full.txt` files for direct AI-agent indexing.
- Deploying FAQ Schema for conversational search engines.
- Claiming Wikidata and Crunchbase entity entries to anchor the brand in the global Knowledge Graph.
- Configuring edge CDN/WAF exception rules for verified AI search engine IP ranges.

---

## 5. Quick Start & Execution

### Environment
Pure Python 3.8+ using only standard library modules (`urllib`, `html.parser`, `json`, `re`, `datetime`, `ssl`, `base64`). Zero third-party dependencies required.

### 1. Basic Public Website Audit
```bash
python skills/audit-orchestrator/scripts/run_audit.py https://example.com
```

### 2. Automatic Site-Type Detection (Recommended)
```bash
python skills/audit-orchestrator/scripts/run_audit.py https://docs.example.com
python skills/audit-orchestrator/scripts/run_audit.py https://shop.example.com
python skills/audit-orchestrator/scripts/run_audit.py https://app.example.com
```
The tool automatically infers likely site categories such as `general`, `saas`, `ecommerce`, `docs`, and `enterprise` from the hostname. You can also force the mode explicitly with `--site-type auto`.

### 3. Explicit Site-Type Override
```bash
python skills/audit-orchestrator/scripts/run_audit.py https://shop.example.com --site-type ecommerce
python skills/audit-orchestrator/scripts/run_audit.py https://docs.example.com --site-type docs
python skills/audit-orchestrator/scripts/run_audit.py https://sales.example.com --site-type enterprise
python skills/audit-orchestrator/scripts/run_audit.py https://docs.example.com --site-type auto
```

### 4. Auditing Secured / HTTPS Sites with Active WAF Bot Probing
```bash
python skills/audit-orchestrator/scripts/run_audit.py https://yourbrand.com --probe-bots --verbose
```

### 5. Auditing Private Staging / Intranet with Self-Signed SSL
```bash
python skills/audit-orchestrator/scripts/run_audit.py https://staging.internal.brand:8443 --insecure
```

### 6. Auditing Localhost / Development Server
```bash
python skills/audit-orchestrator/scripts/run_audit.py http://localhost:3000
```

### 7. Auditing with HTTP Basic Authentication
```bash
python skills/audit-orchestrator/scripts/run_audit.py https://staging.brand.com --auth "qa_user:Password123"
```

### 8. Auditing with Custom Headers (Bearer Token or Cloudflare Access)
```bash
python skills/audit-orchestrator/scripts/run_audit.py https://secure.brand.com   --header "Authorization: Bearer eyJhbGciOi..."   --header "CF-Access-Client-Id: your-client-id"
```

### 9. Auditing with Session Cookies or Proxy
```bash
python skills/audit-orchestrator/scripts/run_audit.py https://staging.brand.com   --cookie "staging_session=abc123xyz"   --proxy "http://proxy.corp.internal:8080"
```

---

## 6. Audit Report Output Schema

```json
{
  "site": "shop.example.com",
  "site_type": "ecommerce",
  "audited_at": "2026-09-10T04:30:00Z",
  "readiness_score": 72,
  "summary": {
    "total_findings": 4,
    "critical": 1,
    "high": 1,
    "medium": 2,
    "low": 0
  },
  "findings": [
    {
      "id": "CR-009",
      "title": "WAF/CDN Actively Blocks AI Search Engine User-Agents",
      "severity": "critical",
      "evidence": "Active firewall probe revealed edge CDN/WAF blocks AI crawlers: GPTBot (HTTP 403), PerplexityBot (HTTP 403), while standard browser traffic is allowed (HTTP 200).",
      "suggested_action": {
        "summary": "Configure Cloudflare / WAF exception rules to allow legitimate AI search engine user-agents through bot management shields.",
        "priority": "critical"
      }
    }
  ],
  "proactive_recommendations": [
    {
      "title": "Publish an /llms.txt Standard Manifest",
      "impact": "high",
      "summary": "Deploy a clean markdown file at /llms.txt for direct LLM agent ingestion."
    }
  ],
  "security_profile": {
    "protocol": "https",
    "ssl_verified": true,
    "auth_applied": false,
    "custom_headers_count": 0,
    "bot_probe_executed": true
  }
}
```

---

## 7. VS Code Integration (1-Click Run & Debug)

The repository includes a ready-to-use `.vscode/` setup:
- **`F5` (Run & Debug)**: Choose from pre-configured profiles including `Audit: Prompt for URL`, `Audit: Secured / Staging Site (with WAF Bot Probe)`, and `Audit: Localhost / Private Staging (--insecure SSL)`.
- **`Ctrl+Shift+B` (Build Task)**: Instantly runs the master audit on `https://example.com`.
- **Integrated Terminal**: Run any advanced flags seamlessly.
