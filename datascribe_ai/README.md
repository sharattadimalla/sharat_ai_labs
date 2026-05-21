# datascribe_ai

An AI agent that generates high-quality, domain-grounded descriptions for dataset fields using a user-provided domain glossary.

---

## How it works

1. **Index** — the domain glossary CSV is embedded and loaded into a ChromaDB vector store
2. **Retrieve** — for each data element, the top-5 semantically similar glossary terms are retrieved
3. **Route** — elements with no relevant glossary coverage are skipped (configurable threshold)
4. **Describe** — a local Ollama LLM generates a description grounded strictly in the retrieved glossary terms, using few-shot examples for quality calibration
5. **Output** — results are written to `{dataset_name}.csv`

---

## Inputs

**Dataset** — defined programmatically or loaded from any source:

| Field | Type | Description |
|---|---|---|
| `name` | str | Field name |
| `data_type` | str | Data type (string, decimal, date, …) |
| `sample_values` | list[str] | Representative sample values |

**Domain glossary CSV** — user-provided, with columns:

| Column | Description |
|---|---|
| `term` | Domain term name |
| `definition` | Full definition |
| `domain` | Subject area (optional) |
| `examples` | Example values (optional) |

---

## Output CSV

Filename: `{dataset_name}.csv`

| Column | Description |
|---|---|
| `name` | Field name |
| `type` | Data type |
| `sample_value` | Sample values |
| `ai_generated_description` | AI-crafted description (blank if skipped) |
| `ai_rationale` | Explanation of how the glossary was applied |
| `ai_confidence_score` | 0.0–1.0 confidence (blank if skipped) |

Skipped fields have `ai_rationale = "Skipped — no relevant glossary coverage"`.

---

## Architecture

```
Dataset (N DataElements)
        │
        ▼
┌───────────────────────────────────────────────┐
│              LangGraph Pipeline               │
│                                               │
│  ┌───────────────┐                            │
│  │retrieve_terms │  vector search ChromaDB    │
│  │               │  → top-5 glossary terms    │
│  └──────┬────────┘                            │
│         │                                     │
│  ┌──────▼────────┐                            │
│  │ route_after   │  min distance ≤ threshold? │
│  │ _retrieve     │                            │
│  └──┬────────┬───┘                            │
│     │        │                                │
│  skip     describe  Ollama LLM (structured    │
│     │        │       JSON) + few-shot refs    │
│     │     evaluate                            │
│     │        │                                │
└─────┼────────┼────────────────────────────────┘
      │        │
      ▼        ▼
 DescriptionResult (per element)
```

---

## Components

| Component | Location | Responsibility |
|---|---|---|
| **Data models** | `models/schemas.py` | Pydantic contracts — `DataElement`, `Dataset`, `DescriptionResult`, `DatasetDescriptionResult` |
| **Glossary loader** | `glossary/loader.py` | Parse glossary CSV → `list[dict]` |
| **Embeddings** | `vector_store/embeddings.py` | `sentence-transformers/all-MiniLM-L6-v2` — local, no API key |
| **Glossary store** | `vector_store/glossary_store.py` | ChromaDB persistent collection; `seed_from_csv()`, `search()`, `is_relevant()` |
| **Few-shot examples** | `examples/descriptions.py` | Reference input→output examples injected into the system prompt |
| **Prompt builder** | `describer/prompt_builder.py` | System prompt (with few-shot examples) + per-element user message + `OUTPUT_SCHEMA` |
| **Engine** | `describer/engine.py` | Calls `ollama.Client.chat(format=OUTPUT_SCHEMA)`; parses response |
| **Graph nodes** | `graph/nodes.py` | `retrieve_terms`, `describe`, `evaluate`, `skip` |
| **Graph edges** | `graph/edges.py` | `route_after_retrieve` — routes to `describe` or `skip` based on glossary relevance |
| **Pipeline** | `graph/pipeline.py` | Compiles the `StateGraph`; exposes `run_element()` and `run_dataset()` |
| **CSV writer** | `output/writer.py` | Writes `DatasetDescriptionResult` to `{dataset_name}.csv` |
| **Sample script** | `demo.py` | End-to-end demo with an e-commerce dataset and 15-term glossary |

---

## Stack

| Layer | Technology |
|---|---|
| Orchestration | LangGraph (`StateGraph`) |
| Vector store | ChromaDB (local persistent) |
| Embeddings | sentence-transformers `all-MiniLM-L6-v2` |
| LLM | Ollama (local) — default `qwen2.5:3b` |
| Data validation | Pydantic v2 |

---

## Quick start

```bash
cd datascribe_ai
cp .env.example .env        # configure OLLAMA_MODEL and OLLAMA_HOST
pip install -r requirements.txt
ollama pull qwen2.5:3b
python demo.py
# Output: data/e-commerce_orders.csv
```

---

## Programmatic usage

```python
from graph.pipeline import run_dataset
from models.schemas import Dataset, DataElement
from output.writer import write_csv

dataset = Dataset(
    name="HR System",
    elements=[
        DataElement(name="employee_id", data_type="string", sample_values=["EMP-001"]),
        DataElement(name="hire_date", data_type="date", sample_values=["2022-06-01"]),
    ],
)

result = run_dataset(dataset, glossary_path="path/to/hr_glossary.csv")
write_csv(result)
```

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_MODEL` | `qwen2.5:3b` | Ollama model tag |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `CHROMA_DB_PATH` | `./chroma_db` | ChromaDB persistence directory |
| `GLOSSARY_SKIP_THRESHOLD` | `0.55` | Max cosine distance to consider a glossary term relevant; elements where the best match exceeds this are skipped |

---

## Glossary CSV format

```csv
term,definition,domain,examples
Order ID,Unique identifier assigned to each customer order.,Orders,ORD-10021
Customer Email,Primary email address associated with a customer account.,Customers,jane@example.com
```

To use a different glossary, pass its path to `run_dataset()`. The vector store is re-seeded automatically when the path changes.
