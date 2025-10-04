"""Placeholder for the Guided Care Plan recommendation page."""
from __future__ import annotations

import streamlit as st

from senior_nav.components import buttons

st.set_page_config(layout="wide")
buttons.page_start()

st.title("Care Plan Recommendation")
st.info("Recommendation UI will be added after navigation wiring is complete.")

st.markdown('<div data-variant="link">', unsafe_allow_html=True)
if buttons.secondary("Refresh recommendation", key="gcp_refresh"):
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

buttons.page_end()
