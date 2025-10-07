from __future__ import annotations
import streamlit as st
from gcp_core.engine import questions_for_section
from gcp_core.state import ensure_session, set_section_complete
from ui.gcp_form import render_section

ensure_session()

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Health & Safety")

with st.form("gcp_health_safety_form"):
    render_section("health_safety", questions_for_section("health_safety"))
    continue_clicked = st.form_submit_button("Continue", type="primary", width="stretch")
    if continue_clicked:
        set_section_complete("safety")
        st.switch_page("app_pages/gcp_v2/gcp_context_prefs_v2.py")

if st.button("◀ Back", type="secondary", width="stretch"):
    st.switch_page("app_pages/gcp_v2/gcp_daily_life_v2.py")

if st.button("Save & exit to Hub", type="secondary", width="stretch"):
    st.switch_page("app_pages/hub.py")
