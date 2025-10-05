from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from gcp_v2.schema import questions_for_section
from ui.gcp_form import render_section, nav_buttons

st.set_page_config(layout="wide", page_title="GCP · Health & Safety")
inject_theme()

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Health & Safety")
render_section("health_safety", questions_for_section("health_safety"))
nav_buttons("pages/gcp_v2/gcp_daily_life_v2.py", "pages/gcp_v2/gcp_context_prefs_v2.py")
