"""Layout helpers for the cost planner shell."""
from __future__ import annotations

from typing import Iterable

import streamlit as st

from . import stepper


def _inject_layout_styles() -> None:
    if st.session_state.get("__sn_layout_styles__"):
        return
    st.session_state["__sn_layout_styles__"] = True
    st.markdown(
        """
        <style>
        .sn-mode-badge {
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.35rem 0.85rem;
          border-radius: 999px;
          background: rgba(43, 118, 229, 0.12);
          color: var(--sn-color-primary);
          font-weight: 600;
          font-size: 0.85rem;
        }
        .sn-progress-label {
          font-size: var(--sn-type-small-size);
          color: rgba(17, 20, 24, 0.6);
          margin-bottom: 0.25rem;
        }
        .sn-drawer-summary {
          background: var(--sn-color-bg-subtle);
          border-radius: var(--sn-radius-lg);
          padding: var(--sn-spacing-lg);
          border: 1px dashed var(--sn-color-border);
        }
        .sn-drawer-summary h4 {
          margin: 0 0 var(--sn-spacing-xs) 0;
        }
        .sn-sidebar-card {
          background: var(--sn-color-bg);
          border-radius: var(--sn-radius-lg);
          border: 1px solid var(--sn-color-border);
          padding: var(--sn-spacing-lg);
          box-shadow: var(--sn-shadow-soft);
        }
        .sn-sidebar-card h4 {
          margin-top: 0;
          margin-bottom: var(--sn-spacing-sm);
        }
        .sn-sidebar-list {
          list-style: none;
          padding: 0;
          margin: 0;
          display: grid;
          gap: 0.35rem;
        }
        .sn-sidebar-list li {
          display: flex;
          justify-content: space-between;
          font-size: var(--sn-type-body-size);
        }
        .sn-sidebar-divider {
          border-top: 1px dashed var(--sn-color-border);
          margin: var(--sn-spacing-md) 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(title: str, badge_text: str, steps: Iterable[str], current_index: int, *, progress: float, progress_label: str) -> None:
    """Render the shell header with title, badge, stepper, and progress."""
    _inject_layout_styles()
    col_title, col_badge = st.columns([4, 1])
    with col_title:
        st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
    with col_badge:
        st.markdown(f"<span class='sn-mode-badge'>{badge_text}</span>", unsafe_allow_html=True)
    stepper.render(steps, current_index)
    st.markdown(f"<div class='sn-progress-label'>{progress_label}</div>", unsafe_allow_html=True)
    st.progress(progress)


def render_sidebar(totals_title: str, rows: list[list[str]], navi_title: str, navi_body: str) -> None:
    """Render the sidebar summary card."""
    _inject_layout_styles()
    st.markdown(
        f"""
        <div class="sn-sidebar-card">
          <h4>{totals_title}</h4>
          <ul class="sn-sidebar-list">
            {''.join(f'<li><span>{label}</span><strong>{value}</strong></li>' for label, value in rows)}
          </ul>
          <div class="sn-sidebar-divider"></div>
          <p style="margin:0; color: rgba(17, 20, 24, 0.72);">{navi_title}</p>
          <p style="margin:0; color: rgba(17, 20, 24, 0.6);">{navi_body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_drawer_summary(label: str, subtotal: str, hint: str) -> None:
    """Render the mini summary box for drawers."""
    _inject_layout_styles()
    st.markdown(
        f"""
        <div class="sn-drawer-summary">
          <h4>{label}: {subtotal}</h4>
          <p style="margin:0; color: rgba(17, 20, 24, 0.6);">{hint}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
