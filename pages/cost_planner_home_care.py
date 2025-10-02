
import streamlit as st

# Cost Planner: Home Care Support
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Home Care Support for John")
st.markdown("<h2>Keep him safe at home.</h2>", unsafe_allow_html=True)
st.markdown("<p>Plan for help with daily tasks.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Home care options with tile style
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Home Care Options")
st.markdown("<p>Choose hours and services for John.</p>", unsafe_allow_html=True)
st.write("Hours per week?")
st.button("10 hours", key="hc_10", type="primary")
st.button("20 hours", key="hc_20", type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_hc", type="secondary")
with col2:
    st.button("Next Option", key="next_hc", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
