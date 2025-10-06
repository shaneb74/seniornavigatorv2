# Cost Planner · Other Monthly Costs (v2)
from __future__ import annotations
import streamlit as st

# ---------------- Theme helpers (match Income/Home Mods style) ----------------
try:
    from ui.cost_planner_template import (
        apply_cost_planner_theme,
        cost_planner_page_container,
        render_app_header,
        render_wizard_hero,
        render_wizard_help,
        Metric, NavButton,  # available if you want later
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

# ---------------- Page content (functionality preserved) ----------------
def render() -> None:
    # same bootstrapping as Income (no set_page_config here)
    apply_cost_planner_theme()

    render_app_header()
    with cost_planner_page_container():
        render_wizard_hero("Other Monthly Costs", "What do you pay monthly?")

        # Keep your text, present it in styled containers
        with st.container(border=True):
            st.subheader("What do you pay monthly?")
            st.caption(
                "Stub page – we’ll wire inputs next: utilities, phone/internet, life insurance, "
                "transportation, auto, auto insurance, monthly debt payments, other. "
                "Includes the facility-move adjustment (~$500) when applicable."
            )

        # Same two-button layout/behavior you had before
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("◀︎ Back to Modules", use_container_width=True):
                st.switch_page("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
        with col2:
            st.button("Save & Continue", disabled=True, help="Coming soon", use_container_width=True)

# ✅ Import-time execution under Streamlit
render()
