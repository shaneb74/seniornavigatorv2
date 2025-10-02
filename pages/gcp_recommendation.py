import streamlit as st

# Guard: ensure session state keys exist
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {},
        'person_name': 'Your Loved One'
    }

ctx = st.session_state.care_context
person_name = ctx.get('person_name', 'Your Loved One')

# Placeholder recommendation values (to be replaced by engine later)
recommendation = ctx.get('recommendation', 'Assisted Living')
reason_text = ctx.get('recommendation_reason', None)

st.title('Your Care Recommendation')

# Personalized intro
st.write(f"Based on what we know about **{person_name}**, this is their personalized expert recommendation.")

# Big clear recommendation
st.markdown(f"## 👉 {recommendation}")

# Supporting explanation (template for now)
if reason_text:
    st.write(reason_text)
else:
    st.write(
        "This recommendation is based on the information you shared about daily life, health, safety, and care preferences. "
        "It highlights the option that provides the right balance of support, independence, and safety at this stage. "
        "Every family is unique — this is a starting point to guide your conversations and next steps."
    )

st.markdown('---')

col1, col2 = st.columns(2)
with col1:
    if st.button('Back to Hub', key='reco_back_hub'):
        st.switch_page('pages/hub.py')
with col2:
    if st.button('Open Cost Planner', key='reco_open_cost'):
        st.switch_page('pages/cost_planner.py')
