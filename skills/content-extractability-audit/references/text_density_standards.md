# DOM Token Density & Signal-to-Noise Ratios

## Token Economics in Machine Reading
AI crawlers operate under strict token and context budget constraints. When an AI tool reads a webpage:
- High DOM overhead (thousands of nested `<div>` tags, verbose SVG markup, inline CSS, inline tracker scripts) floods the tokenizer with non-substantive characters.
- When the **Text-to-HTML ratio drops below 10%**, heuristic text extractors (such as Readability.js, Trafilatura, or LLM scrapers) frequently discard real content as boilerplate or navigation noise.

## Benchmark Metrics

| Metric | Sub-Optimal | Target | Optimal |
| :--- | :--- | :--- | :--- |
| **Text-to-HTML Ratio** | < 10% | 15% - 25% | > 25% |
| **Heading Structure** | 0 H1s or > 3 H1s | Exactly 1 H1 | 1 H1 + structured H2/H3s |
| **Image Alt Coverage** | < 60% with alt | 80% - 95% with alt | 100% descriptive alt |
| **Semantic Element Usage** | `<div>` only | `<main>` present | `<main>`, `<article>`, `<section>` |
