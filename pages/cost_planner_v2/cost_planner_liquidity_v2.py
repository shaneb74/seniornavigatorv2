from __future__ import annotations

from typing import Any, Dict

import streamlit as st

from pages.cost_planner_v2 import _shared as shared
from senior_nav.components import buttons
from ui.theme import inject_theme


st.set_page_config(page_title="Cost Planner · Liquidity & Coverage", layout="wide")


LIQUIDITY_FIELDS = [
    ("cash_checking", "Cash & checking"),
    ("savings", "Savings"),
    ("hsa_fsa", "HSA / FSA balances"),
    ("emergency_fund", "Emergency fund"),
]

COVERAGE_FIELDS = [
    ("ltc_insurance_daily_max", "LTC insurance daily max ($)"),
    ("ltc_insurance_days_covered", "Days covered per benefit period"),
]


def _ensure_defaults(cp: Dict[str, Any]) -> None:
    cp.setdefault("liquidity", {})
    cp.setdefault("coverage", {})


def main() -> None:
    inject_theme()
    cp = shared.cp_state()
    shared.ensure_in_progress("liquidity")
    buttons.page_start()

    _ensure_defaults(cp)
    liquidity = cp["liquidity"]
    coverage = cp["coverage"]

    with shared.page_container():
        st.markdown(
            """
            <div style="margin:2rem 0 1.5rem;">
              <h1 style="margin:0 0 .5rem 0;">Liquidity & Coverage</h1>
              <p style="margin:0;color:var(--ink-muted);">Capture available liquid resources and insurance that can buffer costs.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("""<div style='display:flex;justify-content:flex-end;'>""", unsafe_allow_html=True)
        shared.render_reset_link("liquidity")
        st.markdown("""</div>""", unsafe_allow_html=True)

        st.subheader("Liquidity", divider=True)
        for field_key, label in LIQUIDITY_FIELDS:
            liquidity[field_key] = st.number_input(
                f"{label} ($)",
                min_value=0.0,
                value=float(liquidity.get(field_key) or 0.0),
                key=f"liq_{field_key}",
                step=500.0,
            )

        st.subheader("Coverage", divider=True)
        coverage["ltc_insurance_daily_max"] = st.number_input(
            "LTC insurance daily max ($)",
            min_value=0.0,
            value=float(coverage.get("ltc_insurance_daily_max") or 0.0),
            key="coverage_daily",
            step=50.0,
        )
        coverage["ltc_insurance_days_covered"] = st.number_input(
            "Days covered per benefit period",
            min_value=0,
            value=int(coverage.get("ltc_insurance_days_covered") or 0),
            key="coverage_days",
            step=15,
        )

        st.markdown("""<div style='height:1rem'></div>""", unsafe_allow_html=True)

        liquidity_total = sum(float(liquidity.get(key) or 0.0) for key, _ in LIQUIDITY_FIELDS)
        cp["liquidity_total"] = float(liquidity_total)

        daily = float(coverage.get("ltc_insurance_daily_max") or 0.0)
        days = int(coverage.get("ltc_insurance_days_covered") or 0)
        coverage_monthly = 0.0
        if daily > 0 and days > 0:
            months = max(days / 30.0, 1)
            coverage_monthly = (daily * days) / months
        cp["ltc_coverage_monthly_equiv"] = float(coverage_monthly)

        with st.container(border=True):
            st.markdown(
                f"<div style='display:flex;flex-direction:column;gap:.5rem;'>"
                f"<div><strong>Total liquid resources:</strong> {shared.format_currency(liquidity_total)}</div>"
                f"<div><strong>LTC coverage (monthly equivalent):</strong> {shared.format_currency_precision(coverage_monthly)}</div>"
                "</div>",
                unsafe_allow_html=True,
            )

        summary_parts = []
        if liquidity_total > 0:
            summary_parts.append(f"Cash + Savings: {shared.format_currency(liquidity_total)}")
        if coverage_monthly > 0:
            summary_parts.append(f"LTC coverage ≈ {shared.format_currency_precision(coverage_monthly)}/mo")
        summary = " · ".join(summary_parts)
        shared.set_summary("liquidity", summary)

        shared.render_nav(
            "pages/cost_planner_v2/cost_planner_home_mods_v2.py",
            "pages/cost_planner_v2/cost_planner_caregiver_v2.py",
            next_disabled=False,
            on_continue=lambda: (
                shared.set_status("liquidity", "done"),
                shared.set_summary("liquidity", summary),
            ),
        )

    buttons.page_end()


if __name__ == "__main__":
    main()
