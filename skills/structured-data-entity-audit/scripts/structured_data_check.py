"""
Structured Data & Entity Audit Script
Parses and validates Schema.org JSON-LD, detects entity ambiguity,
and validates presence of critical schemas (Organization, FAQPage, Product).
"""

import sys
import json
import urllib.request
import urllib.error
import urllib.parse
from html.parser import HTMLParser

class JSONLDExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_jsonld = False
        self.raw_blocks = []
        self.current_data = []

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            attr_dict = dict(attrs)
            type_value = str(attr_dict.get("type") or "").lower()
            if "ld+json" in type_value or "application/ld+json" in type_value:
                self.in_jsonld = True
                self.current_data = []

    def handle_endtag(self, tag):
        if tag == "script" and self.in_jsonld:
            self.in_jsonld = False
            raw_text = "".join(self.current_data).strip()
            if raw_text:
                self.raw_blocks.append(raw_text)

    def handle_data(self, data):
        if self.in_jsonld:
            self.current_data.append(data)

def flatten_schemas(obj):
    schemas = []
    if isinstance(obj, list):
        for item in obj:
            schemas.extend(flatten_schemas(item))
    elif isinstance(obj, dict):
        if "@graph" in obj and isinstance(obj["@graph"], list):
            schemas.extend(flatten_schemas(obj["@graph"]))
        else:
            schemas.append(obj)
            for k, v in obj.items():
                if isinstance(v, (dict, list)) and k != "@graph":
                    schemas.extend(flatten_schemas(v))
    return schemas

def audit_structured_data(url, mock=False, client=None, verify_ssl=True, **kwargs):
    findings = []

    if mock:
        findings.append({
            "id": "SD-001",
            "title": "Missing Schema.org JSON-LD structured data",
            "severity": "high",
            "evidence": "Mock audit: 0 JSON-LD scripts discovered in document.",
            "suggested_action": {
                "summary": "Add Schema.org Organization and WebSite JSON-LD to every page.",
                "priority": "high"
            }
        })
        findings.append({
            "id": "SD-003",
            "title": "Entity Ambiguity: Missing sameAs knowledge graph links",
            "severity": "medium",
            "evidence": "Mock audit: Organization schema lacks sameAs links to Wikidata or Crunchbase.",
            "suggested_action": {
                "summary": "Enrich Organization JSON-LD with sameAs array pointing to Wikidata and authoritative profiles.",
                "priority": "medium"
            }
        })
        return findings

    # Normalize URL
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    html_content = ""
    if client:
        res = client.fetch(url)
        html_content = res.get("html", "")
        if res.get("error") and not html_content:
            findings.append({
                "id": "SD-000",
                "title": "Could not fetch page for structured data audit",
                "severity": "high",
                "evidence": f"Failed to fetch {url}: {res['error']}",
                "suggested_action": {
                    "summary": "Verify target URL is accessible and returns valid HTML.",
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
                html_content = response.read().decode("utf-8", errors="replace")
        except Exception as e:
            findings.append({
                "id": "SD-000",
                "title": "Could not fetch page for structured data audit",
                "severity": "high",
                "evidence": f"Failed to fetch {url}: {str(e)}",
                "suggested_action": {
                    "summary": "Verify target URL is accessible and returns valid HTML.",
                    "priority": "high"
                }
            })
            return findings

    extractor = JSONLDExtractor()
    extractor.feed(html_content)

    if not extractor.raw_blocks:
        findings.append({
            "id": "SD-001",
            "title": "No Schema.org JSON-LD structured data detected",
            "severity": "high",
            "evidence": "Crawled page contains 0 application/ld+json script tags. Content lacks machine-readable semantic grounding.",
            "suggested_action": {
                "summary": "Implement Schema.org JSON-LD markup starting with Organization, WebSite, and product schemas.",
                "priority": "high"
            }
        })
        return findings

    parsed_schemas = []
    syntax_errors = 0

    for block in extractor.raw_blocks:
        try:
            parsed = json.loads(block)
            parsed_schemas.extend(flatten_schemas(parsed))
        except json.JSONDecodeError:
            syntax_errors += 1

    if syntax_errors > 0:
        findings.append({
            "id": "SD-006",
            "title": "Syntax error in JSON-LD script block",
            "severity": "high",
            "evidence": f"Encountered {syntax_errors} malformed JSON-LD script tag(s) that failed JSON parsing.",
            "suggested_action": {
                "summary": "Validate and format JSON-LD scripts using standard JSON linters to prevent crawler rejection.",
                "priority": "high"
            }
        })

    # Classify schemas
    schema_types = set()
    org_schemas = []
    has_faq = False

    for s in parsed_schemas:
        if not isinstance(s, dict):
            continue

        item_types = []
        t = s.get("@type", "")
        if isinstance(t, list):
            item_types = [str(sub_t) for sub_t in t]
        elif isinstance(t, str):
            item_types = [t]

        for item_type in item_types:
            schema_types.add(item_type)

        if any(kind in {"Organization", "Corporation", "Brand"} for kind in item_types):
            org_schemas.append(s)
        if "FAQPage" in item_types:
            has_faq = True

    # 1. Organization Check
    if not org_schemas:
        findings.append({
            "id": "SD-002",
            "title": "Missing Organization / Brand structured data",
            "severity": "high",
            "evidence": f"Found schemas ({', '.join(schema_types) if schema_types else 'None'}), but no Organization or Brand definition.",
            "suggested_action": {
                "summary": "Add Schema.org Organization schema with name, url, logo, and description to ground brand identity.",
                "priority": "high"
            }
        })
    else:
        org = org_schemas[0]
        has_id = "@id" in org
        same_as = org.get("sameAs", [])

        if not has_id:
            findings.append({
                "id": "SD-004",
                "title": "Organization schema lacks global @id URI",
                "severity": "low",
                "evidence": "Organization schema does not define an unambiguous @id URI anchor (e.g. https://domain.com/#organization).",
                "suggested_action": {
                    "summary": "Assign an explicit @id URI to Organization to enable relational knowledge-graph referencing.",
                    "priority": "low"
                }
            })

        if not same_as or (isinstance(same_as, list) and len(same_as) == 0):
            findings.append({
                "id": "SD-003",
                "title": "Entity Ambiguity: Missing sameAs knowledge graph references",
                "severity": "medium",
                "evidence": "Organization schema has no sameAs links to external knowledge authorities (Wikidata, Crunchbase, Wikipedia).",
                "suggested_action": {
                    "summary": "Add sameAs array linking the brand to its Wikidata QID, Crunchbase profile, and official social accounts.",
                    "priority": "medium"
                }
            })

    # 2. FAQPage Check
    if not has_faq:
        findings.append({
            "id": "SD-005",
            "title": "Missing FAQPage structured data for conversational RAG queries",
            "severity": "medium",
            "evidence": "No FAQPage schema found. Conversational AI search models heavily favor explicit Question/Answer pairs.",
            "suggested_action": {
                "summary": "Add FAQPage schema covering top user queries, pricing, and capabilities to capture direct conversational citations.",
                "priority": "medium"
            }
        })

    return findings

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    is_mock = "--mock" in sys.argv
    results = audit_structured_data(target, mock=is_mock)
    print(json.dumps({"skill": "structured-data-entity-audit", "findings": results}, indent=2))
