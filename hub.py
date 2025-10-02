import streamlit as st

# Guard: keep context consistent
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }

st.title("Your Concierge Care Hub")
st.caption("Jump into any of the planning tools below…")

st.markdown("---")

# Guided Care Plan tile
st.subheader("Guided Care Plan")
st.write("Answer a short set of questions (3 sections, ~5 minutes) to get a personalized recommendation.")
if st.button("Start Plan", key="hub_gcp_start"):
    st.switch_page("pages/gcp.py")

st.markdown("---")

# Cost Planner tile
st.subheader("Cost Planner")
st.write("Explore the financial side of care, compare options, and see affordability over time.")
if st.button("Start Cost Planner", key="hub_cost_start"):
    st.switch_page("pages/cost_planner.py")

st.markdown("---")

# Plan for My Advisor tile
st.subheader("Plan for My Advisor")
st.write("Fill out a quick intake form that your Advisor can review before your call.")
if st.button("Start Plan for My Advisor", key="hub_pfma_start"):
    st.switch_page("pages/pfma.py")

st.markdown("---")

# AI Advisor tile
st.subheader("AI Advisor")
st.write("Ask questions and get instant answers powered by our AI Advisor.")
if st.button("Open AI Advisor", key="hub_ai_start"):
    st.switch_page("pages/ai_advisor.py")
