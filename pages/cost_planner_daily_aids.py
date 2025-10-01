import streamlit as st

# Daily Living Aids Detail
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Daily Living Aids for John")
st.markdown("<h2>Pick the tools that help.</h2>", unsafe_allow_html=True)
st.markdown("<p>Toggle to see what adds comfort and safety.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Mockup toggles and details
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left;">', unsafe_allow_html=True)
st.write("Select aids for John:")
st.button("Bathing Support ($150)", key="toggle_bathing", type="primary")
st.button("Meal Prep Aid ($100)", key="toggle_meal", type="primary")
st.button("Med Reminder ($60)", key="toggle_med", type="primary")
st.write("Total add-ons: $310")
st.button("Adjust Selections", key="adjust_aids", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_to_modules_da", type="secondary")
with col2:
    st.button("Save & Next", key="next_da", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
