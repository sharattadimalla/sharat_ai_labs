from __future__ import annotations

from typing import TypedDict

from models.schemas import DataElement, DescriptionResult


class DescriptionState(TypedDict):
    element: DataElement
    glossary_terms: list[dict]
    result: DescriptionResult | None
