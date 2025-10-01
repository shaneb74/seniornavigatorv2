import streamlit as st

# Cost Planner: Housing Path Drawer
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Housing Path")
st.markdown("<h2>Keep or sell your home?</h2>", unsafe_allow_html=True)
st.markdown("<p>Adjust your options below.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Housing decision
housing = st.radio("Keep the house?", ["Yes", "No"], key="housing_choice")

if housing == "Yes":
    st.markdown('<div style="display: flex; flex-wrap: wrap; gap: 1rem;">', unsafe_allow_html=True)
    st.markdown('<div style="flex: 1; min-width: 300px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem;">', unsafe_allow_html=True)
    st.write("Mortgage: $0 - $4,000")
    st.write("~ $2,500/mo")
    st.button("Adjust", key="mortgage_adjust", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="flex: 1; min-width: 300px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem;">', unsafe_allow_html=True)
    st.write("HOA: $0 - $800")
    st.write("~ $300/mo")
    st.button("Adjust", key="hoa_adjust", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="flex: 1; min-width: 300px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem;">', unsafe_allow_html=True)
    st.write("Utilities: $200 - $600")
    st.write("~ $400/mo")
    st.button("Adjust", key="utilities_adjust", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="flex: 1; min-width: 300px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem;">', unsafe_allow_html=True)
    st.write("Insurance: $1,000 - $3,000")
    st.write("~ $1,500/mo")
    st.button("Adjust", key="insurance_adjust", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="display: flex; gap: 1rem; margin-top: 1rem;">', unsafe_allow_html=True)
    st.button("Home Equity Line of Credit", key="heloc_open", type="primary")
    st.button("Reverse Mortgage", key="reverse_open", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("Keeping = $5,200/mo")

else:
    st.markdown('<div style="display: flex; flex-wrap: wrap; gap: 1rem;">', unsafe_allow_html=True)
    st.markdown('<div style="flex: 1; min-width: 300px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem;">', unsafe_allow_html=True)
    st.write("Sell in 6 months?")
    st.button("Get ~$450k", key="sell_value", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="flex: 1; min-width: 300px; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem;">', unsafe_allow_html=True)
    st.write("Reinvest?")
    st.button("Adjust Rent/Mortgage", key="reinvest_adjust", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Modules", key="back_to_modules_house", type="secondary")
with col2:
    st.button("Save & Next", key="next_house", type="primary")
st.markdown('</div>', unsafe_allow_html=True)
