from __future__ import annotations

from examples.descriptions import FEW_SHOT_EXAMPLES
from models.schemas import DataElement

_few_shot_text = "\n".join(
    (
        f"Field: {ex['field']} | Type: {ex['data_type']} | Samples: {ex['sample_values']}\n"
        f"Glossary: {'; '.join(t['term'] + ' — ' + t['definition'] for t in ex['glossary_terms'])}\n"
        f'Output: {{"ai_generated_description": "{ex["description"]}", '
        f'"ai_rationale": "{ex["rationale"]}", '
        f'"ai_confidence_score": {ex["confidence"]}}}\n'
    )
    for ex in FEW_SHOT_EXAMPLES
)

SYSTEM_PROMPT = f"""You are an expert technical writer specializing in creating precise, domain-grounded data dictionary descriptions.

Your task is to write a high-quality description for a dataset field using ONLY the provided domain glossary terms.

Rules:
- Ground every statement in the provided glossary terms. Do not introduce outside knowledge or generic definitions.
- Write descriptions that are clear, concise (1-3 sentences), and unambiguous.
- Use domain-specific vocabulary from the glossary terms.
- Confidence scoring:
  - HIGH (≥ 0.85): The field name or sample values directly and unambiguously match one or more glossary terms.
  - MEDIUM (0.65–0.84): The field is likely related to the glossary terms with minor inference required.
  - LOW (< 0.65): The connection to glossary terms is uncertain.
- Return only the JSON object. No markdown, no extra text.

High-quality description examples:
{_few_shot_text}"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "ai_generated_description": {"type": "string"},
        "ai_rationale": {"type": "string"},
        "ai_confidence_score": {"type": "number"},
    },
    "required": ["ai_generated_description", "ai_rationale", "ai_confidence_score"],
}


def build_messages(element: DataElement, glossary_terms: list[dict]) -> list[dict]:
    terms_text = "\n".join(
        f"- {t['term']}: {t['definition']}"
        + (f" (domain: {t['domain']})" if t.get("domain") else "")
        for t in glossary_terms
    )
    samples_text = (
        ", ".join(f'"{v}"' for v in element.sample_values[:3])
        if element.sample_values
        else "N/A"
    )

    user_content = (
        f"Field name: {element.name}\n"
        f"Data type: {element.data_type}\n"
        f"Sample values: {samples_text}\n\n"
        f"Relevant glossary terms:\n{terms_text}\n\n"
        "Return a JSON object with keys: ai_generated_description, ai_rationale, ai_confidence_score."
    )

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]
