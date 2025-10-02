from ui.ux_enhancements import apply_global_ux, render_stepper

import streamlit as st
apply_global_ux()
render_stepper()


# Cost Planner: Daily Living Aids
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Daily Living Aids for John")
st.markdown("<h2>Add safety tools at home.</h2>", unsafe_allow_html=True)
st.markdown("<p>Select aids to support his independence.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Aids options with tile style
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Daily Aids")
st.markdown("<p>Pick tools for John’s safety.</p>", unsafe_allow_html=True)
st.write("Bath chair?")
st.button("Yes", key="da_bath_yes", type="primary")
st.button("No", key="da_bath_no", type="primary")

st.write("Pill dispenser?")
st.button("Yes", key="da_pill_yes", type="primary")
st.button("No", key="da_pill_no", type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_da", type="secondary")
with col2:
    st.button("Next Option", key="next_da", type="primary")
st.markdown('</div>', unsafe_allow_html=True)