import streamlit as st

# Cold-start guard
if "care_context" not in st.session_state:
    st.session_state.care_context = {
        "gcp_answers": {},
        "decision_trace": [],
        "planning_mode": "exploring",
        "care_flags": {},
        "person_name": "Your Loved One",
    }
ctx = st.session_state.care_context
person_name = ctx.get("person_name", "Your Loved One")

st.title(f"Guided Care Plan for {{PERSON_NAME}}")
st.caption("A simple, expert-led way to see what kind of support could fit best right now.")
st.write(
    """
Caring for yourself or someone you love can feel overwhelming. Whether it's for a spouse,
a parent, or your own future, it’s normal to ask: *What do we need? How do we plan? Can we afford it?*

This Guided Care Plan makes the first step easier. Answer 12 quick questions. You’ll get a clear,
personalized recommendation — free, straightforward, and built by experts.

Think of this as a helpful snapshot, not the final word. You can refine as things change.
"""
)

st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    if st.button("Back to Hub", key="gcp_back_hub"):
        st.switch_page("pages/hub.py")
with c2:
    if st.button("Start Section 1", key="gcp_start_section1"):
        st.switch_page("pages/gcp_daily_life.py")
