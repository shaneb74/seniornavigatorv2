import streamlit as st

# Benefits Check Detail
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Benefits Check for John")
st.markdown("<h2>Find savings that work.</h2>", unsafe_allow_html=True)
st.markdown("<p>Tap to see what fits his needs.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Module tile style
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Benefits Check", unsafe_allow_html=True)
st.markdown("<p>VA aid or Medicaid can ease John’s costs. It’s about finding help without losing his care quality.</p>", unsafe_allow_html=True)
st.button("Save & Back to Modules", key="save_bc", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_bc", type="secondary")
with col2:
    st.button("Next: Upgrades", key="next_bc", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
