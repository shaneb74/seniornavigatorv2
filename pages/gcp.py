from ui.ux_enhancements import apply_global_ux, render_stepper

import streamlit as st
apply_global_ux()
render_stepper()


# Guided Care Plan
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Guided Care Plan for your loved one")
st.markdown("<h2>Find his best care path.</h2>", unsafe_allow_html=True)
st.markdown("<p>Answer a few questions to get started.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Plan questions with tile style
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Care Questions")
st.markdown("<p>Help us tailor your loved one’s care options.</p>", unsafe_allow_html=True)
st.write("Does your loved one need help with daily tasks?")
st.button("Yes", key="gcp_daily_yes", type="primary")
st.button("No", key="gcp_daily_no", type="primary")

st.write("Is your loved one comfortable at home?")
st.button("Yes", key="gcp_home_yes", type="primary")
st.button("No", key="gcp_home_no", type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", key="back_gcp", type="secondary")
with col2:
    st.button("Next Step", key="next_gcp", type="primary")
st.markdown('</div>', unsafe_allow_html=True)