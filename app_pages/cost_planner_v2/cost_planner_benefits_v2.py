# Cost Planner · Benefits (v2)
from __future__ import annotations
import streamlit as st
from cost_planner_v2.cp_nav import goto
from ui.state import mark_complete

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
        result = {"prev": False, "next": False}
        if prev:
            with cols[0]:
                result["prev"] = st.button(prev.label, key=prev.key, type="secondary", width="stretch")
        if next:
            with cols[-1]:
                result["next"] = st.button(next.label, key=next.key, type="primary", width="stretch")
        return result

# ---------------- Page content ----------------
def render() -> None:
    # ❌ no st.set_page_config here; it's in app.py
    apply_cost_planner_theme()

    render_app_header()
    with cost_planner_page_container():
        render_wizard_hero("Benefits", "Any benefits to lower your costs?")
        render_wizard_help("VA, Medicaid status, and long-term care insurance are summarized here.")

        with st.container(border=True):
            st.subheader("Cost Planner · Benefits (v2)")
            st.caption(
                "TODO: build inputs for: va_estimate_(A/B), ltc_daily_benefit_(A/B), "
                "medicaid_status → benefits_total"
            )

        # Example metric placeholder if you compute a total later:
        # st.metric("Estimated Monthly Benefit Offset", f"${benefits_total:,.0f}")

        nav_clicks = render_nav_buttons(
            prev=NavButton("← Back to Expenses", "benefits_back"),
            next=NavButton("Save & Continue → Home", "benefits_next", type="primary"),
        )
        if isinstance(nav_clicks, dict):
            if nav_clicks.get("prev"):
                goto("app_pages/cost_planner_v2/cost_planner_expenses_v2.py")
            if nav_clicks.get("next"):
                mark_complete("cp_benefits")
                goto("app_pages/cost_planner_v2/cost_planner_home_v2.py")

# ✅ Import-time execution under Streamlit
render()
