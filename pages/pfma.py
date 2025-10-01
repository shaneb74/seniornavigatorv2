import streamlit as st

st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Plan for My Advisor")
st.markdown("<h2>Book an appointment and prepare.</h2>", unsafe_allow_html=True)
st.markdown("<p>Confirm details for your advisor.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Sections (expanders)
st.expander("Care Needs").write("Confirm ADLs, cognition, etc.")
st.expander("Preferences").write("Home vs move, etc.")
st.expander("Benefits").write("Toggle VA, Medicaid, etc.")

# Book button
st.button("Book Appointment", type="primary")
