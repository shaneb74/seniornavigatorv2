"""Shared UI helpers for the simplified Senior Navigator experience."""
from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from . import navigation


def set_page_config(*, title: str) -> None:
    st.set_page_config(page_title=title, layout="wide")


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
