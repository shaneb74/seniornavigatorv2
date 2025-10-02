from ui.ux_enhancements import apply_global_ux, render_stepper

import streamlit as st
apply_global_ux()
render_stepper()


# Welcome Page
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Senior Care Navigator")
st.markdown("<h2>Find the right care, step by step.</h2>", unsafe_allow_html=True)
st.markdown("<p>Let’s start with a few basics about John.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Navigation buttons
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Get Started", key="get_started", type="primary")
st.markdown('</div>', unsafe_allow_html=True)