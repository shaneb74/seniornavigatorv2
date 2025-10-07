# Cost Planner · Expenses (v2)
from __future__ import annotations

import streamlit as st

from ui.cost_planner_data import MODULE_FIELD_MAP
from ui.cost_planner_forms import compute_gap, cp_state, render_fields


def render() -> None:
    st.header("Expenses")
    st.caption("Capture current monthly spending areas so we can compare them against income.")

    fields = MODULE_FIELD_MAP["expenses"]
    valid, _ = render_fields(fields)

    st.markdown("---")
    if st.button("Save & back to Modules", type="primary", disabled=not valid):
        compute_gap(cp_state())
        try:
            st.switch_page("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
        except Exception:
            st.session_state["nav_target"] = "app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py"
            st.rerun()

        # Same two-button layout/behavior you had before
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("◀︎ Back to Modules", use_container_width=True):
                st.switch_page("app_pages/cost_planner_v2/cost_planner_modules_hub_v2.py")
        with col2:
            st.button("Save & Continue", disabled=True, help="Coming soon", use_container_width=True)

render()
