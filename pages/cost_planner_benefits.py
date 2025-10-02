from ui.ux_enhancements import apply_global_ux, render_stepper

import streamlit as st
apply_global_ux()
render_stepper()


# Cost Planner: Benefits Check
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Benefits Check for your loved one")
st.markdown("<h2>Unlock savings options.</h2>", unsafe_allow_html=True)
st.markdown("<p>Explore eligibility for support.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Benefits options with tile style
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Benefit Options")
st.markdown("<p>Check your loved one’s eligibility.</p>", unsafe_allow_html=True)
st.write("VA benefits?")
st.button("Yes", key="cb_va_yes", type="primary")
st.button("No", key="cb_va_no", type="primary")

st.write("Medicaid?")
st.button("Yes", key="cb_medicaid_yes", type="primary")
st.button("No", key="cb_medicaid_no", type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_cb", type="secondary")
with col2:
    st.button("Next Option", key="next_cb", type="primary")
st.markdown('</div>', unsafe_allow_html=True)