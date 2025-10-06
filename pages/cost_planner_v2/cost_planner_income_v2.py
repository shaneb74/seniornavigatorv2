from __future__ import annotations

from typing import Any, Dict, List, Tuple

import streamlit as st

from pages.cost_planner_v2 import _shared as shared
from senior_nav.components import buttons
from senior_nav.components.choice_chips import choice_single
from ui.theme import inject_theme


st.set_page_config(page_title="Cost Planner · Income", layout="wide")


SOURCE_OPTIONS = [
    "",
    "Social Security",
    "Pension",
    "Annuity",
    "Employment",
    "VA",
    "Other",
]

FREQUENCY_OPTIONS = [
    {"value": "monthly", "label": "Monthly"},
    {"value": "annually", "label": "Annually"},
]


def _ensure_rows(cp: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = cp.setdefault("income_sources", [])
    if not rows:
        rows.append({
            "type": "",
            "amount": None,
            "frequency": "monthly",
            "notes": "",
        })
    return rows


def _render_row(index: int, row: Dict[str, Any], *, can_remove: bool) -> Tuple[Dict[str, Any], bool]:
    removed = False
    with st.container(border=True):
        cols = st.columns([1.2, 0.9, 0.9])
        with cols[0]:
            selection = st.selectbox(
                "Income source",
                SOURCE_OPTIONS,
                index=SOURCE_OPTIONS.index(row.get("type", "")) if row.get("type", "") in SOURCE_OPTIONS else 0,
                key=f"income_type_{index}",
            )
            row["type"] = selection
        with cols[1]:
            amount = st.number_input(
                "Amount",
                min_value=0.0,
                value=float(row.get("amount") or 0.0),
                key=f"income_amount_{index}",
                step=100.0,
                help="Enter an estimated amount (before offsets).",
            )
            row["amount"] = amount
        with cols[2]:
            freq_value = row.get("frequency") or "monthly"
            choice = choice_single(
                "Frequency",
                FREQUENCY_OPTIONS,
                value=freq_value,
                key=f"income_freq_{index}",
            )
            row["frequency"] = choice

        notes = st.text_input(
            "Notes (optional)",
            value=row.get("notes", ""),
            key=f"income_notes_{index}",
        )
        row["notes"] = notes

        if can_remove:
            with st.container():
                st.markdown(
                    "<div style='display:flex;justify-content:flex-end'>",
                    unsafe_allow_html=True,
                )
                if buttons.link("Remove", key=f"income_remove_{index}"):
                    removed = True
                st.markdown("</div>", unsafe_allow_html=True)

    return row, removed


def main() -> None:
    inject_theme()
    cp = shared.cp_state()
    shared.ensure_in_progress("income")
    buttons.page_start()

    rows = _ensure_rows(cp)
    removal_index: int | None = None

    with shared.page_container():
        st.markdown(
            """
            <div style="margin:2rem 0 1.5rem;">
              <h1 style="margin:0 0 .5rem 0;">Income</h1>
              <p style="margin:0;color:var(--ink-muted);">Enter your recurring income. You can estimate.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("""<div style='display:flex;justify-content:flex-end;'>""", unsafe_allow_html=True)
        shared.render_reset_link("income")
        st.markdown("""</div>""", unsafe_allow_html=True)

        st.markdown("""<div style='height:.5rem'></div>""", unsafe_allow_html=True)

        errors: Dict[int, str] = {}
        active_rows: List[Dict[str, Any]] = []

        for idx, data in enumerate(list(rows)):
            rows[idx], remove_clicked = _render_row(idx, data, can_remove=len(rows) > 1)
            if remove_clicked:
                removal_index = idx
            row = rows[idx]

            filled_any = any([
                row.get("type"),
                (row.get("amount") or 0) > 0,
                bool(row.get("notes")),
            ])

            if filled_any:
                active_rows.append(row)
                if not row.get("type"):
                    errors[idx] = "Choose a source type to continue."
                elif row.get("amount") is None:
                    errors[idx] = "Enter an amount to continue."
                elif row.get("amount", 0) < 0:
                    errors[idx] = "Enter an amount to continue."
                elif not row.get("frequency"):
                    errors[idx] = "Choose a frequency so we can estimate your monthly plan."

            if idx in errors:
                st.markdown(
                    f"<div style='color:#B42318;font-size:.85rem;margin:-.25rem 0 .75rem 0;'>{errors[idx]}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown("""<div style='height:.5rem'></div>""", unsafe_allow_html=True)

        if removal_index is not None:
            rows.pop(removal_index)

        if buttons.link("Add another income source", key="income_add"):
            rows.append({"type": "", "amount": None, "frequency": "monthly", "notes": ""})

        monthly_total = sum(shared.monthly_from_amount(r.get("amount"), r.get("frequency")) for r in active_rows)
        cp["income_total_monthly"] = float(monthly_total)

        st.markdown(
            f"<div class='sn-card' style='margin-top:1.5rem;'><strong>Your monthly income total:</strong> {shared.format_currency(monthly_total)}</div>",
            unsafe_allow_html=True,
        )

        summary = ""
        if active_rows:
            summary = f"{len(active_rows)} source{'s' if len(active_rows) != 1 else ''} · {shared.format_currency(monthly_total)}/mo"
        shared.set_summary("income", summary)

        st.markdown("""<div style='height:1.5rem'></div>""", unsafe_allow_html=True)

        next_disabled = bool(errors)

        shared.render_nav(
            "pages/cost_planner_v2/cost_planner_modules_hub_v2.py",
            "pages/cost_planner_v2/cost_planner_expenses_v2.py",
            next_disabled=next_disabled,
            on_continue=lambda: (
                shared.set_status("income", "done"),
                shared.set_summary("income", summary),
            ),
        )

        if next_disabled and shared.status_value("income") == "done":
            shared.set_status("income", "in_progress")

    buttons.page_end()


if __name__ == "__main__":
    main()
