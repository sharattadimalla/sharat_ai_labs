from __future__ import annotations

import json
import os

import ollama
from dotenv import load_dotenv

from classifier.prompt_builder import OUTPUT_SCHEMA, build_messages
from models.schemas import ClassificationResult, DataElement

load_dotenv()

_HIGH_THRESHOLD = float(os.getenv("CONFIDENCE_REVIEW_THRESHOLD", "0.85"))
_MEDIUM_THRESHOLD = 0.65
_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

_client: ollama.Client | None = None


def _get_client() -> ollama.Client:
    global _client
    if _client is None:
        _client = ollama.Client(host=_HOST)
    return _client


def _confidence_level(score: float) -> str:
    if score >= _HIGH_THRESHOLD:
        return "HIGH"
    if score >= _MEDIUM_THRESHOLD:
        return "MEDIUM"
    return "LOW"


def classify(element: DataElement, candidate_tags: list[dict]) -> ClassificationResult:
    """Call a local Ollama model to classify a single data element."""
    client = _get_client()
    messages = build_messages(element, candidate_tags)

    response = client.chat(
        model=_MODEL,
        messages=messages,
        format=OUTPUT_SCHEMA,
    )

    data = json.loads(response.message.content)

    score = max(0.0, min(1.0, float(data["confidence_score"])))
    level = _confidence_level(score)

    return ClassificationResult(
        data_element_name=element.name,
        predicted_sensitive_data_label=data["predicted_sensitive_data_label"],
        confidence_score=score,
        confidence_level=level,
        ai_reasoning=data["ai_reasoning"],
        recommended_handling_policy=data["recommended_handling_policy"],
        needs_review=(level != "HIGH"),
    )
