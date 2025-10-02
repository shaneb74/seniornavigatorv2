import streamlit as st
from ui.ux_enhancements import apply_global_ux, render_stepper
apply_global_ux()
render_stepper('main')

if 'care_context' not in st.session_state:
    st.session_state.care_context = {'audience_type': None, 'person_name': None, 'care_flags': {}, 'plan': {}}
ctx = st.session_state.care_context

st.title("Entry – Who Are We Planning For?")
choice = st.radio("", ["Myself", "Someone Else", "I'm a professional"], index=0, horizontal=True, key="welcome_choice")

if st.button("Continue"):
    if choice == "Myself":
        st.switch_page('pages/tell_us_about_you.py')
    elif choice == "Someone Else":
        st.switch_page('pages/tell_us_about_loved_one.py')
    else:
        st.switch_page('pages/professional_mode.py')
