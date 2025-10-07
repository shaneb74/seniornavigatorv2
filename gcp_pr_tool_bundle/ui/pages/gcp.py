import streamlit as st
from ._common_gcp import load_questions, show_single, show_multi, should_show
from guided_care_plan.state import get_answers

def page():
    st.title("Guided Care Plan — Entry")
    answers = get_answers()
    qs = load_questions()

    # Q0 first
    q0 = next(q for q in qs if q["id"]=="medicaid_status")
    show_single(q0, answers)
    if answers.get("medicaid_status") == "unsure":
        st.info("Medicare is federal health insurance; Medicaid is a need-based program that can pay for long-term care. If you’re unsure, continue—we’ll flag it to verify later.")

    # Q1 only if Q0 != yes
    if answers.get("medicaid_status") != "yes":
        q1 = next(q for q in qs if q["id"]=="funding_confidence")
        show_single(q1, answers)

    st.page_link("ui/pages/gcp_daily_life.py", label="Continue →")

if __name__ == "__main__":
    page()
