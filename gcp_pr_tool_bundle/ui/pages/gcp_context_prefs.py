import streamlit as st
from ._common_gcp import load_questions, show_single, show_multi, should_show
from guided_care_plan.state import get_answers

def page():
    st.title("Context & preferences")
    answers = get_answers()
    ids = {"social_isolation","geographic_access","chronic"}
    for q in load_questions():
        if q["id"] in ids:
            if q["type"]=="single": show_single(q, answers)
            else: show_multi(q, answers)
    st.page_link("ui/pages/gcp_recommendation.py", label="See recommendation →")
    st.page_link("ui/pages/gcp_health_safety.py", label="← Back")

if __name__ == "__main__":
    page()
