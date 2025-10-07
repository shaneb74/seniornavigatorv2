from __future__ import annotations
import streamlit as st
from app_pages.seniornav_util import top_nav, safe_switch
top_nav()

st.markdown("## My Documents")
st.subheader("Keep all of your loved one's records here.")
st.write("Safe storage for your care plans and more.")

st.session_state.setdefault("care_context", {
    "gcp_answers": {},
    "decision_trace": [],
    "planning_mode": "exploring",
    "care_flags": {},
})

g1, g2 = st.columns(2)

with g1:
    st.markdown("#### Care Plan")
    st.caption("your loved one's guided care plan: Home care + VA benefits.")
    c = st.columns([1,1])
    with c[0]:
        st.button("View", type="primary", width="stretch", key="docs_care_view")
    with c[1]:
        st.button("Download", width="stretch", key="docs_care_download")

with g2:
    st.markdown("#### Cost Summary")
    st.caption("your loved one's budget: $1,500/month breakdown.")
    c = st.columns([1,1])
    with c[0]:
        st.button("View", type="primary", width="stretch", key="docs_cost_view")
    with c[1]:
        st.button("Download", width="stretch", key="docs_cost_download")

st.divider()
st.markdown("#### Upload Your Documents")
st.caption("Add insurance forms, med lists, or notes for your loved one.")
st.button("Upload File", type="primary", width="stretch", key="docs_upload_file")

st.divider()
if st.button("Back to Hub", width="stretch"):
    safe_switch("pages/guided_care_hub.py")
