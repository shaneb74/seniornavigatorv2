# Cost Planner v2 · Modules Hub
from __future__ import annotations
import streamlit as st
from cost_planner_v2.cp_state import ensure_cp
from cost_planner_v2.cp_nav import goto
from ui.components import ModuleCard, ModuleGrid, StatusValue
from ui.state import get_completion, mark_complete, set_completion

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
MODULE_CARDS = [
    {
        "key": "cp_income",
        "title": "Income",
        "body": "Add all monthly income—from Social Security to pensions—so your plan is grounded in reality.",
        "icon": "💵",
        "page": "app_pages/cost_planner_v2/cost_planner_income_v2.py",
    },
    {
        "key": "cp_expenses",
        "title": "Expenses",
        "body": "List everyday and care-related expenses to understand your baseline monthly outflow.",
        "icon": "🧾",
        "page": "app_pages/cost_planner_v2/cost_planner_expenses_v2.py",
    },
    {
        "key": "cp_benefits",
        "title": "Benefits",
        "body": "Capture eligible programs (e.g., VA, Medicare supplements) that can offset care costs.",
        "icon": "🎖️",
        "page": "app_pages/cost_planner_v2/cost_planner_benefits_v2.py",
    },
    {
        "key": "cp_home",
        "title": "Home",
        "body": "Note current living situation, housing costs, and expected changes that affect your plan.",
        "icon": "🏠",
        "page": "app_pages/cost_planner_v2/cost_planner_home_v2.py",
    },
    {
        "key": "cp_home_mods",
        "title": "Home Modifications",
        "body": "Record accessibility projects and safety upgrades that support safer living at home.",
        "icon": "🛠️",
        "page": "app_pages/cost_planner_v2/cost_planner_home_mods_v2.py",
    },
    {
        "key": "cp_liquidity",
        "title": "Liquidity",
        "body": "Track cash, savings, and funds you can tap for near-term care needs.",
        "icon": "💡",
        "page": "app_pages/cost_planner_v2/cost_planner_liquidity_v2.py",
    },
    {
        "key": "cp_caregiver",
        "title": "Caregiver",
        "body": "Estimate family and paid caregiver time to see how support translates into cost.",
        "icon": "🤝",
        "page": "app_pages/cost_planner_v2/cost_planner_caregiver_v2.py",
    },
    {
        "key": "cp_assets",
        "title": "Assets",
        "body": "Add investments and property to complete your financial picture.",
        "icon": "📊",
        "page": "app_pages/cost_planner_v2/cost_planner_assets_v2.py",
    },
    {
        "key": "cp_timeline",
        "title": "Timeline",
        "body": "Map key milestones and expected transitions to keep planning proactive and calm.",
        "icon": "📈",
        "page": "app_pages/cost_planner_v2/cost_planner_timeline_v2.py",
    },
]


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
            st.caption("You can save and return anytime.")

        statuses: dict[str, StatusValue] = {}
        for card in MODULE_CARDS:
            statuses[card["key"]] = get_completion(card["key"])

        core_keys = [card["key"] for card in MODULE_CARDS if card["key"] != "cp_timeline"]
        if core_keys:
            if all(statuses.get(key, "not_started") == "complete" for key in core_keys):
                if statuses.get("cp_timeline") == "complete":
                    mark_complete("cost_planner")
                else:
                    set_completion("cost_planner", "in_progress")
            elif any(statuses.get(key, "not_started") != "not_started" for key in core_keys):
                set_completion("cost_planner", "in_progress")

        with st.container(border=True):
            with ModuleGrid(cols=3, gap="large") as cols:
                column_count = len(cols)
                for idx, card in enumerate(MODULE_CARDS):
                    status = statuses.get(card["key"], "not_started")
                    column = cols[idx % column_count]
                    with column:
                        ModuleCard(
                            icon=card["icon"],
                            title=card["title"],
                            body=card["body"],
                            primary_label="Open",
                            on_primary=lambda path=card["page"]: goto(path),
                            secondary_label="Resume" if status == "in_progress" else None,
                            on_secondary=(lambda path=card["page"]: goto(path)) if status == "in_progress" else None,
                            status=status,
                            testid=f"cp-card-{card['key']}",
                        )

# ✅ Import-time execution under Streamlit
render()
