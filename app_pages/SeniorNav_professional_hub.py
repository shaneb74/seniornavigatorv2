from __future__ import annotations
import streamlit as st
from app_pages.seniornav_util import top_nav, safe_switch
top_nav()
st.markdown("## Professional Care Planning — Coming Soon")
st.caption("Build and manage care plans for your clients in one click.")
if st.button("Back to Home", width="stretch"):
    try: st.switch_page("pages/SeniorNav_home.py")
    except Exception: st.query_params["next"]="pages/SeniorNav_home.py"; st.rerun()
