from __future__ import annotations

import csv


def load_glossary(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]
