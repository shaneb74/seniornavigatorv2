
import streamlit as st

# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context


# Cost Planner: Housing Path
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Housing Path for your loved one")
st.markdown("<h2>Plan his living options.</h2>", unsafe_allow_html=True)
st.markdown("<p>Decide to stay or explore new paths.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Housing options with tile style
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Housing Choices")
st.markdown("<p>Select your loved one’s living preference.</p>", unsafe_allow_html=True)
st.write("Stay home?")
st.button("Yes", key="hp_stay_yes", type="primary")
st.button("No", key="hp_stay_no", type="primary")

st.write("Assisted living?")
st.button("Yes", key="hp_assist_yes", type="primary")
st.button("No", key="hp_assist_no", type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_hp", type="secondary")
with col2:
    st.button("Next Option", key="next_hp", type="primary")
st.markdown('</div>', unsafe_allow_html=True)