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

_debug_log('LOADED: export_results.py')

# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context

# Export Results Page
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Export Results")
st.markdown('<div style="background: #f0f0f0; padding: 1rem; border: 1px solid #e0e0e0; border-radius: 8px; margin-bottom: 1.5rem; color: #374151; font-size: 0.9rem;">Exports are protected-requires login. <span style="color: #666;">(Design note: Auth gate goes here.)</span></div>', unsafe_allow_html=True)
st.markdown("<h2>Here's what you've built for your loved one.</h2>", unsafe_allow_html=True)
st.markdown("<p>Download your plans below-secure and ready.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Export tiles
st.markdown('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; justify-items: center; padding: 2rem;">', unsafe_allow_html=True)

# Export Care Plan
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 2rem; text-align: left; min-height: 250px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1); opacity: 0.6;">', unsafe_allow_html=True)
st.markdown("### Export Care Plan")
st.markdown("<p>Your guided care plan: Home care + VA benefits + hearing aids.</p>", unsafe_allow_html=True)
st.button("Export Care Plan", key="export_care", type="primary", disabled=True, help="Login required")
st.markdown('</div>', unsafe_allow_html=True)

# Export Cost Summary
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 2rem; text-align: left; min-height: 250px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1); opacity: 0.6;">', unsafe_allow_html=True)
st.markdown("### Export Cost Summary")
st.markdown("<p>Your budget breakdown: $1,500/month for your loved one's care.</p>", unsafe_allow_html=True)
st.button("Export Cost Summary", key="export_cost", type="primary", disabled=True, help="Login required")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", key="back_export", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
