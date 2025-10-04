"""Lint checks for cost planner design assets."""
from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_cost_planner_copy_file_exists() -> None:
    copy_path = Path("copy/cost_planner_strings.json")
    assert copy_path.exists(), "Cost planner copy file missing"
    data = json.loads(copy_path.read_text())
    assert "app" in data and "mode_selection" in data, "Copy file missing expected sections"


def test_labels_include_medicaid_and_funding() -> None:
    labels_path = Path("guided_care_plan/labels.json")
    labels = json.loads(labels_path.read_text())
    questions = labels.get("questions", {})
    assert "medicaid_status" in questions, "medicaid_status question missing"
    assert "funding_confidence" in questions, "funding_confidence question missing"
