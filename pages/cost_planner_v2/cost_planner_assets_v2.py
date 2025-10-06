from __future__ import annotations

from typing import Any, Dict, List, Tuple

import streamlit as st

from pages.cost_planner_v2 import _shared as shared
from senior_nav.components import buttons
from ui.theme import inject_theme


st.set_page_config(page_title="Cost Planner · Assets & Resources", layout="wide")


TYPE_OPTIONS = [
    "Home (Primary)",
    "Second Property",
    "Retirement (401k/IRA)",
    "Brokerage",
    "Vehicle",
    "Other",
]


def _ensure_rows(cp: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = cp.setdefault("assets", [])
    if not rows:
        rows.append({
            "type": "Home (Primary)",
            "est_value": None,
            "notes": "",
        })
    return rows


def _render_row(index: int, row: Dict[str, Any], *, can_remove: bool) -> Tuple[Dict[str, Any], bool]:
    removed = False
    with st.container(border=True):
        cols = st.columns([1.1, 0.9])
        with cols[0]:
            selection = st.selectbox(
                "Asset type",
                TYPE_OPTIONS,
                index=TYPE_OPTIONS.index(row.get("type", "Home (Primary)"))
                if row.get("type") in TYPE_OPTIONS
                else 0,
                key=f"asset_type_{index}",
            )
            row["type"] = selection
        with cols[1]:
            value = st.number_input(
                "Estimated value",
                min_value=0.0,
                value=float(row.get("est_value") or 0.0),
                key=f"asset_value_{index}",
                step=5000.0,
            )
            row["est_value"] = value

        notes = st.text_area(
            "Notes (optional)",
            value=row.get("notes", ""),
            key=f"asset_notes_{index}",
            height=80,
        )
        row["notes"] = notes

        if can_remove:
            st.markdown(
                "<div style='display:flex;justify-content:flex-end'>",
                unsafe_allow_html=True,
            )
            if buttons.link("Remove", key=f"asset_remove_{index}"):
                removed = True
            st.markdown("</div>", unsafe_allow_html=True)

    return row, removed


def main() -> None:
    inject_theme()
    cp = shared.cp_state()
    shared.ensure_in_progress("assets")
    buttons.page_start()

    rows = _ensure_rows(cp)
    removal_index: int | None = None

    with shared.page_container():
        st.markdown(
            """
            <div style="margin:2rem 0 1.5rem;">
              <h1 style="margin:0 0 .5rem 0;">Assets & Resources</h1>
              <p style="margin:0;color:var(--ink-muted);">These help us discuss long-term options; we won’t assume you’ll sell anything.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("""<div style='display:flex;justify-content:flex-end;'>""", unsafe_allow_html=True)
        shared.render_reset_link("assets")
        st.markdown("""</div>""", unsafe_allow_html=True)

        errors: Dict[int, str] = {}
        active_rows: List[Dict[str, Any]] = []

        for idx, data in enumerate(list(rows)):
            rows[idx], remove_clicked = _render_row(idx, data, can_remove=len(rows) > 1)
            if remove_clicked:
                removal_index = idx
            row = rows[idx]

            filled_any = (row.get("est_value") or 0) > 0 or bool(row.get("notes"))

            if filled_any:
                active_rows.append(row)
                if row.get("est_value") is not None and row.get("est_value") < 0:
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

        if buttons.link("Add another asset", key="asset_add"):
            rows.append({
                "type": "Home (Primary)",
                "est_value": None,
                "notes": "",
            })

        if active_rows:
            labels = [r.get("type") for r in active_rows if r.get("type")]
            summary = " + ".join(labels[:2])
            if len(labels) > 2:
                summary += f" + {len(labels) - 2} more"
        else:
            summary = ""
        shared.set_summary("assets", summary)

        shared.render_nav(
            "pages/cost_planner_v2/cost_planner_caregiver_v2.py",
            "pages/cost_planner_v2/cost_planner_timeline_v2.py",
            next_disabled=False,
            on_continue=lambda: (
                shared.set_status("assets", "done"),
                shared.set_summary("assets", summary),
            ),
        )

    buttons.page_end()


if __name__ == "__main__":
    main()
