
import streamlit as st

# Guard
if 'care_context' not in st.session_state:
    st.session_state.care_context = {}

ctx = st.session_state.care_context
person_name = ctx.get('person_name', 'Your Loved One')

st.title("Plan for My Advisor")
st.caption("Make your call personalized, easy, and fast. It takes about two minutes to confirm a few details so your advisor is expertly prepared.")

st.markdown('---')

col1, col2 = st.columns(2)
with col1:
    if st.button("Start Confirmation", key="pfma_start_confirm", type="primary"):
        st.switch_page("pages/pfma_confirm_care_plan.py")
with col2:
    if st.button("Back to Hub", key="pfma_back_hub"):
        st.switch_page("pages/hub.py")

st.markdown('---')
st.subheader("Prefer to book first?")
st.caption("You can always confirm details after scheduling.")
if st.button("Book My Call", key="pfma_book_call"):
    st.switch_page("pages/appointment_booking.py")
