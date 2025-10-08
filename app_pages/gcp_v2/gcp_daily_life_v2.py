# Guided Care Plan · Daily Life
from __future__ import annotations

import streamlit as st

from gcp_core import ensure_session, get_answers, set_progress, set_resume_target
from ui.gcp_form import render_question

LIVING_CHOICES = [
    {"label": "At home independently", "value": "independent_home"},
    {"label": "At home with family support", "value": "family_home"},
    {"label": "Senior apartment / independent living", "value": "senior_apt"},
    {"label": "Assisted living or similar", "value": "assisted"},
]

ADL_CHOICES = [
    {"label": "Bathing", "value": "bathing"},
    {"label": "Dressing", "value": "dressing"},
    {"label": "Toileting", "value": "toileting"},
    {"label": "Walking / transfers", "value": "mobility"},
    {"label": "Medication reminders", "value": "medications"},
    {"label": "Meals / nutrition", "value": "meals"},
]

SUPPORT_CHOICES = [
    {"label": "Family provides most care", "value": "family"},
    {"label": "Hired in-home caregivers", "value": "paid"},
    {"label": "Mix of family and paid support", "value": "mixed"},
    {"label": "Currently unsupported / needs help", "value": "unsupported"},
]


def _progress_score(required_qids: list[str]) -> int:
    answers = get_answers()
    filled = sum(1 for qid in required_qids if answers.get(qid))
    return int(round((filled / max(len(required_qids), 1)) * 100))


def render() -> None:
    ensure_session()
    st.title("Daily Life & Support")

    with st.form("gcp_daily_life"):
        render_question("living_situation", "Where does the person live today?", "radio", choices=LIVING_CHOICES)
        render_question("adls_support", "Which daily activities need support?", "multiselect", choices=ADL_CHOICES)
        render_question("primary_support", "Who provides most support right now?", "radio", choices=SUPPORT_CHOICES)
        render_question("daily_notes", "Anything else about daily routines?", "textarea", help="Optional notes to share with advisors.")

        submitted = st.form_submit_button("Continue", type="primary", use_container_width=True)
        if submitted:
            set_progress("daily_life", 100)
            set_resume_target("app_pages/gcp_v2/gcp_health_safety_v2.py")
            st.switch_page("app_pages/gcp_v2/gcp_health_safety_v2.py")

    col_back, col_save = st.columns(2)
    with col_back:
        if st.button("◀ Back", type="secondary", use_container_width=True):
            set_resume_target("app_pages/gcp_v2/gcp_landing_v2.py")
            st.switch_page("app_pages/gcp_v2/gcp_landing_v2.py")
    with col_save:
        if st.button("Save & exit", type="secondary", use_container_width=True):
            score = max(40, min(80, _progress_score(["living_situation", "adls_support", "primary_support"])))
            set_progress("daily_life", score)
            set_resume_target("app_pages/gcp_v2/gcp_daily_life_v2.py")
            st.switch_page("app_pages/hub.py")


render()
