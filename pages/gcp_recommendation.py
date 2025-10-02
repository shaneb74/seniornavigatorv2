
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

st.title('Your Care Recommendation')

# Recommendation summary (variable placeholder shown literally for design fidelity)
st.subheader('{RECOMMENDATION}')  # none | in-home care | assisted living | memory care

# Conversational blurb (variable placeholder; dev will populate from copy library)
st.write('{RECO_BLURB}')

st.markdown('---')

col1, col2 = st.columns(2)
with col1:
    if st.button('Back to Hub', key='reco_back_hub'):
        st.switch_page('pages/hub.py')
with col2:
    if st.button('Open Cost Planner', key='reco_open_cost'):
        st.switch_page('pages/cost_planner.py')
