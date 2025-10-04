"""Plan for MyAdvisor TurboTax-style wireframe."""
from __future__ import annotations

import streamlit as st

from ui.cost_planner_template import (
    NavButton,
    apply_turbotax_wizard_theme,
    cost_planner_page_container,
    render_app_header,
    render_module_cards,
    render_nav_buttons,
    render_suggestion,
    render_wizard_help,
    render_wizard_hero,
)


apply_turbotax_wizard_theme()

ctx = st.session_state.setdefault(
    "care_context",
    {
        "person_name": "Your Loved One",
        "care_flags": {},
        "planning_mode": "estimating",
    },
)

person_name = ctx.get("person_name", "Your Loved One")


with cost_planner_page_container():
    render_app_header()
    render_wizard_hero(
        "Plan for MyAdvisor",
        "Book your advisor call, then confirm a few details so the conversation starts with the right context.",
    )

    render_suggestion(
        "Navi can stay with you during the call to capture notes or next steps—just let your advisor know you'd like the help.",
        tone="info",
    )

    card_trigger = render_module_cards(
        [
            {
                "title": "Book your advisor call",
                "description": "Choose a time that works for you. We'll send a confirmation email with the meeting link.",
                "status": "Recommended first",
                "actions": [
                    {
                        "label": "Book now",
                        "key": "pfma_book_call",
                        "type": "primary",
                    }
                ],
            },
            {
                "title": "Confirm details",
                "description": "Review the plan, costs, and paperwork so your advisor can jump straight into solutions.",
                "status": "Takes about 2 minutes",
                "status_class": "positive",
                "actions": [
                    {
                        "label": "Start confirmation",
                        "key": "pfma_start_confirm",
                        "type": "primary",
                    }
                ],
            },
        ]
    )

    if card_trigger == "pfma_book_call":
        st.switch_page("pages/appointment_booking.py")
    elif card_trigger == "pfma_start_confirm":
        st.switch_page("pages/pfma_confirm_care_plan.py")

    render_wizard_help(
        f"We'll pull in everything you've already saved for {person_name}. Update anything that changed and mark it ready for your advisor.",
    )

    clicked = render_nav_buttons(
        [
            NavButton("Back to Hub", "pfma_back_hub"),
        ]
    )

    if clicked == "pfma_back_hub":
        st.switch_page("pages/hub.py")
