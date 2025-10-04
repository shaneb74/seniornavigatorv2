"""Plan for MyAdvisor household & legal confirmation wireframe."""
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


def render_household_summary(household: dict[str, object]) -> None:
    decision_maker = household.get("decision_maker") or "Confirm who signs paperwork"
    legal_docs = household.get("legal_docs") or "Durable POA uploaded?"
    household_notes = household.get("household_notes") or "Household schedule and pets"

    st.markdown(
        f"""
        <table class="summary-table">
          <tbody>
            <tr>
              <td>Primary decision maker</td>
              <td class="amount">{decision_maker}</td>
            </tr>
            <tr>
              <td>Legal documents</td>
              <td class="amount">{legal_docs}</td>
            </tr>
            <tr>
              <td>Household notes</td>
              <td class="amount">{household_notes}</td>
            </tr>
          </tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )


apply_turbotax_wizard_theme()

ctx = st.session_state.setdefault("care_context", {"person_name": "Your Loved One"})
person_name = ctx.get("person_name", "Your Loved One")
household = ctx.get("household_legal")
household_dict = household if isinstance(household, dict) else {}


with cost_planner_page_container():
    render_app_header()
    render_assessment_header(
        "Plan for MyAdvisor · Confirmation",
        persona=person_name,
        mode="Step 5 of 7",
    )

    st.subheader("Household & Legal")
    st.caption("Confirm paperwork and household context so your advisor can prep resources in advance.")

    render_household_summary(household_dict)

    render_suggestion(
        "If any documents are missing, your advisor can help outline the steps to complete them—just mention it.",
        tone="warn",
    )

    agreed = st.checkbox("This looks right", key="pfma_confirm_household_legal_agree", value=False)

    render_wizard_help(
        "Open the Household & Legal section to upload files or tweak notes, then refresh this confirmation step.",
    )

    clicked = render_nav_buttons(
        [
            NavButton("Edit household & legal", "pfma_household_edit"),
            NavButton("Back to overview", "pfma_household_overview"),
            NavButton("Continue", "pfma_household_next", type="primary", disabled=not agreed),
        ]
    )

    if clicked == "pfma_household_edit":
        st.switch_page("pages/household_legal.py")
    elif clicked == "pfma_household_overview":
        st.switch_page("pages/pfma.py")
    elif clicked == "pfma_household_next":
        st.switch_page("pages/pfma_confirm_benefits_coverage.py")
