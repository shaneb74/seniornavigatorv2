import streamlit as st

# ... existing hub layout ...

# Guided Care Plan tile
st.subheader("Guided Care Plan")
if st.button('Start Plan', key='hub_gcp_start'):
    st.switch_page('pages/gcp.py')

# ... other tiles remain unchanged ...
