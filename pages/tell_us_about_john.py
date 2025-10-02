
import streamlit as st

# Tell Us About John - Initial Audienceing
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Tell Us About John")
st.markdown("<h2>A few quick taps to start.</h2>", unsafe_allow_html=True)
st.markdown("<p>Help us guide John’s care in under a minute.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Simple qualifying questions with tile style
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### About John", unsafe_allow_html=True)
st.markdown("<p>These questions help us tailor John’s options—simple and private.</p>", unsafe_allow_html=True)
st.write("Did John serve in the military?")
st.button("Yes", key="military_yes", type="primary")
st.button("No", key="military_no", type="primary")

st.write("Is John on Medicaid now?")
st.button("Yes", key="medicaid_yes", type="primary")
st.button("No", key="medicaid_no", type="primary")

st.write("Does John own a home?")
st.button("Yes", key="home_yes", type="primary")
st.button("No", key="home_no", type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col2:
    st.button("Next: Hub", key="next_hub", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
