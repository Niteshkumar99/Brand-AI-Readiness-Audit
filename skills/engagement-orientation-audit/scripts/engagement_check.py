"""
Engagement & Orientation Audit Script
Evaluates mobile viewport, hero clarity, actionable next steps,
and intrusive friction triggers.
"""

import sys
import json
import re
import urllib.request
import urllib.error
import urllib.parse
from html.parser import HTMLParser

SITE_TYPE_CTA_KEYWORDS = {
    "general": ["get started", "try free", "sign up", "pricing", "learn more", "contact sales"],
    "saas": ["start free", "book demo", "try free", "pricing", "dashboard", "get started"],
    "ecommerce": ["shop now", "buy now", "view pricing", "checkout", "add to cart", "browse products"],
    "docs": ["read docs", "api docs", "view docs", "tutorial", "guide", "documentation"],
    "enterprise": ["contact sales", "talk to sales", "demo", "request pricing", "enterprise solutions"]
}


def get_cta_keywords(site_type="general"):
    return SITE_TYPE_CTA_KEYWORDS.get(site_type.lower(), SITE_TYPE_CTA_KEYWORDS["general"])


class EngagementParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.has_viewport = False
        self.h1_texts = []
        self.current_tag = None
        self.cta_buttons = []
        self.modal_triggers = []
        self.text_buffer = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.current_tag = tag

        if tag == "meta" and attr_dict.get("name", "").lower() == "viewport":
            self.has_viewport = True

        if tag in ("a", "button"):
            href = attr_dict.get("href", "").lower()
            btn_class = attr_dict.get("class", "").lower()
            text_ind = f"{href} {btn_class}"
            if any(k in text_ind for k in ("cta", "signup", "register", "trial", "demo", "pricing", "get-started")):
                self.cta_buttons.append(text_ind)

        class_str = attr_dict.get("class", "").lower()
        id_str = attr_dict.get("id", "").lower()
        combined = f"{class_str} {id_str}"
        if any(p in combined for p in ("newsletter-popup", "email-modal", "lead-capture", "interstitial-overlay", "exit-intent")):
            self.modal_triggers.append(combined)

    def handle_endtag(self, tag):
        self.current_tag = None

    def handle_data(self, data):
        cleaned = data.strip()
        if cleaned:
            self.text_buffer.append(cleaned)
            if self.current_tag == "h1":
                self.h1_texts.append(cleaned)

def audit_engagement(url, mock=False, client=None, verify_ssl=True, site_type="general", **kwargs):
    findings = []
    cta_keywords = get_cta_keywords(site_type)

    if mock:
        findings.append({
            "id": "EO-001",
            "title": "Missing mobile viewport configuration",
            "severity": "high",
            "evidence": "Mock audit: <meta name='viewport'> tag missing.",
            "suggested_action": {
                "summary": "Add responsive viewport tag to ensure proper rendering on mobile AI referral traffic.",
                "priority": "high"
            }
        })
        findings.append({
            "id": "EO-003",
            "title": "Weak primary action pathways (CTAs)",
            "severity": "medium",
            "evidence": "Mock audit: 0 primary CTA links found.",
            "suggested_action": {
                "summary": "Include explicit primary action buttons (Try Free, Pricing, Documentation).",
                "priority": "medium"
            }
        })
        return findings

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    raw_html = ""
    if client:
        res = client.fetch(url)
        raw_html = res.get("html", "")
        if res.get("error") and not raw_html:
            findings.append({
                "id": "EO-000",
                "title": "Could not fetch page for engagement audit",
                "severity": "high",
                "evidence": f"Failed to fetch {url}: {res['error']}",
                "suggested_action": {
                    "summary": "Ensure URL is reachable and returns HTTP 200.",
                    "priority": "high"
                }
            })
            return findings
    else:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=12) as response:
                raw_html = response.read().decode("utf-8", errors="replace")
        except Exception as e:
            findings.append({
                "id": "EO-000",
                "title": "Could not fetch page for engagement audit",
                "severity": "high",
                "evidence": f"Failed to fetch {url}: {str(e)}",
                "suggested_action": {
                    "summary": "Ensure URL is reachable and returns HTTP 200.",
                    "priority": "high"
                }
            })
            return findings

    parser = EngagementParser()
    parser.feed(raw_html)

    if not parser.has_viewport:
        findings.append({
            "id": "EO-001",
            "title": "Missing Mobile Viewport Configuration",
            "severity": "high",
            "evidence": "HTML <head> lacks <meta name='viewport' content='width=device-width, initial-scale=1'>. Causes high mobile bounce rate.",
            "suggested_action": {
                "summary": "Add standard responsive viewport meta tag to guarantee mobile readability for AI referral traffic.",
                "priority": "high"
            }
        })

    vague_h1_keywords = ["welcome", "home", "the future", "revolutionize", "empower", "unlock"]
    if parser.h1_texts:
        primary_h1 = " ".join(parser.h1_texts)
        if len(primary_h1) < 8 or any(v == primary_h1.strip().lower() for v in vague_h1_keywords):
            findings.append({
                "id": "EO-002",
                "title": "Vague or Generic Hero Headline (Weak Orientation)",
                "severity": "medium",
                "evidence": f"Hero H1 is '{primary_h1}'. Fails to explicitly communicate what the brand does within the first 5 seconds.",
                "suggested_action": {
                    "summary": "Rewrite Hero H1 to state concrete product category and core user benefit.",
                    "priority": "medium"
                }
            })
    else:
        findings.append({
            "id": "EO-002",
            "title": "Missing Hero Headline for Immediate Orientation",
            "severity": "high",
            "evidence": "No <h1> heading detected in above-the-fold content. Visitors arriving via AI citations lack orientation anchors.",
            "suggested_action": {
                "summary": "Deploy a clear, descriptive <h1> above the fold articulating product identity.",
                "priority": "high"
            }
        })

    cta_text_patterns = re.findall(
        r"\b(?:" + "|".join(re.escape(k) for k in cta_keywords) + r")\b",
        raw_html,
        re.IGNORECASE
    )
    if not parser.cta_buttons and len(cta_text_patterns) == 0:
        findings.append({
            "id": "EO-003",
            "title": "Weak Primary Action Pathways (Missing CTAs)",
            "severity": "medium",
            "evidence": f"No clear primary Call-To-Action (CTA) buttons or links detected for {site_type} site patterns. Creates dead-end experience.",
            "suggested_action": {
                "summary": f"Add site-appropriate primary CTAs for a {site_type} website, such as pricing, docs, demo, checkout, or sales contact links.",
                "priority": "medium"
            }
        })

    if len(parser.modal_triggers) > 0:
        findings.append({
            "id": "EO-004",
            "title": "Intrusive Interstitial / Modal Friction Detected",
            "severity": "medium",
            "evidence": f"Found popup/modal triggers in DOM: {json.dumps(parser.modal_triggers[:2])}. Immediate modals cause immediate bounce for AI-referred visitors.",
            "suggested_action": {
                "summary": "Delay or eliminate modal popups for first-time visitors referred by external AI search engines.",
                "priority": "medium"
            }
        })

    return findings

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    is_mock = "--mock" in sys.argv
    results = audit_engagement(target, mock=is_mock)
    print(json.dumps({"skill": "engagement-orientation-audit", "findings": results}, indent=2))
