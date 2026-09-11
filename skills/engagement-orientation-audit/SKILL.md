---
name: engagement-orientation-audit
description: Audit on-site visitor engagement, above-the-fold value proposition clarity, mobile viewport configuration, actionable next steps, and cognitive friction/interstitials that cause AI-referred visitors to bounce.
license: Apache-2.0
allowed-tools:
  - run_command
  - view_file
---

# Engagement & Orientation AI-Readiness Audit

## When to use
Use this skill when auditing why visitors referred by AI assistants bounce immediately upon arrival, diagnosing unclear above-the-fold messaging, or detecting aggressive popups and navigation friction.

## Inputs
- **`target_url`** (string, required): The URL or domain to audit.
- **`--mock`** (boolean, optional): Run with simulated payloads for testing.

## Procedure
1. **Mobile Viewport & Responsiveness Check**:
   - Inspect `<head>` for `<meta name="viewport" content="width=device-width, initial-scale=1">`.
   - Flag missing viewport configurations that trigger broken mobile rendering.
2. **Above-the-Fold Hero Value Proposition Clarity**:
   - Extract the primary `<h1>` and introductory text.
   - Evaluate whether the value proposition answers what the product/brand does within 5 seconds.
   - Flag generic placeholders (e.g. "Welcome to our website", "The Future is Now") that lack contextual grounding.
3. **Information Scent & Action Pathway Verification**:
   - Scan for actionable primary call-to-action (CTA) links ("Get Started", "Try Free", "View Docs", "Pricing", "Live Demo").
   - Flag landing pages that present dead ends with no obvious conversion or exploration pathway.
4. **Cognitive Friction & Interstitial Blocker Detection**:
   - Scan for aggressive modal, overlay, newsletter popup, or scroll-locking script patterns.
   - Flag barriers that obstruct the immediate viewing of content promised in the AI citation.
5. **Findings Formulation**:
   - Format actionable findings with severity and concrete remediation advice.

## Output
Emits structured findings conforming to the marketplace audit format:
```json
{
  "findings": [
    {
      "id": "EO-001",
      "title": "Missing Mobile Viewport Meta Tag",
      "severity": "high",
      "evidence": "Document does not declare meta name='viewport'. Causes mobile layout zoom failure.",
      "suggested_action": {
        "summary": "Add <meta name='viewport' content='width=device-width, initial-scale=1.0'> to <head>.",
        "priority": "high"
      }
    }
  ]
}
```

## Progressive Disclosure & References
- AI-Referral Visitor Retention Heuristics: [bounce_heuristics.md](./references/bounce_heuristics.md)
- Executable Python Checker: [engagement_check.py](./scripts/engagement_check.py)
