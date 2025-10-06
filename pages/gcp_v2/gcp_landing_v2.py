from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from gcp_v2.schema import questions_for_section
from ui.gcp_form import render_section, nav_buttons, _state

st.set_page_config(layout="wide", page_title="Guided Care Plan · Start")
inject_theme()

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Guided Care Plan · Start")
st.caption("We’ll begin with financial eligibility, then daily life, health & safety, and preferences.")

# render financial section (Q0/Q1 with conditional logic)
financial_questions = questions_for_section("financial")
for question in financial_questions:
    if question["id"] == "medicaid_status":
        question["label"] = "Are you currently on Medicaid or receiving state long-term care assistance?"
        question["helper"] = (
            "Medicare is federal health insurance. Medicaid is a need-based program that can pay for long-term care. "
            "If you’re unsure, keep going—we’ll flag this to double-check later."
        )
        question["choices"] = [
            ("yes", "Yes"),
            ("no", "No"),
            ("unsure", "I'm not sure"),
        ]
    elif question["id"] == "funding_confidence":
        question["label"] = "How confident do you feel about paying for care?"
        question["choices"] = [
            ("no_worries", "No worries"),
            ("confident", "Confident"),
            ("unsure", "Unsure"),
            ("not_confident", "Not confident"),
        ]

render_section("financial", financial_questions)

data = _state()
if data.get("route") == "medicaid_offramp":
    st.info("It looks like Medicaid may be the right path. We’ll route you to that flow and keep your info handy.")
    nav_buttons("pages/hub.py", "pages/pfma.py")
else:
    nav_buttons("pages/hub.py", "pages/gcp_v2/gcp_daily_life_v2.py")
