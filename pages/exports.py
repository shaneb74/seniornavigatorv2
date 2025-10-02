import streamlit as st
from datetime import datetime
st.header('Exports')
st.write('CSV and PDF export scaffolding')
fn = 'CCA_{Last}_{First}_{date}_{Module}.pdf'
st.code('File naming: ' + 'CCA_{LastName}_{FirstName}_{YYYYMMDD}_{Module}.pdf')
if st.button('Prepare CSV'):
    st.info('Would generate: person_id, care_type, ADL bucket, mobility, monthly totals, benefits, runway, timestamp')
if st.button('Prepare PDF'):
    st.info('Would include: cover page, recommendation, DecisionTrace, blurbs, cost summary, next-steps, contact info')
