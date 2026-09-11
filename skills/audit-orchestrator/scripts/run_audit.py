"""
Advanced Master Audit Orchestrator Script (Entrypoint)
Coordinates the 5 specialized domain audit skills with full support for:
- HTTPS, modern TLS, and self-signed SSL/TLS verification bypass (--insecure)
- Private intranet & localhost dev environments
- HTTP Basic Auth (--auth user:pass)
- Custom Headers (--header "Name: Value", Bearer tokens, Cloudflare tokens)
- Session Cookies (--cookie "key=val")
- Corporate Proxy (--proxy "http://...")
- Active Edge WAF AI-Bot Firewall Probing (--probe-bots)
"""

import sys
import os
import json
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

# Add script directories to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
SKILLS_DIR = SCRIPT_DIR.parent.parent

sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SKILLS_DIR / "crawl-render-audit" / "scripts"))
sys.path.insert(0, str(SKILLS_DIR / "structured-data-entity-audit" / "scripts"))
sys.path.insert(0, str(SKILLS_DIR / "content-extractability-audit" / "scripts"))
sys.path.insert(0, str(SKILLS_DIR / "freshness-authority-audit" / "scripts"))
sys.path.insert(0, str(SKILLS_DIR / "engagement-orientation-audit" / "scripts"))

try:
    from security_client import SecurityAuditClient
except ImportError:
    SecurityAuditClient = None

try:
    from crawl_render_check import audit_crawl_and_render
except ImportError:
    audit_crawl_and_render = None

try:
    from structured_data_check import audit_structured_data
except ImportError:
    audit_structured_data = None

try:
    from extractability_check import audit_extractability
except ImportError:
    audit_extractability = None

try:
    from freshness_check import audit_freshness
except ImportError:
    audit_freshness = None

try:
    from engagement_check import audit_engagement
except ImportError:
    audit_engagement = None

def calculate_score(findings):
    """Calculates AI Readiness Index (0-100)."""
    score = 100
    deductions = {
        "critical": 25,
        "high": 15,
        "medium": 8,
        "low": 3
    }
    for f in findings:
        sev = f.get("severity", "low").lower()
        score -= deductions.get(sev, 5)
    return max(0, min(100, score))

SITE_TYPE_KEYWORDS = {
    "general": ["product", "brand", "pricing", "docs", "contact", "about"],
    "saas": ["dashboard", "trial", "demo", "pricing", "api", "signup"],
    "ecommerce": ["shop", "products", "pricing", "cart", "checkout", "buy"],
    "docs": ["docs", "documentation", "guide", "api", "tutorial", "reference"],
    "enterprise": ["solutions", "enterprise", "security", "contact sales", "demo", "compliance"]
}


def print_usage():
    print("Usage: python skills/audit-orchestrator/scripts/run_audit.py [URL] [options]")
    print()
    print("Examples:")
    print("  python skills/audit-orchestrator/scripts/run_audit.py https://example.com")
    print("  python skills/audit-orchestrator/scripts/run_audit.py https://shop.example.com --site-type ecommerce")
    print("  python skills/audit-orchestrator/scripts/run_audit.py https://docs.example.com --site-type auto")
    print("  python skills/audit-orchestrator/scripts/run_audit.py https://staging.internal.brand:8443 --insecure")
    print()
    print("Options:")
    print("  --mock                  Run mock findings mode")
    print("  --verbose, -v           Show audit progress")
    print("  --insecure, --no-verify-ssl, -k   Disable TLS certificate verification")
    print("  --auth USER:PASS        HTTP Basic Auth credentials")
    print("  --header " + '"Name: Value"' + "   Add a custom HTTP header")
    print("  --cookie VALUE          Add a session cookie")
    print("  --proxy URL             Use an HTTP proxy")
    print("  --probe-bots            Probe AI bot firewall blocks")
    print("  --site-type VALUE       auto|general|saas|ecommerce|docs|enterprise")
    print("  --timeout SECONDS       Request timeout (default: 12)")
    print("  --json-out PATH         Save report to a JSON file")
    print("  --help, -h              Show this help message")


def generate_proactive_recommendations(target_domain, findings, is_secured=True, site_type="general"):
    """Generates mechanism-sound recommendations beyond detected defects."""
    recs = [
        {
            "title": "Publish an /llms.txt Standard Manifest",
            "impact": "high",
            "summary": "Deploy a clean markdown file at /llms.txt and /llms-full.txt describing brand architecture, pricing, and API docs for direct LLM agent ingestion without web scraping friction."
        },
        {
            "title": "Deploy Conversational Q&A Schema (FAQPage)",
            "impact": "high",
            "summary": "Implement Schema.org FAQPage markup on product and documentation pages to capture direct featured quotation in conversational search answers (Perplexity, ChatGPT Search)."
        },
        {
            "title": "Anchor Brand Entity in Wikidata and Crunchbase",
            "impact": "medium",
            "summary": "Create and link verified Wikidata QID and Crunchbase entity entries into your Organization JSON-LD sameAs array to eliminate homonym ambiguity in LLM knowledge graphs."
        },
        {
            "title": "Incorporate Declarative 1-Sentence Value Propositions",
            "impact": "medium",
            "summary": "Structure the primary value proposition as a definitive statement ('[Brand] is a [category] that provides [capability]') to serve as a high-confidence citation anchor for RAG chunking."
        },
        {
            "title": "Maintain WAF Whitelist for Verified AI Search Engine IP Blocks",
            "impact": "high",
            "summary": "Ensure Cloudflare / AWS WAF / Akamai firewall rules permit verified AI crawler User-Agents (GPTBot, PerplexityBot, ClaudeBot) to prevent silent edge drops."
        }
    ]
    return recs

