"""Qualifiers step to tailor drawer visibility."""
from __future__ import annotations

import streamlit as st

from senior_nav.components import banners, formbits
from senior_nav.cost_planner import nav, state


def render() -> None:
    copy = state.get_copy()
    qualifiers_copy = copy["qualifiers"]
    app_copy = copy["app"]
    flags = state.get_flags()
    cp_state = state.get_state()

    st.markdown(f"### {qualifiers_copy['title']}")
    st.write(qualifiers_copy["description"])

    with st.form("cp_qualifiers_form"):
        contribution = formbits.choice_group(
            qualifiers_copy["contribution_style"]["label"],
            qualifiers_copy["contribution_style"]["options"],
            key="cp_contribution_style",
            default=cp_state["qualifiers"].get("contribution_style", "unified"),
        )
        owns_home = formbits.choice_group(
            qualifiers_copy["owns_home"]["label"],
            qualifiers_copy["owns_home"]["options"],
            key="cp_owns_home",
            default="yes" if cp_state["qualifiers"].get("owns_home") else "no",
            horizontal=True,
        )
        is_veteran = formbits.choice_group(
            qualifiers_copy["is_veteran"]["label"],
            qualifiers_copy["is_veteran"]["options"],
            key="cp_is_veteran",
            default="yes" if cp_state["qualifiers"].get("is_veteran") else "no",
            horizontal=True,
        )

        submitted = st.form_submit_button(qualifiers_copy["continue"])

    if flags.get("medicaid_unsure"):
        banner = qualifiers_copy["medicaid_banner"]
        banners.render("info", banner["title"], banner["body"])

    back_col, next_col = st.columns([1, 1])
    with back_col:
        st.button(app_copy["navigation"]["back"], key="cp_qual_back", on_click=nav.go_previous)
    with next_col:
        if submitted:
            state.update_qualifier("contribution_style", contribution)
            state.update_qualifier("owns_home", owns_home == "yes")
            state.update_qualifier("is_veteran", is_veteran == "yes")
            nav.go_next()
        else:
            st.write(" ")
