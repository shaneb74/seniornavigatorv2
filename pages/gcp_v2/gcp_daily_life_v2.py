from __future__ import annotations
import streamlit as st
st.set_page_config(layout="wide", page_title="GCP · Daily Life & Support")
from ui.theme import inject_theme
inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Daily Life & Support")
st.caption("ADLs/IADLs, current supports, caregiver load.")
adl = st.multiselect("Activities needing help", ["Bathing","Dressing","Toileting","Transfers","Feeding","Walking"])
iadl = st.multiselect("Instrumental needs", ["Meals","Med mgt","Finances","Transportation","Housekeeping","Shopping"])
support_hours = st.slider("Estimated weekly support hours", 0, 168, 10)
st.divider()
cols = st.columns(2)
with cols[0]:
    if st.button("◀ Back: Start", use_container_width=True):
        try: st.switch_page("pages/gcp_v2/gcp_landing_v2.py")
        except Exception:
            st.query_params["next"] = "pages/gcp_v2/gcp_landing_v2.py"; st.rerun()
with cols[1]:
    if st.button("Next: Health & Safety ▶", use_container_width=True):
        try: st.switch_page("pages/gcp_v2/gcp_health_safety_v2.py")
        except Exception:
            st.query_params["next"] = "pages/gcp_v2/gcp_health_safety_v2.py"; st.rerun()
