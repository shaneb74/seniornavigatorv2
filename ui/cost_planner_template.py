"""Shared helpers for TurboTax-style wireframe styling.

These utilities provide the TurboTax-inspired presentation that the
product team wants to see applied consistently across our guided
experiences (Cost Planner, Guided Care Plan, Plan for MyAdvisor, etc.).
They intentionally focus on layout and tone; business logic should stay
within the individual pages.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterable, List, Optional

import streamlit as st

from ui.theme import inject_theme


@dataclass
class Metric:
    label: str
    value: str
    delta: Optional[str] = None


@dataclass
class NavButton:
    label: str
    key: str
    type: str = "secondary"
    help: Optional[str] = None
    disabled: bool = False


def apply_cost_planner_theme() -> None:
    """Inject the shared theme and CSS used by the wireframes."""

    inject_theme()

    st.markdown(
        """
<style>
/* Header and Navigation */
.stAppHeader { background-color: #f0f8ff; padding: 1rem; border-bottom: 1px solid #d3d3d3; }
.stAppHeader h1 { color: #1e90ff; font-size: 24px; margin: 0; }
.nav-bar { display: flex; justify-content: space-between; align-items: center; gap: 1rem; }
.nav-item { color: #4682b4; margin-right: 1rem; text-decoration: none; font-weight: 500; }
.login-btn { background-color: #1e90ff; color: white; padding: 0.5rem 1rem; border-radius: 20px; border: none; font-weight: 600; }

/* Qualifiers Header */
.qual-header { display: flex; align-items: center; padding: 1rem; border-bottom: 1px solid #d3d3d3; gap: 0.75rem; }
.back-btn { color: #1e90ff; font-size: 18px; cursor: pointer; }
.assess-label { color: #808080; font-size: 14px; }
.name-btn { background-color: #f0f8ff; color: #1e90ff; border-radius: 20px; padding: 0.2rem 0.8rem; border: 0; font-weight: 600; }
.question-mode { color: #1e90ff; font-size: 14px; margin-left: auto; }

/* Wizard Styling */
.wizard-hero { background: #f0f8ff; padding: 2rem; text-align: center; border-radius: 20px; margin-bottom: 2rem; }
.wizard-title { font-size: 32px; color: #1e90ff; margin-bottom: 0.5rem; }
.wizard-caption { font-size: 17px; color: #808080; max-width: 720px; margin: 0 auto; }
.wizard-help { background-color: #f0f8ff; color: #606060; padding: 0.75rem 1rem; border-radius: 12px; margin-top: 1.25rem; border: 1px solid #d3d3d3; }
.wizard-button { padding: 0.5rem 1.25rem; border-radius: 20px; font-weight: 600; display: inline-flex; align-items: center; justify-content: center; border: none; cursor: pointer; }
.wizard-button-primary { background-color: #1e90ff; color: white; }
.wizard-button-secondary { background-color: #f0f8ff; color: #1e90ff; border: 1px solid #d3d3d3; }
.wizard-suggestion { padding: 1rem; border-radius: 12px; margin-bottom: 1rem; font-size: 15px; }
.wizard-suggestion-info { background-color: #e6f0fa; color: #1e90ff; }
.wizard-suggestion-warn { background-color: #fff3cd; color: #856404; }
.wizard-suggestion-critical { background-color: #f8d7da; color: #721c24; }

/* Module dashboard cards */
.module-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; margin: 1.5rem 0; }
.module-card { background: #ffffff; border-radius: 18px; padding: 1.25rem; border: 1px solid #d3d3d3; box-shadow: 0 12px 30px rgba(30, 144, 255, 0.08); display: flex; flex-direction: column; gap: 0.5rem; }
.module-card h4 { margin: 0; font-size: 18px; color: #1e90ff; }
.module-card p { margin: 0; color: #606060; font-size: 14px; }
.module-card .card-status { display: inline-flex; align-items: center; gap: 0.35rem; background: #f0f8ff; color: #1e90ff; padding: 0.15rem 0.75rem; border-radius: 999px; font-size: 13px; font-weight: 600; }
.module-card .card-status.positive { background: #e6f7eb; color: #2e8b57; }
.module-card .card-status.warning { background: #fff3cd; color: #856404; }
.module-card .card-actions { margin-top: auto; display: flex; gap: 0.5rem; }
.module-card .card-actions a { text-decoration: none; }
.module-card .card-actions .wizard-button { width: 100%; }

/* Tables */
.summary-table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
.summary-table th { text-align: left; font-size: 14px; color: #606060; border-bottom: 1px solid #d3d3d3; padding-bottom: 0.5rem; }
.summary-table td { padding: 0.65rem 0; border-bottom: 1px solid #ededed; font-size: 15px; }
.summary-table td.amount { text-align: right; font-weight: 600; color: #1e90ff; }

/* Utility */
.sn-scope.dashboard.cost-planner-wireframe { padding-bottom: 2rem; }
</style>
""",
        unsafe_allow_html=True,
    )


def render_app_header() -> None:
    st.markdown(
        """
<div class="stAppHeader">
  <div class="nav-bar">
    <h1>Concierge Care Senior Navigator</h1>
    <div>
      <a class="nav-item" href="#">Dashboard</a>
      <a class="nav-item" href="#">Learning Center</a>
      <a class="nav-item" href="#">Get Connected</a>
      <button class="login-btn">Log in or sign up</button>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_assessment_header(section_label: str, *, persona: str = "John", mode: str = "All questions") -> None:
    st.markdown(
        f"""
<div class="qual-header">
  <span class="back-btn">← Back</span>
  <span class="assess-label">{section_label}</span>
  <button class="name-btn">{persona}</button>
  <span class="question-mode">{mode}</span>
</div>
""",
        unsafe_allow_html=True,
    )


def render_wizard_hero(title: str, caption: str) -> None:
    st.markdown("<div class='wizard-hero'>", unsafe_allow_html=True)
    st.markdown(f"<h1 class='wizard-title'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='wizard-caption'>{caption}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_wizard_help(text: str) -> None:
    st.markdown(f"<div class='wizard-help'>{text}</div>", unsafe_allow_html=True)


def render_metrics(metrics: Iterable[Metric]) -> None:
    metric_list = list(metrics)
    if not metric_list:
        return

    cols = st.columns(len(metric_list))
    for col, metric in zip(cols, metric_list):
        with col:
            st.metric(metric.label, metric.value, metric.delta)


def render_nav_buttons(buttons: Iterable[NavButton]) -> Optional[str]:
    """Render navigation buttons and return the key that was clicked."""

    button_list = list(buttons)
    if not button_list:
        return None

    cols = st.columns(len(button_list))
    for col, button in zip(cols, button_list):
        with col:
            if st.button(
                button.label,
                key=button.key,
                type=button.type,
                help=button.help,
                disabled=button.disabled,
            ):
                return button.key
    return None


def apply_turbotax_wizard_theme() -> None:
    """Alias for ``apply_cost_planner_theme`` for broader reuse."""

    apply_cost_planner_theme()


def render_suggestion(text: str, *, tone: str = "info") -> None:
    tone_class = {
        "info": "wizard-suggestion-info",
        "warn": "wizard-suggestion-warn",
        "critical": "wizard-suggestion-critical",
    }.get(tone, "wizard-suggestion-info")
    st.markdown(
        f"<div class='wizard-suggestion {tone_class}'>{text}</div>",
        unsafe_allow_html=True,
    )


def render_module_cards(cards: List[dict]) -> Optional[str]:
    """Render module cards and return the key of a triggered action, if any."""

    if not cards:
        return None

    st.markdown("<div class='module-grid'>", unsafe_allow_html=True)
    triggered: Optional[str] = None
    for card in cards:
        st.markdown("<div class='module-card'>", unsafe_allow_html=True)
        st.markdown(f"<h4>{card.get('title', '')}</h4>", unsafe_allow_html=True)
        if card.get("description"):
            st.markdown(f"<p>{card['description']}</p>", unsafe_allow_html=True)
        if card.get("status"):
            status_class = card.get("status_class", "")
            st.markdown(
                f"<span class='card-status {status_class}'>{card['status']}</span>",
                unsafe_allow_html=True,
            )
        actions = card.get("actions", [])
        if actions:
            st.markdown("<div class='card-actions'>", unsafe_allow_html=True)
            for action in actions:
                action_key = action.get("key", action.get("label", "btn"))
                if st.button(
                    action.get("label", ""),
                    key=action_key,
                    type=action.get("type", "secondary"),
                    help=action.get("help"),
                ):
                    triggered = action_key
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    return triggered


@contextmanager
def cost_planner_page_container() -> None:
    st.markdown(
        "<div class='sn-scope dashboard cost-planner-wireframe'>",
        unsafe_allow_html=True,
    )
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)
