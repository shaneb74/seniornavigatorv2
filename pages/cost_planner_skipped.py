import streamlit as st

# Cost Planner: Skipped Modules
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Review Skipped Options for John")
st.markdown("<h2>Anything else to consider?</h2>", unsafe_allow_html=True)
st.markdown("<p>These might help John’s plan.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Skipped module suggestions with tile style
st.markdown('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; justify-items: center; padding: 1rem;">', unsafe_allow_html=True)
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px; opacity: 0.6;">', unsafe_allow_html=True)
st.markdown("### Long-term Care Insurance", unsafe_allow_html=True)
st.markdown("<p>Could save John $20,000 over time—worth a look.</p>", unsafe_allow_html=True)
st.button("Explore", key="ltc_explore", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px; opacity: 0.6;">', unsafe_allow_html=True)
st.markdown("### Transportation Support", unsafe_allow_html=True)
st.markdown("<p>Eases John’s access to care—check if it fits.</p>", unsafe_allow_html=True)
st.button("Explore", key="transport_explore", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Evaluation", key="back_skipped", type="secondary")
with col2:
    st.button("Finish", key="finish_skipped", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
