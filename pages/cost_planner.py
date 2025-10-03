import streamlit as st
from ui.theme import inject_theme


inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)


if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'estimating',
        'care_flags': {},
        'person_name': 'Your Loved One',
    }

ctx = st.session_state.care_context
person_name = ctx.get('person_name', 'Your Loved One')

st.title(f"Cost Planner for {person_name}")
st.caption("Choose the level of detail that fits your needs right now.")

st.markdown(
"""
Not everyone needs the same level of detail. Some families just want a ballpark idea of what care might cost, while others
want a fully personalized view based on their situation.

- **Estimate Costs**  
  Quick, high-level monthly estimate using a few selections. You can refine later.

- **Plan Costs**  
  Full, personalized planning with detailed modules. Best if you're ready to go deeper.
"""
)

st.markdown('---')

col1, col2, col3 = st.columns([1,1,1])

with col1:
    if st.button("Estimate Costs", key="cp_estimate"):
        ctx['planning_mode'] = 'estimating'
        st.switch_page('pages/cost_planner_estimate.py')

with col2:
    if st.button("Plan Costs", key="cp_plan"):
        ctx['planning_mode'] = 'planning'
        st.switch_page('pages/cost_planner_estimate.py')

with col3:
    if st.button("Back to Hub", key="cp_back_hub"):
        st.switch_page('pages/hub.py')

st.markdown('</div>', unsafe_allow_html=True)