from __future__ import annotations

from typing import Any, Dict, List, Tuple

import streamlit as st

from cost_planner_v2 import _shared as shared
from senior_nav.components import buttons
from senior_nav.components.choice_chips import choice_single
from ui.theme import inject_theme


st.set_page_config(page_title="Cost Planner · Home Modifications", layout="wide")


LABEL_OPTIONS = [
    "Ramp",
    "Bathroom",
    "Widen Doors",
    "Lighting",
    "Other",
]

TIMING_OPTIONS = [
    {"value": "one-time", "label": "One-time"},
    {"value": "this year", "label": "This year"},
    {"value": "next year", "label": "Next year"},
    {"value": "phase over 2+ years", "label": "Phase over 2+ years"},
]


def _ensure_rows(cp: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = cp.setdefault("home_mods", [])
    if not rows:
        rows.append({
            "label": "Ramp",
            "cost": None,
            "when": "one-time",
            "notes": "",
        })
    return rows


def _render_row(index: int, row: Dict[str, Any], *, can_remove: bool) -> Tuple[Dict[str, Any], bool]:
    removed = False
    with st.container(border=True):
        cols = st.columns([1.1, 0.9, 0.9])
        with cols[0]:
            selection = st.selectbox(
                "Project",
                LABEL_OPTIONS,
                index=LABEL_OPTIONS.index(row.get("label", "Ramp"))
                if row.get("label") in LABEL_OPTIONS
                else 0,
                key=f"home_mod_label_{index}",
            )
            row["label"] = selection
        with cols[1]:
            cost = st.number_input(
                "Estimated cost",
                min_value=0.0,
                value=float(row.get("cost") or 0.0),
                key=f"home_mod_cost_{index}",
                step=500.0,
            )
            row["cost"] = cost
        with cols[2]:
            when_value = row.get("when") or "one-time"
            when = choice_single(
                "Timing",
                TIMING_OPTIONS,
                value=when_value,
                key=f"home_mod_when_{index}",
            )
            row["when"] = when

        notes = st.text_area(
            "Notes (optional)",
            value=row.get("notes", ""),
            key=f"home_mod_notes_{index}",
            height=80,
        )
        row["notes"] = notes

        if can_remove:
            st.markdown(
                "<div style='display:flex;justify-content:flex-end'>",
                unsafe_allow_html=True,
            )
            if buttons.link("Remove", key=f"home_mod_remove_{index}"):
                removed = True
            st.markdown("</div>", unsafe_allow_html=True)

    return row, removed


def main() -> None:
    inject_theme()
    cp = shared.cp_state()
    shared.ensure_in_progress("home_mods")
    buttons.page_start()

    rows = _ensure_rows(cp)
    removal_index: int | None = None

    with shared.page_container():
        st.markdown(
            """
            <div style="margin:2rem 0 1.5rem;">
              <h1 style="margin:0 0 .5rem 0;">Home Modifications</h1>
              <p style="margin:0;color:var(--ink-muted);">Optional—only if you foresee changes to make home safer.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("""<div style='display:flex;justify-content:flex-end;'>""", unsafe_allow_html=True)
        shared.render_reset_link("home_mods")
        st.markdown("""</div>""", unsafe_allow_html=True)

        errors: Dict[int, str] = {}
        active_rows: List[Dict[str, Any]] = []

        for idx, data in enumerate(list(rows)):
            rows[idx], remove_clicked = _render_row(idx, data, can_remove=len(rows) > 1)
            if remove_clicked:
                removal_index = idx
            row = rows[idx]

            filled_any = (row.get("cost") or 0) > 0 or bool(row.get("notes"))

            if filled_any:
                active_rows.append(row)
                if row.get("cost") is None:
                    errors[idx] = "Enter an amount to continue."
                elif row.get("cost", 0) < 0:
                    errors[idx] = "Enter an amount to continue."

            if idx in errors:
                st.markdown(
                    f"<div style='color:#B42318;font-size:.85rem;margin:-.25rem 0 .75rem 0;'>{errors[idx]}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown("""<div style='height:.5rem'></div>""", unsafe_allow_html=True)

        if removal_index is not None:
            rows.pop(removal_index)

        if buttons.link("Add another project", key="home_mod_add"):
            rows.append({
                "label": "Ramp",
                "cost": None,
                "when": "one-time",
                "notes": "",
            })

        subtotal = sum(float(r.get("cost") or 0.0) for r in active_rows)
        cp["home_mods_total"] = float(subtotal)

        st.markdown("""<div style='height:1rem'></div>""", unsafe_allow_html=True)
        st.markdown(
            f"<div class='sn-card' style='text-align:right;'><strong>Subtotal:</strong> {shared.format_currency(subtotal)}</div>",
            unsafe_allow_html=True,
        )

        summary = ""
        if active_rows:
            labels = ", ".join(r.get("label") for r in active_rows if r.get("label"))
            summary = f"{labels} · {shared.format_currency(subtotal)} one-time"
        shared.set_summary("home_mods", summary)

        st.markdown("""<div style='height:1.5rem'></div>""", unsafe_allow_html=True)

        next_disabled = bool(errors)

        shared.render_nav(
            "pages/cost_planner_v2/cost_planner_home_v2.py",
            "pages/cost_planner_v2/cost_planner_liquidity_v2.py",
            next_disabled=next_disabled,
            on_continue=lambda: (
                shared.set_status("home_mods", "done"),
                shared.set_summary("home_mods", summary),
            ),
        )

        if next_disabled and shared.status_value("home_mods") == "done":
            shared.set_status("home_mods", "in_progress")

    buttons.page_end()


if __name__ == "__main__":
    main()
