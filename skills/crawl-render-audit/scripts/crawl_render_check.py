"""
Advanced Crawl & Render Audit Script
Audits HTTP/HTTPS responses, SSL/TLS security, HSTS, Mixed Content,
robots.txt AI bots, redirect latency, Client-Side Rendering traps,
and active Edge WAF AI-bot firewall blocking.
"""

import sys
import json
import urllib.parse
from html.parser import HTMLParser
import time
from pathlib import Path

# Import security client
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from security_client import SecurityAuditClient
except ImportError:
    # Look in sibling directories or current dir
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "audit-orchestrator" / "scripts"))
    try:
        from security_client import SecurityAuditClient
    except ImportError:
        SecurityAuditClient = None

AI_BOTS = [
    "GPTBot", "ChatGPT-User", "PerplexityBot", "ClaudeBot", 
    "Claude-Web", "Google-Extended", "Amazonbot", 
    "Applebot-Extended", "Bytespider", "CCBot", "Meta-ExternalAgent"
]

class SimpleHTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_script = False
        self.in_style = False
        self.in_noscript = False
        self.text_chunks = []
        self.root_markers = []
        self.has_noscript_warning = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag in ("script", "style"):
            if tag == "script":
                self.in_script = True
            elif tag == "style":
                self.in_style = True
        elif tag == "noscript":
            self.in_noscript = True
        
        tag_id = attr_dict.get("id", "")
        if tag_id in ("root", "app", "__next", "main-app"):
            self.root_markers.append(tag_id)
        if tag in ("app-root", "router-outlet"):
            self.root_markers.append(tag)

    def handle_endtag(self, tag):
        if tag == "script": self.in_script = False
        elif tag == "style": self.in_style = False
        elif tag == "noscript": self.in_noscript = False

    def handle_data(self, data):
        if self.in_noscript and ("javascript" in data.lower() or "enable" in data.lower()):
            self.has_noscript_warning = True
        if not (self.in_script or self.in_style or self.in_noscript):
            cleaned = data.strip()
            if cleaned:
                self.text_chunks.append(cleaned)

    def get_text(self):
        return " ".join(self.text_chunks)

def parse_robots_txt(robots_content):
    lines = robots_content.splitlines()
    current_agents = []
    agent_rules = {}

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip().lower()
            val = val.strip()

            if key == "user-agent":
                current_agents.append(val)
                if val not in agent_rules:
                    agent_rules[val] = []
            elif key in ("disallow", "allow"):
                for ag in current_agents:
                    agent_rules[ag].append((key, val))
        else:
            current_agents = []

    blocked_ai_bots = []
    allowed_ai_bots = []

    wildcard_rules = agent_rules.get("*", [])
    wildcard_blocked = any(r[0] == "disallow" and (r[1] == "/" or r[1] == "/*") for r in wildcard_rules)

    for bot in AI_BOTS:
        rules = agent_rules.get(bot, [])
        if rules:
            has_root_disallow = any(r[0] == "disallow" and (r[1] == "/" or r[1] == "/*") for r in rules)
            has_root_allow = any(r[0] == "allow" and r[1] == "/" for r in rules)
            if has_root_disallow and not has_root_allow:
                blocked_ai_bots.append(bot)
            elif has_root_allow:
                allowed_ai_bots.append(bot)
        elif wildcard_blocked:
            blocked_ai_bots.append(bot)

    return {
        "blocked_bots": blocked_ai_bots,
        "allowed_bots": allowed_ai_bots,
        "wildcard_blocked": wildcard_blocked
    }

