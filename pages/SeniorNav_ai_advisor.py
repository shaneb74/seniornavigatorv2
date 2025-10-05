from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from pages.seniornav_util import ensure_aud, top_nav

st.set_page_config(layout="wide", page_title="AI Advisor")
inject_theme()
ensure_aud()
top_nav()
st.markdown("## AI Advisor")
st.caption("Describe your situation. The AI Advisor suggests ideas you can review with your human advisor.")
q = st.text_area("Tell us what's going on")
if st.button("Get suggestions", type="primary"):
    st.info("AI suggestions would appear here based on your inputs.")
