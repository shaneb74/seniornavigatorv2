import streamlit as st

# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context

st.title('Guided Care Plan for {PERSON_NAME}')

# ... existing 11–12 questions remain here ...

st.markdown('---')
if st.button('Get my recommendation', key='gcp_get_reco'):
    st.switch_page('pages/gcp_recommendation.py')
