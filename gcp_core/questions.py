from __future__ import annotations
from pathlib import Path
import csv

_ASSETS = Path(__file__).parent / "assets"


def load_questions():
    path = _ASSETS / "questions.csv"
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows.extend(reader)
    return rows
