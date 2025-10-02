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

st.header("Waiting Room")
st.write("Trivia Card: Fun fact. [Get Tip]")
st.write("Partner Spotlight")
if st.button("See All Partners"):
    st.switch_page('pages/trusted_partners.py')
if st.button("Second Opinion: Chat Now"):
    st.switch_page('pages/ai_advisor.py')
if st.button("Back to Hub"):
    st.switch_page('pages/hub.py')