import streamlit as st
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'audience_type': None,
        'person_name': None,
        'care_flags': {},
        'plan': {}
    }
ctx = st.session_state.care_context

st.header('Cost Planner Freeform.Py')
st.write('Placeholder module.')
if st.button('Back to Modules'): st.switch_page('pages/cost_planner_modules.py')