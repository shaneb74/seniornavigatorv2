from __future__ import annotations
import streamlit as st
st.set_page_config(layout="wide", page_title="GCP · Health & Safety")
from ui.theme import inject_theme
inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Health & Safety")
st.caption("Conditions, risks, supervision, fall history, wandering, medication complexity.")
falls = st.selectbox("Falls in last 12 months?", ["No", "Yes, 1–2", "Yes, 3+"])
supervision = st.select_slider("Supervision need", options=["None","Intermittent","Frequent","24/7"])
risks = st.multiselect("Risks observed", ["Wandering","Elopement","Aggression","Weight loss","Medication errors"])
st.divider()
cols = st.columns(2)
with cols[0]:
    if st.button("◀ Back: Daily Life", use_container_width=True):
        try: st.switch_page("pages/gcp_v2/gcp_daily_life_v2.py")
        except Exception:
            st.query_params["next"] = "pages/gcp_v2/gcp_daily_life_v2.py"; st.rerun()
with cols[1]:
    if st.button("Next: Context & Preferences ▶", use_container_width=True):
        try: st.switch_page("pages/gcp_v2/gcp_context_prefs_v2.py")
        except Exception:
            st.query_params["next"] = "pages/gcp_v2/gcp_context_prefs_v2.py"; st.rerun()
