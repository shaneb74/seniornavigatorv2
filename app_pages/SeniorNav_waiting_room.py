from __future__ import annotations

import random

import streamlit as st
from ui.theme import inject_theme
from app_pages.seniornav_util import top_nav, safe_switch

inject_theme()
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

st.divider()
if st.button("Back to Hub", use_container_width=True):
    safe_switch("pages/guided_care_hub.py")
