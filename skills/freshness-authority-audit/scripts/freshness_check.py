"""
Freshness & Authority Audit Script
Scans temporal freshness signals, copyright recency, dateModified metadata,
and organizational transparency (E-E-A-T).
"""

import sys
import json
import re
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from html.parser import HTMLParser

CURRENT_YEAR = datetime.now().year

class FreshnessParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta_dates = {}
        self.links = []
        self.text_chunks = []
        self.in_footer = False
        self.footer_text = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "meta":
            prop = attr_dict.get("property", "") or attr_dict.get("name", "")
            content = attr_dict.get("content", "")
            if any(k in prop.lower() for k in ("date", "modified", "updated", "time", "published")):
                self.meta_dates[prop] = content

        if tag == "a":
            href = attr_dict.get("href", "")
            self.links.append(href.lower())

        if tag == "footer":
            self.in_footer = True

    def handle_endtag(self, tag):
        if tag == "footer":
            self.in_footer = False

    def handle_data(self, data):
        cleaned = data.strip()
        if cleaned:
            self.text_chunks.append(cleaned)
            if self.in_footer:
                self.footer_text.append(cleaned)

def audit_freshness(url, mock=False, client=None, verify_ssl=True, **kwargs):
    findings = []

    if mock:
        findings.append({
            "id": "FA-001",
            "title": "Outdated copyright year detected",
            "severity": "medium",
            "evidence": "Mock audit: Footer indicates '© 2022' without current year.",
            "suggested_action": {
                "summary": "Update copyright notice and ensure regular content review cycles.",
                "priority": "medium"
            }
        })
        findings.append({
            "id": "FA-002",
            "title": "Missing explicit dateModified metadata",
            "severity": "medium",
            "evidence": "Mock audit: No dateModified or article:modified_time meta tag found.",
            "suggested_action": {
                "summary": "Implement dateModified tags in JSON-LD and OpenGraph metadata.",
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
                "id": "FA-000",
                "title": "Could not fetch page for freshness audit",
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
                "id": "FA-000",
                "title": "Could not fetch page for freshness audit",
                "severity": "high",
                "evidence": f"Failed to fetch {url}: {str(e)}",
                "suggested_action": {
                    "summary": "Ensure URL is reachable and returns HTTP 200.",
                    "priority": "high"
                }
            })
            return findings

    parser = FreshnessParser()
    parser.feed(raw_html)
    full_text = " ".join(parser.text_chunks)

    has_date_meta = len(parser.meta_dates) > 0
    has_jsonld_date = bool(re.search(r'"dateModified"\s*:\s*"[^"]+"', raw_html, re.IGNORECASE))

    if not has_date_meta and not has_jsonld_date:
        findings.append({
            "id": "FA-002",
            "title": "Missing explicit dateModified / datePublished metadata",
            "severity": "medium",
            "evidence": "Page does not provide dateModified or article:modified_time tags in meta or JSON-LD. AI crawlers cannot evaluate temporal recency.",
            "suggested_action": {
                "summary": "Embed ISO 8601 dateModified timestamps in OpenGraph meta tags and Schema.org JSON-LD.",
                "priority": "medium"
            }
        })

    copyright_matches = re.findall(r"(?:©|&copy;|copyright)\s*(?:\d{4}\s*[-–—]\s*)?(\d{4})", full_text, re.IGNORECASE)
    if copyright_matches:
        latest_year = max(int(y) for y in copyright_matches if 2000 <= int(y) <= 2035)
        if latest_year < (CURRENT_YEAR - 1):
            findings.append({
                "id": "FA-001",
                "title": f"Stale Copyright Year Detected ({latest_year})",
                "severity": "medium",
                "evidence": f"Discovered copyright notice with year {latest_year} (current year: {CURRENT_YEAR}). Signals an unmaintained site to AI ranking algorithms.",
                "suggested_action": {
                    "summary": f"Update copyright notices to {CURRENT_YEAR} and establish active content maintenance schedules.",
                    "priority": "medium"
                }
            })

    found_about = any("about" in link for link in parser.links)
    found_contact = any("contact" in link for link in parser.links)
    found_privacy = any("privacy" in link for link in parser.links)
    found_terms = any("terms" in link for link in parser.links)

    missing_trust_links = []
    if not found_about: missing_trust_links.append("About")
    if not found_contact: missing_trust_links.append("Contact")
    if not found_privacy: missing_trust_links.append("Privacy Policy")
    if not found_terms: missing_trust_links.append("Terms of Service")

    if len(missing_trust_links) >= 3:
        findings.append({
            "id": "FA-003",
            "title": "Weak Organizational Transparency & E-E-A-T Trust Signals",
            "severity": "low",
            "evidence": f"Could not locate standard organizational identity links: {', '.join(missing_trust_links)}. Weakens entity validation by AI trust filters.",
            "suggested_action": {
                "summary": "Ensure clear footer or navigation links to About, Contact, Privacy, and Terms pages.",
                "priority": "low"
            }
        })

    return findings

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    is_mock = "--mock" in sys.argv
    results = audit_freshness(target, mock=is_mock)
    print(json.dumps({"skill": "freshness-authority-audit", "findings": results}, indent=2))
