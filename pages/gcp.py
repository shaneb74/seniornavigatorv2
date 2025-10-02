import streamlit as st
from pathlib import Path

# Guard minimal context
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {},
        'person_name': 'Your Loved One'
    }
ctx = st.session_state.care_context
person_name = ctx.get('person_name', 'Your Loved One')

# Safe switch helper to avoid crashes when a target isn't registered yet
def safe_switch(target: str, fallback: str = "pages/hub.py"):
    try:
        if Path(target).exists():
            st.switch_page(target)
        else:
            st.switch_page(fallback)
    except Exception:
        st.switch_page(fallback)

st.title(f"Guided Care Plan for {person_name}")
st.caption("A simple, expert‑led way to see what kind of support could fit best right now.")

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
c1, c2 = st.columns(2)
with c1:
    if st.button('Back to Hub', key='gcp_back_hub'):
        safe_switch('pages/hub.py')
with c2:
    if st.button('Start Section 1', key='gcp_start_section1'):
        # Only navigate on click; do NOT call switch_page at import time.
        safe_switch('pages/gcp_daily_life.py')
