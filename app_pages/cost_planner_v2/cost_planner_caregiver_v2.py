# Cost Planner · Caregiver Support (v2)
from __future__ import annotations
import streamlit as st

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

# ---------------- Page content (functionality preserved; styling fixed) ----------------
def render() -> None:
    # same bootstrapping as Income (no set_page_config here)
    apply_cost_planner_theme()

    render_app_header()
    with cost_planner_page_container():
        render_wizard_hero("Caregiver Support", "Who’ll help with in-home care?")
        # Keep your original content, just presented with the shared styles
        with st.container(border=True):
            st.subheader("Who’ll help with in-home care?")
            st.caption(
                "Optional but helpful for in-home care with high needs. "
                "Adds caregiver_cost to monthly all-in."
            )
        st.info(
            "TODO: inputs for caregiver_type, include_caregiver_cost, "
            "caregiver_cost (default 3600 if included)."
        )

        # If you want nav buttons (optional), uncomment and adjust:
        # render_nav_buttons(
        #     prev=NavButton("← Back to Liquidity", "caregiver_back"),
        #     next=NavButton("Save & Continue → Assets", "caregiver_next", type="primary"),
        # )

# ✅ Import-time execution under Streamlit
render()
