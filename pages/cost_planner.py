import streamlit as st

st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Cost Planner")
st.markdown("<h2>Estimate your care costs.</h2>", unsafe_allow_html=True)
st.markdown("<p>Tinker with scenarios or plan in detail.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Drawers (use expanders for design)
st.expander("In-Home Care", expanded=True).write("Costs: $X/month. Adjust details here.")
st.expander("Assisted Living").write("Costs: $Y/month. Toggle options.")
st.expander("Memory Care").write("Costs: $Z/month. Compare scenarios.")

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", type="secondary")
with col2:
    st.button("Proceed to Smart Review", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
