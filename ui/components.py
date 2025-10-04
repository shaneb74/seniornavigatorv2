from __future__ import annotations

from contextlib import contextmanager
from typing import Callable, Iterable, Optional

import streamlit as st


def grid(cols: int = 2):
    """Context-managed grid wrapper."""
    class _Grid:
        def __enter__(self):
            class_attr = "sn-grid two" if cols == 2 else "sn-grid"
            st.markdown(
                f'<div class="{class_attr}">',
                unsafe_allow_html=True,
            )
            return self

        def __exit__(self, exc_type, exc, tb):
            st.markdown("</div>", unsafe_allow_html=True)
            return False

    return _Grid()


def notice(text: str) -> None:
    st.markdown(f'<div class="sn-notice">{text}</div>', unsafe_allow_html=True)


def badge(label: str) -> None:
    st.markdown(f'<span class="sn-badge">{label}</span>', unsafe_allow_html=True)


def button(
    label: str,
    *,
    href: str | None = None,
    primary: bool = False,
    key: str | None = None,
    **kwargs,
) -> bool:
    """Render a pill-shaped button or link."""
    if href:
        cls = "sn-btn primary" if primary else "sn-btn"
        st.markdown(f'<a class="{cls}" href="{href}">{label}</a>', unsafe_allow_html=True)
        return False
    button_type = "primary" if primary else "secondary"
    return st.button(label, key=key, type=button_type, **kwargs)


def card(
    title: str,
    *,
    body: str | None = None,
    badge_text: str | None = None,
    footer: Optional[Callable[[], None]] = None,
    gradient: bool = False,
) -> None:
    classes = "sn-card sn-card--gradient" if gradient else "sn-card"
    st.markdown(f'<div class="{classes}">', unsafe_allow_html=True)
    st.markdown(
        '<div style="display:flex;justify-content:space-between;align-items:center;gap:.8rem;">',
        unsafe_allow_html=True,
    )
    st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
    if badge_text:
        badge(badge_text)
    st.markdown("</div>", unsafe_allow_html=True)
    if body:
        st.markdown(body, unsafe_allow_html=True)
    if footer:
        footer()
    st.markdown("</div>", unsafe_allow_html=True)


def pills(
    options: Iterable[str],
    *,
    value: str | None = None,
    key: str,
    help_text: str | None = None,
) -> str:
    options = list(options)
    if not options:
        raise ValueError("options cannot be empty")
    state_key = f"sn_pills_{key}"
    selected = value if value is not None else st.session_state.get(state_key, options[0])
    cols = st.columns(len(options))
    for idx, option in enumerate(options):
        with cols[idx]:
            pressed = st.button(
                option,
                key=f"{state_key}_{idx}",
                type="primary" if option == selected else "secondary",
                use_container_width=True,
            )
            if pressed:
                selected = option
    st.session_state[state_key] = selected
    if help_text:
        st.caption(help_text)
    return selected


@contextmanager
def card_panel(*, padding: str | None = None, gap: str = "1.4rem"):
    """Context manager that renders content inside a themed card panel."""

    padding_css = padding or "clamp(1.8rem, 3vw, 2.4rem)"
    style = f"padding:{padding_css};display:flex;flex-direction:column;gap:{gap};"
    st.markdown(
        f'<div class="sn-card" style="{style}">',
        unsafe_allow_html=True,
    )
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)
