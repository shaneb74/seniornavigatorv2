"""Scoped button helpers for consistent styling across pages."""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

import streamlit as st

from senior_nav.components import theme

_SCOPE_CLASS = "skn-scope"
_CSS_STATE_KEY = "__sn_buttons_css__"


def _load_css() -> str:
    css_path = Path(__file__).resolve().parent.parent / "static" / "buttons.css"
    try:
        return css_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _ensure_css() -> None:
    if st.session_state.get(_CSS_STATE_KEY):
        return
    css = _load_css()
    if css:
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.session_state[_CSS_STATE_KEY] = True


@contextmanager
def variant(variant_name: str):
    st.markdown(f'<div data-variant="{variant_name}">', unsafe_allow_html=True)
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)


def page_start() -> None:
    """Begin a scoped button region."""
    theme.inject_theme()
    _ensure_css()
    st.markdown(f'<div class="{_SCOPE_CLASS}">', unsafe_allow_html=True)


def page_end() -> None:
    """Close the scoped region."""
    st.markdown("</div>", unsafe_allow_html=True)


def primary(label: str, *, key: str | None = None, **kwargs) -> bool:
    kwargs.setdefault("type", "primary")
    kwargs.setdefault("use_container_width", True)
    with variant("primary"):
        return st.button(label, key=key, **kwargs)


def secondary(label: str, *, key: str | None = None, **kwargs) -> bool:
    kwargs.setdefault("use_container_width", True)
    return st.button(label, key=key, **kwargs)
