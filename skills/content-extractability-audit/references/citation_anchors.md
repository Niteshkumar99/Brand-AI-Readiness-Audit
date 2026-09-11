# LLM Citation Anchors & Quotable Proposition Engineering

## How Retrieval-Augmented Generation (RAG) Selects What to Quote
When an AI assistant constructs an answer, its retrieval pipeline:
1. **Chunks** the fetched HTML into 250-500 token passages.
2. **Scores** passages via semantic embedding similarity and BM25 lexical matching.
3. **Ranks** candidate sentences for factual confidence. Sentences with explicit subjects, definitive verbs, and concrete nouns receive the highest extraction weight.

## The Anatomy of an Unquotable Sentence vs. A Quotable Anchor

### Weak (Unquotable by AI):
> *"We synergize innovative next-gen paradigms to empower enterprise digital evolution."*
- **Problem**: Zero verifiable claims, zero concrete nouns. An LLM summarizer ignores this as marketing noise.

### Strong (High AI Citation Probability):
> *"Acme Cloud is an automated Kubernetes telemetry platform that ingests up to 1,000,000 events per second with sub-50ms latency."*
- **Why it works**:
  - Unambiguous Subject: `Acme Cloud`
  - Explicit Class: `automated Kubernetes telemetry platform`
  - Quantifiable Capabilities: `1,000,000 events per second`, `sub-50ms latency`

## Best Practices for Brand Fact Extractability
1. **The Lead Sentence Rule**: The first sentence under any `<h1>` or `<h2>` must state an atomic fact answering who, what, or how.
2. **Avoid Pricing in Images**: Never render pricing tables, tier comparisons, or architecture diagrams solely in PNG/JPEG/SVG without corresponding HTML `<table>` or plain-text bullet points.
3. **Definitive Terminology**: Use standard industry category terms rather than proprietary coined acronyms.
