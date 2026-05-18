from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class DataElement(BaseModel):
    name: str
    data_type: str
    description: str
    sample_values: list[str] = Field(default_factory=list)
    format: str | None = None


class Dataset(BaseModel):
    name: str | None = None
    description: str | None = None
    elements: list[DataElement]


class ClassificationResult(BaseModel):
    data_element_name: str
    predicted_sensitive_data_label: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    confidence_level: Literal["HIGH", "MEDIUM", "LOW"]
    ai_reasoning: str
    recommended_handling_policy: str
    needs_review: bool


class DatasetClassificationResult(BaseModel):
    dataset_name: str | None
    results: list[ClassificationResult]
