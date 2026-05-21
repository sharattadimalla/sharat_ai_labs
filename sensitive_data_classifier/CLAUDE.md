# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the project

All commands must be run from the `sensitive_data_classifier/` directory (the Python root — imports are relative to it).

```bash
# Install dependencies
pip install -r requirements.txt

# Run the sample script
python demo.py

# Classify programmatically
python -c "
from graph.pipeline import run_dataset
from models.schemas import Dataset, DataElement
ds = Dataset(name='test', elements=[DataElement(name='email', data_type='string', description='user email')])
print(run_dataset(ds).model_dump_json(indent=2))
"
```

## Prerequisites

Ollama must be running with a model pulled:
```bash
ollama serve
ollama pull qwen2.5:3b
```

Configure via `.env` (copy from `.env.example`). Key variables:
- `OLLAMA_MODEL` — model tag (default `qwen2.5:3b`)
- `OLLAMA_HOST` — Ollama server URL (default `http://localhost:11434`)
- `CHROMA_DB_PATH` — where ChromaDB persists (default `./chroma_db`)
- `CONFIDENCE_REVIEW_THRESHOLD` — score above which level = HIGH (default `0.85`)

## Architecture

The engine follows a two-phase design: **vector retrieval narrows the search space, then the LLM classifies**.

### Phase 1 — Vector retrieval (`vector_store/`)
`taxonomy/definitions.py` holds 27 sensitive tags (PII, PHI, PCI DSS, GDPR Special), each with a `label`, `description`, `handling_policy`, and `frameworks` list. On first run, `taxonomy_store.seed_if_empty()` embeds every tag using `sentence-transformers/all-MiniLM-L6-v2` (local, no API) and upserts them into a ChromaDB persistent collection keyed by label. At classify time, `taxonomy_store.search(query, top_k=5)` returns the 5 most semantically similar tags to use as LLM candidates.

### Phase 2 — LLM classification (`classifier/`)
`prompt_builder.py` builds an Ollama-compatible message list: a static system prompt (role + confidence rules) and a dynamic user message containing the data element fields plus the retrieved candidate tags. `OUTPUT_SCHEMA` is a plain JSON schema dict passed to `ollama.Client.chat(format=OUTPUT_SCHEMA)` to constrain the model's response to a valid JSON object. `engine.py` parses the response and maps `confidence_score` to `confidence_level` (HIGH ≥ 0.85, MEDIUM ≥ 0.65, LOW < 0.65).

### Orchestration (`graph/`)
A LangGraph `StateGraph` wires the two phases together via three nodes in `nodes.py`:
1. `retrieve_tags` — queries ChromaDB
2. `classify` — calls `engine.classify()`
3. `evaluate` — sets `needs_review=True` when confidence is not HIGH

`edges.py` contains `route_after_evaluate`, a conditional routing function that currently always goes to `END` but is the extension point for adding branches (e.g., a human-review queue or a re-classify loop).

`pipeline.py` compiles the graph once (singleton) and exposes two public functions:
- `run_element(DataElement) -> ClassificationResult`
- `run_dataset(Dataset) -> DatasetClassificationResult`

### Data contracts (`models/schemas.py`)
All inputs and outputs are Pydantic v2 models. `DataElement` is the input unit; `ClassificationResult` is the per-element output with `predicted_sensitive_data_label`, `confidence_score`, `confidence_level`, `ai_reasoning`, `recommended_handling_policy`, and `needs_review`.

## Extending the taxonomy

Add new sensitive tags to `taxonomy/definitions.py` (follow the existing dict structure), then delete `./chroma_db/` to force a re-seed on next run. Alternatively call `taxonomy_store.add_tag(tag)` at runtime without restarting.

## Swapping the LLM

Change `OLLAMA_MODEL` in `.env` to any model available in your Ollama instance. The engine uses `ollama.Client.chat` with structured JSON output (`format=OUTPUT_SCHEMA`) — any model that supports Ollama's structured output API will work.
