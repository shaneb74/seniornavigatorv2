from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from gcp_v2.schema import questions_for_section
from ui.gcp_form import render_section, nav_buttons

inject_theme()

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Context & Preferences")
render_section("context_prefs", questions_for_section("context_prefs"))
nav_buttons("pages/gcp_v2/gcp_health_safety_v2.py", "pages/gcp_v2/gcp_recommendation_v2.py")
