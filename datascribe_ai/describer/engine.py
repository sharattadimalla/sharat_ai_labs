from __future__ import annotations

import json
import os

import ollama
from dotenv import load_dotenv

from describer.prompt_builder import OUTPUT_SCHEMA, build_messages
from models.schemas import DataElement, DescriptionResult

load_dotenv()

_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

_client: ollama.Client | None = None


def _get_client() -> ollama.Client:
    global _client
    if _client is None:
        _client = ollama.Client(host=_HOST)
    return _client


def describe(element: DataElement, glossary_terms: list[dict]) -> DescriptionResult:
    client = _get_client()
    messages = build_messages(element, glossary_terms)

    response = client.chat(
        model=_MODEL,
        messages=messages,
        format=OUTPUT_SCHEMA,
    )

    data = json.loads(response.message.content)
    score = max(0.0, min(1.0, float(data["ai_confidence_score"])))

    return DescriptionResult(
        name=element.name,
        data_type=element.data_type,
        sample_values=element.sample_values,
        ai_generated_description=data["ai_generated_description"],
        ai_rationale=data["ai_rationale"],
        ai_confidence_score=score,
        skipped=False,
    )
