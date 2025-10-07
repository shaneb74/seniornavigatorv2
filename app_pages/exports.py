import streamlit as st
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

# Debug: non-visual logger
def _debug_log(msg: str):
    try:
        print(f"[SNAV] {msg}")
    except Exception:
        pass

_debug_log('LOADED: exports.py')

# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context

# Exports Page (placeholder - moved to export_results)
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Exports")
st.markdown("<h2>Your exported data.</h2>", unsafe_allow_html=True)
st.markdown("<p>This page is now handled by Export Results. Please use that page.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", key="back_exports", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
