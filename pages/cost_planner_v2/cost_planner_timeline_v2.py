"""Cost Planner v2 · Timeline (results) — canonical, self-contained page."""
from __future__ import annotations

import streamlit as st

# Prefer shared theme/components if available, else graceful fallbacks.
try:
    from ui.cost_planner_template import (
        apply_cost_planner_theme,
        cost_planner_page_container,
        render_app_header,
        render_wizard_hero,
        render_wizard_help,
        render_metrics,
        Metric,
        NavButton,
        render_nav_buttons,
    )
except Exception:
    # Light fallbacks so this page never crashes
    def apply_cost_planner_theme(): pass
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
        def __init__(self, label: str, key: str, type: str = "secondary", icon: str|None=None):
            self.label, self.key, self.type, self.icon = label, key, type, icon
    def render_metrics(items):
        cols = st.columns(len(items))
        for c, m in zip(cols, items):
            with c: st.metric(m.title, m.value)
    def render_nav_buttons(buttons=None, prev=None, next=None):
        left, right = st.columns(2)
        with left:
            if prev and st.button(prev.label, key=prev.key, type="secondary", use_container_width=True):
                st.switch_page("pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
        with right:
            if next and st.button(next.label, key=next.key, type="primary", use_container_width=True):
                st.switch_page("pages/expert_review.py")

# Pull derived numbers from shared state
from cost_planner_v2.cp_state import derive

try:
    d = derive()
except Exception:
    d = {}

monthly_all_in = int(round(d.get("monthly_all_in", 0) or 0))
income_total   = int(round(d.get("income_total", 0) or 0))
benefits_total = int(round(d.get("benefits_total", 0) or 0))
gap            = int(round(d.get("gap", 0) or 0))
assets_total   = int(round(d.get("assets_total_effective", 0) or 0))
runway_months  = d.get("runway_months", "Unlimited")

def _fmt_money(n: int) -> str:
    return f"${n:,.0f}"

def _fmt_runway(r):
    return "Unlimited" if r == "Unlimited" else f"{int(round(r)):,} months"

def main() -> None:
    st.set_page_config(page_title="Cost Planner · Timeline", layout="wide")
    apply_cost_planner_theme()

    with cost_planner_page_container():
        render_app_header()
        render_wizard_hero("Your Money Timeline", "Here’s how long your money lasts with the choices so far.")
        if gap <= 0:
            render_wizard_help("Your income + benefits currently cover your estimated monthly costs.")
        else:
            render_wizard_help("If you have a gap, we’ll show how long savings cover the shortfall.")

        render_metrics([
            Metric("All-in monthly cost", _fmt_money(monthly_all_in)),
            Metric("Income + benefits", _fmt_money(income_total + benefits_total)),
            Metric("Monthly gap", _fmt_money(max(gap, 0))),
            Metric("Assets available", _fmt_money(assets_total)),
            Metric("Runway", _fmt_runway(runway_months)),
        ])

        # CTA row
        render_nav_buttons(
            prev=NavButton("← Back to Modules", "tl_back"),
            next=NavButton("Continue → Expert Review", "tl_next", type="primary")
        )

if __name__ == "__main__" or True:
    main()
