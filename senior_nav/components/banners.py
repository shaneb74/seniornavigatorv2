"""Banner helpers for inline alerts."""
from __future__ import annotations

import streamlit as st

_LEVEL_CLASS = {
    "info": "sn-banner--info",
    "warning": "sn-banner--warning",
    "critical": "sn-banner--warning",
    "success": "sn-banner--success",
}

_LEVEL_ICON = {
    "info": "💡",
    "warning": "⚠️",
    "critical": "❗",
    "success": "✅",
}


def render(level: str, title: str, body: str) -> None:
    """Render a banner with semantic styling."""
    css_class = _LEVEL_CLASS.get(level, "sn-banner--info")
    icon = _LEVEL_ICON.get(level, "💡")
    st.markdown(
        f"""
        <div class="sn-banner {css_class}">
          <div class="sn-banner__icon">{icon}</div>
          <div class="sn-banner__content">
            <h4>{title}</h4>
            <p>{body}</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
