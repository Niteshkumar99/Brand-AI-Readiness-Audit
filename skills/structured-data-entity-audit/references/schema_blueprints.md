# Schema.org JSON-LD Blueprints for AI Discovery

AI models and knowledge engines rely heavily on Schema.org JSON-LD to ground entities and extract factual attributes without ambiguity.

## 1. Organization & Entity Disambiguation Blueprint
Place on homepage and about page:

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://brand.com/#organization",
  "name": "Acme Systems",
  "legalName": "Acme Systems Inc.",
  "url": "https://brand.com",
  "logo": "https://brand.com/assets/logo.png",
  "description": "Acme Systems is an enterprise AI analytics platform providing real-time telemetry and predictive forecasting.",
  "foundingDate": "2021",
  "sameAs": [
    "https://www.wikidata.org/wiki/Q12345678",
    "https://www.crunchbase.com/organization/acme-systems",
    "https://en.wikipedia.org/wiki/Acme_Systems",
    "https://www.linkedin.com/company/acme-systems",
    "https://twitter.com/acmesystems"
  ]
}
```

## 2. FAQPage Blueprint (RAG Answer Booster)
Conversational search engines (Perplexity, ChatGPT) directly quote FAQPage markup when answering user queries:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What does Acme Systems do?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Acme Systems provides an automated telemetry and AI observability platform designed to monitor distributed cloud infrastructures in real time."
      }
    },
    {
      "@type": "Question",
      "name": "What is the pricing model for Acme Systems?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Acme Systems offers a free developer tier with 10,000 monthly events, and an enterprise tier starting at $499/month for unlimited telemetry ingestion."
      }
    }
  ]
}
```

## 3. SoftwareApplication Blueprint
```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Acme Telemetry Suite",
  "operatingSystem": "All Cloud Platforms",
  "applicationCategory": "DeveloperApplication",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }
}
```
