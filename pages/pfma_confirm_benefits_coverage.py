
import streamlit as st

# Guard
if 'care_context' not in st.session_state:
    st.session_state.care_context = {}

ctx = st.session_state.care_context
person_name = ctx.get('person_name', 'Your Loved One')

st.title("Benefits & Coverage")
st.caption("Confirm the details below. If something looks off, jump back to edit, then return here.")

st.markdown('---')
st.subheader("Summary")
st.write("Benefits & Coverage summary will appear here.")

st.markdown('---')
agreed = st.checkbox("This looks right", key="pfma_confirm_benefits_coverage_agree", value=False)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Back to Benefits & Coverage", key="pfma_confirm_benefits_coverage_agree_back"):
        st.switch_page("pages/benefits_coverage.py")
with col2:
    if st.button("Back to PFMA", key="pfma_confirm_benefits_coverage_agree_pfma"):
        st.switch_page("pages/pfma.py")
with col3:
    if st.button("Next", key="pfma_confirm_benefits_coverage_agree_next", disabled=not agreed):
        st.switch_page("pages/pfma_confirm_personal_info.py")
