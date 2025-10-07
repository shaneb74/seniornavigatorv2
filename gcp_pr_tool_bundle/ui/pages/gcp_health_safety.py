import streamlit as st
from ._common_gcp import load_questions, show_single, show_multi, should_show
from guided_care_plan.state import get_answers

def page():
    st.title("Health & safety")
    answers = get_answers()
    ids = {"cognition","behavior_risks","falls","med_mgmt","mobility","supervision","home_safety"}
    for q in load_questions():
        if q["id"] in ids and should_show(q, answers):
            if q["type"]=="single": show_single(q, answers)
            else: show_multi(q, answers)
    st.page_link("ui/pages/gcp_context_prefs.py", label="Continue →")
    st.page_link("ui/pages/gcp_daily_life.py", label="← Back")

if __name__ == "__main__":
    page()
