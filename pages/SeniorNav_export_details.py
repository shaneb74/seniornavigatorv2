from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from pages.seniornav_util import top_nav

st.set_page_config(layout="wide", page_title="Export Details")
inject_theme()
top_nav()
st.markdown("## Export Details")
st.caption("Export your care plan and related information.")
if st.button("Export PDF", type="primary"):
    st.success("Export started.")
