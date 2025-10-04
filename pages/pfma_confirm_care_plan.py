"""Plan for MyAdvisor care plan confirmation wireframe."""
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


def render_summary_block(recommendation: str) -> None:
    st.markdown(
        """
        <table class="summary-table">
          <tbody>
            <tr>
              <td>Advisor-ready recommendation</td>
              <td class="amount">{recommendation}</td>
            </tr>
            <tr>
              <td>Next best option</td>
              <td class="amount">Capture during call</td>
            </tr>
          </tbody>
        </table>
        """.format(recommendation=recommendation or "Recommendation TBD"),
        unsafe_allow_html=True,
    )


apply_turbotax_wizard_theme()

ctx = st.session_state.setdefault("care_context", {"person_name": "Your Loved One"})
person_name = ctx.get("person_name", "Your Loved One")
recommendation = ctx.get("gcp_recommendation") or "Recommendation ready soon"


with cost_planner_page_container():
    render_app_header()
    render_assessment_header(
        "Plan for MyAdvisor · Confirmation",
        persona=person_name,
        mode="Step 1 of 7",
    )

    st.subheader("Care Plan")
    st.caption("Confirm the plan highlights your advisor should know before the call.")

    render_summary_block(recommendation)

    render_suggestion(
        "Bring up any concerns about timelines or logistics—your advisor can flag them for follow-up.",
        tone="info",
    )

    agreed = st.checkbox("This looks right", key="pfma_confirm_care_plan_agree", value=False)

    render_wizard_help(
        "Need edits? Jump back to Guided Care Plan, update the recommendation, then return here to reconfirm.",
    )

    clicked = render_nav_buttons(
        [
            NavButton("Edit care plan", "pfma_care_plan_edit"),
            NavButton("Back to overview", "pfma_care_plan_overview"),
            NavButton("Continue", "pfma_care_plan_next", type="primary", disabled=not agreed),
        ]
    )

    if clicked == "pfma_care_plan_edit":
        st.switch_page("pages/gcp.py")
    elif clicked == "pfma_care_plan_overview":
        st.switch_page("pages/pfma.py")
    elif clicked == "pfma_care_plan_next":
        st.switch_page("pages/pfma_confirm_cost_plan.py")
