from __future__ import annotations

from pydantic import BaseModel, Field


class DataElement(BaseModel):
    name: str
    data_type: str
    sample_values: list[str] = []


class Dataset(BaseModel):
    name: str
    elements: list[DataElement]


class DescriptionResult(BaseModel):
    name: str
    data_type: str
    sample_values: list[str]
    ai_generated_description: str | None = None
    ai_rationale: str | None = None
    ai_confidence_score: float | None = Field(None, ge=0.0, le=1.0)
    skipped: bool = False


class DatasetDescriptionResult(BaseModel):
    dataset_name: str
    results: list[DescriptionResult]
