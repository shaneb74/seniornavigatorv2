from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
from pages.seniornav_util import ensure_aud, top_nav

st.set_page_config(layout="wide", page_title="Waiting Room")
inject_theme()
ensure_aud()
top_nav()
st.markdown("## One moment…")
st.caption("We’re preparing your session.")
if st.button("Back to Home", use_container_width=True):
    try: st.switch_page("pages/SeniorNav_home.py")
    except Exception: st.query_params["next"]="pages/SeniorNav_home.py"; st.rerun()
