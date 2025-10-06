from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from ui.gcp_form import _state, nav_buttons

st.set_page_config(layout="wide", page_title="GCP · Recommendation")
inject_theme()

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Your Draft Recommendation")
data = _state()
ans = data.get("answers", {})
ctx = data.get("payment_context", "private")

if ctx == "medicaid":
    st.warning("Based on your answer, Medicaid may be your best next step. We’ll connect you to the right off-ramp and keep your info for PFMA.")
    nav_buttons("pages/gcp_v2/gcp_context_prefs_v2.py", "pages/pfma.py")
else:
    st.markdown("### Snapshot")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Payment context:** Private")
        st.markdown(f"**Funding confidence:** {ans.get('funding_confidence','(not set)')}")
        st.markdown(f"**Who for:** {ans.get('who_for','(not set)')}")
        st.markdown(f"**Current living:** {ans.get('living_now','(not set)')}")
    with col2:
        st.markdown(f"**Cognition:** {ans.get('cognition','(not set)')}")
        st.markdown(f"**Falls:** {ans.get('falls','(not set)')}")
        st.markdown(f"**Med mgmt:** {ans.get('med_mgmt','(not set)')}")
    st.info("This is a draft. Your advisor can refine it with you, then export via PFMA.")
    nav_buttons("pages/gcp_v2/gcp_context_prefs_v2.py", "pages/pfma.py")
