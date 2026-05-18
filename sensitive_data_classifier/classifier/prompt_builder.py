from __future__ import annotations

from models.schemas import DataElement

SYSTEM_PROMPT = """\
You are an expert data governance analyst specializing in sensitive data classification.

Your task is to classify a given data element against a standard taxonomy of sensitive \
data categories covering PII (Personally Identifiable Information), PHI (Protected \
Health Information), PCI DSS (Payment Card Industry data), and GDPR special categories.

Rules:
- Choose the single most accurate sensitive tag from the candidate list provided.
- If none of the candidates apply, output the label "Not Sensitive".
- Your confidence_score must reflect genuine uncertainty:
  - 0.85-1.0 = HIGH: the field is clearly and unambiguously sensitive.
  - 0.65-0.84 = MEDIUM: likely sensitive but some ambiguity exists.
  - 0.0-0.64 = LOW: you are uncertain; a human should review.
- Provide a concise ai_reasoning (2-3 sentences) explaining your decision.
- Provide the recommended_handling_policy from the matched tag. \
  If not sensitive, output "No special handling required."
- Respond ONLY with a JSON object — no markdown, no explanation outside the JSON.
"""

# JSON schema used to constrain Ollama structured output
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "predicted_sensitive_data_label": {"type": "string"},
        "confidence_score": {"type": "number"},
        "ai_reasoning": {"type": "string"},
        "recommended_handling_policy": {"type": "string"},
    },
    "required": [
        "predicted_sensitive_data_label",
        "confidence_score",
        "ai_reasoning",
        "recommended_handling_policy",
    ],
}


def build_messages(element: DataElement, candidate_tags: list[dict]) -> list[dict]:
    samples = (
        ", ".join(element.sample_values) if element.sample_values else "not provided"
    )
    fmt = element.format or "not provided"

    candidates_text = "\n".join(
        f"  {i + 1}. {tag['label']}: {tag['document']}"
        for i, tag in enumerate(candidate_tags)
    )

    user_content = (
        f"Data element to classify:\n"
        f"  Name: {element.name}\n"
        f"  Data type: {element.data_type}\n"
        f"  Description: {element.description}\n"
        f"  Sample values: {samples}\n"
        f"  Format: {fmt}\n\n"
        f"Candidate sensitive tags (ranked by semantic similarity):\n"
        f"{candidates_text}\n\n"
        f"Return a JSON object with keys: predicted_sensitive_data_label, "
        f"confidence_score, ai_reasoning, recommended_handling_policy."
    )

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]
