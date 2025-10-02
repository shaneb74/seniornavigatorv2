import streamlit as st

if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context
answers = ctx.setdefault('gcp_answers', {})

st.title('Guided Care Plan — Daily Life & Support')
st.caption('Step 1 of 3')

st.markdown('---')

adl_opts = ['Independent', 'Occasional reminders', 'Help with some tasks', 'Rely on help for most tasks']
answers['adl_dependency'] = st.radio(
    'How well can you manage everyday activities like bathing, dressing, or preparing meals on your own?',
    adl_opts,
    index=adl_opts.index(answers.get('adl_dependency', adl_opts[0])),
    key='q_adl_dependency'
)
st.caption('ADLs include bathing, dressing, meals, and chores. This tells us the level of daily support.')

cg_opts = ['I have support most of the time','I have support a few days a week','I have support occasionally','I don’t have regular support']
answers['caregiver_support_level'] = st.radio(
    'How much regular support do you have from a caregiver or family member?',
    cg_opts,
    index=cg_opts.index(answers.get('caregiver_support_level', cg_opts[0])),
    key='q_caregiver_support'
)
st.caption('Strong support can offset higher daily needs.')

med_opts = ['None','A few, easy to manage','Several, harder to manage','Not sure']
answers['meds_complexity'] = st.radio(
    'Do you take medications, and how manageable is the routine?',
    med_opts,
    index=med_opts.index(answers.get('meds_complexity', med_opts[0])),
    key='q_meds_complexity'
)
st.caption('This helps us understand missed‑med risk when combined with cognition.')

soc_opts = ['Frequent contact','Occasional contact','Rarely see others','Often alone']
answers['social_isolation'] = st.radio(
    'How often do you connect with friends, family, or activities?',
    soc_opts,
    index=soc_opts.index(answers.get('social_isolation', soc_opts[0])),
    key='q_social_isolation'
)

st.markdown('---')
col1, col2 = st.columns(2)
with col1:
    if st.button('Back', key='daily_back'):
        st.switch_page('pages/gcp.py')
with col2:
    if st.button('Next', key='daily_next'):
        st.switch_page('pages/gcp_health_safety.py')
