# Guided Care Plan · Recommendation
from __future__ import annotations

import streamlit as st

from gcp_core import (
    ensure_session,
    get_answers,
    get_medicaid_ack,
    get_medicaid_status,
    set_medicaid_ack,
    set_progress,
    set_resume_target,
)
from ui.gcp_form import BEHAVIOR_CHOICES

CRITICAL_BEHAVIORS = {"wandering", "aggression", "elopement", "exit_seeking"}
BEHAVIOR_LABELS = {choice["value"]: choice["label"] for choice in BEHAVIOR_CHOICES}


def _medicaid_notice(status: str) -> None:
    if status != "yes":
        return
    acknowledged = get_medicaid_ack()
    with st.container(border=True):
        st.subheader("Medicaid reminder")
        st.write(
            "Because you shared that the person has **Medicaid**, our paid advisor services are limited. "
            "You can still review this recommendation, save it, and explore Medicaid resources that may apply."
        )
        cols = st.columns([1, 1])
        with cols[0]:
            st.link_button("Medicaid resources", "https://www.medicaid.gov/")
        with cols[1]:
            if not acknowledged and st.button("Got it", type="primary"):
                set_medicaid_ack(True)
                st.experimental_rerun()


def _build_summary(answers: dict) -> list[str]:
    summary: list[str] = []
    living = answers.get("living_situation")
    if living:
        summary.append(f"Currently living: **{living.replace('_', ' ').title()}**")
    primary_support = answers.get("primary_support")
    if primary_support:
        summary.append(f"Main support today: **{primary_support.replace('_', ' ').title()}**")
    adls = answers.get("adls_support")
    if isinstance(adls, list) and adls:
        items = ", ".join(item.replace('_', ' ') for item in adls)
        summary.append(f"Needs help with: **{items}**")
    cognition = answers.get("cognition_level")
    if cognition:
        summary.append(f"Cognition level: **{cognition.replace('_', ' ').title()}**")
    priorities = answers.get("top_priorities")
    if isinstance(priorities, list) and priorities:
        items = ", ".join(item.replace('_', ' ') for item in priorities)
        summary.append(f"Priorities: **{items}**")
    preferred = answers.get("preferred_setting")
    if preferred:
        summary.append(f"Leaning toward: **{preferred.replace('_', ' ').title()}**")
    return summary


def _safety_notes(behavior_tokens: list[str]) -> list[str]:
    notes: list[str] = []
    critical = [token for token in behavior_tokens if token in CRITICAL_BEHAVIORS]
    if critical:
        labels = ", ".join(BEHAVIOR_LABELS.get(token, token) for token in critical)
        notes.append(f"**Safety checkpoint:** Watch for {labels}. Consider supervised settings or secure memory care.")
    return notes


def render() -> None:
    ensure_session()
    answers = get_answers()
    medicaid_status = get_medicaid_status(answers)

    st.title("Recommendation")
    st.write("Here’s what stood out from your Guided Care Plan responses.")

    _medicaid_notice(medicaid_status)

    summary_points = _build_summary(answers)
    if summary_points:
        st.subheader("What we heard")
        for point in summary_points:
            st.markdown(f"- {point}")

    behaviors = answers.get("behavior_risks") or []
    if isinstance(behaviors, list):
        safety = _safety_notes(behaviors)
        if safety:
            st.subheader("Safety checkpoints")
            for note in safety:
                st.markdown(f"- {note}")

    timeline = answers.get("timeline_goal")
    if timeline:
        st.markdown(f"**Timeline focus:** {timeline}")

    advisor_questions = answers.get("advisor_questions")
    if advisor_questions:
        with st.container(border=True):
            st.subheader("Questions for your advisor")
            st.write(advisor_questions)

    button_cols = st.columns(2 if medicaid_status != "yes" else 1)
    if medicaid_status != "yes":
        with button_cols[0]:
            if st.button("Continue to Cost Planner", type="primary", use_container_width=True):
                st.switch_page("app_pages/cost_planner_v2/cost_planner_landing_v2.py")
        with button_cols[1]:
            if st.button("Return to Care Hub", type="secondary", use_container_width=True):
                st.switch_page("app_pages/hub.py")
    else:
        with button_cols[0]:
            if st.button("Return to Care Hub", type="secondary", use_container_width=True):
                st.switch_page("app_pages/hub.py")

    set_progress("context_prefs", 100)
    set_progress("done", 100)
    set_resume_target("app_pages/gcp_v2/gcp_recommendation_v2.py")


render()
