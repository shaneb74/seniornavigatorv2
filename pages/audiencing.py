import streamlit as st
from ui.ux_enhancements import apply_global_ux, render_stepper

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

st.header("Who Are We Planning For?")
st.write("We’ll tune the language and steps based on your choice.")

aud_choice = st.session_state.get('aud_choice', ctx.get('audience_type'))

aud_choice = st.radio(
    "I'm planning for...",
    options=["Myself", "Someone else", "I'm a professional"],
    index={"Myself":0, "Someone else":1, "I'm a professional":2}.get(aud_choice, 0),
    horizontal=True,
    key='aud_choice'
)

# If professional, ask the subtype
pro_choice = None
if aud_choice == "I'm a professional":
    pro_choice = st.radio("Which best describes you?", ["Discharge Planner", "Referral"], index=0, horizontal=True, key='pro_choice')
    ctx['professional_role'] = pro_choice

# Persist audience
if aud_choice == "Myself":
    ctx['audience_type'] = 'self'
elif aud_choice == "Someone else":
    ctx['audience_type'] = 'proxy'
else:
    ctx['audience_type'] = 'pro'

# Contextual copy
if ctx['audience_type'] == 'self':
    st.success("Great. We’ll speak directly to you and your needs.")
elif ctx['audience_type'] == 'proxy':
    st.info("Understood. We’ll frame guidance for a family member or person you support.")
else:
    st.warning("Professional mode: content may be shortened and focus on referral-ready details.")

st.markdown('<div class="sn-sticky-bottom">', unsafe_allow_html=True)
b1, b2 = st.columns([1,1])
with b1:
    if st.button("Back: Welcome"):
        st.switch_page('pages/hub.py')
with b2:
    if st.button("Next"):
        if ctx['audience_type'] == 'self':
            st.switch_page('pages/tell_us_about_you.py')
        elif ctx['audience_type'] == 'proxy':
            st.switch_page('pages/tell_us_about_loved_one.py')
        else:
            role = ctx.get('professional_role', 'Discharge Planner')
            if role == 'Discharge Planner':
                st.switch_page('pages/professional_discharge.py')
            else:
                st.switch_page('pages/professional_referral.py')
st.markdown('</div>', unsafe_allow_html=True)
