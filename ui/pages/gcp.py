"""Placeholder for the Guided Care Plan page."""
from __future__ import annotations

import streamlit as st

from senior_nav.components.theme import inject_theme

st.set_page_config(layout="wide")
inject_theme()

st.title("Guided Care Plan")
st.info("Detailed UI will ship in a later wiring milestone.")
