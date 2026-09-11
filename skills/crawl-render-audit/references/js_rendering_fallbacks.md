# JS-Rendering Traps & SSR/SSG Architectural Solutions

## The Fundamental Problem: Fast-Crawl vs. Headless Browser
When a user asks ChatGPT or Perplexity a question:
1. The AI search engine issues hundreds of sub-second HTTP GET requests across Candidate URLs.
2. Because executing JavaScript via headless Chromium instances consumes 100x-500x more CPU, memory, and time, **fast retrieval crawlers inspect only the raw initial HTML payload**.
3. If the website is a pure Single-Page Application (SPA) with `<div id="root"></div>` that requires JavaScript hydration to render text, the crawler sees an empty page.
4. **Outcome**: The AI crawler assumes the page contains zero substantive facts and skips citing it.

## The 4 Detection Signals
1. **Empty Body Shell**: Less than 150 printable text characters inside `<body>`, despite dozens of `<script>` tags.
2. **Framework Mount Markers**: Elements like `<div id="root">`, `<div id="__next">`, or `<app-root></app-root>` containing no server-rendered child nodes.
3. **Noscript Warnings**: Presence of `<noscript>You need to enable JavaScript to run this app.</noscript>`.
4. **Heavy Hydration Bundles**: Initial bundle size > 2MB without pre-rendered semantic HTML.

## Remediation Roadmap
1. **Adopt Server-Side Rendering (SSR) or Static-Site Generation (SSG)**:
   - Next.js (App Router / React Server Components)
   - Nuxt.js (Universal Mode)
   - Astro or SvelteKit
2. **Dynamic Rendering / Edge Pre-rendering**:
   - Detect AI crawler User-Agents at the CDN / Cloudflare Edge level.
   - Serve pre-rendered static HTML snapshots directly to AI crawlers while serving standard interactive bundles to human browsers.
