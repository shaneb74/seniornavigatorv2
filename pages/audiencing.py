import streamlit as st
from ui.ux_enhancements import apply_global_ux, render_stepper

apply_global_ux()
render_stepper('main')

st.header("Who Are We Planning For?")
st.write("Choose the option that best matches your situation. This helps us tailor the plan.")

# Simple segmented controls that match your existing style philosophy
opt = st.radio(
    "I'm planning for...",
    options=["One person", "Two people", "I'm a professional"],
    index=0,
    horizontal=True,
)

with st.container():
    st.markdown('<div class="sn-sticky-bottom">', unsafe_allow_html=True)
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Back: Hub"):
            st.switch_page('pages/hub.py')
    with col2:
        if st.button("Next: Tell Us About You"):
            st.switch_page('pages/tell_us_about_you.py')
    st.markdown('</div>', unsafe_allow_html=True)
