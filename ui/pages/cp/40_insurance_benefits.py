"""Insurance & benefits drawer UI."""
from __future__ import annotations

import streamlit as st

from senior_nav.components import buttons, formbits, layout
from senior_nav.cost_planner import nav, state

DRAWER_KEY = "insurance_benefits"


def render() -> None:
    buttons.page_start()
    copy = state.get_copy()
    drawer_copy = copy["drawers"][DRAWER_KEY]
    app_copy = copy["app"]
    nav.mark_drawer_open(DRAWER_KEY)

    st.markdown(f"### {drawer_copy['title']}")
    st.caption(drawer_copy["caption"])

    qualifiers = state.get_state()["qualifiers"]
    hidden_fields = set()
    if qualifiers.get("is_veteran") is False:
        hidden_fields.add("va_benefits")

    with st.form(f"cp_{DRAWER_KEY}_form"):
        for field_key, label in drawer_copy["fields"].items():
            if field_key in hidden_fields:
                continue
            formbits.currency_input(label, key=f"cp_{DRAWER_KEY}_{field_key}")
        with buttons.variant("primary"):
            submitted = st.form_submit_button(app_copy["navigation"]["continue"])

    layout.render_drawer_summary(
        app_copy["drawer_summary_label"],
        drawer_copy["subtotal"],
        drawer_copy["summary_hint"],
    )

    back_col, next_col = st.columns([1, 1])
    with back_col:
        with buttons.variant("secondary"):
            if buttons.secondary(app_copy["navigation"]["back"], key="cp_insurance_back"):
                nav.go_previous()
    with next_col:
        if submitted:
            nav.mark_drawer_complete(DRAWER_KEY)
            nav.go_next()
        else:
            st.write(" ")
    buttons.page_end()
