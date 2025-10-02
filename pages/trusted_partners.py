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

apply_global_ux(); render_stepper('main')

st.header("Trusted Partners")
cols = st.columns(2)
partners = ["Health Plan One","Senior Life AI","PillSync","Longevity Link"]
for i,p in enumerate(partners):
    with cols[i%2]:
        st.write(f"**{p}**")
        st.button("Connect", key=f"conn_{i}")
if st.button("Back to Waiting Room"):
    st.switch_page('pages/waiting_room.py')