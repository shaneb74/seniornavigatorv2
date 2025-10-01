import streamlit as st

# Initialize step if needed
if "gcp_step" not in st.session_state:
    st.session_state.gcp_step = 1

# Progress rail
total_steps = 12
step = st.session_state.gcp_step
segs = ''.join(
    f'<div class="seg{" active" if i < step else ""}"></div>'
    for i in range(total_steps)
)
rail = f'<div class="progress-rail">{segs}</div>'
st.markdown(rail, unsafe_allow_html=True)

# Sample question (design stub; repeat for 12)
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title(f"Guided Care Plan - Question {step}")
st.markdown("<h2>Example: What is your cognition level?</h2>", unsafe_allow_html=True)
st.markdown("<p>Select the option that best describes.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

cognition = st.radio(
    "Cognition Level",
    ["No issues", "Mild forgetfulness", "Moderate impairment", "Severe dementia"],
    key="cognition_level"
)

# Why we ask
st.markdown('<div class="scn-why-wrap">', unsafe_allow_html=True)
st.info("Why we ask: This helps determine if memory care is needed.")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back", type="secondary")
with col2:
    st.button("Next", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
