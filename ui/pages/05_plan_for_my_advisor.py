"""Placeholder for the Plan for My Advisor page."""
from __future__ import annotations

import streamlit as st

from senior_nav.components.theme import inject_theme

st.set_page_config(layout="wide")
inject_theme()

st.title("Plan for My Advisor")
st.info("Advisor plan UI will be implemented in a later milestone.")
