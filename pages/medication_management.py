
import streamlit as st

# Debug: non-visual logger
def _debug_log(msg: str):
    try:
        print(f"[SNAV] {msg}")
    except Exception:
        pass

_debug_log('LOADED: medication_management.py')


# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context


# Medication Management
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Medication Management for your loved one")
st.markdown("<h2>Simplify his meds, avoid risks.</h2>", unsafe_allow_html=True)
st.markdown("<p>Review doses and interactions.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Medication review tile
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left; min-height: 250px;">', unsafe_allow_html=True)
st.markdown("### Med Review")
st.markdown("<p>Pills: 5 daily. Polypharmacy risk: Medium. Suggestion: Consolidate doses.</p>", unsafe_allow_html=True)
st.checkbox("This looks right?", key="med_man_confirm")
st.button("Save Med Plan", key="save_med_man", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", key="back_med", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)