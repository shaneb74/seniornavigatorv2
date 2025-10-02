
import streamlit as st

# Guard
if 'care_context' not in st.session_state:
    st.session_state.care_context = {}

ctx = st.session_state.care_context
person_name = ctx.get('person_name', 'Your Loved One')

st.title("Plan for My Advisor")
st.caption("Book time with a concierge advisor and finalize a shareable package.")

st.markdown('---')
st.subheader("Appointment Booking")
st.caption("Schedule a call and tell us the best time to reach you.")
col1, col2 = st.columns(2)
with col1:
    if st.button("Book My Call", key="pfma_book"):
        st.switch_page("pages/appointment_booking.py")
with col2:
    if st.button("Back to Hub", key="pfma_back_hub"):
        st.switch_page("pages/hub.py")

st.markdown('---')
st.subheader("Confirmation Pages")
st.caption("Review and confirm each area of your plan. These were drawers before; now they open as pages.")

cols = st.columns(3)
with cols[0]:
    st.write("**Care Plan Confirmer**")
    if st.button("Open", key="pfma_open_care_plan_confirmer"):
        st.switch_page("pages/care_plan_confirm.py")
with cols[1]:
    st.write("**Cost Plan Confirmer**")
    if st.button("Open", key="pfma_open_cost_plan_confirmer"):
        st.switch_page("pages/cost_planner_evaluation.py")
with cols[2]:
    st.write("**Care Needs**")
    if st.button("Open", key="pfma_open_care_needs"):
        st.switch_page("pages/care_needs.py")

# Additional confirm pages for parity
cols2 = st.columns(3)
with cols2[0]:
    st.write("**Care Preferences**")
    if st.button("Open", key="pfma_open_care_prefs"):
        st.switch_page("pages/care_prefs.py")
with cols2[1]:
    st.write("**Household & Legal**")
    if st.button("Open", key="pfma_open_household_legal"):
        st.switch_page("pages/household_legal.py")
with cols2[2]:
    st.write("**Benefits & Coverage**")
    if st.button("Open", key="pfma_open_benefits_cov"):
        st.switch_page("pages/benefits_coverage.py")

cols3 = st.columns(3)
with cols3[0]:
    st.write("**Personal Info**")
    if st.button("Open", key="pfma_open_personal_info"):
        st.switch_page("pages/personal_info.py")
with cols3[1]:
    st.write("**Finish Prep**")
    if st.button("Finish Prep", key="pfma_finish_prep"):
        st.switch_page("pages/hub.py")
with cols3[2]:
    st.write(" ")
