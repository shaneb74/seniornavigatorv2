import streamlit as st
from ui.ux_enhancements import apply_global_ux, render_stepper

apply_global_ux()
render_stepper('hub')

if 'care_context' not in st.session_state:
    st.session_state.care_context = {'audience_type': None, 'person_name': None, 'care_flags': {}, 'plan': {}}
ctx = st.session_state.care_context
name = ctx.get('person_name') or "your loved one"

st.title("Hub")
st.caption(f"You're working on a plan for {name}. Pick what you want to do next.")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Guided Care Plan")
    st.write("Answer a few questions to get a recommendation.")
    if st.button("Open Guided Care Plan"):
        st.switch_page('pages/gcp.py')

    st.markdown("---")

    st.subheader("Plan for My Advisor")
    st.write("Book a call and prep the advisor-ready package.")
    if st.button("Open PFMA"):
        st.switch_page('pages/appointment_booking.py')

with c2:
    st.subheader("Cost Planner")
    st.write("Estimate monthly costs and runway, or do full planning.")
    if st.button("Open Cost Planner"):
        st.switch_page('pages/cost_planner.py')

    st.markdown("---")

    st.subheader("Extras")
    colx, coly = st.columns(2)
    with colx:
        if st.button("Medication Management"):
            st.switch_page('pages/medication_management.py')
        if st.button("AI Advisor"):
            st.switch_page('pages/ai_advisor.py')
    with coly:
        if st.button("Risk Navigator"):
            st.switch_page('pages/risk_navigator.py')
        if st.button("Waiting Room"):
            st.switch_page('pages/waiting_room.py')
