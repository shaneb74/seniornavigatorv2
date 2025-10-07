from __future__ import annotations
import streamlit as st
from app_pages.seniornav_util import top_nav, safe_switch
top_nav()
st.markdown("## Export Details")
st.caption("Export your care plan and related information.")
if st.button("Export PDF", type="primary"):
    st.success("Export started.")
