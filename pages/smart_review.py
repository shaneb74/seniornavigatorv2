import streamlit as st

st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Smart Review")
st.markdown("<h2>Get expert insights on your plan.</h2>", unsafe_allow_html=True)
st.markdown("<p>Select an expert and submit for review.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Expert selection
expert = st.radio(
    "Choose Expert",
    ["Senior Living Advisor", "Physician Second Opinion", "Medicare Plan Review"]
)

# Submit
st.button("Submit for Review", type="primary")

# Placeholder output
st.info("Expert notes will appear here.")
