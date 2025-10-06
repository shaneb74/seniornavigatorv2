from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from gcp_v2.schema import questions_for_section
from ui.gcp_form import render_section, nav_buttons

st.set_page_config(layout="wide", page_title="GCP · Context & Preferences")
inject_theme()

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Context & Preferences")

context_questions = questions_for_section("context_prefs")
for question in context_questions:
    if question["id"] == "chronic":
        question["label"] = "Any chronic conditions we should plan for?"
        question["helper"] = "Select all that apply."
        question["choices"] = [
            ("diabetes", "Diabetes"),
            ("parkinson", "Parkinson’s"),
            ("stroke", "Stroke"),
            ("copd", "COPD"),
            ("chf", "Heart failure (CHF)"),
            ("other", "Other condition"),
            ("none", "No chronic conditions"),
        ]
    elif question["id"] == "preferences":
        question["label"] = "Any strong care preferences?"
        question["helper"] = "Select all that apply."
        question["choices"] = [
            ("stay_home", "Stay at home"),
            ("be_near_family", "Be near family"),
            ("structured_care", "Structured community"),
            ("private_room", "Private room"),
            ("none", "No strong preferences"),
        ]

render_section("context_prefs", context_questions)
nav_buttons("pages/gcp_v2/gcp_health_safety_v2.py", "pages/gcp_v2/gcp_recommendation_v2.py")
