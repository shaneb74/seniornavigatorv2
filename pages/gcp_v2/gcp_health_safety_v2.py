from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from gcp_v2.schema import questions_for_section
from ui.gcp_form import render_section, nav_buttons

st.set_page_config(layout="wide", page_title="GCP · Health & Safety")
inject_theme()

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Health & Safety")

health_questions = questions_for_section("health_safety")
for question in health_questions:
    if question["id"] == "cognition":
        question["label"] = "How is memory and thinking?"
        question["choices"] = [
            ("normal", "Sharp and consistent"),
            ("mild", "Mild changes"),
            ("moderate", "Noticeable confusion"),
            ("severe", "Severe memory loss"),
        ]
    elif question["id"] == "behavior_risks":
        question["label"] = "Any wandering or unsafe behaviors?"
        question["helper"] = "Select all that apply."
        question["choices"] = [
            ("wandering", "Wandering"),
            ("agitation", "Agitation or aggression"),
            ("exit_seeking", "Tries to leave unsafely"),
            ("none", "None of these"),
        ]
    elif question["id"] == "falls":
        question["label"] = "Any falls in the last 12 months?"
        question["choices"] = [
            ("none", "No falls"),
            ("one", "One fall"),
            ("recurrent", "More than one fall"),
        ]
    elif question["id"] == "med_mgmt":
        question["label"] = "How complex are medications to manage?"
        question["choices"] = [
            ("simple", "Simple routine"),
            ("several", "Several medications"),
            ("complex", "Complex schedule or frequent changes"),
        ]
    elif question["id"] == "home_safety":
        question["label"] = "Is the home setup safe (stairs/bath/etc.)?"
        question["choices"] = [
            ("safe", "Safe setup"),
            ("some_risks", "Some safety risks"),
            ("unsafe", "Needs major safety support"),
        ]
    elif question["id"] == "supervision":
        question["label"] = "Do they have the supervision they need at home?"
        question["choices"] = [
            ("always", "Always covered"),
            ("sometimes", "Covered most of the time"),
            ("rarely", "Covered occasionally"),
            ("never", "Rarely or never covered"),
        ]

render_section("health_safety", health_questions)
nav_buttons("pages/gcp_v2/gcp_daily_life_v2.py", "pages/gcp_v2/gcp_context_prefs_v2.py")
