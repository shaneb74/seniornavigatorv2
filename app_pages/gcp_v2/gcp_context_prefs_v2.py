# Guided Care Plan · Context & Preferences
from __future__ import annotations

import streamlit as st

from gcp_core import ensure_session, get_answers, set_progress, set_resume_target
from ui.gcp_form import render_question

SETTING_CHOICES = [
    {"label": "Stay at home with support", "value": "stay_home"},
    {"label": "Move to independent living", "value": "independent"},
    {"label": "Assisted living or memory care", "value": "assisted_memory"},
    {"label": "Still evaluating options", "value": "unsure"},
]

PRIORITY_CHOICES = [
    {"label": "Safety and supervision", "value": "safety"},
    {"label": "Social connection", "value": "social"},
    {"label": "Wellness & rehab", "value": "wellness"},
    {"label": "Budget / affordability", "value": "budget"},
    {"label": "Location / near family", "value": "location"},
]

FAMILY_CHOICES = [
    {"label": "We’re aligned and ready to act", "value": "aligned"},
    {"label": "We’re discussing options", "value": "discussing"},
    {"label": "We need help getting on the same page", "value": "need_alignment"},
]


def _progress_score(required_qids: list[str]) -> int:
    answers = get_answers()
    filled = sum(1 for qid in required_qids if answers.get(qid))
    return int(round((filled / max(len(required_qids), 1)) * 100))


def render() -> None:
    ensure_session()
    st.title("Context & Preferences")
    st.write("Share what matters most so recommendations feel personal.")

    with st.form("gcp_context_prefs"):
        render_question(
            "preferred_setting",
            "Which setting feels like the next natural step?",
            "radio",
            choices=SETTING_CHOICES,
        )
        render_question(
            "top_priorities",
            "What are your top priorities right now?",
            "multiselect",
            choices=PRIORITY_CHOICES,
        )
        render_question(
            "family_alignment",
            "How aligned is the family or care team?",
            "radio",
            choices=FAMILY_CHOICES,
        )
        render_question(
            "timeline_goal",
            "Is there a target timeframe or milestone?",
            "text",
            help="Example: ‘Find a community before winter.’",
        )
        render_question(
            "advisor_questions",
            "Questions you want to ask a senior advisor?",
            "textarea",
            help="Optional — helps us prepare next steps for you.",
        )

        submitted = st.form_submit_button("See recommendation", type="primary", use_container_width=True)
        if submitted:
            set_progress("context_prefs", 100)
            set_resume_target("app_pages/gcp_v2/gcp_recommendation_v2.py")
            st.switch_page("app_pages/gcp_v2/gcp_recommendation_v2.py")

    col_back, col_save = st.columns(2)
    with col_back:
        if st.button("◀ Back", type="secondary", use_container_width=True):
            set_resume_target("app_pages/gcp_v2/gcp_health_safety_v2.py")
            st.switch_page("app_pages/gcp_v2/gcp_health_safety_v2.py")
    with col_save:
        if st.button("Save & exit", type="secondary", use_container_width=True):
            score = max(40, min(80, _progress_score(["preferred_setting", "top_priorities", "family_alignment"])))
            set_progress("context_prefs", score)
            set_resume_target("app_pages/gcp_v2/gcp_context_prefs_v2.py")
            st.switch_page("app_pages/hub.py")


render()
