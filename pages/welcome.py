from ui.ux_enhancements import apply_global_ux, render_stepper
import streamlit as st

apply_global_ux()
render_stepper('main')

if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'audience_type': None,
        'professional_role': None,
        'people': [],
        'care_flags': {},
        'derived_flags': {}
    }
ctx = st.session_state.care_context

st.title("Welcome")
st.write("Let’s set up your experience. Who are we planning for today?")

audience = st.radio(
    "I'm planning for...",
    ["Myself", "Someone else", "I'm a professional"],
    index=0,
    horizontal=True,
    key='welcome_aud_choice'
)

if audience == "I'm a professional":
    st.radio("Choose one:", ["Discharge Planner", "Referral"], index=0, horizontal=True, key='welcome_pro_choice')

st.markdown('<div class="sn-sticky-bottom">', unsafe_allow_html=True)
c1, c2 = st.columns([1,1])
with c2:
    if st.button("Get Started"):
        choice = st.session_state.get('welcome_aud_choice', "Myself")
        if choice == "Myself":
            st.session_state.care_context['audience_type'] = 'self'
        elif choice == "Someone else":
            st.session_state.care_context['audience_type'] = 'proxy'
        else:
            st.session_state.care_context['audience_type'] = 'pro'
            st.session_state.care_context['professional_role'] = st.session_state.get('welcome_pro_choice', 'Discharge Planner')
        st.switch_page('pages/audiencing.py')
st.markdown('</div>', unsafe_allow_html=True)
