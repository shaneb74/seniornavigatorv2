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

st.title('Guided Care Plan — Health & Safety')
st.caption('Step 2 of 3')

st.markdown('---')

cog_opts = ['Sharp','Sometimes forgetful','Frequent memory issues','Serious confusion']
answers['cognition_level'] = st.radio(
    'How would you rate your memory and thinking in daily life?',
    cog_opts,
    index=cog_opts.index(answers.get('cognition_level', cog_opts[0])),
    key='q_cognition'
)
st.caption("We'll pair this with medications and safety to gauge supervision needs.")

mob_opts = ['I walk easily','I use a cane','I use a walker','I use a wheelchair']
answers['mobility'] = st.radio(
    'How do you usually get around?',
    mob_opts,
    index=mob_opts.index(answers.get('mobility', mob_opts[0])),
    key='q_mobility'
)
st.caption('We mean typical movement at home and outside.')

cond_opts = ['Diabetes','Hypertension','Dementia',"Parkinson's",'Stroke','CHF','COPD','Arthritis']
answers['chronic_conditions'] = st.multiselect(
    'Do you have any ongoing health conditions? Select all that apply.',
    cond_opts,
    default=answers.get('chronic_conditions', []),
    key='q_chronic_conditions'
)
st.caption('Select all that apply. Dementia strongly influences recommendations.')

fall_opts = ['Yes','No','Not sure']
answers['recent_fall'] = st.radio(
    'Has there been a fall in the last 6 months?',
    fall_opts,
    index=fall_opts.index(answers.get('recent_fall', 'No')),
    key='q_recent_fall'
)
st.caption('Recent falls increase the need for supervision or home changes.')

home_opts = ['Well-prepared','Mostly safe','Needs modifications','Not suitable']
answers['home_setup_safety'] = st.radio(
    'How safe and manageable is your home for daily living as you age?',
    home_opts,
    index=home_opts.index(answers.get('home_setup_safety', home_opts[0])),
    key='q_home_safety'
)
st.caption('Think stairs, bathrooms, lighting, grab bars, and trip hazards.')

st.markdown('---')
col1, col2 = st.columns(2)
with col1:
    if st.button('Back', key='health_back'):
        st.switch_page('pages/gcp_daily_life.py')
with col2:
    if st.button('Next', key='health_next'):
        st.switch_page('pages/gcp_context_prefs.py')
