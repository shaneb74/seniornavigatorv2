"""Placeholder for the Smart Review page."""
from __future__ import annotations

import streamlit as st

from senior_nav.components.theme import inject_theme

st.set_page_config(layout="wide")
inject_theme()

st.title("Smart Review")
st.info("Smart Review UI will be implemented in a later milestone.")
