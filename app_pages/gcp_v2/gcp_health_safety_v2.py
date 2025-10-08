# Guided Care Plan · Health & Safety
from __future__ import annotations

import streamlit as st

from gcp_core import ensure_session, get_answers, set_progress, set_resume_target
from ui.gcp_form import BEHAVIOR_CHOICES, COGNITION_QID, render_question

COGNITION_CHOICES = [
    {"label": "Sharp / no noticeable decline", "value": "intact"},
    {"label": "Mild forgetfulness or cueing needed", "value": "mild_decline"},
    {"label": "Moderate memory issues, needs prompts", "value": "moderate_decline"},
    {"label": "Advanced dementia / needs supervision", "value": "advanced_dementia"},
    {"label": "Severe memory loss / constant oversight", "value": "needs_supervision"},
]

FALL_HISTORY_CHOICES = [
    {"label": "No falls in the last year", "value": "none"},
    {"label": "One fall, no injury", "value": "single_no_injury"},
    {"label": "Multiple falls or injury", "value": "recurrent"},
]

MEDICAL_CHOICES = [
    {"label": "Stable health, routine needs", "value": "stable"},
    {"label": "Chronic conditions to monitor", "value": "chronic_monitor"},
    {"label": "Recent hospital stay or rehab", "value": "recent_rehab"},
]


def _progress_score(required_qids: list[str]) -> int:
    answers = get_answers()
    filled = sum(1 for qid in required_qids if answers.get(qid))
    return int(round((filled / max(len(required_qids), 1)) * 100))


def render() -> None:
    ensure_session()
    st.title("Health & Safety")

    with st.form("gcp_health_safety"):
        render_question(
            COGNITION_QID,
            "How would you describe cognition or memory today?",
            "radio",
            choices=COGNITION_CHOICES,
        )
        render_question(
            "behavior_risks",
            "Are you noticing any behaviors that need planning?",
            "multiselect",
            choices=BEHAVIOR_CHOICES,
            help="Only shown when cognition suggests higher risks.",
        )
        render_question(
            "fall_history",
            "Any history of falls in the last 12 months?",
            "radio",
            choices=FALL_HISTORY_CHOICES,
        )
        render_question(
            "medical_needs",
            "How complex are ongoing medical needs?",
            "radio",
            choices=MEDICAL_CHOICES,
        )
        render_question(
            "health_notes",
            "Any specific medical or safety notes?",
            "textarea",
            help="Optional for context when you talk with advisors.",
        )

        submitted = st.form_submit_button("Continue", type="primary", use_container_width=True)
        if submitted:
            set_progress("health_safety", 100)
            set_resume_target("app_pages/gcp_v2/gcp_context_prefs_v2.py")
            st.switch_page("app_pages/gcp_v2/gcp_context_prefs_v2.py")

    col_back, col_save = st.columns(2)
    with col_back:
        if st.button("◀ Back", type="secondary", use_container_width=True):
            set_resume_target("app_pages/gcp_v2/gcp_daily_life_v2.py")
            st.switch_page("app_pages/gcp_v2/gcp_daily_life_v2.py")
    with col_save:
        if st.button("Save & exit", type="secondary", use_container_width=True):
            score = max(40, min(80, _progress_score([COGNITION_QID, "fall_history", "medical_needs"])))
            set_progress("health_safety", score)
            set_resume_target("app_pages/gcp_v2/gcp_health_safety_v2.py")
            st.switch_page("app_pages/hub.py")


render()
