"""Session helpers and metadata for the Guided Care Plan."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Tuple

import streamlit as st

from audiencing import ensure_audiencing_state

PACKAGE_ROOT = Path(__file__).resolve().parent

QUESTION_ORDER: List[str] = [
    "who_for",
    "living_now",
    "caregiver_support",
    "adl_help",
    "cognition",
    "behavior_risks",
    "falls",
    "med_mgmt",
    "home_safety",
    "supervision",
    "chronic",
    "preferences",
    "funding_confidence",
]


@lru_cache(maxsize=1)
def _load_labels() -> Dict[str, Dict[str, Dict[str, str]]]:
    labels_path = PACKAGE_ROOT / "labels.json"
    with labels_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def get_question_meta(question_id: str) -> Dict[str, object]:
    """Return metadata (label, helper text, options) for a question id."""

    data = _load_labels().get("questions", {})
    meta = data.get(question_id)
    if not meta:
        raise KeyError(f"Unknown Guided Care Plan question id: {question_id}")
    return meta


def ensure_gcp_session() -> Tuple[Dict[str, object], Dict[str, object]]:
    """Guarantee session storage for answers and evaluation output."""

    answers = st.session_state.setdefault("gcp_answers", {})
    gcp_result = st.session_state.setdefault(
        "gcp",
        {
            "recommended_setting": None,
            "care_intensity": None,
            "safety_flags": [],
            "chronic_conditions": [],
            "payment_context": None,
            "funding_confidence": None,
            "audiencing_snapshot": None,
            "DecisionTrace": None,
        },
    )
    return answers, gcp_result


STEP_TITLES = [
    "Daily Life & Support",
    "Health & Safety",
    "Context & Preferences",
    "Financial Confidence",
    "Recommendation",
]


def render_stepper(current_step: int) -> None:
    """Render a simple progress stepper for the Guided Care Plan."""

    total_steps = len(STEP_TITLES)
    current = max(0, min(current_step, total_steps))
    ratio = current / total_steps if total_steps else 0
    st.markdown(
        f"<div class='sn-gcp-stepper'><div class='sn-gcp-progress' style='width:{ratio * 100:.0f}%;'></div></div>",
        unsafe_allow_html=True,
    )

    steps_html = ["<div class='sn-gcp-steps'>"]
    for idx, title in enumerate(STEP_TITLES, start=1):
        cls = "sn-step-active" if idx == current_step else ""
        steps_html.append(f"<span class='{cls}'>{idx}. {title}</span>")
    steps_html.append("</div>")
    st.markdown("".join(steps_html), unsafe_allow_html=True)


def current_audiencing_snapshot() -> Dict[str, object]:
    """Return the latest audiencing snapshot, ensuring defaults."""

    snapshot = st.session_state.get("audiencing_snapshot")
    if snapshot:
        return snapshot
    state = ensure_audiencing_state()
    return {
        "entry": state.get("entry"),
        "qualifiers": state.get("qualifiers", {}).copy(),
        "route": state.get("route", {}).copy(),
    }
