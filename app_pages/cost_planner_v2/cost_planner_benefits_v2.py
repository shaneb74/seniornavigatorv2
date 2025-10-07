# Cost Planner · Benefits (v2)
from __future__ import annotations

import streamlit as st

<<<<<<< Updated upstream
# ---------------- Theme helpers ----------------
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
          .sn-card{background:var(--surface);border:1px solid rgba(0,0,0,.08);
                   border-radius:14px;padding:clamp(1rem,2vw,1.5rem);}
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
                    st.switch_page("app_pages/cost_planner_v2/cost_planner_expenses_v2.py")
        if next:
            with cols[-1]:
                if st.button(next.label, key=next.key, type="primary", use_container_width=True):
                    st.switch_page("app_pages/cost_planner_v2/cost_planner_home_v2.py")
=======
from ui.cost_planner_data import MODULE_FIELD_MAP
from ui.cost_planner_forms import compute_gap, cp_state, render_fields
from ui import va_drawer

>>>>>>> Stashed changes

def render() -> None:
    st.header("Benefits & Coverage")
    st.caption("Record Medicare/Medicaid/VA programs and other supportive coverage.")

    fields = MODULE_FIELD_MAP["benefits"]
    valid, _ = render_fields(fields)

    st.markdown("---")
    left, right = st.columns([1, 1])
    with left:
        if st.button("Check Veterans benefits", type="primary"):
            va_drawer.open_drawer()

    saved, estimate = va_drawer.render_in_sidebar()
    with right:
        va_amount = float(cp_state().get("inc_va_monthly", 0) or 0)
        st.metric("VA benefit (monthly, planned)", f"${va_amount:,.0f}")

    st.markdown("---")
    if st.button("Save & back to Modules", type="primary", disabled=not valid):
        if cp_state().get("ben_va_status") == "No" and cp_state().get("ben_va_auto_estimate", True):
            cp_state()["inc_va_monthly"] = 0.0
        compute_gap(cp_state())
        try:
            st.switch_page("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
        except Exception:
            st.session_state["nav_target"] = "app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py"
            st.rerun()


render()
