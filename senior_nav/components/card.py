"""Card helpers for high-fidelity UI shells."""
from __future__ import annotations

from html import escape
from typing import Callable

import streamlit as st


def _inject_card_styles() -> None:
    if st.session_state.get("__sn_card_styles__"):
        return
    st.session_state["__sn_card_styles__"] = True
    st.markdown(
        """
        <style>
        .sn-card__surface {
          background: var(--sn-color-bg);
          border: 1px solid var(--sn-color-border);
          border-radius: var(--sn-radius-lg);
          padding: var(--sn-spacing-xl);
          box-shadow: var(--sn-shadow-soft);
          display: flex;
          flex-direction: column;
          gap: var(--sn-spacing-md);
          min-height: 100%;
        }
        .sn-card__title {
          font-size: var(--sn-type-h2-size);
          font-weight: var(--sn-type-h2-weight);
          margin: 0;
        }
        .sn-card__subtitle {
          color: rgba(17, 20, 24, 0.64);
          font-size: 1.05rem;
          margin: 0;
        }
        .sn-card__body {
          color: rgba(17, 20, 24, 0.72);
          flex: 1;
        }
        .sn-card__cta {
          width: fit-content;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_basic(title: str, body: str | None = None, footer: str | None = None) -> None:
    """Render a static informational card."""
    _inject_card_styles()
    st.markdown(
        f"""
        <div class="sn-card__surface">
          <h3 class="sn-card__title">{title}</h3>
          {f'<p class="sn-card__body">{body}</p>' if body else ''}
          {f'<div class="sn-card__footer">{footer}</div>' if footer else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_action(
    title: str,
    body: str,
    button_label: str,
    key: str,
    *,
    on_click: Callable[[], None],
    disabled: bool = False,
) -> None:
    """Render a call-to-action card with a button."""
    _inject_card_styles()
    placeholder = st.container()
    with placeholder:
        st.markdown(
            f"""
            <div class=\"sn-card__surface\">
              <h3 class=\"sn-card__title\">{title}</h3>
              <p class=\"sn-card__body\">{body}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.button(button_label, key=key, on_click=on_click, disabled=disabled)


def card_panel(*, title: str, subtitle: str | None = None, body: Callable[[], None]) -> None:
    """Render a structured card surface with a callable body."""

    _inject_card_styles()
    container = st.container()
    with container:
        st.markdown('<div class="sn-card__surface">', unsafe_allow_html=True)
        st.markdown(
            f'<h3 class="sn-card__title">{escape(title)}</h3>',
            unsafe_allow_html=True,
        )
        if subtitle:
            st.markdown(
                f'<p class="sn-card__subtitle">{escape(subtitle)}</p>',
                unsafe_allow_html=True,
            )
        st.markdown('<div class="sn-card__body">', unsafe_allow_html=True)
        body()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
