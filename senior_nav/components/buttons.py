"""Scoped button helpers for consistent styling across pages."""
from __future__ import annotations

import streamlit as st

_SCOPE_KEY = "__sn_buttons_scope_stack__"


def page_start():
    stack = st.session_state.setdefault(_SCOPE_KEY, 0)
    st.session_state[_SCOPE_KEY] = stack + 1
    st.markdown('<div class="sn-scope">', unsafe_allow_html=True)


def page_end():
    stack = st.session_state.get(_SCOPE_KEY, 0)
    if stack > 0:
        st.markdown('</div>', unsafe_allow_html=True)
        st.session_state[_SCOPE_KEY] = stack - 1


def primary(
    label: str,
    key: str | None = None,
    *,
    disabled: bool = False,
    use_container_width: bool = False,
) -> bool:
    st.markdown('<div data-variant="primary">', unsafe_allow_html=True)
    clicked = st.button(
        label,
        key=key,
        disabled=disabled,
        use_container_width=use_container_width,
    )
    st.markdown('</div>', unsafe_allow_html=True)
    return clicked


def secondary(
    label: str,
    key: str | None = None,
    *,
    disabled: bool = False,
    use_container_width: bool = False,
) -> bool:
    st.markdown('<div data-variant="secondary">', unsafe_allow_html=True)
    clicked = st.button(
        label,
        key=key,
        disabled=disabled,
        use_container_width=use_container_width,
    )
    st.markdown('</div>', unsafe_allow_html=True)
    return clicked


def link(
    label: str,
    key: str | None = None,
    *,
    disabled: bool = False,
    use_container_width: bool = False,
) -> bool:
    st.markdown('<div data-variant="link">', unsafe_allow_html=True)
    clicked = st.button(
        label,
        key=key,
        disabled=disabled,
        use_container_width=use_container_width,
    )
    st.markdown('</div>', unsafe_allow_html=True)
    return clicked
