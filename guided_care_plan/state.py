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
    "daily_tasks_support",
    "medication_management",
    "caregiver_support",
    "falls_history",
    "cognition",
    "behavior_signals",
    "supervision_need",
    "living_situation",
    "partner_support",
    "home_safety",
    "veteran_benefits",
    "chronic_conditions",
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
    "Daily Life",
    "Health & Safety",
    "Context & Preferences",
    "Medical Check",
    "Recommendation",
]


def render_stepper(current_step: int) -> None:
    """Render a simple progress stepper for the Guided Care Plan."""

    total_steps = len(STEP_TITLES)
    if current_step < 0:
        current_step = 0
    if current_step > total_steps:
        current_step = total_steps

    progress_ratio = current_step / total_steps
    st.progress(progress_ratio)

    cols = st.columns(total_steps)
    for idx, (col, title) in enumerate(zip(cols, STEP_TITLES), start=1):
        with col:
            if idx <= current_step:
                col.markdown(f"**{idx}. {title}**")
            else:
                col.caption(f"{idx}. {title}")


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
