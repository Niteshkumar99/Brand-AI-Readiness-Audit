# Brand AI-Readiness Scoring & Severity Rubric

## 1. Severity Deduction Formula

Audits begin with a baseline score of **100 points**. Empirical findings deduct points according to severity:

| Severity Level | Point Deduction | Rationale |
| :--- | :--- | :--- |
| **Critical** | -25 pts | Completely blocks AI crawling or content access (e.g. robots.txt blocking GPTBot, HTTP 500, noindex). |
| **High** | -15 pts | Prevents content parsing or entity identification (e.g. CSR rendering trap, missing all Schema.org, missing mobile viewport). |
| **Medium** | -8 pts | Dilutes LLM retrieval confidence or creates bounce risk (e.g. low text density, entity ambiguity, stale copyright, weak CTAs). |
| **Low** | -3 pts | Minor technical gaps (e.g. missing @id URI, competing H1s, missing footer terms link). |

Final Score = `max(0, 100 - SUM(deductions))`

## 2. Readiness Tiers

- **90 - 100 (AI Leader)**: Fully accessible to AI crawlers, explicit Schema.org graph disambiguation, high quotable proposition density, friction-free referral onboarding.
- **75 - 89 (AI Ready)**: Visible and indexable by AI crawlers; minor opportunities in entity linking or conversational FAQ schemas.
- **50 - 74 (At Risk)**: Significant discoverability friction or high bounce likelihood for AI-referred visitors.
- **0 - 49 (Invisible / Broken)**: Content is invisible to fast-crawlers due to access blocks or client-side rendering traps.
