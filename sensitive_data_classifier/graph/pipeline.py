from __future__ import annotations

from langgraph.graph import END, StateGraph

from graph.edges import route_after_evaluate
from graph.nodes import classify, evaluate, retrieve_tags
from graph.state import ClassificationState
from models.schemas import (
    ClassificationResult,
    Dataset,
    DatasetClassificationResult,
    DataElement,
)

_pipeline = None


def _build_pipeline():
    graph = StateGraph(ClassificationState)
    graph.add_node("retrieve_tags", retrieve_tags)
    graph.add_node("classify", classify)
    graph.add_node("evaluate", evaluate)

    graph.set_entry_point("retrieve_tags")
    graph.add_edge("retrieve_tags", "classify")
    graph.add_edge("classify", "evaluate")
    graph.add_conditional_edges("evaluate", route_after_evaluate, {END: END})

    return graph.compile()


def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        _pipeline = _build_pipeline()
    return _pipeline


def run_element(element: DataElement) -> ClassificationResult:
    """Classify a single data element through the LangGraph pipeline."""
    initial_state: ClassificationState = {
        "element": element,
        "candidate_tags": [],
        "result": None,
    }
    final_state = _get_pipeline().invoke(initial_state)
    return final_state["result"]


def run_dataset(dataset: Dataset) -> DatasetClassificationResult:
    """Classify all elements in a dataset; returns results in input order."""
    results = [run_element(element) for element in dataset.elements]
    return DatasetClassificationResult(
        dataset_name=dataset.name,
        results=results,
    )
