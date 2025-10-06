from __future__ import annotations

from typing import Any, Dict

import streamlit as st

from cost_planner_v2 import _shared as shared
from senior_nav.components import buttons
from senior_nav.components.choice_chips import choice_single
from ui.theme import inject_theme


st.set_page_config(page_title="Cost Planner · Home & Housing", layout="wide")


OWN_OPTIONS = [
    {"value": "yes", "label": "Yes"},
    {"value": "no", "label": "No"},
    {"value": "unsure", "label": "Unsure"},
]


def _ensure_defaults(cp: Dict[str, Any]) -> None:
    cp.setdefault("home_own", "")


def main() -> None:
    inject_theme()
    cp = shared.cp_state()
    shared.ensure_in_progress("home")
    buttons.page_start()

    _ensure_defaults(cp)

    with shared.page_container():
        st.markdown(
            """
            <div style="margin:2rem 0 1.5rem;">
              <h1 style="margin:0 0 .5rem 0;">Home & Housing</h1>
              <p style="margin:0;color:var(--ink-muted);">Determine your housing situation and the major cost drivers.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("""<div style='display:flex;justify-content:flex-end;'>""", unsafe_allow_html=True)
        shared.render_reset_link("home")
        st.markdown("""</div>""", unsafe_allow_html=True)

        owner_choice = cp.get("home_own") or "unsure"
        owner_choice = choice_single(
            "Do you own your home?",
            OWN_OPTIONS,
            value=owner_choice,
            key="home_own_choice",
        )
        cp["home_own"] = owner_choice

        st.info("These help estimate net housing costs.")

        errors: list[str] = []

        if owner_choice == "yes":
            col1, col2 = st.columns(2)
            with col1:
                mortgage = st.number_input(
                    "Mortgage payment ($/mo)",
                    min_value=0.0,
                    value=float(cp.get("home_mortgage_payment") or 0.0),
                    key="home_mortgage",
                )
                cp["home_mortgage_payment"] = mortgage
            with col2:
                insurance = st.number_input(
                    "Home insurance ($/mo)",
                    min_value=0.0,
                    value=float(cp.get("home_insurance") or 0.0),
                    key="home_insurance",
                )
                cp["home_insurance"] = insurance

            col3, col4 = st.columns(2)
            with col3:
                taxes = st.number_input(
                    "Property taxes ($/mo)",
                    min_value=0.0,
                    value=float(cp.get("home_taxes") or 0.0),
                    key="home_taxes",
                )
                cp["home_taxes"] = taxes
            with col4:
                hoa = st.number_input(
                    "HOA / dues ($/mo, optional)",
                    min_value=0.0,
                    value=float(cp.get("home_hoa") or 0.0),
                    key="home_hoa",
                )
                cp["home_hoa"] = hoa

        elif owner_choice == "no":
            rent = st.number_input(
                "Rent ($/mo)",
                min_value=0.0,
                value=float(cp.get("home_rent") or 0.0),
                key="home_rent",
            )
            cp["home_rent"] = rent

        else:
            st.markdown(
                "<div style='display:flex;justify-content:flex-start;margin:.75rem 0;'>",
                unsafe_allow_html=True,
            )
            if buttons.link("I’ll fill this later", key="home_skip"):
                shared.set_status("home", "in_progress")
                shared.set_summary("home", "Unsure about housing costs")
                shared.goto_module("home_mods")
            st.markdown("</div>", unsafe_allow_html=True)

        summary = ""
        if owner_choice == "yes":
            total = sum(
                float(cp.get(key) or 0.0)
                for key in ["home_mortgage_payment", "home_insurance", "home_taxes", "home_hoa"]
            )
            summary = f"Owner · {shared.format_currency(total)}/mo"
        elif owner_choice == "no":
            rent_val = float(cp.get("home_rent") or 0.0)
            summary = f"Renter · {shared.format_currency(rent_val)}/mo"
        elif owner_choice == "unsure":
            summary = "Unsure about housing costs"

        if summary:
            shared.set_summary("home", summary)

        next_disabled = owner_choice in {"yes", "no"} and bool(errors)

        shared.render_nav(
            "pages/cost_planner_v2/cost_planner_benefits_v2.py",
            "pages/cost_planner_v2/cost_planner_home_mods_v2.py",
            next_disabled=next_disabled,
            on_continue=lambda: (
                shared.set_status("home", "done"),
                shared.set_summary("home", summary),
            ),
        )

        if next_disabled and shared.status_value("home") == "done":
            shared.set_status("home", "in_progress")

    buttons.page_end()


if __name__ == "__main__":
    main()
