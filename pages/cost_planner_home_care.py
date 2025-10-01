import streamlit as st

# Home Care Support Detail
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Home Care Support for John")
st.markdown("<h2>Customize your care hours.</h2>", unsafe_allow_html=True)
st.markdown("<p>Slide to see how much support fits John’s needs.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Mockup slider and details
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left;">', unsafe_allow_html=True)
st.write("Weekly Hours: 0 to 40")
st.write("Tasks: Morning help, evening check-ins, meal prep")
st.write("Cost range: $1,050 - $1,500/month @ $21/hr")
st.write("Current: ~ $1,260/month (20 hrs)")
st.button("Adjust Hours", key="adjust_hours", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_to_modules_hc", type="secondary")
with col2:
    st.button("Save & Next", key="next_hc", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
