"""Shared utilities for Cost Planner v2 Streamlit pages."""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Callable

import streamlit as st

from cost_planner_v2.cp_nav import goto
from cost_planner_v2.cp_state import ensure_cp
from senior_nav.components import buttons


MODULE_DEFS: dict[str, dict[str, Any]] = {
    "income": {
        "title": "Income",
        "description": "Monthly income sources and estimated totals.",
        "page": "pages/cost_planner_v2/cost_planner_income_v2.py",
        "reset_keys": ["income_sources", "income_total_monthly", "summary_income"],
    },
    "expenses": {
        "title": "Expenses",
        "description": "Recurring living, care, and medical expenses.",
        "page": "pages/cost_planner_v2/cost_planner_expenses_v2.py",
        "reset_keys": ["expense_items", "expenses_total_monthly", "summary_expenses"],
    },
    "benefits": {
        "title": "Benefits & Offsets",
        "description": "Coverage that reduces your monthly spend.",
        "page": "pages/cost_planner_v2/cost_planner_benefits_v2.py",
        "reset_keys": ["benefits", "benefits_total_monthly", "summary_benefits"],
    },
    "home": {
        "title": "Home & Housing",
        "description": "Mortgage, rent, and other housing drivers.",
        "page": "pages/cost_planner_v2/cost_planner_home_v2.py",
        "reset_keys": [
            "home_own",
            "home_mortgage_payment",
            "home_insurance",
            "home_taxes",
            "home_hoa",
            "home_rent",
            "summary_home",
        ],
    },
    "home_mods": {
        "title": "Home Modifications",
        "description": "Projects to make the home safer or more accessible.",
        "page": "pages/cost_planner_v2/cost_planner_home_mods_v2.py",
        "reset_keys": ["home_mods", "home_mods_total", "summary_home_mods"],
    },
    "liquidity": {
        "title": "Liquidity & Coverage",
        "description": "Cash buffers and insurance that can cover care costs.",
        "page": "pages/cost_planner_v2/cost_planner_liquidity_v2.py",
        "reset_keys": [
            "liquidity",
            "coverage",
            "liquidity_total",
            "ltc_coverage_monthly_equiv",
            "summary_liquidity",
        ],
    },
    "caregiver": {
        "title": "Caregiver Support",
        "description": "Unpaid help and respite budgets.",
        "page": "pages/cost_planner_v2/cost_planner_caregiver_v2.py",
        "reset_keys": [
            "cg_unpaid_available",
            "cg_unpaid_hours_per_week",
            "cg_relief_budget_monthly",
            "summary_caregiver",
        ],
    },
    "assets": {
        "title": "Assets & Resources",
        "description": "Long-term resources that inform planning conversations.",
        "page": "pages/cost_planner_v2/cost_planner_assets_v2.py",
        "reset_keys": ["assets", "summary_assets"],
    },
    "timeline": {
        "title": "Timeline & Projection",
        "description": "12-month runway view using your inputs.",
        "page": "pages/cost_planner_v2/cost_planner_timeline_v2.py",
        "reset_keys": [
            "timeline_projection",
            "timeline_flag_depletion_month",
            "timeline_include_mods",
            "timeline_include_ltc_coverage",
            "timeline_show_detail",
            "summary_timeline",
        ],
    },
}

MODULE_ORDER: list[str] = [
    "income",
    "expenses",
    "benefits",
    "home",
    "home_mods",
    "liquidity",
    "caregiver",
    "assets",
    "timeline",
]


@dataclass
class StatusMeta:
    label: str
    fg: str
    bg: str


STATUS_LOOKUP: dict[str, StatusMeta] = {
    "done": StatusMeta("Done", "#0B5CD8", "rgba(11, 92, 216, 0.08)"),
    "in_progress": StatusMeta("In progress", "#475467", "rgba(17, 20, 24, 0.08)"),
    "not_started": StatusMeta("Not started", "#475467", "rgba(17, 20, 24, 0.04)"),
}


def cp_state() -> dict[str, Any]:
    cp = ensure_cp()
    for module in MODULE_DEFS:
        cp.setdefault(f"status_{module}", "not_started")
        cp.setdefault(f"summary_{module}", "")
    return cp


