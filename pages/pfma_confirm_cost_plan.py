"""Plan for MyAdvisor cost plan confirmation wireframe."""
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


def render_cost_summary(estimate: dict[str, object]) -> None:
    setting = estimate.get("setting_label") or estimate.get("setting") or "In-home care"
    monthly = estimate.get("estimate_monthly")
    zipcode = estimate.get("zip")
    monthly_text = f"${monthly:,.0f}/mo" if isinstance(monthly, (int, float)) and monthly > 0 else "Estimate coming soon"
    zipcode_text = f"ZIP {zipcode}" if zipcode else "Update ZIP during call"

    st.markdown(
        f"""
        <table class="summary-table">
          <tbody>
            <tr>
              <td>Setting focus</td>
              <td class="amount">{setting}</td>
            </tr>
            <tr>
              <td>Estimated monthly cost</td>
              <td class="amount">{monthly_text}</td>
            </tr>
            <tr>
              <td>Location check</td>
              <td class="amount">{zipcode_text}</td>
            </tr>
          </tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )


apply_turbotax_wizard_theme()

ctx = st.session_state.setdefault("care_context", {"person_name": "Your Loved One"})
person_name = ctx.get("person_name", "Your Loved One")
estimate = ctx.get("cost_estimate")
estimate_dict = estimate if isinstance(estimate, dict) else {}


with cost_planner_page_container():
    render_app_header()
    render_assessment_header(
        "Plan for MyAdvisor · Confirmation",
        persona=person_name,
        mode="Step 2 of 7",
    )

    st.subheader("Cost Plan")
    st.caption("Confirm the high-level cost view so your advisor can tailor financial options.")

    render_cost_summary(estimate_dict)

    render_suggestion(
        "Bring recent bills or statements to the call if you want help exploring payment offsets.",
        tone="warn",
    )

    agreed = st.checkbox("This looks right", key="pfma_confirm_cost_plan_agree", value=False)

    render_wizard_help(
        "Need to make adjustments? Open Cost Planner in another tab, refresh this page, and continue when ready.",
    )

    clicked = render_nav_buttons(
        [
            NavButton("Edit cost plan", "pfma_cost_plan_edit"),
            NavButton("Back to overview", "pfma_cost_plan_overview"),
            NavButton("Continue", "pfma_cost_plan_next", type="primary", disabled=not agreed),
        ]
    )

    if clicked == "pfma_cost_plan_edit":
        st.switch_page("pages/cost_planner_modules.py")
    elif clicked == "pfma_cost_plan_overview":
        st.switch_page("pages/pfma.py")
    elif clicked == "pfma_cost_plan_next":
        st.switch_page("pages/pfma_confirm_care_needs.py")
