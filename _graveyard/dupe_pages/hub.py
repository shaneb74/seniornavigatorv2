"""Care Planning Hub landing page shell."""
from __future__ import annotations

import streamlit as st

from senior_nav.components.theme import inject_theme


def main() -> None:
    inject_theme()

    people = st.session_state.get("people", {})
    care_recipient = people.get("care_recipient", {})
    planner = people.get("planner", {})

    display_name = care_recipient.get("preferred_name") or care_recipient.get("name") or "your person"
    planner_display = planner.get("name") or "You"

    st.title("Care Planning Hub")
    st.caption(f"Planning for **{display_name}** - set up by **{planner_display}**")

    # Existing hub tiles remain unchanged for this patch.


if __name__ == "__main__":
    main()
