# Auditing HTTPS, Private Networks & Secured Staging Environments

## 1. Overview
Brands frequently test new websites, redesigns, and AI features on **private staging servers, VPN intranets, or secured environments** before making them public. Ensuring AI discoverability *before* launch requires an audit engine capable of navigating these security layers safely without making site-altering changes.

The Brand AI-Readiness Audit Marketplace supports enterprise security configurations:
- **HTTPS & Modern TLS (1.2 / 1.3)**
- **Self-Signed & Internal Enterprise CA Certificates (`--insecure` / `--no-verify-ssl`)**
- **HTTP Basic Authentication (`--auth user:pass`)**
- **Bearer & Custom Security Headers (`--header "Authorization: Bearer <token>"`)**
- **Cloudflare Zero Trust / Access Service Tokens (`CF-Access-Client-Id` / `CF-Access-Client-Secret`)**
- **Preview & Staging Cookies (`--cookie "preview_env=staging; session=..."`)**
- **Corporate Egress Proxies (`--proxy http://proxy:8080`)**
- **Active Edge WAF / CDN AI-Bot Probing (`--probe-bots`)**

---

## 2. Advanced Diagnostic Signals for Secured Environments

### A. The WAF / Edge CDN "Silent Blocker" (`CR-009`)
Many organizations believe their site is accessible to AI search engines because their `robots.txt` contains no disallow rules. However, their **Cloudflare Bot Management, Akamai, Imperva, or AWS WAF** is configured to block or issue CAPTCHAs to non-browser User-Agents.
- **Problem**: When `GPTBot` or `PerplexityBot` requests a page, the CDN immediately returns `403 Forbidden` or a JavaScript challenge (`cf-turnstile`).
- **Detection**: The engine performs an active side-by-side probe comparing standard browser requests against real AI crawler User-Agents.
- **Fix**: Add a WAF exception rule to allow verified AI crawler IP ranges and user-agents while maintaining DDoS protection.

### B. Insecure Mixed-Content Assets (`CR-011`)
When an HTTPS page embeds stylesheets, scripts, or images via unencrypted `http://` URLs:
- Modern browsers and AI headless scrapers block the unencrypted assets under mixed-content security policies.
- Critical product data or styling is dropped from the rendered page.
- **Fix**: Update all asset references to protocol-relative `//` or explicit `https://` URLs.

### C. Strict-Transport-Security (HSTS) Validation (`CR-010`)
AI answer engines (Google Gemini, Perplexity, ChatGPT Search) score domain reliability higher when `Strict-Transport-Security` is enforced.
- Prevents SSL-stripping attacks and enforces encrypted transport.
- Target header: `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`

---

## 3. Command Line Examples for Secured & Private Targets

### 1. Auditing Localhost / Development Server
```bash
python skills/audit-orchestrator/scripts/run_audit.py http://localhost:3000
python skills/audit-orchestrator/scripts/run_audit.py https://127.0.0.1:8443 --insecure
```

### 2. Auditing Staging with HTTP Basic Authentication
```bash
python skills/audit-orchestrator/scripts/run_audit.py https://staging.brand.com --auth "qa_tester:SuperSecret123"
```

### 3. Auditing with Custom Auth Token or Cloudflare Access
```bash
python skills/audit-orchestrator/scripts/run_audit.py https://internal.brand.com \
  --header "CF-Access-Client-Id: your-client-id" \
  --header "CF-Access-Client-Secret: your-client-secret" \
  --insecure
```

### 4. Auditing with Active AI-Bot WAF Probing
```bash
python skills/audit-orchestrator/scripts/run_audit.py https://yourbrand.com --probe-bots
```

### 5. Auditing Behind a Corporate Proxy
```bash
python skills/audit-orchestrator/scripts/run_audit.py https://yourbrand.com --proxy "http://proxy.corp.internal:8080"
```
