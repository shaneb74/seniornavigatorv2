import streamlit as st

# Housing Path Detail
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Housing Path for John")
st.markdown("<h2>Decide home or new start.</h2>", unsafe_allow_html=True)
st.markdown("<p>Balance costs and comfort for his future.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Module tile style
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Housing Path", unsafe_allow_html=True)
st.markdown("<p>Keeping the home means upkeep; selling opens equity. For John, it’s about what fits his life and wallet.</p>", unsafe_allow_html=True)
st.button("Save & Back to Modules", key="save_hp", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_hp", type="secondary")
with col2:
    st.button("Next: Benefits", key="next_hp", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
