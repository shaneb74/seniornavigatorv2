"""Placeholder for the Cost Planner intro page."""
from __future__ import annotations

import streamlit as st

from senior_nav.components.theme import inject_theme

st.set_page_config(layout="wide")
inject_theme()

st.title("Cost Planner")
st.info("Cost Planner shell will be wired in a subsequent pass.")
