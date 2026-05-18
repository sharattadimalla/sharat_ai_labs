# sharat_ai_labs

A collection of AI solutions for data and enterprise use cases.

---

## Projects

### [sensitive_data_classifier](./sensitive_data_classifier/)

An AI matching engine that classifies dataset fields as sensitive data elements against a standard PII / PHI / PCI DSS / GDPR taxonomy.

**Output per data element:**
- `predicted_sensitive_data_label` — matched taxonomy label or "Not Sensitive"
- `confidence_score` + `confidence_level` (HIGH / MEDIUM / LOW)
- `ai_reasoning` — explanation of the decision
- `recommended_handling_policy` — data handling guidance
- `needs_review` — flagged when confidence is not HIGH

---

### Architecture

```
Dataset (N DataElements)
        │
        ▼
┌───────────────────────────────────────────────┐
│              LangGraph Pipeline               │
│                                               │
│  ┌─────────────┐                              │
│  │retrieve_tags│  vector search ChromaDB      │
│  │             │  → top-5 candidate tags      │
│  └──────┬──────┘                              │
│         │                                     │
│  ┌──────▼──────┐                              │
│  │  classify   │  Ollama LLM (structured JSON)│
│  │             │  + candidate tags in prompt  │
│  └──────┬──────┘                              │
│         │                                     │
│  ┌──────▼──────┐                              │
│  │  evaluate   │  map score → HIGH/MEDIUM/LOW │
│  │             │  set needs_review flag       │
│  └──────┬──────┘                              │
└─────────┼─────────────────────────────────────┘
          │
          ▼
 ClassificationResult (per element)
```

The engine runs each `DataElement` through the graph independently and returns results in the same order as the input.

---

### Components

| Component | Location | Responsibility |
|---|---|---|
| **Data models** | `models/schemas.py` | Pydantic contracts — `DataElement`, `Dataset`, `ClassificationResult`, `DatasetClassificationResult` |
| **Taxonomy** | `taxonomy/definitions.py` | 27 sensitive tag definitions (PII ×10, PHI ×6, PCI DSS ×5, GDPR Special ×6) with label, description, handling policy, and regulatory frameworks |
| **Embeddings** | `vector_store/embeddings.py` | `sentence-transformers/all-MiniLM-L6-v2` wrapped as a ChromaDB `EmbeddingFunction` — runs fully local, no API key |
| **Taxonomy store** | `vector_store/taxonomy_store.py` | ChromaDB persistent collection; seeds from taxonomy on first run; exposes `search(query, top_k)` and `add_tag(tag)` |
| **Prompt builder** | `classifier/prompt_builder.py` | Assembles the system prompt and per-element user message; defines `OUTPUT_SCHEMA` (JSON schema for Ollama structured output) |
| **Engine** | `classifier/engine.py` | Calls `ollama.Client.chat(format=OUTPUT_SCHEMA)`; parses response; maps confidence score to level |
| **Graph nodes** | `graph/nodes.py` | Three LangGraph node functions: `retrieve_tags`, `classify`, `evaluate` |
| **Graph edges** | `graph/edges.py` | `route_after_evaluate` — conditional routing function (extension point for adding human-review or re-classify branches) |
| **Pipeline** | `graph/pipeline.py` | Compiles the `StateGraph` once (singleton); exposes `run_element()` and `run_dataset()` |
| **Sample script** | `sample.py` | End-to-end demo with 9 mixed data elements |

---

### Stack

| Layer | Technology |
|---|---|
| Orchestration | LangGraph (`StateGraph`) |
| Vector store | ChromaDB (local persistent) |
| Embeddings | sentence-transformers `all-MiniLM-L6-v2` |
| LLM | Ollama (local) — default `qwen2.5:3b` |
| Data validation | Pydantic v2 |

---

### Quick start

```bash
cd sensitive_data_classifier
cp .env.example .env        # configure OLLAMA_MODEL and OLLAMA_HOST
pip install -r requirements.txt
ollama pull qwen2.5:3b
python sample.py
```

To classify a different model, set `OLLAMA_MODEL` in `.env` to any model available in your Ollama instance.

To add a custom sensitive tag, append to `taxonomy/definitions.py` and delete `./chroma_db/` to trigger a re-seed.
