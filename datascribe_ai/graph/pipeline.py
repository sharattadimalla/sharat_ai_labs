from __future__ import annotations

from langgraph.graph import END, StateGraph

from graph.edges import route_after_retrieve
from graph.nodes import describe, evaluate, retrieve_terms, skip
from graph.state import DescriptionState
from models.schemas import DataElement, Dataset, DatasetDescriptionResult, DescriptionResult
from vector_store import glossary_store

_pipeline = None


def _build_pipeline():
    graph = StateGraph(DescriptionState)

    graph.add_node("retrieve_terms", retrieve_terms)
    graph.add_node("describe", describe)
    graph.add_node("evaluate", evaluate)
    graph.add_node("skip", skip)

    graph.set_entry_point("retrieve_terms")
    graph.add_conditional_edges(
        "retrieve_terms",
        route_after_retrieve,
        {"describe": "describe", "skip": "skip"},
    )
    graph.add_edge("describe", "evaluate")
    graph.add_edge("evaluate", END)
    graph.add_edge("skip", END)

    return graph.compile()


def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        _pipeline = _build_pipeline()
    return _pipeline


def run_element(element: DataElement, glossary_path: str) -> DescriptionResult:
    glossary_store.seed_from_csv(glossary_path)
    pipeline = _get_pipeline()
    final_state = pipeline.invoke(
        {"element": element, "glossary_terms": [], "result": None}
    )
    return final_state["result"]


def run_dataset(dataset: Dataset, glossary_path: str) -> DatasetDescriptionResult:
    glossary_store.seed_from_csv(glossary_path)
    pipeline = _get_pipeline()
    results = []
    for element in dataset.elements:
        final_state = pipeline.invoke(
            {"element": element, "glossary_terms": [], "result": None}
        )
        results.append(final_state["result"])
    return DatasetDescriptionResult(dataset_name=dataset.name, results=results)
