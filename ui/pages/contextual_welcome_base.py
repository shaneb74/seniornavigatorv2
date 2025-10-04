"""Base rendering helpers for contextual welcome flows."""
from __future__ import annotations

import streamlit as st

from senior_nav.components.card import card_panel
from senior_nav.components.nav import safe_switch_page
from senior_nav.components.theme import inject_theme

RELATIONSHIP_CHOICES = ["child", "spouse", "sibling", "friend", "other"]


def render(which: str) -> None:
    """Render the contextual welcome experience.

    Args:
        which: Either ``"you"`` for self entry or ``"loved"`` for proxy entry.
    """

    inject_theme()
    st.session_state.setdefault("audiencing", {"entry": "self"})
    st.session_state.setdefault(
        "people",
        {
            "care_recipient": {"name": "", "preferred_name": ""},
            "planner": {"name": "", "relationship": ""},
        },
    )

    entry = st.session_state["audiencing"].get("entry", "self")
    people = st.session_state["people"]

    _left, center_col, _right = st.columns([1, 2, 1])
    with center_col:
        st.title("Welcome")
        st.caption("Let’s set up your planning details. You can change these later.")

        def form_body() -> None:
            care_recipient = people["care_recipient"]
            planner = people["planner"]

            care_recipient["name"] = (
                st.text_input(
                    "Who are we planning for? (full name)",
                    value=care_recipient["name"],
                    placeholder="e.g., Mary Johnson",
                ).strip()
            )
            care_recipient["preferred_name"] = (
                st.text_input(
                    "Preferred name (optional)",
                    value=care_recipient["preferred_name"],
                    placeholder="e.g., Mary",
                ).strip()
            )

            is_proxy = entry == "proxy" or which == "loved"
            if is_proxy:
                planner["name"] = (
                    st.text_input(
                        "Your name",
                        value=planner["name"],
                        placeholder="e.g., John Johnson",
                    ).strip()
                )
                rel_index = (
                    RELATIONSHIP_CHOICES.index(planner["relationship"])
                    if planner["relationship"] in RELATIONSHIP_CHOICES
                    else 0
                )
                planner["relationship"] = st.selectbox(
                    "Your relationship to them",
                    options=RELATIONSHIP_CHOICES,
                    index=rel_index,
                )
            else:
                planner["name"] = care_recipient["name"]
                planner["relationship"] = "self"
                st.info(
                    "You’re planning for yourself. We’ll use your name for both planner and person."
                )

            st.session_state["people"] = {
                "care_recipient": care_recipient,
                "planner": planner,
            }

            errors: list[str] = []
            if not care_recipient["name"]:
                errors.append("Please enter the name of the person you’re planning for.")
            if is_proxy and not planner["name"]:
                errors.append("Please enter your name.")
            if is_proxy and not planner["relationship"]:
                errors.append("Please select your relationship.")

            for message in errors:
                st.warning(message)

            disabled = len(errors) > 0
            if st.button(
                "Continue", type="primary", use_container_width=True, disabled=disabled
            ):
                for key in ("name", "preferred_name"):
                    people["care_recipient"][key] = people["care_recipient"][key].strip()
                people["planner"]["name"] = people["planner"]["name"].strip()
                st.session_state["people"] = people

                st.session_state.setdefault("gcp_status", "start")
                st.session_state.setdefault("cp_status", "start")
                st.session_state.setdefault("pfma_status", "start")

                safe_switch_page("ui/pages/hub.py")

        card_panel(
            title=(
                "Planning for yourself"
                if entry == "self" or which == "you"
                else "Planning for a loved one"
            ),
            subtitle=None,
            body=form_body,
        )
