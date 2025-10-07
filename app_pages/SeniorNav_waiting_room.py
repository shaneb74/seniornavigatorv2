from __future__ import annotations

import random

import streamlit as st
<<<<<<< Updated upstream
from ui.theme import inject_theme
from app_pages.seniornav_util import top_nav, safe_switch

inject_theme()
=======

from app_pages.seniornav_util import safe_switch, top_nav

>>>>>>> Stashed changes
top_nav()

st.markdown("## Waiting Room Hub")
st.caption("Stay engaged while we finalize your personalized plan.")
st.markdown(
    """
    <div style="margin-bottom:1.2rem;color:#475569;font-size:15px;line-height:1.55;">
      Take a breather, explore a quick resource, or line up the next conversation
      while your Concierge Advisor prepares the next steps.
    </div>
    """,
    unsafe_allow_html=True,
)

MESSAGE_KEY = "waiting_room_message"
TRIVIA_TIPS = [
    "Brain boost: Try naming three healthy snacks that begin with the same letter.",
    "Memory jog: Share one favorite story with a friend today—storytelling keeps cognition sharp.",
    "Balance break: Stand up, hold a countertop, and rise on your toes ten times for circulation.",
]

<<<<<<< Updated upstream
with c1:
    st.markdown("#### Trivia Time")
    st.caption("Fun fact: Did you know 1 in 5 seniors miss a med dose? Click for a tip!")
    st.button("Get Tip", use_container_width=True)

with c2:
    st.markdown("#### Partner Spotlight")
    st.caption("Explore our trusted partners — vetted for your peace of mind.")
    if st.button("See All Partners", use_container_width=True):
        safe_switch("pages/SeniorNav_trusted_partners.py")

with c3:
    st.markdown("#### Second Opinion")
    st.caption("Get a quick geriatrics review before your call — no cost.")
    st.button("Chat Now", use_container_width=True)
=======

def _set_message(message: str) -> None:
    st.session_state[MESSAGE_KEY] = message


MODULES = [
    {
        "icon": "🧩",
        "title": "Trivia & Brain Teasers",
        "description": "Give your mind a quick workout with light prompts and fun facts.",
        "button": "Play trivia",
        "key": "waiting_trivia",
        "action": "trivia",
    },
    {
        "icon": "🤝",
        "title": "Partner Spotlight",
        "description": "Browse vetted partners who specialize in senior housing, care, and support.",
        "button": "See all partners",
        "key": "waiting_partners",
        "action": "partners",
        "path": "pages/SeniorNav_trusted_partners.py",
    },
    {
        "icon": "🩺",
        "title": "Second Opinion",
        "description": "Line up a physician consult to review care options before your next decision.",
        "button": "Request a second opinion",
        "key": "waiting_second_opinion",
        "action": "message",
        "message": (
            "Let your advisor know you'd like a physician consult. We'll coordinate a geriatrics "
            "second opinion to review medications, safety, and care recommendations."
        ),
    },
    {
        "icon": "📚",
        "title": "Resource Library",
        "description": "Find checklists, benefits guides, and funding ideas tailored for senior care.",
        "button": "View resources",
        "key": "waiting_resources",
        "action": "message",
        "message": (
            "Resource hub coming soon: we'll share funding guides, housing checklists, and benefit "
            "eligibility tools to keep planning easy between advisor sessions."
        ),
    },
]

cols = st.columns(2, gap="large")
for index, module in enumerate(MODULES):
    column = cols[index % len(cols)]
    with column:
        with st.container(border=True):
            st.markdown(f"### {module['icon']} {module['title']}")
            st.caption(module["description"])
            if module["action"] == "trivia":
                if st.button(module["button"], key=module["key"], type="primary"):
                    _set_message(random.choice(TRIVIA_TIPS))
            elif module["action"] == "partners":
                if st.button(module["button"], key=module["key"], type="primary"):
                    safe_switch(module["path"])
            else:
                if st.button(module["button"], key=module["key"], type="primary"):
                    _set_message(module["message"])

message = st.session_state.get(MESSAGE_KEY)
if message:
    st.info(message)
>>>>>>> Stashed changes

st.divider()
if st.button("Back to Hub", use_container_width=True):
    safe_switch("pages/guided_care_hub.py")
