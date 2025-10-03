
import streamlit as st
from ui.theme import inject_theme

inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

# Guard
if 'care_context' not in st.session_state:
    st.session_state.care_context = {}

ctx = st.session_state.care_context
person_name = ctx.get('person_name', 'Your Loved One')

st.title("Plan for My Advisor")
st.caption("Make your call personalized, easy, and fast. Book your call first, then confirm details so your advisor is expertly prepared.")

st.markdown('---')
# Primary CTA: Book first
c1, c2 = st.columns(2)
with c1:
    if st.button("Book My Call", key="pfma_book_call", type="primary"):
        st.switch_page("pages/appointment_booking.py")
with c2:
    if st.button("Back to Hub", key="pfma_back_hub"):
        st.switch_page("pages/hub.py")

st.markdown('---')
st.subheader("After booking, confirm a few details")
st.caption("It takes about two minutes. This helps your advisor prepare a tailored conversation.")

if st.button("Start Confirmation", key="pfma_start_confirm"):
    st.switch_page("pages/pfma_confirm_care_plan.py")

st.markdown('</div>', unsafe_allow_html=True)
