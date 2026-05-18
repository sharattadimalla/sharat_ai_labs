from __future__ import annotations

from classifier import engine
from graph.state import ClassificationState
from vector_store import taxonomy_store


def retrieve_tags(state: ClassificationState) -> ClassificationState:
    element = state["element"]
    query_parts = [element.name, element.description]
    if element.sample_values:
        query_parts.extend(element.sample_values[:3])
    query = " ".join(query_parts)
    tags = taxonomy_store.search(query, top_k=5)
    return {**state, "candidate_tags": tags}


def classify(state: ClassificationState) -> ClassificationState:
    result = engine.classify(state["element"], state["candidate_tags"])
    return {**state, "result": result}


def evaluate(state: ClassificationState) -> ClassificationState:
    result = state["result"]
    if result is None:
        return state
    updated = result.model_copy(
        update={"needs_review": result.confidence_level != "HIGH"}
    )
    return {**state, "result": updated}
