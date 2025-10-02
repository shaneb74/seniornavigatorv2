import streamlit as st
from ui.ux_enhancements import apply_global_ux, render_stepper

# Debug: non-visual logger
def _debug_log(msg: str):
    try:
        print(f"[SNAV] {msg}")
    except Exception:
        pass

_debug_log('LOADED: welcome.py')

apply_global_ux()
render_stepper('main')

if 'care_context' not in st.session_state:
    st.session_state.care_context = {'audience_type': None, 'person_name': None, 'care_flags': {}, 'plan': {}}
ctx = st.session_state.care_context
# Guard: ensure expected keys exist
if 'gcp_answers' not in ctx: ctx['gcp_answers'] = {}
if 'decision_trace' not in ctx: ctx['decision_trace'] = []
if 'planning_mode' not in ctx: ctx['planning_mode'] = 'exploring'
if 'care_flags' not in ctx: ctx['care_flags'] = {}


st.title("Entry – Who Are We Planning For?")
choice = st.radio("Who are we planning for?", ["Myself", "Someone Else", "I'm a professional"], index=0, horizontal=True, key="welcome_choice", label_visibility='collapsed')

if st.button("Continue"):
    if choice == "Myself":
        st.switch_page('pages/tell_us_about_you.py')
    elif choice == "Someone Else":
        st.switch_page('pages/tell_us_about_loved_one.py')
    else:
        st.switch_page('pages/professional_mode.py')
