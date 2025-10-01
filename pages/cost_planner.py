import streamlit as st

# Cost Planner: Mode Selection
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Cost Planner")
st.markdown("<h2>See it. Shape it. Settle it.</h2>", unsafe_allow_html=True)
st.markdown("<p>In two minutes, you'll know what's possible—without the overwhelm.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Mode selection cards
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; min-height: 200px; text-align: center;">', unsafe_allow_html=True)
    st.markdown("### Explore Costs")
    st.write("Quickly see what care might cost for John—no pressure, just numbers that update as you play.")
    if st.button("Start Exploring", key="explore_start", type="primary"):
        st.switch_page("pages/cost_planner_modules.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; min-height: 200px; text-align: center;">', unsafe_allow_html=True)
    st.markdown("### Build Your Plan")
    st.write("Follow our guide: step-by-step, expert-backed, ends with a print-ready summary for John.")
    if st.button("Start Planning", key="plan_start", type="primary"):
        st.switch_page("pages/cost_planner_modules.py")
    st.markdown('</div>', unsafe_allow_html=True)
