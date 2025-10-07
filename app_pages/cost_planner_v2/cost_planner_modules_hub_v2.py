# Cost Planner v2 · Modules Hub
from __future__ import annotations
import streamlit as st
from cost_planner_v2.cp_state import ensure_cp
from cost_planner_v2.cp_nav import goto

# ---------------- Theme helpers (match Income/Home Mods pattern) ----------------
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
        # simple two-button layout if needed later
        cols = st.columns(2)
        if prev:
            with cols[0]:
                st.button(prev.label, key=prev.key, type="secondary", width="stretch")
        if next:
            with cols[-1]:
                st.button(next.label, key=next.key, type="primary", width="stretch")

# ---------------- Page content (functionality preserved) ----------------
def render() -> None:
    # same bootstrapping as Income/Home Mods
    apply_cost_planner_theme()
    ensure_cp()

    render_app_header()
    with cost_planner_page_container():
        # Header + helper text
        with st.container(border=True):
            st.subheader("Your Plan Modules (v2)")
            st.caption("Work through modules in any order. Then view Your Money Timeline.")

        modules = [
            ("Income", "cost_planner_income_v2.py"),
            ("Other Monthly Costs", "cost_planner_expenses_v2.py"),
            ("Caregiver Support", "cost_planner_caregiver_v2.py"),
            ("Benefits", "cost_planner_benefits_v2.py"),
            ("Home Decisions", "cost_planner_home_v2.py"),
            ("Liquidity Nudge", "cost_planner_liquidity_v2.py"),
            ("Home Modifications", "cost_planner_home_mods_v2.py"),
            ("Assets", "cost_planner_assets_v2.py"),
        ]

        # List modules exactly like before, just using Streamlit containers for styling
        for label, page in modules:
            with st.container(border=True):
                cols = st.columns([3, 1])
                with cols[0]:
                    st.write(f"**{label}**")
                with cols[1]:
                    if st.button("Open", key=f"open_{label}", width="stretch"):
                        goto(page)

        # Primary CTA
        st.markdown("---")
        if st.button("View Money Timeline", type="primary", width="stretch"):
            goto("cost_planner_timeline_v2.py")

# ✅ Import-time execution under Streamlit
render()
