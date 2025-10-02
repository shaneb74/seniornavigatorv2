from ui.ux_enhancements import apply_global_ux, render_stepper

import streamlit as st
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'audience_type': None,
        'professional_role': None,
        'person_name': None,
        'care_flags': {},
        'derived_flags': {}
    }
ctx = st.session_state.care_context

apply_global_ux()
render_stepper()


# Cost Planner: Mode
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Cost Planner for your loved one")
st.radio('Planning mode', options=['Exploring', 'Planning'], index=0, horizontal=True, key='planning_mode')
st.markdown("<h2>Choose your planning style.</h2>", unsafe_allow_html=True)
st.markdown("<p>Step-by-step or freeform—your call.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Mode selection with tile style
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Planning Mode")
st.markdown("<p>Select how you’d like to explore costs.</p>", unsafe_allow_html=True)
st.button("Step-by-Step", key="step_mode", type="primary")
st.button("Freeform", key="free_mode", type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", key="back_cost", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)
ctx['planning_mode'] = st.session_state.get('planning_mode', 'Exploring').lower()
