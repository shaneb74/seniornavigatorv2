
import streamlit as st

# Debug: non-visual logger
def _debug_log(msg: str):
    try:
        print(f"[SNAV] {msg}")
    except Exception:
        pass

_debug_log('LOADED: trusted_partners.py')


# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context


# Trusted Partners Page
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Trusted Partners")
st.markdown("<h2>Meet our vetted partners.</h2>", unsafe_allow_html=True)
st.markdown("<p>We carefully select these services for honesty and senior-first care—no ads, no upsell.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Partner cards
st.markdown('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; justify-items: center; padding: 2rem;">', unsafe_allow_html=True)

# Health Plan One
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 2rem; text-align: left; min-height: 300px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
st.markdown("### Health Plan One")
st.markdown("<p>A Medicare brokerage offering a one-stop shop to compare over 50 plans. Carrier-agnostic, no pushy calls—just clear options.</p>", unsafe_allow_html=True)
st.markdown("<ul><li>Free enrollment support</li><li>Price lock tool</li></ul>", unsafe_allow_html=True)
if st.button("Connect", key="hp_one_connect", type="primary"):
    st.write("Link to Health Plan One would go here.")
st.markdown('</div>', unsafe_allow_html=True)

# Senior Life AI
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 2rem; text-align: left; min-height: 300px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
st.markdown("### Senior Life AI")
st.markdown("<p>AI-driven tests for cognitive decline and fall prediction, using your phone camera for early insights.</p>", unsafe_allow_html=True)
st.markdown("<ul><li>Quick cognitive check</li><li>Fall-risk predictor</li></ul>", unsafe_allow_html=True)
if st.button("Start Test", key="senior_life_connect", type="primary"):
    st.write("Link to Senior Life AI would go here.")
st.markdown('</div>', unsafe_allow_html=True)

# PillSync
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 2rem; text-align: left; min-height: 300px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
st.markdown("### PillSync")
st.markdown("<p>Medication management with daily reminders, interaction alerts, and one-tap reordering—no spam.</p>", unsafe_allow_html=True)
st.markdown("<ul><li>Custom reminders</li><li>Interaction checks</li></ul>", unsafe_allow_html=True)
if st.button("Sign Up Free", key="pillsync_connect", type="primary"):
    st.write("Link to PillSync would go here.")
st.markdown('</div>', unsafe_allow_html=True)

# Longevity Link
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 2rem; text-align: left; min-height: 300px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
st.markdown("### Longevity Link")
st.markdown("<p>Long-term care coverage for home help, memory care, and hospice—lock in rates before they rise.</p>", unsafe_allow_html=True)
st.markdown("<ul><li>Covers home and facility care</li><li>Price stability</li></ul>", unsafe_allow_html=True)
if st.button("Get Quote", key="longevity_connect", type="primary"):
    st.write("Link to Longevity Link would go here.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Waiting Room", key="back_partners", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)