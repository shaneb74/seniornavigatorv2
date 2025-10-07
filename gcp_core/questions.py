from __future__ import annotations
import csv
from pathlib import Path
from typing import Dict, Iterable, Sequence, Tuple

_ASSETS = Path(__file__).parent / "assets"

BEHAVIOR_RISKS_QID = "behavior_risks"
BEHAVIOR_RISKS_LABEL = "Any wandering or unsafe behaviors? (check all that apply)"
BEHAVIOR_RISKS_OPTIONS: Sequence[Tuple[str, str]] = (
    ("wandering", "Wandering"),
    ("aggression", "Aggression"),
    ("elopement", "Elopement (trying to leave)"),
    ("exit_seeking", "Exit-seeking"),
    ("confusion", "Confusion or disorientation"),
    ("sundowning", "Sundowning (agitation, especially at night)"),
    ("repetitive_questioning", "Repetitive questioning"),
    ("poor_judgment", "Poor judgment (making unsafe decisions)"),
    ("hoarding", "Hoarding (collecting or hiding items excessively)"),
    ("sleep_disturbances", "Sleep disturbances (irregular sleep or insomnia)"),
)
BEHAVIOR_RISKS_LABEL_BY_TOKEN: Dict[str, str] = {token: label for token, label in BEHAVIOR_RISKS_OPTIONS}
_BEHAVIOR_RISKS_CONDITIONAL = "SHOW when cognition in {'severe'}"

COGNITION_SEVERE_TOKENS = {
    "severe",
    "severe_decline",
    "significant_decline",
    "diagnosed_dementia",
    "alzheimers_dementia",
    "alzheimers",
    "dementia",
    "advanced_impairment",
}


def _behavior_rows(template: Dict[str, str]) -> Iterable[Dict[str, str]]:
    base = {
        **template,
        "id": BEHAVIOR_RISKS_QID,
        "label": BEHAVIOR_RISKS_LABEL,
        "type": "multi",
        "conditional_show": template.get("conditional_show") or _BEHAVIOR_RISKS_CONDITIONAL,
    }
    base.pop("choice_id", None)
    base.pop("choice_label", None)
    for token, label in BEHAVIOR_RISKS_OPTIONS:
        yield {
            **base,
            "choice_id": token,
            "choice_label": label,
        }


def load_questions():
    path = _ASSETS / "questions.csv"
    rows = []
    behavior_template: Dict[str, str] | None = None
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("id") == BEHAVIOR_RISKS_QID:
                behavior_template = behavior_template or row
                continue
            rows.append(row)

    if behavior_template is None:
        behavior_template = {
            "id": BEHAVIOR_RISKS_QID,
            "label": BEHAVIOR_RISKS_LABEL,
            "type": "multi",
            "choice_id": "",
            "choice_label": "",
            "conditional_show": _BEHAVIOR_RISKS_CONDITIONAL,
        }

    rows.extend(_behavior_rows(behavior_template))
    return rows
