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

apply_global_ux(); render_stepper('cost')

st.header("Cost Planner")
st.write("Choose a mode.")
col1,col2 = st.columns(2)
with col1:
    if st.button("Back to Hub"):
        st.switch_page('pages/hub.py')
with col2:
    pass
st.markdown("---")
if st.button("Step-by-Step"):
    st.switch_page('pages/cost_planner_modules.py')
if st.button("Freeform"):
    st.switch_page('pages/cost_planner_freeform.py')