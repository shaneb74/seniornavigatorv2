import streamlit as st

from ui.theme import inject_theme

st.set_page_config(layout="wide")

inject_theme()

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

# Debug: non-visual logger
def _debug_log(msg: str):
    try:
        print(f"[SNAV] {msg}")
    except Exception:
        pass

_debug_log('LOADED: my_documents.py')

# Guard: ensure session state keys exist across cold restarts
if 'care_context' not in st.session_state:
    st.session_state.care_context = {
        'gcp_answers': {},
        'decision_trace': [],
        'planning_mode': 'exploring',
        'care_flags': {}
    }
ctx = st.session_state.care_context

# My Documents Page
st.markdown('<div class="documents-hero">', unsafe_allow_html=True)
st.title("My Documents")
st.markdown("<h2>Keep all of your loved one's records here.</h2>", unsafe_allow_html=True)
st.markdown("<p class='max-ch'>Safe storage for your care plans and more.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Document tiles
st.markdown('<div class="documents-grid">', unsafe_allow_html=True)

documents = [
    {
        "title": "Care Plan",
        "copy": "your loved one's guided care plan: Home care + VA benefits.",
        "view_key": "view_care_doc",
        "download_key": "download_care_doc",
    },
    {
        "title": "Cost Summary",
        "copy": "your loved one's budget: $1,500/month breakdown.",
        "view_key": "view_cost_doc",
        "download_key": "download_cost_doc",
    },
]

for doc in documents:
    st.markdown('<div class="documents-card card section">', unsafe_allow_html=True)
    st.markdown(f"<h3>{doc['title']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p class='documents-card__body max-ch'>{doc['copy']}</p>", unsafe_allow_html=True)
    st.markdown('<div class="documents-card__actions">', unsafe_allow_html=True)
    st.button("View", key=doc["view_key"], type="primary", use_container_width=True)
    st.button("Download", key=doc["download_key"], type="secondary", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Upload Placeholder
st.markdown('<div class="documents-card card section documents-upload">', unsafe_allow_html=True)
st.markdown("<h3>Upload Your Documents</h3>", unsafe_allow_html=True)
st.markdown("<p>Add insurance forms, med lists, or notes for your loved one.</p>", unsafe_allow_html=True)
st.button("Upload File", key="upload_doc", type="primary", use_container_width=True)
st.markdown('<div class="documents-divider"></div>', unsafe_allow_html=True)
st.button("Back to Hub", key="back_docs", type="secondary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
