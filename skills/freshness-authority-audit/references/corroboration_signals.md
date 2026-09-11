# Multi-Source Consensus & Temporal Authority in LLM Citations

## Why Agreement Across the Web Shapes AI Answers
Modern AI assistants (ChatGPT, Claude, Perplexity, Gemini) do not treat all web claims equally:
1. **Consensus Requirement**: A claim repeated identically across multiple independent, high-authority sources is treated as factual truth. A claim that appears only on an isolated page is treated as unverified or marketing puffery.
2. **Temporal Decay**: Retrieval models apply a temporal decay penalty to documents without explicit `dateModified` timestamps or displaying outdated years. If another source provides a date from the current year, the AI assistant will cite that source instead.

## Critical Trust Signals for AI Engines
1. **Explicit Timestamps**:
   - `<meta property="article:modified_time" content="2026-02-15T10:00:00Z">`
   - JSON-LD `"dateModified": "2026-02-15"`
2. **Organizational Attribution (E-E-A-T)**:
   - Visible author credentials or verified organization entity.
   - Verifiable contact and legal pages (`/about`, `/contact`, `/privacy`, `/terms`).
