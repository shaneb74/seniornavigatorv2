
import streamlit as st

# Appointment Booking
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Schedule My Call")
st.markdown("<h2>We’ll call you within 24 hours.</h2>", unsafe_allow_html=True)
st.markdown("<p>Help us reach you—quick and easy.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Booking form with tile style
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Contact Details", unsafe_allow_html=True)
st.markdown("<p>Fill in to book your concierge call for your loved one.</p>", unsafe_allow_html=True)
name = st.text_input("Your Name", value="Your Name")
relationship = st.text_input("Relationship to your loved one", value="e.g., Son")
phone = st.text_input("Best Phone Number", value="123-456-7890")
email = st.text_input("Email", value="your@email.com")
time = st.radio("Best Time to Call", ["Morning", "Afternoon", "Evening"])
notes = st.text_area("Notes (optional)", value="Any special instructions?")
if st.button("Book My Call", key="book_call", type="primary"):
    st.switch_page("pages/appointment_interstitial.py")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", key="back_appt", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)
