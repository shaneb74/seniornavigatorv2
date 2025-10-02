import streamlit as st
from ui.ux_enhancements import apply_global_ux, render_stepper
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'audience_type': None,
        'person_name': None,
        'care_flags': {},
        'plan': {}
    }
ctx = st.session_state.care_context

apply_global_ux(); render_stepper('main')

st.header("Appointment Booking")
with st.form("appt_form"):
    name = st.text_input("Name")
    relationship = st.text_input("Relationship to resident")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    time = st.text_input("Preferred time")
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Book My Call")
if submitted:
    st.switch_page('pages/appointment_interstitial.py')
if st.button("Back to Hub"):
    st.switch_page('pages/hub.py')