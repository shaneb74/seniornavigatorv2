from __future__ import annotations
import streamlit as st
st.set_page_config(layout="wide", page_title="GCP · Context & Preferences")
from ui.theme import inject_theme
inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Context & Preferences")
st.caption("Living situation, budget comfort, location, culture, routines, pets.")
living = st.selectbox("Current living situation", ["Own home","Rent","With family","Facility"])
budget = st.select_slider("Budget comfort per month (rough)", options=["<$2k","$2–4k","$4–6k","$6–8k","$8k+"])
location = st.text_input("Preferred location(s)")
notes = st.text_area("Other important preferences")
st.divider()
cols = st.columns(2)
with cols[0]:
    if st.button("◀ Back: Health & Safety", use_container_width=True):
        try: st.switch_page("pages/gcp_v2/gcp_health_safety_v2.py")
        except Exception:
            st.query_params["next"] = "pages/gcp_v2/gcp_health_safety_v2.py"; st.rerun()
with cols[1]:
    if st.button("Next: Recommendation ▶", use_container_width=True):
        try: st.switch_page("pages/gcp_v2/gcp_recommendation_v2.py")
        except Exception:
            st.query_params["next"] = "pages/gcp_v2/gcp_recommendation_v2.py"; st.rerun()
