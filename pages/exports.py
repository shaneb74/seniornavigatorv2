
import streamlit as st

# Exports Page (placeholder - moved to export_results)
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Exports")
st.markdown("<h2>Your exported data.</h2>", unsafe_allow_html=True)
st.markdown("<p>This page is now handled by Export Results. Please use that page.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", key="back_exports", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)
