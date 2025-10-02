import streamlit as st
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

st.header('Pre-Visit Prep')
st.write('Quick prep checklist. This is a temporary stub to resolve routing.')
if st.button('Back to Hub'):
    st.switch_page('pages/hub.py')
st.header('Plan for My Advisor')
st.subheader('Appointment Booking')
with st.form('appt_form'):
    name = st.text_input('Your name', value=ctx.get('person_name') or '')
    relation = st.selectbox('Relationship to resident', ['Self','Spouse/Partner','Child','Sibling','Friend','Other'])
    phone = st.text_input('Phone')
    zipc = st.text_input('ZIP')
    age_band = st.selectbox('Age band', ['<65','65-74','75-84','85+'])
    urgency = st.selectbox('Urgency', ['Routine','Soon','Urgent'])
    window = st.selectbox('Preferred time window', ['Morning','Afternoon','Evening'])
    date = st.date_input('Preferred date')
    submitted = st.form_submit_button('Book appointment')
if 'pfma_confirmed' not in st.session_state:
    st.session_state.pfma_confirmed = False
if submitted:
    st.session_state.pfma_confirmed = True
if st.session_state.pfma_confirmed:
    st.success('We’ve got your request. A concierge will reach out shortly to confirm details and next steps.')
st.markdown('---')
st.subheader('Confirmation Drawers')
for label in ['Care Plan Confirmer','Cost Planner Confirmer','Care Needs','Care Preferences','Household & Legal Basics','Benefits & Coverage','Personal Info']:
    with st.expander(label):
        st.write('Pre-filled content goes here, editable before export.')
# PFMA_APPT_SCAFFOLD
