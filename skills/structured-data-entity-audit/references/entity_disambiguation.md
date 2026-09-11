# Entity Disambiguation & Knowledge Graph Grounding

## Why Entity Ambiguity Cripples AI Citations
When an AI assistant receives a prompt such as:
> *"What does Acme do and how much does it cost?"*

The retrieval system performs entity linking. If "Acme" could refer to a brick manufacturer, an animation corporation, or a cloud software startup, the AI calculates a confidence score across each candidate.

If your website provides **no explicit disambiguation**, the AI assistant:
1. May hallucinate the details of another company sharing the name.
2. May refuse to answer due to low entity confidence.
3. May omit citations entirely.

## How to Establish Absolute Entity Identity

1. **Explicit `@id` URI**:
   Assign a permanent URI anchor to your organization, e.g. `https://brand.com/#organization`. This allows child schemas (Product, WebSite, Article) to link back to the exact organization node via `"publisher": {"@id": "https://brand.com/#organization"}`.

2. **The `sameAs` Authority Mesh**:
   The `sameAs` property explicitly links your domain to nodes in curated global knowledge graphs:
   - **Wikidata**: The single most influential open knowledge graph ingested by Google Knowledge Graph, OpenAI, and Anthropic.
   - **Crunchbase**: Primary corporate identity registry.
   - **Wikipedia**: Encyclopedic authority anchor.
   - **Official Social Profiles**: Verifiable social proof.

By supplying these links, you elevate your brand from an unverified string of characters to an authenticated node in the global knowledge graph.
