
import streamlit as st

# Debug: non-visual logger
def _debug_log(msg: str):
    try:
        print(f"[SNAV] {msg}")
    except Exception:
        pass

_debug_log('LOADED: cost_planner.py')


# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context


# Cost Planner: Mode
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Cost Planner for your loved one")
st.markdown("<h2>Choose your planning style.</h2>", unsafe_allow_html=True)
st.markdown("<p>Estimating costs or Planning—your call.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Mode selection with tile style
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Planning Mode")
st.markdown("<p>Select how you’d like to explore costs.</p>", unsafe_allow_html=True)
st.button("Estimating costs", key="step_mode", type="primary")
st.button("Planning", key="free_mode", type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", key="back_cost", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)
st.write("Choose how deep you want to go right now.")
st.markdown('---')
if st.button('Estimating costs'):
    st.switch_page('pages/cost_planner_modules.py')
if st.button('Planning'):
    st.switch_page('pages/cost_planner_modules.py')