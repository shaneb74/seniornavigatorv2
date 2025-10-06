from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from pages.seniornav_util import top_nav

st.set_page_config(layout="wide", page_title="Professional Hub")
inject_theme()
top_nav()
st.markdown("## Professional Care Planning — Coming Soon")
st.caption("Build and manage care plans for your clients in one click.")
if st.button("Back to Home", use_container_width=True):
    try: st.switch_page("pages/SeniorNav_home.py")
    except Exception: st.query_params["next"]="pages/SeniorNav_home.py"; st.rerun()
