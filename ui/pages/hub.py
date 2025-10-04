"""Placeholder for the Care Planning Hub page."""
from __future__ import annotations

import streamlit as st

from senior_nav.components.theme import inject_theme

st.set_page_config(layout="wide")
inject_theme()

st.title("Care Planning Hub")
st.info("Hub UI will be delivered in a subsequent PR once global components are ready.")
