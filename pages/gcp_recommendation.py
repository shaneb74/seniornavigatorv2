
import streamlit as st

if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'person_name': 'Your Loved One',
        'gcp_answers': {},
        'decision_trace': [],
    }

name = st.session_state.care_context.get('person_name', 'Your Loved One')

st.title(f"Guided Care Plan Recommendation for {name}")
st.write("This is a placeholder so navigation doesn't break. The real recommendation view is wired elsewhere.")

col1, col2 = st.columns(2)
with col1:
    if st.button("Back to Hub", key="gcp_rec_back"):
        st.switch_page("pages/hub.py")
with col2:
    if st.button("Open Cost Planner", key="gcp_rec_open_cp"):
        st.switch_page("pages/cost_planner.py")
