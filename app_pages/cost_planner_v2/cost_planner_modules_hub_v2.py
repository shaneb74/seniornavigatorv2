# Cost Planner v2 · Modules Hub
from __future__ import annotations
import streamlit as st
from cost_planner_v2.cp_state import ensure_cp
from cost_planner_v2.cp_nav import goto
from ui.cost_planner import MODULES, _answers, _gcp

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
                st.button(prev.label, key=prev.key, type="secondary", use_container_width=True)
        if next:
            with cols[-1]:
                st.button(next.label, key=next.key, type="primary", use_container_width=True)

# ---------------- Page content (functionality preserved) ----------------
def render() -> None:
    # same bootstrapping as Income/Home Mods
    apply_cost_planner_theme()
    ensure_cp()

    render_app_header()
    with cost_planner_page_container():
        with st.container(border=True):
            st.header("Cost Planner · Modules")
            st.caption("Choose a section to review or update. Only the most relevant modules are shown.")

        data = {}
        data.update(_gcp(st.session_state))
        data.update(_answers(st.session_state))

        # List modules exactly like before, just using Streamlit containers for styling
        for label, page in modules:
            with st.container(border=True):
                cols = st.columns([3, 1])
                with cols[0]:
                    st.write(f"**{label}**")
                with cols[1]:
                    if st.button("Open", key=f"open_{label}", use_container_width=True):
                        goto(page)

        # Primary CTA
        st.markdown("---")
        if st.button("View Money Timeline", type="primary", use_container_width=True):
            goto("cost_planner_timeline_v2.py")

# ✅ Import-time execution under Streamlit
render()
