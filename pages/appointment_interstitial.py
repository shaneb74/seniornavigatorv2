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

st.header("Appointment Scheduled")
st.write("Call scheduled for tomorrow.")
col1,col2 = st.columns(2)
with col1:
    if st.button("Do Prep Now (Recommended)"):
        st.switch_page('pages/pfma.py')
with col2:
    if st.button("Skip & Remind Me"):
        st.switch_page('pages/hub.py')