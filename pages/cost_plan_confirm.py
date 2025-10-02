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

st.header("Cost Plan Confirmation")
st.write("Summary: $1,500/month (10 hrs home care + aids). (placeholder)")
ok = st.checkbox("This looks right?", key="cost_ok")

col1,col2 = st.columns(2)
with col1:
    if st.button("Back to Care Plan"):
        st.switch_page('pages/care_plan_confirm.py')
with col2:
    if st.button("Next: Care Needs"):
        st.switch_page('pages/care_needs.py')