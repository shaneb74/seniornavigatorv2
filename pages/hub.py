import streamlit as st
from ui.ux_enhancements import apply_global_ux, render_stepper
apply_global_ux(); render_stepper('hub')

if 'care_context' not in st.session_state:
    st.session_state.care_context = {'audience_type': None, 'person_name': None, 'care_flags': {}, 'plan': {}}
ctx = st.session_state.care_context

st.title("Hub")
name = ctx.get('person_name') or "your loved one"

left, main = st.columns([1,3], gap="large")
with left:
    st.write("**Navigation**")
    st.write("• Who Are We Planning For?")
    st.write(f"• Tell Us About {name}")
    st.write("• Hub")
    st.write("• Waiting Room")
    st.write("• AI Advisor")
with main:
    st.subheader("Prep for Call")
    st.write("Quick 5-minute setup.")
    if st.button("Start Prep"):
        st.switch_page('pages/care_plan_confirm.py')
    st.markdown("---")
    st.subheader("Explore Tools")
    c1,c2 = st.columns(2)
    with c1:
        if st.button("Guided Care Plan"):
            st.switch_page('pages/gcp.py')
        if st.button("Plan for My Advisor"):
            st.switch_page('pages/appointment_booking.py')
        if st.button("Risk Navigator"):
            st.switch_page('pages/risk_navigator.py')
    with c2:
        if st.button("Cost Planner"):
            st.switch_page('pages/cost_planner.py')
        if st.button("Medication Management"):
            st.switch_page('pages/medication_management.py')
