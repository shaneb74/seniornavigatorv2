
import streamlit as st
from ui.theme import inject_theme

inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

# Guard
if 'care_context' not in st.session_state:
    st.session_state.care_context = {}

ctx = st.session_state.care_context
person_name = ctx.get('person_name', 'Your Loved One')

st.title("Care Plan Confirmer")
st.caption("Confirm the details below. If something looks off, jump back to edit, then return here.")

st.markdown('---')
st.subheader("Summary")
st.write(ctx.get("gcp_recommendation", "Recommendation TBD"))

st.markdown('---')
agreed = st.checkbox("This looks right", key="pfma_confirm_care_plan_agree", value=False)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Back to Care Plan", key="pfma_confirm_care_plan_agree_back"):
        st.switch_page("pages/gcp.py")
with col2:
    if st.button("Back to PFMA", key="pfma_confirm_care_plan_agree_pfma"):
        st.switch_page("pages/pfma.py")
with col3:
    if st.button("Next", key="pfma_confirm_care_plan_agree_next", disabled=not agreed):
        st.switch_page("pages/pfma_confirm_cost_plan.py")

st.markdown('</div>', unsafe_allow_html=True)
