"""Plan for MyAdvisor care preferences confirmation wireframe."""
from __future__ import annotations

import streamlit as st

from ui.cost_planner_template import (
    NavButton,
    apply_turbotax_wizard_theme,
    cost_planner_page_container,
    render_app_header,
    render_assessment_header,
    render_nav_buttons,
    render_suggestion,
    render_wizard_help,
)


def render_prefs_summary(prefs: dict[str, object]) -> None:
    living_goal = prefs.get("living_goal") or "Stay at home with support"
    social = prefs.get("social_needs") or "Prefers small group interactions"
    communication = prefs.get("communication") or "Share updates with family group text"

    st.markdown(
        f"""
        <table class="summary-table">
          <tbody>
            <tr>
              <td>Living preference</td>
              <td class="amount">{living_goal}</td>
            </tr>
            <tr>
              <td>Social connection</td>
              <td class="amount">{social}</td>
            </tr>
            <tr>
              <td>Communication plan</td>
              <td class="amount">{communication}</td>
            </tr>
          </tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )


apply_turbotax_wizard_theme()

ctx = st.session_state.setdefault("care_context", {"person_name": "Your Loved One"})
person_name = ctx.get("person_name", "Your Loved One")
prefs = ctx.get("care_preferences")
prefs_dict = prefs if isinstance(prefs, dict) else {}


with cost_planner_page_container():
    render_app_header()
    render_assessment_header(
        "Plan for MyAdvisor · Confirmation",
        persona=person_name,
        mode="Step 4 of 7",
    )

    st.subheader("Care Preferences")
    st.caption("Confirm the tone and boundaries you'd like your advisor to respect during the call.")

    render_prefs_summary(prefs_dict)

    render_suggestion(
        "Flag any hard lines—like no overnight moves—so your advisor keeps recommendations aligned.",
        tone="info",
    )

    agreed = st.checkbox("This looks right", key="pfma_confirm_care_prefs_agree", value=False)

    render_wizard_help(
        "Update preferences in Care Preferences anytime; we'll sync them automatically when you reopen this step.",
    )

    clicked = render_nav_buttons(
        [
            NavButton("Edit care preferences", "pfma_care_prefs_edit"),
            NavButton("Back to overview", "pfma_care_prefs_overview"),
            NavButton("Continue", "pfma_care_prefs_next", type="primary", disabled=not agreed),
        ]
    )

    if clicked == "pfma_care_prefs_edit":
        st.switch_page("pages/care_prefs.py")
    elif clicked == "pfma_care_prefs_overview":
        st.switch_page("pages/pfma.py")
    elif clicked == "pfma_care_prefs_next":
        st.switch_page("pages/pfma_confirm_household_legal.py")
