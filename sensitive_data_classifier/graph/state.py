from __future__ import annotations

from typing import TypedDict

from models.schemas import ClassificationResult, DataElement


class ClassificationState(TypedDict):
    element: DataElement
    candidate_tags: list[dict]
    result: ClassificationResult | None
