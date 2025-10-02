
import streamlit as st

# Appointment Interstitial
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Call Scheduled!")
st.markdown("<h2>Your advisor will call tomorrow.</h2>", unsafe_allow_html=True)
st.markdown("<p>Let’s make it awesome—prep now or later.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Interstitial message with tile style
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Next Steps for John", unsafe_allow_html=True)
st.markdown("<p>Your call is set! Prep the Plan for My Advisor now (2 min) to give your advisor a head start. More details = faster, better help. Skip now? We’ll remind you.</p>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Do Prep Now (Recommended)", key="prep_now", type="primary"):
        st.switch_page("pages/pfma.py")
with col2:
    if st.button("Skip & Remind Me", key="skip_prep", type="secondary"):
        st.switch_page("pages/hub.py")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation (handled by buttons)
