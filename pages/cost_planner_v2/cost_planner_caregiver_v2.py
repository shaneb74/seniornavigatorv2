from __future__ import annotations

from typing import Any, Dict

import streamlit as st

from cost_planner_v2 import _shared as shared
from senior_nav.components import buttons
from senior_nav.components.choice_chips import choice_single
from ui.theme import inject_theme


st.set_page_config(page_title="Cost Planner · Caregiver Support", layout="wide")


SUPPORT_OPTIONS = [
    {"value": "yes", "label": "Yes"},
    {"value": "no", "label": "No"},
    {"value": "unsure", "label": "Unsure"},
]


def _ensure_defaults(cp: Dict[str, Any]) -> None:
    cp.setdefault("cg_unpaid_available", "unsure")


def main() -> None:
    inject_theme()
    cp = shared.cp_state()
    shared.ensure_in_progress("caregiver")
    buttons.page_start()

    _ensure_defaults(cp)

    with shared.page_container():
        st.markdown(
            """
            <div style="margin:2rem 0 1.5rem;">
              <h1 style="margin:0 0 .5rem 0;">Caregiver Support</h1>
              <p style="margin:0;color:var(--ink-muted);">Share the informal support you have and whether you budget for respite.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("""<div style='display:flex;justify-content:flex-end;'>""", unsafe_allow_html=True)
        shared.render_reset_link("caregiver")
        st.markdown("""</div>""", unsafe_allow_html=True)

        support = choice_single(
            "Do you have unpaid caregiver support?",
            SUPPORT_OPTIONS,
            value=cp.get("cg_unpaid_available", "unsure"),
            key="cg_support",
        )
        cp["cg_unpaid_available"] = support

        errors: list[str] = []

        if support == "yes":
            hours = st.number_input(
                "Estimated unpaid hours per week",
                min_value=0.0,
                value=float(cp.get("cg_unpaid_hours_per_week") or 0.0),
                key="cg_hours",
            )
            cp["cg_unpaid_hours_per_week"] = hours
            if hours == 0:
                errors.append("Enter an amount to continue.")
        else:
            cp.pop("cg_unpaid_hours_per_week", None)

        relief = st.number_input(
            "Budget for respite / relief ($/mo, optional)",
            min_value=0.0,
            value=float(cp.get("cg_relief_budget_monthly") or 0.0),
            key="cg_relief",
        )
        cp["cg_relief_budget_monthly"] = relief

        if support == "yes" and errors:
            st.markdown(
                "<div style='color:#B42318;font-size:.85rem;margin-top:.5rem;'>Enter the unpaid hours to continue.</div>",
                unsafe_allow_html=True,
            )

        summary = ""
        if support == "yes":
            hours_val = float(cp.get("cg_unpaid_hours_per_week") or 0.0)
            summary = f"Unpaid {hours_val:,.0f} hrs/wk"
        elif support == "no":
            summary = "No unpaid support"
        else:
            summary = "Caregiver support TBD"
        shared.set_summary("caregiver", summary)

        next_disabled = support == "yes" and bool(errors)

        shared.render_nav(
            "pages/cost_planner_v2/cost_planner_liquidity_v2.py",
            "pages/cost_planner_v2/cost_planner_assets_v2.py",
            next_disabled=next_disabled,
            on_continue=lambda: (
                shared.set_status("caregiver", "done"),
                shared.set_summary("caregiver", summary),
            ),
        )

        if next_disabled and shared.status_value("caregiver") == "done":
            shared.set_status("caregiver", "in_progress")

    buttons.page_end()


if __name__ == "__main__":
    main()
