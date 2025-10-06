from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from gcp_v2.schema import questions_for_section
from ui.gcp_form import render_section, nav_buttons

st.set_page_config(layout="wide", page_title="GCP · Daily Life & Support")
inject_theme()

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Daily Life & Support")

daily_life_questions = questions_for_section("daily_life_support")
for question in daily_life_questions:
    if question["id"] == "who_for":
        question["label"] = "Who are you planning for?"
        question["choices"] = [
            ("self", "Myself"),
            ("parent", "Parent"),
            ("spouse", "Spouse or partner"),
            ("other", "Someone else"),
        ]
    elif question["id"] == "living_now":
        question["label"] = "Where do they live today?"
        question["choices"] = [
            ("own_home", "In their own home"),
            ("with_family", "With family"),
            ("independent", "Independent/retirement community"),
            ("assisted", "Assisted living"),
            ("memory", "Memory care"),
            ("skilled", "Skilled nursing"),
        ]
    elif question["id"] == "caregiver_support":
        question["label"] = "How much caregiver support is available?"
        question["choices"] = [
            ("none", "No regular help"),
            ("few_days_week", "Help a few days a week"),
            ("most_days", "Help most days"),
            ("24_7", "Help around the clock"),
        ]
    elif question["id"] == "adl_help":
        question["label"] = "How many daily activities need hands-on help?"
        question["choices"] = [
            ("0-1", "0–1 activities"),
            ("2-3", "2–3 activities"),
            ("4-5", "4–5 activities"),
            ("6+", "6 or more activities"),
        ]

render_section("daily_life_support", daily_life_questions)
nav_buttons("pages/gcp_v2/gcp_landing_v2.py", "pages/gcp_v2/gcp_health_safety_v2.py")
