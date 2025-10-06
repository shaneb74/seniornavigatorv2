from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from app_pages.seniornav_util import top_nav, safe_switch

st.set_page_config(layout="wide", page_title="My Account")
inject_theme()
top_nav()

st.markdown("## My Account")
st.subheader("Your profile & access")
st.write("Manage your details and resources for your loved one.")

ctx = st.session_state.setdefault("care_context", {
    "gcp_answers": {},
    "decision_trace": [],
    "planning_mode": "exploring",
    "care_flags": {},
})

grid = st.columns(2)

with grid[0]:
    st.markdown("#### Edit Info")
    st.caption("Update your name, email, or phone number.")
    st.button("Edit Details", type="primary", use_container_width=True)

with grid[1]:
    st.markdown("#### My Documents")
    st.caption("View and manage your loved one's stored documents.")
    if st.button("Go to Documents", type="primary", use_container_width=True):
        safe_switch("pages/SeniorNav_my_documents.py")

with grid[0]:
    st.markdown("#### Export Results")
    st.caption("Download your care plan and cost summary.")
    if st.button("Export Now", type="primary", use_container_width=True):
        safe_switch("pages/SeniorNav_export_results.py")

with grid[1]:
    st.markdown("#### Change Password")
    st.caption("Update your account password securely.")
    st.button("Change Password", type="primary", use_container_width=True)

st.divider()
logout_cols = st.columns([1,1,1])
with logout_cols[1]:
    st.button("Log Out", type="primary", use_container_width=True)

st.divider()
if st.button("Back to Hub", use_container_width=True):
    safe_switch("pages/guided_care_hub.py")
