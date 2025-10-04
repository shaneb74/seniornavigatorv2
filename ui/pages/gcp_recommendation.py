"""Placeholder for the Guided Care Plan recommendation page."""
from __future__ import annotations

import streamlit as st

from senior_nav.components.theme import inject_theme

st.set_page_config(layout="wide")
inject_theme()

st.title("Care Plan Recommendation")
st.info("Recommendation UI will be added after navigation wiring is complete.")
