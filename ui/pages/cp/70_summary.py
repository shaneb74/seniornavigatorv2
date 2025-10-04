"""Summary step."""
from __future__ import annotations

import streamlit as st

from senior_nav.cost_planner import nav, state


def render() -> None:
    copy = state.get_copy()
    summary_copy = copy["summary"]
    app_copy = copy["app"]
    totals = app_copy["sidebar"]["totals_rows"]

    st.markdown(f"### {summary_copy['title']}")
    st.write(summary_copy["intro"])

    rows_html = "".join(
        f"<tr><td>{label}</td><td style='text-align:right;font-weight:600;'>{value}</td></tr>"
        for label, value in totals
    )
    st.markdown(
        f"""
        <table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
          <thead>
            <tr style="text-align:left; border-bottom:1px solid var(--sn-color-border);">
              <th>{summary_copy['table_headers'][0]}</th>
              <th style="text-align:right;">{summary_copy['table_headers'][1]}</th>
            </tr>
          </thead>
          <tbody>
            {rows_html}
          </tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )

    action_col1, action_col2 = st.columns(2)
    with action_col1:
        st.button(summary_copy["actions"]["download"], key="cp_summary_download", disabled=True)
    with action_col2:
        st.button(summary_copy["actions"]["share"], key="cp_summary_share", disabled=True)

    back_col, next_col = st.columns([1, 1])
    with back_col:
        st.button(app_copy["navigation"]["back"], key="cp_summary_back", on_click=nav.go_previous)
    with next_col:
        st.button(app_copy["navigation"]["continue"], key="cp_summary_continue", on_click=nav.go_next)
