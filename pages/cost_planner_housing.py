import streamlit as st

# Housing Path Detail
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Housing Path for John")
st.markdown("<h2>Keep or sell the family home?</h2>", unsafe_allow_html=True)
st.markdown("<p>Explore options to fit John’s budget.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Mockup housing options
housing = st.radio("Choose your path:", ["Keep", "Sell"], key="housing_path")
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; text-align: left;">', unsafe_allow_html=True)
if housing == "Keep":
    st.write("John’s 2-bed home:")
    st.write("Mortgage: ~ $2,000/mo")
    st.write("HOA: ~ $300/mo")
    st.write("Utilities: ~ $400/mo")
    st.write("Insurance: ~ $1,500/mo")
    st.write("Total: $5,200/mo")
    st.button("Adjust Costs", key="adjust_keep", type="primary")
    st.button("Add HELOC", key="add_heloc", type="primary")
    st.button("Add Reverse Mortgage", key="add_reverse", type="primary")
else:
    st.write("Sell John’s home:")
    st.write("Est. value: ~ $450,000")
    st.button("Get Offer", key="get_offer", type="primary")
    st.write("Reinvest options:")
    st.button("Adjust Rent", key="adjust_rent", type="primary")
    st.button("Adjust New Mortgage", key="adjust_mortgage", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_to_modules_hp", type="secondary")
with col2:
    st.button("Save & Next", key="next_hp", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
