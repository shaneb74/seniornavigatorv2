"""Navigation helpers for Streamlit multi-page experience."""
from __future__ import annotations

import streamlit as st


def safe_switch_page(target: str) -> None:
    """Attempt to navigate using ``st.switch_page`` with a graceful fallback."""
    try:
        st.switch_page(target)
    except Exception:  # Streamlit < 1.23 fallback behaviour
        st.session_state["next_page"] = target
        st.experimental_rerun()
