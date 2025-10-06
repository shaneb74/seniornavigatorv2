"""Shared UI helpers for the simplified Senior Navigator experience."""
from __future__ import annotations

from typing import Any, Dict

import streamlit as st
import streamlit.components.v1 as components

from . import navigation


def configure_page(*, page_title: str | None = None, layout: str = "wide", **kwargs: Any) -> None:
    """Apply Streamlit's page config but never crash if it's too late."""

    config: Dict[str, Any] = {"layout": layout, **kwargs}
    if page_title is not None:
        config["page_title"] = page_title

    try:
        st.set_page_config(**config)
    except Exception as exc:  # pragma: no cover - depends on Streamlit runtime
        message = getattr(exc, "message", str(exc))
        st.warning(
            "We couldn't apply the custom page configuration. "
            "The page will continue with Streamlit defaults.",
        )
        print(f"[page-config] {type(exc).__name__}: {message}")


def set_page_config(*, title: str) -> None:
    configure_page(page_title=title)


def header(title: str, subtitle: str | None = None) -> None:
    st.title(title)
    if subtitle:
        st.caption(subtitle)


def render_ai_launcher() -> None:
    """Render a floating button that opens the AI Advisor page."""

    value = components.html(
        """
        <div class="sn-ai-launcher">
          <button onclick="Streamlit.setComponentValue('open')">🤖 AI Advisor</button>
        </div>
        <style>
          .sn-ai-launcher {
            position: fixed;
            bottom: 1.5rem;
            right: 1.5rem;
            z-index: 1000;
          }
          .sn-ai-launcher button {
            background: #1d4ed8;
            color: #fff;
            border-radius: 999px;
            padding: 0.65rem 1.4rem;
            border: none;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 10px 30px rgba(29, 78, 216, 0.35);
          }
          .sn-ai-launcher button:hover {
            background: #1e40af;
          }
        </style>
        """,
        height=0,
    )
    if value == "open":
        navigation.switch_page(navigation.AI_ADVISOR_PAGE)
