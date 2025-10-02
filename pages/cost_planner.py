
import streamlit as st

# Session-state guard (safe, no visual change)
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {},
        'person_name': 'Your Loved One',
    }

ctx = st.session_state.care_context
person_name = ctx.get('person_name', 'Your Loved One')

st.title(f"Cost Planner for {person_name}")

st.caption("Choose the level of detail that fits your needs right now.")

st.markdown("""
Not everyone needs the same level of detail. Some families just want a ballpark idea of what care might cost, while others
want a fully personalized view based on their situation.

- **Estimate Costs**  
  Choose this if you're simply curious what different care options might cost on average. It's quick, easy, and gives you a general picture without needing much detail.

- **Plan Costs**  
  Choose this if you'd like to build a personalized financial plan based on your (or your loved one's) specific circumstances. This uses your details to tailor the estimate for your family.
""")

st.markdown('---')

col1, col2, col3 = st.columns([1,1,1])

with col1:
    if st.button("Estimate Costs", key="cp_estimate"):
        ctx['planning_mode'] = 'estimating'
        st.switch_page('pages/cost_planner_modules.py')

with col2:
    if st.button("Plan Costs", key="cp_plan"):
        ctx['planning_mode'] = 'planning'
        st.switch_page('pages/cost_planner_modules.py')

with col3:
    if st.button("Back to Hub", key="cp_back_hub"):
        st.switch_page('pages/hub.py')
