from __future__ import annotations
import streamlit as st
from gcp_core.engine import questions_for_section
from gcp_core.state import ensure_session, set_section_complete
from ui.gcp_form import render_section

ensure_session()

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Context & Preferences")

with st.form("gcp_context_prefs_form"):
    render_section("context_prefs", questions_for_section("context_prefs"))
    continue_clicked = st.form_submit_button("Continue", type="primary", width="stretch")
    if continue_clicked:
        set_section_complete("context")
        st.switch_page("app_pages/gcp_v2/gcp_recommendation_v2.py")

if st.button("◀ Back", type="secondary", width="stretch"):
    st.switch_page("app_pages/gcp_v2/gcp_health_safety_v2.py")

if st.button("Save & exit to Hub", type="secondary", width="stretch"):
    st.switch_page("app_pages/hub.py")
