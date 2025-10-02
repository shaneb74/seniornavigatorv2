
import streamlit as st

# Risk Navigator
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Risk Navigator for your loved one")
st.markdown("<h2>Spot risks before they happen.</h2>", unsafe_allow_html=True)
st.markdown("<p>Check his safety and prevent ER trips.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Risk assessment tile
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Risk Check")
st.markdown("<p>Fall risk: Moderate (stairs). ER visits: 1 last year. Action: Add grab bars.</p>", unsafe_allow_html=True)
st.checkbox("This looks right?", key="risk_nav_confirm")
st.button("Save Risk Plan", key="save_risk_nav", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", key="back_risk", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)
