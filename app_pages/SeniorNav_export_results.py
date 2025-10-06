from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from pages.seniornav_util import top_nav, safe_switch

st.set_page_config(layout="wide", page_title="Export Details")
inject_theme()
top_nav()

st.markdown("## Export Results")
st.subheader("Here's what you've built for your loved one.")
st.write("Download your plans below — secure and ready.")
st.info("Exports are protected — requires login. (Design note: Auth gate goes here.)")

ctx = st.session_state.setdefault("care_context", {
    "gcp_answers": {},
    "decision_trace": [],
    "planning_mode": "exploring",
    "care_flags": {},
})
authed = st.session_state.get("is_authenticated", False)

c1, c2 = st.columns(2)
with c1:
    st.markdown("#### Export Care Plan")
    st.caption("Your guided care plan: Home care + VA benefits + hearing aids.")
    st.button("Export Care Plan", type="primary", disabled=not authed, help=None if authed else "Login required", use_container_width=True)
with c2:
    st.markdown("#### Export Cost Summary")
    st.caption("Your budget breakdown: $1,500/month for your loved one's care.")
    st.button("Export Cost Summary", type="primary", disabled=not authed, help=None if authed else "Login required", use_container_width=True)

st.divider()
if st.button("Back to Hub", use_container_width=True):
    safe_switch("pages/guided_care_hub.py")
