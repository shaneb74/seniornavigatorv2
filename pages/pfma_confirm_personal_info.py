"""Plan for MyAdvisor personal info confirmation wireframe."""
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


def render_person_summary(person: dict[str, object]) -> None:
    phone = person.get("phone") or "Add best call-back number"
    email = person.get("email") or "Add email for follow-up notes"
    contact = person.get("preferred_contact") or "Advisor will confirm during call"

    st.markdown(
        f"""
        <table class="summary-table">
          <tbody>
            <tr>
              <td>Phone</td>
              <td class="amount">{phone}</td>
            </tr>
            <tr>
              <td>Email</td>
              <td class="amount">{email}</td>
            </tr>
            <tr>
              <td>Preferred contact method</td>
              <td class="amount">{contact}</td>
            </tr>
          </tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )


apply_turbotax_wizard_theme()

ctx = st.session_state.setdefault("care_context", {"person_name": "Your Loved One"})
person_name = ctx.get("person_name", "Your Loved One")
personal = ctx.get("personal_info")
personal_dict = personal if isinstance(personal, dict) else {}


with cost_planner_page_container():
    render_app_header()
    render_assessment_header(
        "Plan for MyAdvisor · Confirmation",
        persona=person_name,
        mode="Step 7 of 7",
    )

    st.subheader("Personal Info")
    st.caption("Confirm contact information so your advisor can follow up with next steps.")

    render_person_summary(personal_dict)

    render_suggestion(
        "Double-check voicemail and inbox access—advisors often send summaries within a few hours.",
        tone="info",
    )

    agreed = st.checkbox("This looks right", key="pfma_confirm_personal_info_agree", value=False)

    render_wizard_help(
        "If you're done, finish prep to return to the hub with everything marked ready for your advisor.",
    )

    clicked = render_nav_buttons(
        [
            NavButton("Edit personal info", "pfma_personal_edit"),
            NavButton("Back to overview", "pfma_personal_overview"),
            NavButton("Finish prep", "pfma_personal_finish", type="primary", disabled=not agreed),
        ]
    )

    if clicked == "pfma_personal_edit":
        st.switch_page("pages/personal_info.py")
    elif clicked == "pfma_personal_overview":
        st.switch_page("pages/pfma.py")
    elif clicked == "pfma_personal_finish":
        st.switch_page("pages/hub.py")
