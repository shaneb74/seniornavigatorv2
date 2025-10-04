"""Placeholder for the Audiencing entry page."""
from __future__ import annotations

import streamlit as st

from senior_nav.components.theme import inject_theme

st.set_page_config(layout="wide")
inject_theme()

st.title("Audiencing")
st.info("Audiencing UI will be implemented in a follow-up wiring pass.")
