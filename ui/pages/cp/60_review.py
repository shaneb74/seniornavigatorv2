"""Review step."""
from __future__ import annotations

import streamlit as st

from senior_nav.components import banners, layout
from senior_nav.cost_planner import nav, state


def render() -> None:
    copy = state.get_copy()
    review_copy = copy["review"]
    app_copy = copy["app"]

    st.markdown(f"### {review_copy['title']}")
    st.write(review_copy["intro"])

    for drawer_key, label in review_copy["accordion"].items():
        drawer_copy = copy["drawers"][drawer_key]
        with st.expander(label, expanded=drawer_key == "housing"):
            st.write(drawer_copy["caption"])
            layout.render_drawer_summary(
                app_copy["drawer_summary_label"],
                drawer_copy["subtotal"],
                drawer_copy["summary_hint"],
            )

    st.markdown(f"#### {review_copy['suggestions_title']}")
    for suggestion in review_copy["suggestions"]:
        banners.render(suggestion["level"], suggestion["title"], suggestion["body"])

    back_col, next_col = st.columns([1, 1])
    with back_col:
        st.button(app_copy["navigation"]["back"], key="cp_review_back", on_click=nav.go_previous)
    with next_col:
        st.button(app_copy["navigation"]["continue"], key="cp_review_continue", on_click=nav.go_next)
