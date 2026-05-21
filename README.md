# sharat_ai_labs

A collection of AI solutions for data and enterprise use cases.

---

## Projects

### [sensitive_data_classifier](./sensitive_data_classifier/)

An AI matching engine that classifies dataset fields as sensitive data elements against a standard PII / PHI / PCI DSS / GDPR taxonomy. Runs entirely locally — no external API calls.

See [`sensitive_data_classifier/README.md`](./sensitive_data_classifier/README.md) for architecture, setup, and usage.

### [datascribe_ai](./datascribe_ai/)

An AI agent that generates high-quality, domain-grounded descriptions for dataset fields. Takes a dataset (name, type, sample values) and a domain glossary CSV, indexes the glossary, and crafts descriptions strictly anchored to glossary vocabulary. Fields with no glossary coverage are skipped. Outputs `{dataset_name}.csv` with descriptions, rationale, and confidence scores.

See [`datascribe_ai/README.md`](./datascribe_ai/README.md) for architecture, setup, and usage.
