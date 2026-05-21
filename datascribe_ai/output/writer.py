from __future__ import annotations

import csv
import os

from models.schemas import DatasetDescriptionResult


def write_csv(result: DatasetDescriptionResult, output_dir: str = ".") -> str:
    filename = f"{result.dataset_name.lower().replace(' ', '_')}.csv"
    filepath = os.path.join(output_dir, filename)

    os.makedirs(output_dir, exist_ok=True)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["name", "type", "sample_value", "ai_generated_description", "ai_rationale", "ai_confidence_score"]
        )
        for r in result.results:
            writer.writerow(
                [
                    r.name,
                    r.data_type,
                    ", ".join(r.sample_values) if r.sample_values else "",
                    r.ai_generated_description or "",
                    r.ai_rationale or "",
                    r.ai_confidence_score if r.ai_confidence_score is not None else "",
                ]
            )

    return filepath
