import streamlit as st
from ui.ux_enhancements import apply_global_ux, render_stepper

# Debug: non-visual logger
def _debug_log(msg: str):
    try:
        print(f"[SNAV] {msg}")
    except Exception:
        pass

_debug_log('LOADED: tell_us_about_loved_one.py')

apply_global_ux(); render_stepper('main')

if 'care_context' not in st.session_state:
    st.session_state.care_context = {'audience_type': 'proxy', 'person_name': None, 'care_flags': {}, 'plan': {}}
ctx = st.session_state.care_context
# Guard: ensure expected keys exist
if 'gcp_answers' not in ctx: ctx['gcp_answers'] = {}
if 'decision_trace' not in ctx: ctx['decision_trace'] = []
if 'planning_mode' not in ctx: ctx['planning_mode'] = 'exploring'
if 'care_flags' not in ctx: ctx['care_flags'] = {}

ctx['audience_type'] = 'proxy'

st.header("Tell Us About Your Loved One")
name = st.text_input("Their name", value=ctx.get('person_name') or "", key="name_proxy")
is_vet = st.radio("Served in the military?", ["No","Yes"], index=0, horizontal=True) == "Yes"
on_med = st.radio("On Medicaid now?", ["No","Yes"], index=0, horizontal=True) == "Yes"
owns_home = st.radio("Own a home?", ["No","Yes"], index=0, horizontal=True) == "Yes"

if st.button("Next: Build Care Plan", disabled=(not name.strip())):
    ctx['person_name'] = name.strip()
    ctx['care_flags'].update({'is_veteran': is_vet, 'on_medicaid': on_med, 'owns_home': owns_home})
    st.switch_page('pages/hub.py')