"""Plan for MyAdvisor care needs confirmation wireframe."""
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


def render_needs_summary(needs: dict[str, object]) -> None:
    activities = needs.get("adls") or "Activities of daily living to review"
    safety = needs.get("safety") or "Safety considerations captured in Guided Care Plan"
    stamina = needs.get("stamina") or "Energy and stamina conversation points"

    st.markdown(
        f"""
        <table class="summary-table">
          <tbody>
            <tr>
              <td>Daily support focus</td>
              <td class="amount">{activities}</td>
            </tr>
            <tr>
              <td>Safety & risks</td>
              <td class="amount">{safety}</td>
            </tr>
            <tr>
              <td>Energy & stamina</td>
              <td class="amount">{stamina}</td>
            </tr>
          </tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )


apply_turbotax_wizard_theme()

ctx = st.session_state.setdefault("care_context", {"person_name": "Your Loved One"})
person_name = ctx.get("person_name", "Your Loved One")
needs = ctx.get("care_needs")
needs_dict = needs if isinstance(needs, dict) else {}


with cost_planner_page_container():
    render_app_header()
    render_assessment_header(
        "Plan for MyAdvisor · Confirmation",
        persona=person_name,
        mode="Step 3 of 7",
    )

    st.subheader("Care Needs")
    st.caption("Highlight what day-to-day help is most important for the advisor to know.")

    render_needs_summary(needs_dict)

    render_suggestion(
        "If needs change quickly, jot down notes right before the call so you can give the advisor the latest picture.",
        tone="info",
    )

    agreed = st.checkbox("This looks right", key="pfma_confirm_care_needs_agree", value=False)

    render_wizard_help(
        "Need to tweak? Revisit the Care Needs module, refresh, and mark it ready here when finished.",
    )

    clicked = render_nav_buttons(
        [
            NavButton("Edit care needs", "pfma_care_needs_edit"),
            NavButton("Back to overview", "pfma_care_needs_overview"),
            NavButton("Continue", "pfma_care_needs_next", type="primary", disabled=not agreed),
        ]
    )

    if clicked == "pfma_care_needs_edit":
        st.switch_page("pages/care_needs.py")
    elif clicked == "pfma_care_needs_overview":
        st.switch_page("pages/pfma.py")
    elif clicked == "pfma_care_needs_next":
        st.switch_page("pages/pfma_confirm_care_prefs.py")
