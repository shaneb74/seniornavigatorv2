import streamlit as st

# Cost Planner: Recommended Modules
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Recommended Cost Modules")
st.markdown("<h2>Adjust your care options.</h2>", unsafe_allow_html=True)
st.markdown("<p>Slide to see costs update instantly.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Module cards
st.markdown('<div style="display: flex; flex-wrap: wrap; gap: 1rem;">', unsafe_allow_html=True)
st.markdown('<div style="flex: 1; min-width: 300px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem;">', unsafe_allow_html=True)
st.markdown("### Daily Living Aids")
st.write("Adjust support level (e.g., 0-10 hours/week)")
st.button("Open Slider", key="daily_aids_open", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="flex: 1; min-width: 300px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem;">', unsafe_allow_html=True)
st.markdown("### Home Care Hours")
st.write("Set weekly care hours (e.g., 0-40)")
st.button("Open Slider", key="home_care_open", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="flex: 1; min-width: 300px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem;">', unsafe_allow_html=True)
st.markdown("### Facility Options")
st.write("Compare assisted living vs. memory care")
st.button("Open Options", key="facility_open", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Mode", key="back_to_mode", type="secondary")
with col2:
    st.button("Next: Expert Review", key="next_review", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
