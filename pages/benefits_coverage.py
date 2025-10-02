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

st.header("Benefits & Coverage")
st.write("Details: e.g., Insurance: Blue Cross. VA: Yes. (placeholder)")
ok = st.checkbox("This looks right?")

col1,col2 = st.columns(2)
with col1:
    if st.button("Back to Household"):
        st.switch_page('pages/household_legal.py')
with col2:
    if st.button("Next: Personal Info"):
        st.switch_page('pages/personal_info.py')