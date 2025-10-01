import streamlit as st

# Tell Us About John - Initial Audienceing
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Tell Us About John")
st.markdown("<h2>Quick questions to guide your journey.</h2>", unsafe_allow_html=True)
st.markdown("<p>Just a few taps—takes less than a minute!</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Simple qualifying questions
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left;">', unsafe_allow_html=True)
st.write("Did John serve in the military?")
st.button("Yes", key="military_yes", type="primary")
st.button("No", key="military_no", type="primary")

st.write("Is John currently on Medicaid?")
st.button("Yes", key="medicaid_yes", type="primary")
st.button("No", key="medicaid_no", type="primary")

st.write("Does John own a home?")
st.button("Yes", key="home_yes", type="primary")
st.button("No", key="home_no", type="primary")

# Conditional alerts (mockup text)
if st.button("Yes", key="medicaid_yes_alert", type="primary", help="Hidden trigger"):
    st.warning("Heads up: Medicaid is federal. Visit benefits.gov for details. We’ll handle the rest!")
if st.button("Yes", key="military_yes_alert", type="primary", help="Hidden trigger"):
    st.info("Great! We’ll flag VA options for John later.")

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col2:
    st.button("Next: Hub", key="next_hub", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
