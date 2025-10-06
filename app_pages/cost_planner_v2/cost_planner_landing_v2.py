# Cost Planner v2 · Landing
from __future__ import annotations
import streamlit as st

# ---------------- Theme helpers (match Income pattern) ----------------
try:
    from ui.cost_planner_template import (
        apply_cost_planner_theme,
        cost_planner_page_container,
        render_app_header,
        render_wizard_hero,
        render_wizard_help,
        render_nav_buttons,
        Metric, NavButton,
    )
except Exception:
    # graceful fallbacks
    def apply_cost_planner_theme():
        st.markdown("""
        <style>
          :root{--brand:#0B5CD8;--surface:#f6f8fa;--ink:#111418}
          .sn-card{
            background:var(--surface);
            border:1px solid rgba(0,0,0,.08);
            border-radius:14px;
            padding:clamp(1rem,2vw,1.5rem);
          }
        </style>
        """, unsafe_allow_html=True)
    from contextlib import contextmanager
    @contextmanager
    def cost_planner_page_container(): yield
    def render_app_header(): st.markdown("### Cost Planner")
    def render_wizard_hero(title: str, subtitle: str = ""):
        st.markdown(f"## {title}")
        if subtitle: st.caption(subtitle)
    def render_wizard_help(text: str): st.info(text)
    class Metric:
        def __init__(self, title: str, value: str): self.title, self.value = title, value
    class NavButton:
        def __init__(self, label: str, key: str, type: str = "secondary", icon: str | None = None):
            self.label, self.key, self.type, self.icon = label, key, type, icon
    def render_nav_buttons(buttons=None, prev=None, next=None):
        cols = st.columns(2)
        if prev:
            with cols[0]:
                if st.button(prev.label, key=prev.key, type="secondary", use_container_width=True):
                    st.switch_page("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
        if next:
            with cols[-1]:
                if st.button(next.label, key=next.key, type="primary", use_container_width=True):
                    st.switch_page("app_pages/cost_planner_v2/cost_planner_timeline_v2.py")

# ---------------- Page content (functionality preserved) ----------------
def render() -> None:
    # same bootstrapping as Income
    apply_cost_planner_theme()

    render_app_header()
    with cost_planner_page_container():
        render_wizard_hero(
            "Cost Planner",
            "A simple, conversational way to estimate care costs or plan your budget in detail."
        )
        render_wizard_help("You can start light and add more later.")

        # First info card
        with st.container(border=True):
            st.subheader("Cost Planner")
            st.caption(
                "A simple, conversational way to estimate care costs or plan your budget in detail. "
                "You can start light and add more later."
            )

        # How to start
        with st.container(border=True):
            st.subheader("How do you want to start?")
            st.markdown(
                "- **Estimate** — quick monthly care cost using a few inputs "
                "(pulls from Guided Care Plan if available).\n"
                "- **Plan** — detailed modules (income, expenses, benefits, home, assets) "
                "to see your runway."
            )

        # Actions
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Start planning", type="primary", use_container_width=True):
                st.switch_page("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
        with col2:
            if st.button("Jump to Timeline (dev)", use_container_width=True):
                st.switch_page("app_pages/cost_planner_v2/cost_planner_timeline_v2.py")

# ✅ Import-time execution under Streamlit
render()
