# Cost Planner · Home Decisions (v2)
from __future__ import annotations
import streamlit as st

# ---------------- Theme helpers (match working Income pattern) ----------------
try:
    from ui.cost_planner_template import (
        apply_cost_planner_theme,
        cost_planner_page_container,
        render_app_header,
        render_wizard_hero,
        render_wizard_help,
        Metric, NavButton,  # available if you add nav later
    )
except Exception:
    # graceful fallbacks (won’t crash if helpers are missing)
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

# ---------------- Page content (functionality preserved; styling fixed) ----------------
def render() -> None:
    # same bootstrapping as Income (no set_page_config here)
    apply_cost_planner_theme()

    render_app_header()
    with cost_planner_page_container():
        render_wizard_hero("Home Decisions", "What’s the plan for your home?")

        # Keep your content, present in styled containers
        with st.container(border=True):
            st.subheader("What’s the plan for your home?")
            st.caption(
                "If moving to a facility and not maintaining the home, you can consider selling, "
                "renting, or a reverse mortgage estimate."
            )

        st.info(
            "TODO: add inputs for sale proceeds, rental income, or reverse mortgage $/month (no fees modeling)."
        )

# ✅ Import-time execution under Streamlit
render()
