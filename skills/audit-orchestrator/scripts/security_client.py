"""
Security & Network Client for Brand AI-Readiness Audit
Supports HTTPS (TLS 1.2/1.3), self-signed SSL/TLS verification bypass,
HTTP Basic Auth, custom headers, cookies, corporate proxy,
and active AI-bot WAF firewall probing.
"""

import urllib.request
import urllib.parse
import urllib.error
import http.client
import ssl
import base64
import re
import time
import socket
from html.parser import HTMLParser

DEFAULT_BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

AI_BOT_PROBES = {
    "GPTBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.2; +https://openai.com/gptbot)",
    "PerplexityBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)",
    "ClaudeBot": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +https://claudebot.anthropic.com)",
    "Google-Extended": "Mozilla/5.0 (compatible; Google-Extended; +https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers)"
}

class SecurityAuditClient:
    def __init__(
        self,
        verify_ssl=True,
        auth=None,          # ("username", "password")
        headers=None,       # dict of header key-values
        cookies=None,       # string or dict
        proxy=None,         # "http://proxy:8080"
        timeout=12
    ):
        self.verify_ssl = verify_ssl
        self.auth = auth
        self.custom_headers = headers or {}
        self.cookies = cookies
        self.proxy = proxy
        self.timeout = timeout
        self.ssl_context = self._create_ssl_context()
        self.opener = self._build_opener()

    def _create_ssl_context(self):
        """Creates an SSLContext configured for modern HTTPS with optional verify bypass."""
        if not self.verify_ssl:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            return ctx
        else:
            ctx = ssl.create_default_context()
            # Enforce modern TLS where supported
            try:
                ctx.minimum_version = ssl.TLSVersion.TLSv1_2
            except AttributeError:
                pass
            return ctx

    def _build_opener(self):
        """Constructs a urllib opener with custom handlers for SSL, Auth, and Proxy."""
        handlers = []

        # HTTPS handler with our SSL context
        https_handler = urllib.request.HTTPSHandler(context=self.ssl_context)
        handlers.append(https_handler)

        # Proxy handler
        if self.proxy:
            proxy_handler = urllib.request.ProxyHandler({
                "http": self.proxy,
                "https": self.proxy
            })
            handlers.append(proxy_handler)

        opener = urllib.request.build_opener(*handlers)
        return opener

    def fetch(self, url, user_agent=None, extra_headers=None):
        """
        Executes a secure, authenticated HTTP/HTTPS GET request.
        Returns a dict:
        {
          "status": 200,
          "headers": {...},
          "html": "...",
          "latency_ms": 150.2,
          "url": "https://...",
          "ssl_info": {...},
          "error": None
        }
        """
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        req_headers = {
            "User-Agent": user_agent or DEFAULT_BROWSER_UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9"
        }

        # Apply custom headers
        for k, v in self.custom_headers.items():
            req_headers[k] = v

        if extra_headers:
            for k, v in extra_headers.items():
                req_headers[k] = v

        # Apply Basic Auth
        if self.auth:
            username, password = self.auth
            auth_str = f"{username}:{password}"
            encoded_auth = base64.b64encode(auth_str.encode("utf-8")).decode("ascii")
            req_headers["Authorization"] = f"Basic {encoded_auth}"

        # Apply Cookies
        if self.cookies:
            if isinstance(self.cookies, dict):
                cookie_str = "; ".join(f"{k}={v}" for k, v in self.cookies.items())
            else:
                cookie_str = str(self.cookies)
            req_headers["Cookie"] = cookie_str

        req = urllib.request.Request(url, headers=req_headers)
        start_time = time.time()

        ssl_info = {
            "is_https": url.startswith("https://"),
            "cert_verified": self.verify_ssl,
            "hsts_present": False,
            "hsts_header": ""
        }

        try:
            with self.opener.open(req, timeout=self.timeout) as response:
                latency = round((time.time() - start_time) * 1000, 2)
                res_headers = dict(response.headers)
                final_url = response.geturl()
                status_code = response.getcode()

                # Extract HSTS
                hsts = res_headers.get("Strict-Transport-Security", "")
                if hsts:
                    ssl_info["hsts_present"] = True
                    ssl_info["hsts_header"] = hsts

                body_bytes = response.read()
                raw_html = body_bytes.decode("utf-8", errors="replace")

                return {
                    "status": status_code,
                    "headers": res_headers,
                    "html": raw_html,
                    "latency_ms": latency,
                    "url": final_url,
                    "ssl_info": ssl_info,
                    "error": None
                }

        except urllib.error.HTTPError as e:
            latency = round((time.time() - start_time) * 1000, 2)
            res_headers = dict(e.headers) if hasattr(e, "headers") else {}
            body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
            return {
                "status": e.code,
                "headers": res_headers,
                "html": body,
                "latency_ms": latency,
                "url": url,
                "ssl_info": ssl_info,
                "error": f"HTTPError {e.code}: {e.reason}"
            }

        except urllib.error.URLError as e:
            return {
                "status": None,
                "headers": {},
                "html": "",
                "latency_ms": 0,
                "url": url,
                "ssl_info": ssl_info,
                "error": f"URLError: {str(e.reason)}"
            }

        except Exception as e:
            return {
                "status": None,
                "headers": {},
                "html": "",
                "latency_ms": 0,
                "url": url,
                "ssl_info": ssl_info,
                "error": f"Exception: {str(e)}"
            }

    def probe_ai_firewall(self, url):
        """
        Actively probes edge WAF (Cloudflare, Akamai, AWS WAF, Imperva)
        to detect if AI crawler User-Agents are blocked or challenged
        while standard browsers are allowed.
        """
        results = {
            "browser_status": None,
            "blocked_bots": [],
            "challenged_bots": [],
            "allowed_bots": []
        }

        # 1. Baseline Browser Request
        base_res = self.fetch(url, user_agent=DEFAULT_BROWSER_UA)
        results["browser_status"] = base_res["status"]

        if base_res["status"] != 200:
            # Baseline failed, cannot isolate bot-specific WAF behavior
            return results

        # 2. Probe AI user-agents
        for bot_name, bot_ua in AI_BOT_PROBES.items():
            res = self.fetch(url, user_agent=bot_ua)
            code = res["status"]
            html = res["html"].lower()

            is_challenge = any(term in html for term in (
                "cf-turnstile", "challenge-running", "cloudflare ray id", 
                "datadome", "perimeterx", "captcha", "security check"
            ))

            if code in (403, 401, 429, 503):
                results["blocked_bots"].append((bot_name, code))
            elif is_challenge and code in (200, 403):
                results["challenged_bots"].append((bot_name, "CAPTCHA/Challenge"))
            elif code == 200:
                results["allowed_bots"].append(bot_name)

        return results

    def check_mixed_content(self, html, page_url):
        """Identifies insecure HTTP asset references on an HTTPS page."""
        if not page_url.startswith("https://"):
            return []

        insecure_assets = []
        # Look for src="http://..." or href="http://...css"
        pattern = r'(?:src|href)=["\'](http://[^"\']+\.(?:js|css|png|jpg|jpeg|svg|webp|gif|woff2?))["\']'
        matches = re.findall(pattern, html, re.IGNORECASE)
        for m in set(matches):
            insecure_assets.append(m)
        return insecure_assets
