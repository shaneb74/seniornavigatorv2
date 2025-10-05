from __future__ import annotations
import streamlit as st
st.set_page_config(layout="wide", page_title="Guided Care Plan · Start")
from ui.theme import inject_theme
inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Guided Care Plan · Start")
st.caption("Answer a few sections to understand needs, safety, context and get a tailored recommendation.")
c1, c2 = st.columns([1,1], gap="large")
with c1:
    st.markdown("### What to expect")
    st.markdown("- Daily life & support\n- Health & safety\n- Context & preferences\n- Final recommendation")
with c2:
    st.markdown("### Tips")
    st.markdown("- Answer honestly; you can always revise\n- Unsure? Use your best guess")
st.divider()
if st.button("Begin · Daily Life & Support ➜", use_container_width=True):
    try:
        st.switch_page("pages/gcp_v2/gcp_daily_life_v2.py")
    except Exception:
        st.query_params["next"] = "pages/gcp_v2/gcp_daily_life_v2.py"
        st.rerun()
