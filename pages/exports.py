import streamlit as st

st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("Exports")
st.markdown("<h2>Download your plan.</h2>", unsafe_allow_html=True)
st.markdown("<p>CSV or PDF summary.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Download buttons
st.download_button("Download CSV", data="placeholder,csv,data", file_name="plan.csv", mime="text/csv")
st.download_button("Download PDF", data="placeholder pdf", file_name="plan.pdf", mime="application/pdf")
