# Cost Planner · Caregiver Support (v2)
from __future__ import annotations

import streamlit as st

<<<<<<< Updated upstream
# ---------------- Theme helpers (same pattern as Income) ----------------
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
                    st.switch_page("app_pages/cost_planner_v2/cost_planner_liquidity_v2.py")
        if next:
            with cols[-1]:
                if st.button(next.label, key=next.key, type="primary", use_container_width=True):
                    st.switch_page("app_pages/cost_planner_v2/cost_planner_assets_v2.py")
=======
from ui.cost_planner_data import MODULE_FIELD_MAP
from ui.cost_planner_forms import compute_gap, cp_state, render_fields

>>>>>>> Stashed changes

def render() -> None:
    st.header("Caregiver Support")
    st.caption("Track informal caregiver hours, burnout risk, and out-of-pocket expenses.")

    fields = MODULE_FIELD_MAP["caregiver"]
    valid, _ = render_fields(fields)

    st.markdown("---")
    if st.button("Save & back to Modules", type="primary", disabled=not valid):
        compute_gap(cp_state())
        try:
            st.switch_page("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
        except Exception:
            st.session_state["nav_target"] = "app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py"
            st.rerun()


render()
