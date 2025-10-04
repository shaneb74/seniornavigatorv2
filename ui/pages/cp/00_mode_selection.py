"""Mode selection step for the cost planner."""
from __future__ import annotations

import streamlit as st

from senior_nav.components import buttons, card
from senior_nav.cost_planner import nav, state


def _open_login_modal() -> None:
    st.session_state["__cp_show_login_modal__"] = True


def render() -> None:
    buttons.page_start()
    copy = state.get_copy()
    mode_copy = copy["mode_selection"]

    st.markdown(f"### {mode_copy['headline']}")

    cards = mode_copy["cards"]
    col_explore, col_plan = st.columns(2)

    with col_explore:
        card.render_action(
            cards["explore"]["title"],
            cards["explore"]["body"],
            cards["explore"]["cta"],
            key="cp_mode_explore",
            on_click=_select_exploring,
        )

    with col_plan:
        card.render_action(
            cards["plan"]["title"],
            cards["plan"]["body"],
            cards["plan"]["cta"],
            key="cp_mode_plan",
            on_click=_open_login_modal,
        )

    if st.session_state.get("__cp_show_login_modal__"):
        modal = mode_copy["login_modal"]
        with st.modal(modal["title"]):
            st.write(modal["body"])
            if buttons.primary(modal["confirm"], key="cp_login_confirm"):
                st.session_state["__cp_show_login_modal__"] = False
                _set_mode("planning")
                nav.go_next()

    buttons.page_end()


def _set_mode(mode: str) -> None:
    state.set_mode(mode)
    if mode == "exploring":
        # Reset suggestions so exploring mode stays quiet.
        state.get_state()["ui"].setdefault("suggestions_shown", set()).clear()


def _select_exploring() -> None:
    _set_mode("exploring")
    nav.go_next()
