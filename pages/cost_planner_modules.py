import streamlit as st
from ui.ux_enhancements import apply_global_ux, render_stepper
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'audience_type': None,
        'person_name': None,
        'care_flags': {},
        'plan': {}
    }
ctx = st.session_state.care_context

apply_global_ux(); render_stepper('cost')

st.header("Module Picker")
c1,c2 = st.columns(2)
with c1:
    if st.button("Home Care Support"):
        st.switch_page('pages/cost_planner_home_care.py')
    if st.button("Housing Path"):
        st.switch_page('pages/cost_planner_housing.py')
    if st.button("Benefits Check"):
        st.switch_page('pages/cost_planner_benefits.py')
with c2:
    if st.button("Daily Living Aids"):
        st.switch_page('pages/cost_planner_daily_aids.py')
    if st.button("Age-in-Place Upgrades"):
        st.switch_page('pages/cost_planner_mods.py')

st.markdown("---")
b1,b2 = st.columns(2)
with b1:
    if st.button("Back to Mode"):
        st.switch_page('pages/cost_planner.py')
with b2:
    if st.button("Next: Expert Review"):
        st.switch_page('pages/cost_planner_evaluation.py')