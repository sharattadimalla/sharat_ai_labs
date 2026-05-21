from __future__ import annotations

from graph.state import DescriptionState
from vector_store.glossary_store import is_relevant


def route_after_retrieve(state: DescriptionState) -> str:
    if is_relevant(state.get("glossary_terms", [])):
        return "describe"
    return "skip"
