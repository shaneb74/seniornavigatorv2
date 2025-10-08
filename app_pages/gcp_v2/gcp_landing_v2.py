# Guided Care Plan · Landing
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
from ui.gcp_form import render_question

MEDICAID_CHOICES = [
    {"label": "Yes", "value": "yes"},
    {"label": "No", "value": "no"},
    {"label": "Not sure", "value": "unsure"},
]

FUNDING_CHOICES = [
    {"label": "Confident about funding without Medicaid", "value": "confident"},
    {"label": "Need guidance on paying for care", "value": "needs_help"},
    {"label": "Still deciding", "value": "deciding"},
]


def _medicaid_notice(status: str, acknowledged: bool) -> None:
    if status not in {"yes", "unsure"} or acknowledged:
        return
    with st.container(border=True):
        st.subheader("About Medicaid")
        st.write(
            "We provide limited services for families using **Medicaid** or state long-term care assistance. "
            "You’re welcome to continue the Guided Care Plan to receive a personalized recommendation. "
            "You can also explore Medicaid resources to understand coverage and next steps."
        )
        col_left, col_right = st.columns([1, 1])
        with col_left:
            st.link_button("Learn more about Medicaid", "https://www.medicaid.gov/")
            st.caption("Opens in a new tab.")
        with col_right:
            if st.button("I understand — continue", type="primary"):
                set_medicaid_ack(True)
                st.experimental_rerun()


def _landing_progress_ready(status: str, acknowledged: bool, answers: dict) -> bool:
    if status == "no":
        return bool(answers.get("funding_confidence"))
    if status in {"yes", "unsure"}:
        return acknowledged
    return False


def render() -> None:
    ensure_session()
    answers = get_answers()

    st.title("Guided Care Plan")
    st.write("Let’s begin with funding basics, then we’ll cover daily life, health & safety, and preferences.")

    render_question(
        "medicaid_status",
        "Does the person currently have Medicaid coverage?",
        "radio",
        choices=MEDICAID_CHOICES,
    )

    medicaid_status = get_medicaid_status(answers)
    acknowledged = get_medicaid_ack()

    if medicaid_status not in {"yes", "unsure"} and acknowledged:
        set_medicaid_ack(False)
        acknowledged = False

    if medicaid_status == "no":
        render_question(
            "funding_confidence",
            "How confident are you about covering care without Medicaid?",
            "radio",
            choices=FUNDING_CHOICES,
        )

    _medicaid_notice(medicaid_status, acknowledged)

    ready_to_continue = _landing_progress_ready(medicaid_status, acknowledged, answers)
    if not ready_to_continue:
        if medicaid_status == "no":
            st.caption("Select your Medicaid status and share how confident you feel about non-Medicaid funding to continue.")
        elif medicaid_status in {"yes", "unsure"}:
            st.caption("Please acknowledge the Medicaid notice above to keep going.")
        else:
            st.caption("Let us know about Medicaid coverage to continue.")

    col_continue, col_save = st.columns([3, 1])
    with col_continue:
        if st.button("Continue", type="primary", use_container_width=True, disabled=not ready_to_continue):
            set_progress("landing", 100)
            set_resume_target("app_pages/gcp_v2/gcp_daily_life_v2.py")
            st.switch_page("app_pages/gcp_v2/gcp_daily_life_v2.py")
    with col_save:
        if st.button("Save & exit", type="secondary", use_container_width=True):
            set_progress("landing", max(40, int(ready_to_continue) * 60))
            set_resume_target("app_pages/gcp_v2/gcp_landing_v2.py")
            st.switch_page("app_pages/hub.py")


render()
