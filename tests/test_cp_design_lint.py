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


def test_labels_include_expected_gcp_questions() -> None:
    labels_path = Path("guided_care_plan/labels.json")
    labels = json.loads(labels_path.read_text())
    questions = labels.get("questions", {})
    expected = {
        "medicaid_status": ["yes", "no", "unsure"],
        "funding_confidence": ["no_worries", "confident", "unsure", "not_confident"],
        "who_for": ["self", "parent", "spouse", "other"],
        "living_now": ["own_home", "with_family", "independent", "assisted", "memory", "skilled"],
        "caregiver_support": ["none", "few_days_week", "most_days", "24_7"],
        "adl_help": ["0-1", "2-3", "4-5", "6+"],
        "cognition": ["normal", "mild", "moderate", "severe"],
        "behavior_risks": ["wandering", "agitation", "exit_seeking", "none"],
        "falls": ["none", "one", "recurrent"],
        "med_mgmt": ["simple", "several", "complex"],
        "home_safety": ["safe", "some_risks", "unsafe"],
        "supervision": ["always", "sometimes", "rarely", "never"],
        "chronic": ["diabetes", "parkinson", "stroke", "copd", "chf", "other", "none"],
        "preferences": ["stay_home", "be_near_family", "structured_care", "private_room", "none"],
    }

    assert set(questions.keys()) == set(expected.keys()), "Labels must include the v1.2.0 question set"

    for question_id, expected_values in expected.items():
        meta = questions.get(question_id)
        assert meta, f"Missing labels for {question_id}"
        options = meta.get("options", [])
        if options and isinstance(options[0], dict):
            values = [opt.get("value") for opt in options]
        else:
            values = list(options)
        assert values == expected_values, f"Options for {question_id} do not match expected"
