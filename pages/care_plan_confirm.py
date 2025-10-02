import streamlit as st
from ui.ux_enhancements import apply_global_ux, render_stepper
apply_global_ux(); render_stepper('main')

if 'care_context' not in st.session_state:
    st.session_state.care_context = {'plan': {}}
ctx = st.session_state.care_context

st.header("Care Plan Confirmation")
st.write("Summary: In-home care, 10 hours/week, light supervision. (placeholder)")
ok = st.checkbox("This looks right?", key="cpc_ok")

col1,col2 = st.columns(2)
with col1:
    if st.button("Back to Booking"):
        st.switch_page('pages/appointment_booking.py')
with col2:
    if st.button("Next: Cost Plan"):
        st.switch_page('pages/cost_plan_confirm.py')
