from __future__ import annotations

from langgraph.graph import END

from graph.state import ClassificationState


def route_after_evaluate(state: ClassificationState) -> str:
    """Extension point: route based on confidence. Currently always goes to END."""
    return END
