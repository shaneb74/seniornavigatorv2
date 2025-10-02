from ui.ux_enhancements import apply_global_ux, render_stepper

import streamlit as st
apply_global_ux()
render_stepper()


# Cost Planner: Evaluation
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Cost Planner Evaluation for your loved one")
st.markdown("<h2>Review your plan.</h2>", unsafe_allow_html=True)
st.markdown("<p>Check and confirm your choices.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Evaluation tile
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Plan Review")
st.markdown("<p>Total cost: $1,500/month. Includes home care and aids.</p>", unsafe_allow_html=True)
st.checkbox("This looks right?", key="cp_eval_confirm")
st.button("Save Plan", key="save_eval", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_eval", type="secondary")
with col2:
    st.button("Finish", key="finish_eval", type="primary")
st.markdown('</div>', unsafe_allow_html=True)