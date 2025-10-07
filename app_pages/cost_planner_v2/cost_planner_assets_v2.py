# Cost Planner · Assets (v2)
from __future__ import annotations
import streamlit as st

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
                if st.button(prev.label, key=prev.key, type="secondary", width="stretch"):
                    st.switch_page("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
        if next:
            with cols[-1]:
                if st.button(next.label, key=next.key, type="primary", width="stretch"):
                    st.switch_page("app_pages/cost_planner_v2/cost_planner_timeline_v2.py")

# ---------------- Page content ----------------
def render() -> None:
    # ❌ no st.set_page_config here; it's in app.py
    apply_cost_planner_theme()

    render_app_header()
    with cost_planner_page_container():
        render_wizard_hero("Assets", "What savings or assets can you tap?")
        render_wizard_help(
            "Keep it simple: cash, brokerage, IRA/401k combined, home equity, other assets, "
            "plus any one-time liquidity nudge."
        )

        with st.container(border=True):
            st.subheader("Cost Planner · Assets (v2)")
            st.caption(
                "TODO: inputs for cash_savings, brokerage_taxable, ira_total, home_equity "
                "(if owner), other_assets, liquidity_total → assets_total_effective"
            )

        # Example total metric placeholder (wire-up when you store values)
        # st.metric("Total Effective Assets", f"${total:,.0f}")

        # Nav (adjust targets if your flow differs)
        render_nav_buttons(
            prev=NavButton("← Back to Modules", "assets_back"),
            next=NavButton("Save & Continue → Timeline", "assets_next", type="primary"),
        )

# ✅ Import-time execution under Streamlit
render()
