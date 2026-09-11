"""
Content Extractability & Machine Readability Audit Script
Evaluates Text-to-HTML density, heading hierarchy, non-text fact trapping (image alts),
semantic HTML structure, and quotable atomic propositions.
"""

import sys
import json
import re
import urllib.request
import urllib.error
import urllib.parse
from html.parser import HTMLParser

class ExtractabilityParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_script = False
        self.in_style = False
        self.in_svg = False
        self.current_tag = None
        self.h1_list = []
        self.h2_list = []
        self.h3_list = []
        self.images = []
        self.semantic_tags = set()
        self.text_tokens = []
        self.current_heading_text = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.current_tag = tag

        if tag in ("script", "style", "svg"):
            if tag == "script": self.in_script = True
            elif tag == "style": self.in_style = True
            elif tag == "svg": self.in_svg = True

        if tag in ("main", "article", "section", "header", "footer", "nav"):
            self.semantic_tags.add(tag)

        if tag == "img":
            alt = attr_dict.get("alt", None)
            src = attr_dict.get("src", "")
            self.images.append({"src": src, "alt": alt})

        if tag in ("h1", "h2", "h3"):
            self.current_heading_text = []

    def handle_endtag(self, tag):
        if tag == "script": self.in_script = False
        elif tag == "style": self.in_style = False
        elif tag == "svg": self.in_svg = False

        if tag in ("h1", "h2", "h3"):
            full_text = " ".join(self.current_heading_text).strip()
            if full_text:
                if tag == "h1": self.h1_list.append(full_text)
                elif tag == "h2": self.h2_list.append(full_text)
                elif tag == "h3": self.h3_list.append(full_text)
            self.current_heading_text = []

        self.current_tag = None

    def handle_data(self, data):
        if not (self.in_script or self.in_style or self.in_svg):
            cleaned = data.strip()
            if cleaned:
                self.text_tokens.append(cleaned)
                if self.current_tag in ("h1", "h2", "h3"):
                    self.current_heading_text.append(cleaned)

    def get_full_text(self):
        return " ".join(self.text_tokens)

def audit_extractability(url, mock=False, client=None, verify_ssl=True, **kwargs):
    findings = []

    if mock:
        findings.append({
            "id": "CE-001",
            "title": "Low Text-to-HTML Density Ratio",
            "severity": "medium",
            "evidence": "Mock audit: Visible text is 5.4% of total HTML markup. Dilutes LLM context extraction.",
            "suggested_action": {
                "summary": "Reduce bloated inline markup and elevate factual text in semantic HTML elements.",
                "priority": "medium"
            }
        })
        findings.append({
            "id": "CE-004",
            "title": "Facts trapped in images lacking alt text",
            "severity": "medium",
            "evidence": "Mock audit: 8 out of 10 images have empty or missing alt attributes.",
            "suggested_action": {
                "summary": "Add comprehensive descriptive alt text to all informational images and infographics.",
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
                "id": "CE-000",
                "title": "Could not fetch page for extractability audit",
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
                "id": "CE-000",
                "title": "Could not fetch page for extractability audit",
                "severity": "high",
                "evidence": f"Failed to fetch {url}: {str(e)}",
                "suggested_action": {
                    "summary": "Ensure URL is reachable and returns HTTP 200.",
                    "priority": "high"
                }
            })
            return findings

    parser = ExtractabilityParser()
    parser.feed(raw_html)

    body_text = parser.get_full_text()
    raw_bytes = len(raw_html.encode("utf-8"))
    text_bytes = len(body_text.encode("utf-8"))
    ratio = (text_bytes / raw_bytes * 100) if raw_bytes > 0 else 0

    if ratio < 10.0:
        findings.append({
            "id": "CE-001",
            "title": "Low Text-to-HTML Density Ratio",
            "severity": "medium",
            "evidence": f"Visible text makes up only {ratio:.1f}% of total HTML bytes (threshold 10%). Heavy markup dilutes LLM chunking efficiency.",
            "suggested_action": {
                "summary": "Prune redundant DOM wrappers, inline SVG/scripts, and ensure substantive factual text dominates the payload.",
                "priority": "medium"
            }
        })

    h1_count = len(parser.h1_list)
    if h1_count == 0:
        findings.append({
            "id": "CE-002",
            "title": "Missing primary <h1> heading",
            "severity": "high",
            "evidence": "Document contains 0 <h1> elements. LLMs rely on H1 to identify the core topical centroid.",
            "suggested_action": {
                "summary": "Define a single, explicit <h1> heading clearly stating what the product/brand is.",
                "priority": "high"
            }
        })
    elif h1_count > 2:
        findings.append({
            "id": "CE-003",
            "title": "Multiple competing <h1> headings",
            "severity": "low",
            "evidence": f"Found {h1_count} distinct <h1> headings: {json.dumps(parser.h1_list[:3])}. Can create ambiguous topical signals in RAG chunking.",
            "suggested_action": {
                "summary": "Consolidate to a single clear <h1> representing page topic, converting secondary headings to <h2>.",
                "priority": "low"
            }
        })

    total_images = len(parser.images)
    missing_alt = [img for img in parser.images if img["alt"] is None or img["alt"].strip() == ""]
    if total_images > 0 and len(missing_alt) > 0:
        pct_missing = (len(missing_alt) / total_images) * 100
        if len(missing_alt) >= 3 or pct_missing > 35:
            findings.append({
                "id": "CE-004",
                "title": "Facts locked in non-text images without descriptive alt text",
                "severity": "medium",
                "evidence": f"Found {len(missing_alt)} of {total_images} images ({pct_missing:.0f}%) lacking descriptive alt attributes.",
                "suggested_action": {
                    "summary": "Add descriptive alt text to all informative images, diagrams, and feature screenshots so text-only AI scrapers can parse them.",
                    "priority": "medium"
                }
            })

    if "main" not in parser.semantic_tags and "article" not in parser.semantic_tags:
        findings.append({
            "id": "CE-005",
            "title": "Missing semantic HTML5 container elements (<main> or <article>)",
            "severity": "low",
            "evidence": f"Page relies on non-semantic <div> elements. Semantic tags found: {list(parser.semantic_tags)}.",
            "suggested_action": {
                "summary": "Wrap primary factual body content in <main> and <article> tags to aid automated content extractors.",
                "priority": "low"
            }
        })

    definitional_patterns = [
        r"\b(?:is|are)\s+(?:an?|the)\s+[a-z0-9\-\s]{4,35}\b",
        r"\bprovides\s+[a-z0-9\-\s]{4,35}\b",
        r"\bdesigned\s+to\s+[a-z0-9\-\s]{4,35}\b",
        r"\bpricing\s+starts\s+at\b",
        r"\bfeatures\s+include\b"
    ]
    matches = sum(1 for pat in definitional_patterns if re.search(pat, body_text, re.IGNORECASE))
    if matches == 0 and len(body_text) > 300:
        findings.append({
            "id": "CE-006",
            "title": "Low Density of Quotable Atomic Propositions",
            "severity": "medium",
            "evidence": "Body text lacks explicit definitional statements ('Brand is an X that provides Y'). Content appears marketing-heavy without clear declarative facts.",
            "suggested_action": {
                "summary": "Introduce concise, declarative 1-sentence capability summaries that conversational models can directly extract and quote.",
                "priority": "medium"
            }
        })

    return findings

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    is_mock = "--mock" in sys.argv
    results = audit_extractability(target, mock=is_mock)
    print(json.dumps({"skill": "content-extractability-audit", "findings": results}, indent=2))
