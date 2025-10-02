from ui.ux_enhancements import apply_global_ux, render_stepper
import streamlit as st
apply_global_ux()
render_stepper('main')

st.header("Discharge Planner")
st.write("This is a placeholder screen. Routing and form will be wired later.")

if st.button("Back: Audiencing"):
    st.switch_page('pages/audiencing.py')
