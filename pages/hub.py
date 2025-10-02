
import streamlit as st

# Session-state guard (safe, no visual change)
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }

st.title("Your Concierge Care Hub")

# ===== Guided Care Plan tile =====
st.markdown("### Guided Care Plan")
st.write("Answer a short set of questions (3 sections) to get a personalized recommendation.")
# Use a unique key and route explicitly
if st.button("Start Plan", key="hub_gcp_start"):
    st.switch_page("pages/gcp.py")

st.divider()

# ===== Cost Planner tile =====
st.markdown("### Cost Planner")
st.write("Explore costs or do full planning.")
if st.button("Start Cost Planner", key="hub_cost_start"):
    st.switch_page("pages/cost_planner.py")

st.divider()

# ===== Plan for My Advisor tile =====
st.markdown("### Plan for My Advisor")
st.write("Quick intake so an advisor can review before your call.")
if st.button("Get Connected", key="hub_pfma_start"):
    st.switch_page("pages/pfma.py")

st.divider()

# ===== Medication Management tile =====
st.markdown("### Medication Management")
if st.button("Start Review", key="hub_med_start"):
    st.switch_page("pages/medication_management.py")

st.divider()

# ===== Risk Navigator tile =====
st.markdown("### Risk Navigator")
if st.button("Run Check", key="hub_risk_start"):
    st.switch_page("pages/risk_navigator.py")
