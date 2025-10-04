"""Theme helpers for the Senior Care Navigator UI shell."""
from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import streamlit as st

from senior_nav.ui_style import tokens

_STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
_CHIP_CSS_PATH = _STATIC_DIR / "chips.css"

_THEME_STATE_KEY = "__sn_theme_injected__"
_BUTTONS_STATE_KEY = "__sn_buttons_css__"
_BUTTONS_CSS_CACHE: str | None = None


def _build_css() -> str:
    palette = tokens.PALETTE
    spacing = tokens.SPACING
    radius = tokens.RADIUS
    type_scale = tokens.TYPE

    return dedent(
        f"""
        <style>
        :root {{
          --sn-color-primary: {palette['primary']};
          --sn-color-ink: {palette['ink']};
          --sn-color-bg: {palette['bg']};
          --sn-color-bg-subtle: {palette['bgSubtle']};
          --sn-color-border: {palette['border']};
          --sn-color-info-bg: {palette['infoBG']};
          --sn-color-warn-bg: {palette['warnBG']};
          --sn-color-success-bg: {palette['successBG']};
          --sn-radius-sm: {radius['sm']}px;
          --sn-radius-md: {radius['md']}px;
          --sn-radius-lg: {radius['lg']}px;
          --sn-spacing-xs: {spacing['xs']}px;
          --sn-spacing-sm: {spacing['sm']}px;
          --sn-spacing-md: {spacing['md']}px;
          --sn-spacing-lg: {spacing['lg']}px;
          --sn-spacing-xl: {spacing['xl']}px;
          --sn-spacing-xxl: {spacing['xxl']}px;
          --sn-type-h1-size: {type_scale['h1']['size']}px;
          --sn-type-h2-size: {type_scale['h2']['size']}px;
          --sn-type-body-size: {type_scale['body']['size']}px;
          --sn-type-small-size: {type_scale['small']['size']}px;
          --sn-type-h1-weight: {type_scale['h1']['weight']};
          --sn-type-h2-weight: {type_scale['h2']['weight']};
          --sn-type-body-weight: {type_scale['body']['weight']};
          --sn-type-small-weight: {type_scale['small']['weight']};
          --sn-shadow-soft: 0 18px 38px rgba(17, 20, 24, 0.08);
        }}

        .sn-surface {{
          background: var(--sn-color-bg);
          color: var(--sn-color-ink);
        }}

        .sn-card {{
          background: var(--sn-color-bg);
          border: 1px solid var(--sn-color-border);
          border-radius: var(--sn-radius-lg);
          padding: var(--sn-spacing-xl);
          box-shadow: var(--sn-shadow-soft);
        }}

        .sn-card h1,
        .sn-card h2,
        .sn-card h3 {{
          margin-top: 0;
          color: var(--sn-color-ink);
        }}

        .sn-card p {{
          margin-bottom: var(--sn-spacing-md);
          font-size: var(--sn-type-body-size);
          color: rgba(17, 20, 24, 0.72);
        }}

        .sn-banner {{
          border-radius: var(--sn-radius-md);
          border: 1px solid var(--sn-color-border);
          padding: var(--sn-spacing-lg);
          display: flex;
          gap: var(--sn-spacing-md);
          align-items: flex-start;
        }}

        .sn-banner__icon {{
          font-size: 1.25rem;
          line-height: 1;
        }}

        .sn-banner__content > h4 {{
          margin: 0 0 var(--sn-spacing-xs) 0;
          font-size: var(--sn-type-h2-size);
          font-weight: var(--sn-type-h2-weight);
          color: var(--sn-color-ink);
        }}

        .sn-banner__content > p {{
          margin: 0;
          font-size: var(--sn-type-body-size);
          font-weight: var(--sn-type-body-weight);
          color: rgba(17, 20, 24, 0.72);
        }}

        .sn-banner--info {{ background: var(--sn-color-info-bg); }}
        .sn-banner--warning {{ background: var(--sn-color-warn-bg); }}
        .sn-banner--success {{ background: var(--sn-color-success-bg); }}

        .sn-stepper {{
          display: flex;
          gap: var(--sn-spacing-sm);
          flex-wrap: wrap;
          list-style: none;
          padding: 0;
          margin: 0;
          font-size: var(--sn-type-small-size);
        }}

        .sn-stepper__item {{
          display: inline-flex;
          align-items: center;
          gap: var(--sn-spacing-xs);
          padding: var(--sn-spacing-xs) var(--sn-spacing-sm);
          border-radius: var(--sn-radius-md);
          background: var(--sn-color-bg-subtle);
          color: var(--sn-color-ink);
        }}

        .sn-stepper__item.is-active {{
          background: var(--sn-color-primary);
          color: var(--sn-color-bg);
          font-weight: 600;
        }}

        .sn-stepper__item::before {{
          content: attr(data-step);
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 1.65rem;
          height: 1.65rem;
          border-radius: 999px;
          background: rgba(43, 118, 229, 0.14);
          color: inherit;
          font-weight: 600;
          font-size: 0.82rem;
        }}
        </style>
        """
    )


def _load_buttons_css() -> str:
    """Read and cache the scoped primary/secondary/link button CSS."""
    global _BUTTONS_CSS_CACHE
    if _BUTTONS_CSS_CACHE is not None:
        return _BUTTONS_CSS_CACHE

    css_path = _STATIC_DIR / "buttons.css"
    try:
        _BUTTONS_CSS_CACHE = css_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        _BUTTONS_CSS_CACHE = ""
    return _BUTTONS_CSS_CACHE


def inject_theme() -> None:
    """Inject shared theme + component CSS once per session."""
    if st.session_state.get(_THEME_STATE_KEY):
        return

    # Base token-driven theme
    st.markdown(_build_css(), unsafe_allow_html=True)

    # Scoped button styles (primary/secondary/link)
    buttons_css = _load_buttons_css()
    if buttons_css:
        st.markdown(f"<style>{buttons_css}</style>", unsafe_allow_html=True)

    # Choice chips styling
    if _CHIP_CSS_PATH.exists():
        chips_css = _CHIP_CSS_PATH.read_text(encoding="utf-8")
        st.markdown(f"<style>{chips_css}</style>", unsafe_allow_html=True)

    # Mark injected
    st.session_state[_THEME_STATE_KEY] = True
    st.session_state.setdefault(_BUTTONS_STATE_KEY, True)