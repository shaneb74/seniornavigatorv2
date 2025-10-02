import streamlit as st
from ui.ux_enhancements import apply_global_ux, render_stepper
apply_global_ux(); render_stepper('main')

if 'care_context' not in st.session_state:
    st.session_state.care_context = {'audience_type': 'self', 'person_name': None, 'care_flags': {}, 'plan': {}}
ctx = st.session_state.care_context
ctx['audience_type'] = 'self'

st.header("Tell Us About You")
name = st.text_input("Your name", value=ctx.get('person_name') or "", key="name_self")
is_vet = st.radio("Served in the military?", ["No","Yes"], index=0, horizontal=True) == "Yes"
on_med = st.radio("On Medicaid now?", ["No","Yes"], index=0, horizontal=True) == "Yes"
owns_home = st.radio("Own a home?", ["No","Yes"], index=0, horizontal=True) == "Yes"

if st.button("Next: Build Care Plan", disabled=(not name.strip())):
    ctx['person_name'] = name.strip()
    ctx['care_flags'].update({'is_veteran': is_vet, 'on_medicaid': on_med, 'owns_home': owns_home})
    st.switch_page('pages/hub.py')
