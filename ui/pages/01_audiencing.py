"""Audiencing entry point for selecting who we're planning for."""
from __future__ import annotations

import streamlit as st

from senior_nav.components.nav import safe_switch_page
from senior_nav.components.theme import inject_theme


def _set_entry(val: str) -> None:
    st.session_state.setdefault("audiencing", {})
    st.session_state["audiencing"]["entry"] = val


def main() -> None:
    inject_theme()
    st.title("Who are you planning for?")

    _left, center_col, _right = st.columns([1, 2, 1])
    with center_col:
        if st.button("I'm planning for myself", use_container_width=True):
            _set_entry("self")
            safe_switch_page("ui/pages/contextual_welcome.py")
        if st.button("I'm helping someone", use_container_width=True):
            _set_entry("proxy")
            safe_switch_page("ui/pages/contextual_welcome.py")


if __name__ == "__main__":
    main()
