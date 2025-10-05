from __future__ import annotations
import streamlit as st
from ui.theme import inject_theme
try:
    from cost_planner_v2.cp_nav import goto
except Exception:
    def goto(path:str):
        try: st.switch_page(path)
        except Exception:
            st.query_params["next"]=path; st.rerun()

st.set_page_config(layout="wide", page_title="GCP · Medicaid Off-Ramp")
inject_theme()

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Medicaid Path")
st.info("You indicated current Medicaid or state long-term care assistance.")

st.markdown("""
If you already qualify for Medicaid, we’ll guide you to resources and the **Plan for My Advisor** workflow tailored to Medicaid beneficiaries.
If you’re unsure, you can still explore private-pay options and verify later.
""")

c1,c2 = st.columns(2)
with c1:
    if st.button("◀ Back: Start", use_container_width=True):
        goto("pages/gcp_v2/gcp_landing_v2.py")
with c2:
    if st.button("Continue to PFMA ▶", use_container_width=True):
        goto("pages/pfma.py")