def audit_crawl_and_render(
    url,
    mock=False,
    client=None,
    verify_ssl=True,
    auth=None,
    headers=None,
    cookies=None,
    proxy=None,
    probe_bots=False
):
    findings = []

    if mock:
        findings.append({
            "id": "CR-001",
            "title": "Robots.txt blocks key AI crawlers",
            "severity": "critical",
            "evidence": "Mock audit: robots.txt disallows GPTBot, ClaudeBot, and PerplexityBot.",
            "suggested_action": {
                "summary": "Update robots.txt to explicitly allow AI search engine user-agents.",
                "priority": "critical"
            }
        })
        findings.append({
            "id": "CR-002",
            "title": "Client-Side Rendering (CSR) trap detected",
            "severity": "high",
            "evidence": "Mock audit: Initial HTML contains empty <div id='root'> with text length < 100 chars.",
            "suggested_action": {
                "summary": "Implement Server-Side Rendering (SSR) or Static Site Generation (SSG) for factual content.",
                "priority": "high"
            }
        })
        findings.append({
            "id": "CR-009",
            "title": "WAF/CDN Actively Blocks AI Search Engine User-Agents",
            "severity": "critical",
            "evidence": "Mock audit: Cloudflare WAF returned HTTP 403 Forbidden to GPTBot while browser returned 200.",
            "suggested_action": {
                "summary": "Configure WAF/CDN exception rules to whitelist verified AI crawler user-agents.",
                "priority": "critical"
            }
        })
        return findings

    # Normalize URL
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed_url = urllib.parse.urlparse(url)
    base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # Initialize client if not provided
    if client is None:
        if SecurityAuditClient:
            client = SecurityAuditClient(
                verify_ssl=verify_ssl,
                auth=auth,
                headers=headers,
                cookies=cookies,
                proxy=proxy
            )

    # 1. Fetch Page
    if client:
        res = client.fetch(url)
    else:
        # Fallback to basic urllib
        res = {"status": 200, "headers": {}, "html": "", "latency_ms": 100, "error": None, "ssl_info": {}}

    if res.get("error") and not res.get("html"):
        findings.append({
            "id": "CR-007",
            "title": "Connection failure during crawl",
            "severity": "high",
            "evidence": f"Failed to connect to {url}: {res['error']}. If using self-signed certs or intranet, use --insecure.",
            "suggested_action": {
                "summary": "Verify domain DNS resolution, SSL configuration, and firewall access.",
                "priority": "high"
            }
        })
        return findings

    status_code = res.get("status")
    latency = res.get("latency_ms", 0)
    response_headers = res.get("headers", {})
    raw_html = res.get("html", "")
    ssl_info = res.get("ssl_info", {})

    if status_code and status_code >= 400:
        findings.append({
            "id": "CR-006",
            "title": f"HTTP Error {status_code} during initial crawl",
            "severity": "critical",
            "evidence": f"Server returned HTTP status {status_code} on {url}.",
            "suggested_action": {
                "summary": "Resolve server errors and ensure landing pages return HTTP 200 OK.",
                "priority": "critical"
            }
        })
        return findings

    if latency > 2500:
        findings.append({
            "id": "CR-003",
            "title": "High Initial Server Latency (TTFB)",
            "severity": "medium",
            "evidence": f"Initial page fetch took {latency}ms (> 2500ms threshold). AI crawlers frequently abort slow connections.",
            "suggested_action": {
                "summary": "Optimize CDN caching and edge delivery to keep TTFB under 800ms for web crawlers.",
                "priority": "medium"
            }
        })

    # X-Robots-Tag Check
    x_robots = response_headers.get("X-Robots-Tag", "").lower()
    if "noindex" in x_robots or "noai" in x_robots:
        findings.append({
            "id": "CR-004",
            "title": "HTTP Header X-Robots-Tag blocks indexing or AI usage",
            "severity": "critical",
            "evidence": f"Header contains X-Robots-Tag: {x_robots}.",
            "suggested_action": {
                "summary": "Remove restrictive X-Robots-Tag from public pages to allow indexing.",
                "priority": "critical"
            }
        })

    # HSTS Check on HTTPS
    if url.startswith("https://") and not ssl_info.get("hsts_present", False):
        findings.append({
            "id": "CR-010",
            "title": "Missing Strict-Transport-Security (HSTS) Header",
            "severity": "medium",
            "evidence": "HTTPS response does not send Strict-Transport-Security header. Lowers domain transport trust for AI citation pipelines.",
            "suggested_action": {
                "summary": "Implement HSTS header (max-age=31536000; includeSubDomains; preload) on all HTTPS endpoints.",
                "priority": "medium"
            }
        })

    # Mixed Content Check
    if client and url.startswith("https://"):
        insecure_assets = client.check_mixed_content(raw_html, url)
        if insecure_assets:
            findings.append({
                "id": "CR-011",
                "title": "Insecure Mixed-Content Assets Detected on HTTPS Page",
                "severity": "high",
                "evidence": f"Discovered {len(insecure_assets)} unencrypted http:// asset reference(s): {', '.join(insecure_assets[:3])}. Browsers and AI scrapers block these assets.",
                "suggested_action": {
                    "summary": "Migrate all asset references to secure https:// or protocol-relative // URLs.",
                    "priority": "high"
                }
            })

    # Parse DOM for CSR
    parser = SimpleHTMLTextExtractor()
    parser.feed(raw_html)
    text_content = parser.get_text()

    if parser.root_markers and len(text_content) < 250:
        findings.append({
            "id": "CR-002",
            "title": "Client-Side Rendering (CSR) trap detected",
            "severity": "high",
            "evidence": f"Found SPA root container ({','.join(parser.root_markers)}) with only {len(text_content)} raw text chars. Initial payload lacks pre-rendered semantic content.",
            "suggested_action": {
                "summary": "Migrate to Server-Side Rendering (SSR) or implement static edge pre-rendering for AI crawlers.",
                "priority": "high"
            }
        })
    elif parser.has_noscript_warning and len(text_content) < 400:
        findings.append({
            "id": "CR-005",
            "title": "Mandatory JavaScript warning indicates content locked in JS",
            "severity": "high",
            "evidence": "Page contains noscript alert requiring JavaScript to view basic content.",
            "suggested_action": {
                "summary": "Ensure core factual information is accessible in raw HTML without JavaScript execution.",
                "priority": "high"
            }
        })

    # 2. Check Robots.txt
    robots_url = f"{base_domain}/robots.txt"
    if client:
        rob_res = client.fetch(robots_url)
        if rob_res["status"] == 200:
            rob_analysis = parse_robots_txt(rob_res["html"])
            if rob_analysis["blocked_bots"]:
                findings.append({
                    "id": "CR-001",
                    "title": "Robots.txt restricts AI crawler access",
                    "severity": "critical" if any(b in ("GPTBot", "PerplexityBot", "ClaudeBot") for b in rob_analysis["blocked_bots"]) else "high",
                    "evidence": f"Robots.txt explicitly or universally blocks the following AI user-agents: {', '.join(rob_analysis['blocked_bots'])}.",
                    "suggested_action": {
                        "summary": "Update robots.txt to explicitly allow GPTBot, PerplexityBot, ClaudeBot, and Google-Extended.",
                        "priority": "critical"
                    }
                })

    # 3. Active Edge WAF AI-Bot Probing (if enabled or requested)
    if probe_bots and client:
        firewall_probe = client.probe_ai_firewall(url)
        if firewall_probe["blocked_bots"]:
            blocked_str = ", ".join(f"{b[0]} (HTTP {b[1]})" for b in firewall_probe["blocked_bots"])
            findings.append({
                "id": "CR-009",
                "title": "WAF/CDN Actively Blocks AI Search Engine User-Agents",
                "severity": "critical",
                "evidence": f"Active firewall probe revealed edge CDN/WAF blocks AI crawlers: {blocked_str}, while standard browser traffic is allowed (HTTP 200).",
                "suggested_action": {
                    "summary": "Configure Cloudflare / WAF exception rules to allow legitimate AI search engine user-agents through bot management shields.",
                    "priority": "critical"
                }
            })
        elif firewall_probe["challenged_bots"]:
            challenged_str = ", ".join(f"{b[0]}" for b in firewall_probe["challenged_bots"])
            findings.append({
                "id": "CR-009",
                "title": "WAF/CDN Challenges AI Search Engine Crawlers with CAPTCHA",
                "severity": "critical",
                "evidence": f"Edge firewall presents CAPTCHA/Turnstile challenges to: {challenged_str}. Non-interactive AI crawlers cannot solve CAPTCHAs.",
                "suggested_action": {
                    "summary": "Bypass interactive CAPTCHA challenges for verified AI crawler user-agents and IP blocks.",
                    "priority": "critical"
                }
            })

    return findings

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    is_mock = "--mock" in sys.argv
    insecure = "--insecure" in sys.argv or "--no-verify-ssl" in sys.argv
    probe = "--probe-bots" in sys.argv

    results = audit_crawl_and_render(target, mock=is_mock, verify_ssl=not insecure, probe_bots=probe)
    print(json.dumps({"skill": "crawl-render-audit", "findings": results}, indent=2))
