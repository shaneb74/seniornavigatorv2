import streamlit as st
from ._common_gcp import load_questions, show_single, show_multi, should_show
from guided_care_plan.state import get_answers

def page():
    st.title("Daily life & support")
    answers = get_answers()
    ids = {"adl_help","caregiver_support"}
    for q in load_questions():
        if q["id"] in ids:
            show_single(q, answers)
    st.page_link("ui/pages/gcp_health_safety.py", label="Continue →")
    st.page_link("ui/pages/gcp.py", label="← Back")

if __name__ == "__main__":
    page()
