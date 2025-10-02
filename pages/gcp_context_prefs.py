
import streamlit as st

# Session-state guard (no visual change)
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context
answers = ctx.setdefault('gcp_answers', {})

st.title('Guided Care Plan — Context & Preferences')
st.caption('Step 3 of 3')

st.markdown('---')

# Funding confidence
fund_opts = ['Very confident','Somewhat confident','Somewhat concerned','Very concerned']
answers['funding_confidence'] = st.radio(
    'How would you describe your financial situation when it comes to paying for care?',
    fund_opts,
    index=fund_opts.index(answers.get('funding_confidence', fund_opts[1])),
    key='q_funding_confidence'
)
st.caption('This helps right-size options for budget.')

# Geographic access
geo_opts = ['Very easy','Fairly easy','Somewhat difficult','Very difficult']
answers['geographic_access'] = st.radio(
    'How accessible are services like pharmacies, grocery stores, and doctors from your home?',
    geo_opts,
    index=geo_opts.index(answers.get('geographic_access', geo_opts[0])),
    key='q_geo_access'
)
st.caption('Think drive time, transit availability, and how quickly you can get prescriptions or appointments.')

# Willingness to move
move_opts = ['I prefer to stay home',"I'd rather stay home but open if needed","I'm comfortable either way","I'm comfortable moving"]
answers['move_willingness'] = st.radio(
    'If care is recommended, how open are you to changing where care happens?',
    move_opts,
    index=move_opts.index(answers.get('move_willingness', move_opts[0])),
    key='q_move_willingness'
)
st.caption('This frames recommendations. It does not override safety.')

st.markdown('---')
col1, col2 = st.columns(2)
with col1:
    if st.button('Back', key='context_back'):
        st.switch_page('pages/gcp_health_safety.py')
with col2:
    if st.button('Get my recommendation', key='context_next_get_reco'):
        st.switch_page('pages/gcp_recommendation.py')
