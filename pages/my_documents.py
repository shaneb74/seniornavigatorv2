from ui.ux_enhancements import apply_global_ux, render_stepper

import streamlit as st
apply_global_ux()
render_stepper()


# My Documents Page
st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
st.title("My Documents")
st.markdown("<h2>Keep all of John’s records here.</h2>", unsafe_allow_html=True)
st.markdown("<p>Safe storage for your care plans and more.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Document tiles
st.markdown('<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 2rem; justify-items: center; padding: 2rem;">', unsafe_allow_html=True)

# Care Plan Document
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 2rem; text-align: left; min-height: 250px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
st.markdown("### Care Plan")
st.markdown("<p>John’s guided care plan: Home care + VA benefits.</p>", unsafe_allow_html=True)
st.button("View", key="view_care_doc", type="primary")
st.button("Download", key="download_care_doc", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)

# Cost Summary Document
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 2rem; text-align: left; min-height: 250px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
st.markdown("### Cost Summary")
st.markdown("<p>John’s budget: $1,500/month breakdown.</p>", unsafe_allow_html=True)
st.button("View", key="view_cost_doc", type="primary")
st.button("Download", key="download_cost_doc", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)

# Upload Placeholder
st.markdown('<div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 2rem; text-align: left; min-height: 250px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
st.markdown("### Upload Your Documents")
st.markdown("<p>Add insurance forms, med lists, or notes for John.</p>", unsafe_allow_html=True)
st.button("Upload File", key="upload_doc", type="primary")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Navigation
st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])
with col1:
    st.button("Back to Hub", key="back_docs", type="secondary")
st.markdown('</div>', unsafe_allow_html=True)