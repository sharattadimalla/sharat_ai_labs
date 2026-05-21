from __future__ import annotations

from describer import engine
from graph.state import DescriptionState
from models.schemas import DescriptionResult
from vector_store import glossary_store


def retrieve_terms(state: DescriptionState) -> DescriptionState:
    el = state["element"]
    samples = " ".join(el.sample_values[:3])
    query = f"{el.name} {el.data_type} {samples}".strip()
    terms = glossary_store.search(query, top_k=5)
    return {**state, "glossary_terms": terms}


def skip(state: DescriptionState) -> DescriptionState:
    el = state["element"]
    result = DescriptionResult(
        name=el.name,
        data_type=el.data_type,
        sample_values=el.sample_values,
        ai_generated_description=None,
        ai_rationale="Skipped — no relevant glossary coverage",
        ai_confidence_score=None,
        skipped=True,
    )
    return {**state, "result": result}


def describe(state: DescriptionState) -> DescriptionState:
    result = engine.describe(state["element"], state["glossary_terms"])
    return {**state, "result": result}


def evaluate(state: DescriptionState) -> DescriptionState:
    return state
