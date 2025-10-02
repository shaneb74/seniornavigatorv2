import streamlit as st
from ui.ux_enhancements import apply_global_ux, render_stepper
apply_global_ux(); render_stepper('cost')

st.header("Cost Planner")
st.write("Choose how deep you want to go right now.")

col1, col2 = st.columns(2)
with col1:
    if st.button("Back to Hub"):
        st.switch_page('pages/hub.py')
with col2:
    st.empty()

st.markdown("---")
st.subheader("Pick a mode")

if st.button("Estimating costs"):
    st.switch_page('pages/cost_planner_modules.py')

if st.button("Planning"):
    st.switch_page('pages/cost_planner_modules.py')