def detect_site_type(url):
    """Infers a likely site category from the URL/hostname."""
    if not url:
        return "general"

    host = urllib.parse.urlparse(url if url.startswith(("http://", "https://")) else f"https://{url}").netloc.lower()
    if not host:
        host = str(url).lower()

    host = host.replace("www.", "")

    ecommerce_markers = ("shop", "store", "cart", "checkout", "product", "products", "buy", "sell", "catalog")
    docs_markers = ("docs", "doc", "developer", "dev", "api", "reference", "guide", "tutorial", "learn")
    saas_markers = ("app", "platform", "dashboard", "cloud", "login", "signup", "workspace", "software")
    enterprise_markers = ("enterprise", "business", "solutions", "security", "corp", "company", "sales")

    if any(marker in host for marker in ecommerce_markers):
        return "ecommerce"
    if any(marker in host for marker in docs_markers):
        return "docs"
    if any(marker in host for marker in saas_markers):
        return "saas"
    if any(marker in host for marker in enterprise_markers):
        return "enterprise"
    return "general"


def run_master_audit(
    url,
    mock=False,
    verbose=False,
    verify_ssl=True,
    auth=None,
    headers=None,
    cookies=None,
    proxy=None,
    probe_bots=False,
    timeout=12,
    site_type="general"
):
    if site_type in (None, "", "auto"):
        site_type = detect_site_type(url)

    if verbose:
        print(f"[*] Initializing Advanced AI-Readiness Audit...")
        print(f"    Target: {url}")
        print(f"    SSL Verification: {'Enabled' if verify_ssl else 'Bypassed (--insecure)'}")
        if auth: print(f"    Authentication: Basic Auth enabled")
        if headers: print(f"    Custom Headers: {list(headers.keys())}")
        if cookies: print(f"    Session Cookies: configured")
        if proxy: print(f"    Proxy: {proxy}")
        if probe_bots: print(f"    WAF Bot Probing: Active")

    # Clean domain
    parsed = urllib.parse.urlparse(url if url.startswith(("http://", "https://")) else f"https://{url}")
    site_domain = parsed.netloc or parsed.path

    # Initialize shared SecurityAuditClient
    client = None
    if SecurityAuditClient and not mock:
        client = SecurityAuditClient(
            verify_ssl=verify_ssl,
            auth=auth,
            headers=headers,
            cookies=cookies,
            proxy=proxy,
            timeout=timeout
        )

    all_findings = []

    # 1. Crawl & Render Audit
    if verbose: print("[1/5] Running Crawl, Render & WAF Firewall Audit...")
    if audit_crawl_and_render:
        try:
            f1 = audit_crawl_and_render(
                url,
                mock=mock,
                client=client,
                verify_ssl=verify_ssl,
                auth=auth,
                headers=headers,
                cookies=cookies,
                proxy=proxy,
                probe_bots=probe_bots
            )
            all_findings.extend(f1)
        except Exception as e:
            if verbose: print(f"    Warning: crawl_render_check error: {e}")

    # 2. Structured Data & Entity Audit
    if verbose: print("[2/5] Running Structured Data & Entity Graph Audit...")
    if audit_structured_data:
        try:
            f2 = audit_structured_data(url, mock=mock, client=client, verify_ssl=verify_ssl)
            all_findings.extend(f2)
        except Exception as e:
            if verbose: print(f"    Warning: structured_data_check error: {e}")

    # 3. Content Extractability Audit
    if verbose: print("[3/5] Running Content Extractability & Token Density Audit...")
    if audit_extractability:
        try:
            f3 = audit_extractability(url, mock=mock, client=client, verify_ssl=verify_ssl)
            all_findings.extend(f3)
        except Exception as e:
            if verbose: print(f"    Warning: extractability_check error: {e}")

    # 4. Freshness & Authority Audit
    if verbose: print("[4/5] Running Freshness, Recency & E-E-A-T Audit...")
    if audit_freshness:
        try:
            f4 = audit_freshness(url, mock=mock, client=client, verify_ssl=verify_ssl)
            all_findings.extend(f4)
        except Exception as e:
            if verbose: print(f"    Warning: freshness_check error: {e}")

    # 5. Engagement & Orientation Audit
    if verbose: print("[5/5] Running On-Site Orientation & Friction Audit...")
    if audit_engagement:
        try:
            f5 = audit_engagement(url, mock=mock, client=client, verify_ssl=verify_ssl, site_type=site_type)
            all_findings.extend(f5)
        except Exception as e:
            if verbose: print(f"    Warning: engagement_check error: {e}")

    # Deduplicate findings by ID
    seen_ids = set()
    unique_findings = []
    for f in all_findings:
        fid = f.get("id")
        if fid not in seen_ids:
            seen_ids.add(fid)
            unique_findings.append(f)

    # Sort findings by severity priority: critical -> high -> medium -> low
    sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    unique_findings.sort(key=lambda x: sev_order.get(x.get("severity", "low").lower(), 9))

    # Calculate summary counts
    summary = {
        "total_findings": len(unique_findings),
        "critical": sum(1 for f in unique_findings if f.get("severity") == "critical"),
        "high": sum(1 for f in unique_findings if f.get("severity") == "high"),
        "medium": sum(1 for f in unique_findings if f.get("severity") == "medium"),
        "low": sum(1 for f in unique_findings if f.get("severity") == "low")
    }

    readiness_score = calculate_score(unique_findings)
    proactive_recs = generate_proactive_recommendations(site_domain, unique_findings, site_type=site_type)

    report = {
        "site": site_domain,
        "site_type": site_type,
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "readiness_score": readiness_score,
        "summary": summary,
        "findings": unique_findings,
        "proactive_recommendations": proactive_recs,
        "security_profile": {
            "protocol": "https" if url.startswith("https://") else "http",
            "ssl_verified": verify_ssl,
            "auth_applied": bool(auth),
            "custom_headers_count": len(headers) if headers else 0,
            "bot_probe_executed": probe_bots
        }
    }

    return report

