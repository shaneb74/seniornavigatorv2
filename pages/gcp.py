import streamlit as st
from ui.ux_enhancements import apply_global_ux, render_stepper
apply_global_ux(); render_stepper('main')

if 'care_context' not in st.session_state:
    st.session_state.care_context = {'plan': {}}
ctx = st.session_state.care_context

st.header("Guided Care Plan")
needs_adl = st.radio("Needs help with daily tasks?", ["No","Yes"], index=0, horizontal=True) == "Yes"
comfortable_home = st.radio("Comfortable at home?", ["Yes","No"], index=0, horizontal=True) == "No"

col1,col2 = st.columns(2)
with col1:
    if st.button("Back to Hub"):
        st.switch_page('pages/hub.py')
with col2:
    if st.button("Next Step"):
        ctx['plan']['care_profile'] = {'needs_adl': needs_adl, 'home_concern': comfortable_home}
        st.switch_page('pages/care_plan_confirm.py')
