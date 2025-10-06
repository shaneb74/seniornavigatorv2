from __future__ import annotations

import streamlit as st

from senior_nav import navigation
from senior_nav.state import ensure_base_state
from senior_nav.ui import header, set_page_config


set_page_config(title="AI Advisor")
ensure_base_state()
header("AI Advisor", "Ask for guidance or jump to another step.")

messages = st.session_state.setdefault("ai_messages", [])
for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask the AI Advisor…")
nav_target: str | None = None

if prompt:
    messages.append({"role": "user", "content": prompt})
    response = "I noted that. You can continue exploring from the hub."
    lower = prompt.lower()
    if "cost" in lower:
        response = "Opening the cost planner so you can review funding."
        nav_target = navigation.COST_PLANNER_PAGE
    elif "care plan" in lower or "guided" in lower:
        response = "Taking you back to the Guided Care Plan."
        nav_target = navigation.GCP_PAGE
    elif "document" in lower or "download" in lower:
        response = "Let's open your documents so you can review and share them."
        nav_target = navigation.DOCUMENTS_PAGE
    elif "advisor" in lower or "book" in lower:
        response = "I'll take you to the advisor booking page."
        nav_target = navigation.PFMA_PAGE
    messages.append({"role": "assistant", "content": response})
    st.session_state.ai_messages = messages

if st.button("Back to hub"):
    navigation.switch_page(navigation.HUB_PAGE)

col1, col2, col3, col4 = st.columns(4)
if col1.button("Guided Care Plan", use_container_width=True):
    navigation.switch_page(navigation.GCP_PAGE)
if col2.button("Cost Planner", use_container_width=True):
    navigation.switch_page(navigation.COST_PLANNER_PAGE)
if col3.button("My Documents", use_container_width=True):
    navigation.switch_page(navigation.DOCUMENTS_PAGE)
if col4.button("Advisor booking", use_container_width=True):
    navigation.switch_page(navigation.PFMA_PAGE)

if nav_target:
    navigation.switch_page(nav_target)
