"""Shared helpers for contextual welcome variants (placeholder)."""
from __future__ import annotations

import streamlit as st

from senior_nav.components.theme import inject_theme


def render(which: str) -> None:
    """Temporary placeholder render until the detailed UI is wired."""
    st.set_page_config(layout="wide")
    inject_theme()
    st.title("Contextual Welcome")
    st.info(f"Contextual welcome variant '{which}' will be implemented soon.")
