from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from gcp_v2.schema import questions_for_section
from ui.gcp_form import render_section, nav_buttons, _state

inject_theme()

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Guided Care Plan · Start")
st.caption("We’ll begin with financial eligibility, then daily life, health & safety, and preferences.")

# render financial section (Q0/Q1 with conditional logic)
render_section("financial", questions_for_section("financial"))

data = _state()
if data.get("route") == "medicaid_offramp":
    st.info("It looks like Medicaid may be the right path. We’ll route you to that flow and keep your info handy.")
    nav_buttons("pages/hub.py", "pages/pfma.py")
else:
    nav_buttons("pages/hub.py", "pages/gcp_v2/gcp_daily_life_v2.py")
