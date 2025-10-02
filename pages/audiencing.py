import streamlit as st
from ui.ux_enhancements import apply_global_ux, render_stepper

apply_global_ux()
render_stepper('main')

if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'audience_type': None,
        'professional_role': None,
        'person_name': None,
        'care_flags': {},
        'derived_flags': {},
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'review_log': []
    }
ctx = st.session_state.care_context

st.header('Who Are We Planning For?')
st.caption('Entry mode sets tone and copy; toggles guide routing and module visibility.')

# Entry mode
aud_choice = st.radio("I'm planning for...", ["Myself", "Someone else", "I'm a professional"], index=0, horizontal=True, key='aud_choice')
if aud_choice == 'Myself':
    ctx['audience_type'] = 'self'
elif aud_choice == 'Someone else':
    ctx['audience_type'] = 'proxy'
else:
    ctx['audience_type'] = 'pro'
if ctx['audience_type'] == 'pro':
    ctx['professional_role'] = st.radio('Which best describes you?', ['Discharge Planner', 'Referral'], index=0, horizontal=True)

# Qualifiers
st.subheader('Qualifiers')
q1,q2,q3 = st.columns(3)
with q1:
    ctx['care_flags']['is_veteran'] = st.toggle('Veteran status', value=bool(ctx['care_flags'].get('is_veteran', False)))
with q2:
    ctx['care_flags']['has_partner'] = st.toggle('Has partner/spouse', value=bool(ctx['care_flags'].get('has_partner', False)))
with q3:
    ctx['care_flags']['owns_home'] = st.toggle('Owns home', value=bool(ctx['care_flags'].get('owns_home', False)))
q4,q5 = st.columns(2)
with q4:
    ctx['care_flags']['on_medicaid'] = st.toggle('Medicaid today', value=bool(ctx['care_flags'].get('on_medicaid', False)))
with q5:
    ENABLE_URGENT = True
    ctx['care_flags']['urgent'] = st.toggle('Urgent case', value=bool(ctx['care_flags'].get('urgent', False))) if ENABLE_URGENT else False

# Routing decision
st.markdown('<div class="sn-sticky-bottom">', unsafe_allow_html=True)
b1,b2 = st.columns([1,1])
with b1:
    if st.button('Back: Welcome'):
        st.switch_page('pages/welcome.py') if (Path('pages')/ 'welcome.py').exists() else st.switch_page('pages/hub.py')
with b2:
    if st.button('Next'):
        if ctx['audience_type'] == 'pro':
            role = ctx.get('professional_role','Discharge Planner')
            st.switch_page('pages/professional_discharge.py' if role=='Discharge Planner' else 'pages/professional_referral.py')
        else:
            if ctx['care_flags'].get('on_medicaid') or ctx['care_flags'].get('urgent'):
                st.switch_page('pages/pfma.py')
            else:
                st.switch_page('pages/care_needs.py')
st.markdown('</div>', unsafe_allow_html=True)