@contextmanager
def page_container(max_width: int = 940):
    st.markdown(
        f"<div class='cp-page' style='max-width:{max_width}px;margin:0 auto;'>",
        unsafe_allow_html=True,
    )
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)


def status_value(module: str) -> str:
    cp = cp_state()
    return cp.get(f"status_{module}", "not_started")


def set_status(module: str, value: str) -> None:
    cp = cp_state()
    cp[f"status_{module}"] = value


def ensure_in_progress(module: str) -> None:
    current = status_value(module)
    if current == "not_started":
        set_status(module, "in_progress")


def set_summary(module: str, summary: str) -> None:
    cp_state()[f"summary_{module}"] = summary


def reset_module(module: str) -> None:
    cp = cp_state()
    config = MODULE_DEFS.get(module, {})
    for key in config.get("reset_keys", []):
        cp.pop(key, None)
    cp[f"status_{module}"] = "not_started"
    cp[f"summary_{module}"] = ""


def module_summary(module: str) -> str:
    cp = cp_state()
    return cp.get(f"summary_{module}", "") or "Add details to get started"


def render_status_pill(module: str) -> None:
    status = status_value(module)
    meta = STATUS_LOOKUP.get(status, STATUS_LOOKUP["not_started"])
    st.markdown(
        f"""
        <span style="display:inline-flex;align-items:center;gap:.35rem;padding:.25rem .5rem;border-radius:999px;
                     background:{meta.bg};color:{meta.fg};font-size:.8rem;font-weight:600;">
            <span style="width:.5rem;height:.5rem;border-radius:999px;background:{meta.fg};display:inline-block"></span>
            {meta.label}
        </span>
        """,
        unsafe_allow_html=True,
    )


def render_nav(
    prev_path: str | None,
    next_path: str | None,
    *,
    next_disabled: bool = False,
    on_continue: Callable[[], None] | None = None,
) -> None:
    cols = st.columns(2)
    with cols[0]:
        if prev_path:
            back_key = prev_path.replace("/", "_")
            if buttons.secondary("Back", key=f"nav_back_{back_key}"):
                goto(prev_path)
    with cols[1]:
        if next_path:
            next_key = next_path.replace("/", "_")
            if buttons.primary(
                "Continue",
                key=f"nav_next_{next_key}",
                disabled=next_disabled,
            ):
                if not next_disabled:
                    if on_continue is not None:
                        on_continue()
                    goto(next_path)


def render_reset_link(module: str, *, label: str = "Reset module") -> None:
    if buttons.link(label, key=f"reset_{module}"):
        reset_module(module)
        st.experimental_rerun()


def monthly_from_amount(amount: float | None, frequency: str | None) -> float:
    if amount is None:
        return 0.0
    if frequency == "annually":
        return float(amount) / 12.0
    return float(amount)


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def format_currency_precision(value: float) -> str:
    return f"${value:,.2f}"


def legend_row() -> None:
    pills = []
    for status_key in ("done", "in_progress", "not_started"):
        meta = STATUS_LOOKUP[status_key]
        pills.append(
            f"<span style='display:inline-flex;align-items:center;gap:.35rem;padding:.25rem .5rem;border-radius:999px;"
            f"background:{meta.bg};color:{meta.fg};font-size:.8rem;font-weight:600;'>"
            f"<span style='width:.5rem;height:.5rem;border-radius:999px;background:{meta.fg};display:inline-block'></span>"
            f"{meta.label}</span>"
        )
    st.markdown(
        "<div style='display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;font-size:.85rem;color:var(--ink-muted);'>"
        "<span style='margin-right:.5rem;'>Status:</span>"
        + "".join(pills)
        + "</div>",
        unsafe_allow_html=True,
    )


def goto_module(module: str) -> None:
    config = MODULE_DEFS.get(module)
    if config:
        goto(config["page"])


def modules_data() -> Iterable[tuple[str, dict[str, Any]]]:
    for module in MODULE_ORDER:
        yield module, MODULE_DEFS[module]
