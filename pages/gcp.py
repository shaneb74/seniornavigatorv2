import streamlit as st

# Session-state guard
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context

st.title('Guided Care Plan for {PERSON_NAME}')
st.caption('A simple, expert-led way to see what kind of support could fit best right now.')

st.write(
    """
Caring for yourself or someone you love can feel overwhelming. Whether you're thinking about your spouse,
a parent, or your own future, it's normal to wonder: *What do we need? How do we plan? Can we afford it?*

This Guided Care Plan makes the first step easier. In a few minutes, you'll answer 12 simple questions.
Your answers create a clear starting point and a personalized recommendation — free, straightforward, and
designed by experts who've guided thousands of families through the same decisions.

Think of this as a helpful snapshot, not a final decision. You can adjust as things change, and we’ll
point you to next steps when you’re ready.
    """
)

st.markdown('---')
col1, col2 = st.columns(2)
with col1:
    if st.button('Back to Hub', key='gcp_back_hub'):
        st.switch_page('pages/hub.py')
with col2:
    if st.button('Start Section 1', key='gcp_start_section1'):
        st.switch_page('pages/gcp_daily_life.py')
