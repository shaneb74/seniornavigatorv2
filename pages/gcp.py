
import streamlit as st

# Session-state guard (no visual change)
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context
answers = ctx.setdefault('gcp_answers', {})

st.title('Guided Care Plan for {PERSON_NAME}')
st.caption('A brief, structured set of questions in three short sections.')

st.markdown('---')
col1, col2 = st.columns(2)
with col1:
    if st.button('Back to Hub', key='gcp_back_hub'):
        st.switch_page('pages/hub.py')
with col2:
    if st.button('Start Section 1', key='gcp_start_section1'):
        st.switch_page('pages/gcp_daily_life.py')
