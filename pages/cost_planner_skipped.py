
import streamlit as st

# Cost Planner: Skipped
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Skipped Modules for John")
st.markdown("<h2>Review what you missed.</h2>", unsafe_allow_html=True)
st.markdown("<p>Add these later if needed.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Skipped modules tile
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Skipped Items")
st.markdown("<p>You skipped: Housing Path, Benefits Check.</p>", unsafe_allow_html=True)
st.button("Revisit Skipped", key="revisit_skipped", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Evaluation", key="back_skipped", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)
