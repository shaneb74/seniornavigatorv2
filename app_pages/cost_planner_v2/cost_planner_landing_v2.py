# Cost Planner v2 · Landing
from __future__ import annotations

import streamlit as st

# ---------------- Theme helpers (match Income pattern) ----------------
try:
    from ui.cost_planner_template import (
        apply_cost_planner_theme,
        cost_planner_page_container,
        render_app_header,
        render_wizard_hero,
        render_wizard_help,
    )
except Exception:
    # graceful fallbacks
    def apply_cost_planner_theme():
        st.markdown(
            """
        <style>
          :root{--brand:#0B5CD8;--surface:#f6f8fa;--ink:#111418}
          .sn-card{
            background:var(--surface);
            border:1px solid rgba(0,0,0,.08);
            border-radius:14px;
            padding:clamp(1rem,2vw,1.5rem);
          }
        </style>
        """,
            unsafe_allow_html=True,
        )

    from contextlib import contextmanager

    @contextmanager
    def cost_planner_page_container():
        yield

    def render_app_header():
        st.markdown("### Cost Planner")

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
                    st.switch_page("app_pages/cost_planner_v2/cost_planner_timeline_v2.py")

    def render_wizard_help(text: str):
        st.info(text)


_ESTIMATE_BY_SETTING = {
    "In-home care": 3800,
    "Assisted Living": 5200,
    "Memory Care": 6800,
    "Memory Care (High Acuity)": 8200,
}

_ALLOWED = set(_ESTIMATE_BY_SETTING.keys())

_ALIASES = {
    "aging in place": "In-home care",
    "in home": "In-home care",
    "in-home": "In-home care",
    "home with help": "In-home care",
    "home care": "In-home care",
    "al": "Assisted Living",
    "assisted": "Assisted Living",
    "assisted living": "Assisted Living",
    "memory": "Memory Care",
    "memory care": "Memory Care",
    "mc": "Memory Care",
    "memory care (high acuity)": "Memory Care (High Acuity)",
    "high acuity memory": "Memory Care (High Acuity)",
    "high-acuity memory": "Memory Care (High Acuity)",
    "mc high": "Memory Care (High Acuity)",
}

_SELECT_CHOICES = [
    "In-home care",
    "Assisted Living",
    "Memory Care",
    "Memory Care (High Acuity)",
]

_SHOW_EXPLORER_KEY = "cpv2_cost_explorer_open"
_SELECT_STATE_KEY = "cpv2_cost_explorer_choice"
_ESTIMATE_FOOTNOTE = (
    "Estimates are illustrative and vary by location and provider. "
    "Sign in to add your income, benefits, housing, and assets."
)


def _normalize_setting(label: str | None) -> str | None:
    if not label:
        return None
    s = label.strip().lower()

    for k in _ALLOWED:
        if s == k.lower():
            return k

    if s in _ALIASES:
        return _ALIASES[s]

    if "home" in s or "aging" in s or "place" in s:
        return "In-home care"
    if "assist" in s:
        return "Assisted Living"
    if "memory" in s and ("high" in s or "acuity" in s or "complex" in s):
        return "Memory Care (High Acuity)"
    if "memory" in s:
        return "Memory Care"

    if "snf" in s or "skilled" in s or "nursing" in s:
        return None

    return None


def _estimate_monthly_cost(setting_label: str | None) -> int | None:
    s = _normalize_setting(setting_label or "")
    return _ESTIMATE_BY_SETTING.get(s) if s else None


def _get_gcp_setting_from_snapshot() -> str | None:
    gcp_state = st.session_state.get("gcp")
    if isinstance(gcp_state, dict):
        raw = gcp_state.get("recommended_setting")
        if isinstance(raw, str):
            return raw
    return None


def _format_currency(value: int | None) -> str:
    if value is None:
        return "—"
    return f"${value:,.0f}"


def _safe_switch_page(target: str) -> None:
    try:
        st.switch_page(target)  # type: ignore[attr-defined]
    except Exception:
        st.warning(f"Navigation failed. Verify {target} is registered in app.py.")


def _render_action_cards() -> str | None:
    authed = bool(st.session_state.get("is_authenticated", False))
    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.subheader("Start Planning")
            st.caption(
                "Sign in to update your income, benefits, housing, and assets for a full Cost Planner view."
            )
            if st.button(
                "Start Planning",
                type="primary",
                disabled=not authed,
                help=None if authed else "Sign in required",
                key="cpv2_start_planning",
                use_container_width=True,
            ):
                _safe_switch_page("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py")

    with col2:
        with st.container(border=True):
            st.subheader("Explore my care costs")
            st.caption(
                "Preview monthly care costs using the Guided Care Plan recommendation or pick a setting."
            )
            if st.button(
                "Explore my care costs",
                type="secondary",
                key="cpv2_explore_costs",
                use_container_width=True,
            ):
                st.session_state[_SHOW_EXPLORER_KEY] = True

    return _normalize_setting(_get_gcp_setting_from_snapshot())


def _render_cost_explorer(recommendation: str | None) -> None:
    recommendation = recommendation if recommendation in _ALLOWED else None

    with st.container(border=True):
        if recommendation:
            st.subheader(f"Based on your Guided Care Plan recommendation: {recommendation}.")
            estimate = _estimate_monthly_cost(recommendation)
        else:
            st.subheader("Choose a care setting to preview costs.")
            choice = st.selectbox(
                "Care setting",
                _SELECT_CHOICES,
                key=_SELECT_STATE_KEY,
            )
            estimate = _estimate_monthly_cost(choice)

        if recommendation is None and estimate is None:
            st.caption("Select a care setting to see an estimated monthly cost.")
            return

        st.metric("Estimated monthly cost", _format_currency(estimate))
        st.caption(_ESTIMATE_FOOTNOTE)


# ---------------- Page content ----------------
def render() -> None:
    apply_cost_planner_theme()

    render_app_header()
    with cost_planner_page_container():
        render_wizard_hero(
            "Cost Planner",
            "Estimate care costs quickly or dig into detailed planning when you sign in.",
        )
        render_wizard_help("Get a quick estimate now, then add more detail when you're ready.")

        recommendation = _render_action_cards()

        if recommendation not in _ALLOWED:
            st.info(
                "No recommendation found yet. You can still preview by choosing a care setting below, "
                "or complete the Guided Care Plan for a more tailored estimate."
            )
            recommendation = None

        show_explorer = st.session_state.get(_SHOW_EXPLORER_KEY, bool(recommendation))
        if recommendation and _SHOW_EXPLORER_KEY not in st.session_state:
            st.session_state[_SHOW_EXPLORER_KEY] = True

        if show_explorer:
            _render_cost_explorer(recommendation)

        # Actions
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Start planning", type="primary", use_container_width=True):
                st.switch_page("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
        with col2:
            if st.button("Jump to Timeline (dev)", use_container_width=True):
                st.switch_page("app_pages/cost_planner_v2/cost_planner_timeline_v2.py")

# ✅ Import-time execution under Streamlit
render()
