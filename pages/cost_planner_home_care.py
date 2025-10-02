import streamlit as st

# Home Care Support Detail
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Home Care Support for John")
st.markdown("<h2>Support that keeps him home.</h2>", unsafe_allow_html=True)
st.markdown("<p>Helps with daily tasks—safe, independent living.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Module tile style
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Home Care Support", unsafe_allow_html=True)
st.markdown("<p>Many seniors thrive at home with help—meds, meals, or a friendly face. For John, this means staying put longer, avoiding big moves.</p>", unsafe_allow_html=True)
st.button("Save & Back to Modules", key="save_hc", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_hc", type="secondary")
with col2:
    st.button("Next: Daily Aids", key="next_hc", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
