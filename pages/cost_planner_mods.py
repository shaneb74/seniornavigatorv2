import streamlit as st

# Age-in-Place Upgrades Detail
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Age-in-Place Upgrades for John")
st.markdown("<h2>Safety upgrades for home.</h2>", unsafe_allow_html=True)
st.markdown("<p>Keep him secure where he loves.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Module tile style
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Age-in-Place Upgrades", unsafe_allow_html=True)
st.markdown("<p>Grab bars or stair lifts let John stay home safely, cutting fall risks and delay care moves.</p>", unsafe_allow_html=True)
st.button("Save & Back to Modules", key="save_mods", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_mods", type="secondary")
with col2:
    st.button("Next: Evaluation", key="next_mods", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
