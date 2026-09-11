# AI Crawler & Scraper User Agent Registry

AI assistants use specialized web crawlers to retrieve real-time data, build search indexes, and ground citations. Blocking these user agents directly removes the brand from conversational AI answers.

| Crawler / Bot Name | Primary Operator | Purpose | User Agent Token |
| :--- | :--- | :--- | :--- |
| **GPTBot** | OpenAI | Training data & citation grounding for ChatGPT | `GPTBot` |
| **ChatGPT-User** | OpenAI | Real-time browsing actions taken on user request | `ChatGPT-User` |
| **PerplexityBot** | Perplexity AI | Real-time search and retrieval for Perplexity answers | `PerplexityBot` |
| **ClaudeBot** | Anthropic | Training & search retrieval for Claude | `ClaudeBot` |
| **Claude-Web** | Anthropic | Real-time web browsing during user conversations | `Claude-Web` |
| **Google-Extended** | Google | Grounding for Gemini, Google AI Overviews, Vertex AI | `Google-Extended` |
| **Amazonbot** | Amazon | Web indexing for Alexa and Amazon AI services | `Amazonbot` |
| **Applebot-Extended** | Apple | Grounding for Apple Intelligence & Siri | `Applebot-Extended` |
| **Bytespider** | ByteDance | Indexing for TikTok and ByteDance AI models | `Bytespider` |
| **CCBot** | Common Crawl | Public web archive used by almost all open LLMs | `CCBot` |
| **Meta-ExternalAgent** | Meta | Grounding and retrieval for Meta AI | `Meta-ExternalAgent` |

## Recommended `robots.txt` Configuration

To maximize AI visibility while protecting sensitive internal paths:

```txt
# Allow legitimate AI retrieval crawlers
User-agent: GPTBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

# Disallow sensitive or authenticated paths
Disallow: /admin/
Disallow: /api/private/
Disallow: /checkout/
```
