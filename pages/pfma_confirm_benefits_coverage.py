"""Plan for MyAdvisor benefits & coverage confirmation wireframe."""
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


def render_benefits_summary(benefits: dict[str, object]) -> None:
    primary = benefits.get("primary_insurance") or "Medicare Part A & B"
    secondary = benefits.get("secondary_insurance") or "Secondary plan not set"
    veteran = "Eligible" if benefits.get("is_veteran") else "Ask about VA support"

    st.markdown(
        f"""
        <table class="summary-table">
          <tbody>
            <tr>
              <td>Primary coverage</td>
              <td class="amount">{primary}</td>
            </tr>
            <tr>
              <td>Secondary coverage</td>
              <td class="amount">{secondary}</td>
            </tr>
            <tr>
              <td>VA benefits</td>
              <td class="amount">{veteran}</td>
            </tr>
          </tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )


apply_turbotax_wizard_theme()

ctx = st.session_state.setdefault("care_context", {"person_name": "Your Loved One"})
person_name = ctx.get("person_name", "Your Loved One")
benefits = ctx.get("benefits")
benefits_dict = benefits if isinstance(benefits, dict) else {}


with cost_planner_page_container():
    render_app_header()
    render_assessment_header(
        "Plan for MyAdvisor · Confirmation",
        persona=person_name,
        mode="Step 6 of 7",
    )

    st.subheader("Benefits & Coverage")
    st.caption("Confirm health coverage and financial support options before the advisor call.")

    render_benefits_summary(benefits_dict)

    render_suggestion(
        "If coverage is unclear, jot down policy numbers so your advisor can verify during or after the call.",
        tone="info",
    )

    agreed = st.checkbox("This looks right", key="pfma_confirm_benefits_agree", value=False)

    render_wizard_help(
        "Need adjustments? Open Benefits & Coverage, update insurance or aid, then refresh this step.",
    )

    clicked = render_nav_buttons(
        [
            NavButton("Edit benefits", "pfma_benefits_edit"),
            NavButton("Back to overview", "pfma_benefits_overview"),
            NavButton("Continue", "pfma_benefits_next", type="primary", disabled=not agreed),
        ]
    )

    if clicked == "pfma_benefits_edit":
        st.switch_page("pages/benefits_coverage.py")
    elif clicked == "pfma_benefits_overview":
        st.switch_page("pages/pfma.py")
    elif clicked == "pfma_benefits_next":
        st.switch_page("pages/pfma_confirm_personal_info.py")
