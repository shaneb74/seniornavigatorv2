import streamlit as st

# Welcome screen (Audiencing)
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Senior Care Navigator")
st.markdown("<h2>Find the right care, step by step.</h2>", unsafe_allow_html=True)
st.markdown("<p>Let's get started by understanding who you're planning for.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Role chips
role = st.radio(
    "Who is this plan for?",
    ["Self", "Spouse/Partner", "Adult child", "Relative", "Friend/Neighbor", "Professional"],
    key="audience_role"
)

# Optional inputs
zip_code = st.text_input("ZIP Code (optional)", max_chars=5, key="zip")
age_band = st.radio(
    "Age band (optional)",
    ["<65", "65–74", "75–84", "85–89", "90+"],
    key="age_band"
)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col2:
    st.button("Continue to Hub", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
