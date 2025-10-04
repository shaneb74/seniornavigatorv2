"""Confirm step."""
from __future__ import annotations

import streamlit as st

from senior_nav.components import buttons, formbits
from senior_nav.cost_planner import nav, state


def render() -> None:
    buttons.page_start()
    copy = state.get_copy()
    confirm_copy = copy["confirm"]
    app_copy = copy["app"]

    st.markdown(f"### {confirm_copy['title']}")
    st.write(confirm_copy["intro"])

    _ = formbits.checklist(confirm_copy["checklist"], key_prefix="cp_confirm_list")
    ready = formbits.confirmation_checkbox(confirm_copy["confirm_label"], key="cp_confirm_ready")

    action_col1, action_col2 = st.columns([1, 1])
    with action_col1:
        with buttons.variant("secondary"):
            if buttons.secondary(app_copy["navigation"]["back"], key="cp_confirm_back"):
                nav.go_previous()
    with action_col2:
        if buttons.primary(confirm_copy["share_button"], key="cp_confirm_share", disabled=not ready):
            st.success(confirm_copy["share_note"])
            st.balloons()

    st.caption(confirm_copy["share_note"])
    buttons.page_end()
