import streamlit as st

# Daily Living Aids Detail
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Daily Living Aids for John")
st.markdown("<h2>Tools for safety and ease.</h2>", unsafe_allow_html=True)
st.markdown("<p>Simple aids prevent falls and keep routines smooth.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Module tile style
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Daily Living Aids", unsafe_allow_html=True)
st.markdown("<p>Items like bath chairs or pill boxes help John stay safe and on track, cutting the need for constant care.</p>", unsafe_allow_html=True)
st.button("Save & Back to Modules", key="save_da", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_da", type="secondary")
with col2:
    st.button("Next: Housing", key="next_da", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
