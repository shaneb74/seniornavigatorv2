
import streamlit as st
from ui.theme import inject_theme

inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

# Debug: non-visual logger
def _debug_log(msg: str):
    try:
        print(f"[SNAV] {msg}")
    except Exception:
        pass

_debug_log('LOADED: cost_planner_mods.py')


# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context


# Cost Planner: Age-in-Place Upgrades
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Age-in-Place Upgrades for your loved one")
st.markdown("<h2>Make his home safer.</h2>", unsafe_allow_html=True)
st.markdown("<p>Add upgrades to support independence.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Upgrades options with tile style
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Upgrade Options")
st.markdown("<p>Select upgrades for your loved one's home.</p>", unsafe_allow_html=True)
st.write("Grab bars?")
st.button("Yes", key="cm_grab_yes", type="primary")
st.button("No", key="cm_grab_no", type="primary")

st.write("Stair lift?")
st.button("Yes", key="cm_stair_yes", type="primary")
st.button("No", key="cm_stair_no", type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_cm", type="secondary")
with col2:
    st.button("Next Option", key="next_cm", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
