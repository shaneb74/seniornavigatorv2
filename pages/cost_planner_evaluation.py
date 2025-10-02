import streamlit as st

# Cost Planner: Expert Agent Evaluation
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Expert Agent Review")
st.markdown("<h2>Let’s check your plan.</h2>", unsafe_allow_html=True)
st.markdown("<p>Our AI agent has some thoughts.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# AI Agent mockup
st.image("https://via.placeholder.com/100", caption="AI Agent", use_column_width=True)
st.write("Hi! I noticed you skipped Medicaid eligibility—want my take? It could save you thousands.")
st.button("View Medicaid Tip", key="medicaid_tip", type="primary", help="Optional insight")

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_eval", type="secondary")
with col2:
    st.button("Next: Skipped Items", key="next_eval", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
