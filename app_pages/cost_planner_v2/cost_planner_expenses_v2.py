# Cost Planner · Other Monthly Costs (v2)
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
                if st.button(prev.label, key=prev.key, type="secondary", use_container_width=True):
                    st.switch_page("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
        if next:
            with cols[-1]:
                if st.button(next.label, key=next.key, type="primary", use_container_width=True):
                    st.switch_page("app_pages/cost_planner_v2/cost_planner_benefits_v2.py")

# ---------------- Page content ----------------
def render() -> None:
    # ❌ no st.set_page_config here; it's in app.py
    apply_cost_planner_theme()

    render_app_header()
    with cost_planner_page_container():
        render_wizard_hero("Other Monthly Costs", "What do you pay monthly?")
        render_wizard_help(
            "Stub page — we’ll wire inputs next: utilities, phone/internet, life insurance, "
            "transportation, auto, auto insurance, monthly debt payments, other. "
            "Includes the facility-move adjustment (~$500) when applicable."
        )

        with st.container(border=True):
            st.subheader("Cost Planner · Other Monthly Costs (v2)")
            st.caption(
                "This section will collect monthly expense inputs and roll them into the overall plan."
            )

        # Example placeholder until inputs are added:
        # st.metric("Estimated Monthly Other Costs", f"${other_costs_total:,.0f}")

        render_nav_buttons(
            prev=NavButton("← Back to Modules", "expenses_back"),
            next=NavButton("Save & Continue → Benefits", "expenses_next", type="primary"),
        )

# ✅ Import-time execution under Streamlit
render()
