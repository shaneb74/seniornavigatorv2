from __future__ import annotations

from typing import Any, Dict, List, Tuple

import streamlit as st

from pages.cost_planner_v2 import _shared as shared
from senior_nav.components import buttons
from senior_nav.components.choice_chips import choice_single
from ui.theme import inject_theme


st.set_page_config(page_title="Cost Planner · Benefits & Offsets", layout="wide")


PROGRAM_OPTIONS = [
    "Medicaid",
    "Medicare Advantage Add-Ons",
    "LTC Insurance",
    "VA Benefits",
    "Other",
]

FREQUENCY_OPTIONS = [
    {"value": "monthly", "label": "Monthly"},
    {"value": "annually", "label": "Annually"},
]


def _ensure_rows(cp: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = cp.setdefault("benefits", [])
    if not rows:
        rows.append({
            "program": "Medicaid",
            "amount": None,
            "frequency": "monthly",
            "notes": "",
        })
    return rows


def _render_row(index: int, row: Dict[str, Any], *, can_remove: bool) -> Tuple[Dict[str, Any], bool, str | None]:
    removed = False
    helper: str | None = None
    with st.container(border=True):
        cols = st.columns([1.2, 0.9, 0.9])
        with cols[0]:
            selection = st.selectbox(
                "Program",
                PROGRAM_OPTIONS,
                index=PROGRAM_OPTIONS.index(row.get("program", "Medicaid"))
                if row.get("program") in PROGRAM_OPTIONS
                else 0,
                key=f"benefit_program_{index}",
            )
            row["program"] = selection
        with cols[1]:
            amount = st.number_input(
                "Amount",
                min_value=0.0,
                value=float(row.get("amount") or 0.0),
                key=f"benefit_amount_{index}",
                step=100.0,
            )
            row["amount"] = amount
        with cols[2]:
            freq_value = row.get("frequency") or "monthly"
            freq = choice_single(
                "Frequency",
                FREQUENCY_OPTIONS,
                value=freq_value,
                key=f"benefit_freq_{index}",
            )
            row["frequency"] = freq

        notes = st.text_input(
            "Notes (optional)",
            value=row.get("notes", ""),
            key=f"benefit_notes_{index}",
        )
        row["notes"] = notes

        if can_remove:
            st.markdown(
                "<div style='display:flex;justify-content:flex-end'>",
                unsafe_allow_html=True,
            )
            if buttons.link("Remove", key=f"benefit_remove_{index}"):
                removed = True
            st.markdown("</div>", unsafe_allow_html=True)

        if row.get("program") == "Medicaid" and (row.get("amount") or 0) > 0:
            helper = "Medicaid coverage structures vary; confirm with advisor."

    return row, removed, helper


def main() -> None:
    inject_theme()
    cp = shared.cp_state()
    shared.ensure_in_progress("benefits")
    buttons.page_start()

    rows = _ensure_rows(cp)
    removal_index: int | None = None

    medicaid_context = False
    gcp_state = st.session_state.get("gcp", {})
    if gcp_state.get("payment_context") == "medicaid":
        medicaid_context = True
    aud = st.session_state.get("audiencing", {}).get("qualifiers", {})
    if aud.get("on_medicaid"):
        medicaid_context = True

    with shared.page_container():
        st.markdown(
            """
            <div style="margin:2rem 0 1.5rem;">
              <h1 style="margin:0 0 .5rem 0;">Benefits & Offsets</h1>
              <p style="margin:0;color:var(--ink-muted);">Capture benefits and other offsets that reduce your monthly spend.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if medicaid_context:
            st.info("We’ll tailor offsets for Medicaid.")

        st.markdown("""<div style='display:flex;justify-content:flex-end;margin-top:.5rem;'>""", unsafe_allow_html=True)
        shared.render_reset_link("benefits")
        st.markdown("""</div>""", unsafe_allow_html=True)

        errors: Dict[int, str] = {}
        active_rows: List[Dict[str, Any]] = []

        for idx, data in enumerate(list(rows)):
            rows[idx], remove_clicked, helper = _render_row(idx, data, can_remove=len(rows) > 1)
            if remove_clicked:
                removal_index = idx
            row = rows[idx]

            filled_any = (row.get("amount") or 0) > 0 or bool(row.get("notes"))

            if filled_any:
                active_rows.append(row)
                if not row.get("program"):
                    errors[idx] = "Choose a program to continue."
                elif row.get("amount") is None:
                    errors[idx] = "Enter an amount to continue."
                elif row.get("amount", 0) < 0:
                    errors[idx] = "Enter an amount to continue."
                elif not row.get("frequency"):
                    errors[idx] = "Choose a frequency so we can estimate your monthly plan."

            if helper and idx not in errors:
                st.markdown(
                    f"<div style='margin:.25rem 0;color:#027A48;font-size:.85rem;'>{helper}</div>",
                    unsafe_allow_html=True,
                )

            if idx in errors:
                st.markdown(
                    f"<div style='color:#B42318;font-size:.85rem;margin:-.25rem 0 .75rem 0;'>{errors[idx]}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown("""<div style='height:.5rem'></div>""", unsafe_allow_html=True)

        if removal_index is not None:
            rows.pop(removal_index)

        if buttons.link("Add another offset", key="benefit_add"):
            rows.append({
                "program": "Medicaid",
                "amount": None,
                "frequency": "monthly",
                "notes": "",
            })

        monthly_total = sum(shared.monthly_from_amount(r.get("amount"), r.get("frequency")) for r in active_rows)
        cp["benefits_total_monthly"] = float(monthly_total)

        st.markdown("""<div style='height:1rem'></div>""", unsafe_allow_html=True)
        st.markdown(
            f"<div class='sn-card' style='background:rgba(2,122,72,0.08);border-color:rgba(2,122,72,0.24);'>"
            f"<strong>Offsets per month:</strong> −{shared.format_currency(monthly_total)}</div>",
            unsafe_allow_html=True,
        )

        summary = ""
        if active_rows:
            summary = (
                f"{len(active_rows)} offset{'s' if len(active_rows) != 1 else ''} · −{shared.format_currency(monthly_total)}/mo"
            )
        shared.set_summary("benefits", summary)

        st.markdown("""<div style='height:1.5rem'></div>""", unsafe_allow_html=True)

        next_disabled = bool(errors)

        shared.render_nav(
            "pages/cost_planner_v2/cost_planner_expenses_v2.py",
            "pages/cost_planner_v2/cost_planner_home_v2.py",
            next_disabled=next_disabled,
            on_continue=lambda: (
                shared.set_status("benefits", "done"),
                shared.set_summary("benefits", summary),
            ),
        )

        if next_disabled and shared.status_value("benefits") == "done":
            shared.set_status("benefits", "in_progress")

    buttons.page_end()


if __name__ == "__main__":
    main()