def parse_cli_args(args):
    target_url = "https://example.com"
    json_out = None
    mock_mode = False
    verbose_mode = False
    verify_ssl = True
    auth = None
    headers = {}
    cookies = None
    proxy = None
    probe_bots = False
    timeout = 12
    site_type = "auto"

    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("--help", "-h"):
            print_usage()
            raise SystemExit(0)
        if arg == "--mock":
            mock_mode = True
        elif arg in ("-v", "--verbose"):
            verbose_mode = True
        elif arg in ("--insecure", "--no-verify-ssl", "-k"):
            verify_ssl = False
        elif arg == "--probe-bots":
            probe_bots = True
        elif arg == "--auth" and i + 1 < len(args):
            auth_val = args[i + 1]
            if ":" in auth_val:
                auth = tuple(auth_val.split(":", 1))
            i += 1
        elif arg in ("-H", "--header") and i + 1 < len(args):
            header_val = args[i + 1]
            if ":" in header_val:
                hk, hv = header_val.split(":", 1)
                headers[hk.strip()] = hv.strip()
            i += 1
        elif arg in ("-b", "--cookie") and i + 1 < len(args):
            cookies = args[i + 1]
            i += 1
        elif arg == "--proxy" and i + 1 < len(args):
            proxy = args[i + 1]
            i += 1
        elif arg == "--timeout" and i + 1 < len(args):
            try:
                timeout = float(args[i + 1])
            except ValueError:
                pass
            i += 1
        elif arg == "--site-type" and i + 1 < len(args):
            candidates = ["auto", "general", "saas", "ecommerce", "docs", "enterprise"]
            value = args[i + 1].lower()
            if value in candidates:
                site_type = value
            else:
                print(f"Warning: unsupported site type '{args[i + 1]}'. Valid values: {', '.join(candidates)}")
            i += 1
        elif arg == "--json-out" and i + 1 < len(args):
            json_out = args[i + 1]
            i += 1
        elif not arg.startswith("-"):
            target_url = arg
        i += 1

    return {
        "target_url": target_url,
        "json_out": json_out,
        "mock_mode": mock_mode,
        "verbose_mode": verbose_mode,
        "verify_ssl": verify_ssl,
        "auth": auth,
        "headers": headers,
        "cookies": cookies,
        "proxy": proxy,
        "probe_bots": probe_bots,
        "timeout": timeout,
        "site_type": site_type
    }

def main():
    cfg = parse_cli_args(sys.argv[1:])

    report = run_master_audit(
        url=cfg["target_url"],
        mock=cfg["mock_mode"],
        verbose=cfg["verbose_mode"],
        verify_ssl=cfg["verify_ssl"],
        auth=cfg["auth"],
        headers=cfg["headers"],
        cookies=cfg["cookies"],
        proxy=cfg["proxy"],
        probe_bots=cfg["probe_bots"],
        timeout=cfg["timeout"],
        site_type=cfg.get("site_type", "auto")
    )
    json_str = json.dumps(report, indent=2)

    if cfg["json_out"]:
        out_path = Path(cfg["json_out"])
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(json_str + "\n")
        print(f"Audit report saved to: {out_path}")
    else:
        print(json_str)

if __name__ == "__main__":
    main()
