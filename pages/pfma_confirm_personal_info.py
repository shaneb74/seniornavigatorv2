
import streamlit as st

if 'care_context' not in st.session_state:
    st.session_state.care_context = {}

ctx = st.session_state.care_context
person_name = ctx.get('person_name', 'Your Loved One')

st.title("Personal Info")
st.caption("Confirm contact and key details for your advisor.")

st.markdown('---')
st.subheader("Summary")
st.write("Personal information summary will appear here.")

st.markdown('---')
agreed = st.checkbox("This looks right", key="pfma_confirm_personal_info_agree", value=False)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Back to Personal Info", key="pfma_pi_back"):
        st.switch_page("pages/personal_info.py")
with col2:
    if st.button("Back to PFMA", key="pfma_pi_pfma"):
        st.switch_page("pages/pfma.py")
with col3:
    if st.button("Finish Prep", key="pfma_finish", disabled=not agreed):
        st.switch_page("pages/hub.py")
