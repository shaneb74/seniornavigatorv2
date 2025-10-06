from __future__ import annotations

from pathlib import Path

import streamlit as st

from senior_nav import navigation
from senior_nav.documents import list_documents, register_user_upload
from senior_nav.state import ensure_base_state, require_entry_ready
from senior_nav.ui import header, render_ai_launcher, set_page_config


set_page_config(title="My Documents")
ensure_base_state()
require_entry_ready()

header("My Documents", "View, download, and upload supporting files.")

documents = list_documents()
if not documents:
    st.info("Your Care Plan and Cost Summary will appear here after you save them.")
else:
    for doc in documents:
        with st.container(border=True):
            st.markdown(f"### {doc.title}")
            st.caption(f"Kind: {doc.kind} · Updated {doc.created_at}")
            doc_path = Path(doc.path)
            if doc_path.exists():
                data = doc_path.read_bytes()
                st.download_button(
                    "Download",
                    data=data,
                    file_name=doc_path.name,
                    mime=doc.metadata.get("mime", "application/octet-stream"),
                    key=f"download_{doc.doc_id}",
                )
                if doc_path.suffix in {".json", ".txt"}:
                    with st.expander("Preview"):
                        try:
                            st.code(doc_path.read_text("utf-8"), language="json")
                        except Exception:
                            st.write("(Binary file)")
            else:
                st.warning("Document file missing from disk. Try exporting again.")

st.markdown("---")

st.subheader("Upload a document")
uploaded = st.file_uploader("Add a file to share with your advisor", type=None)
if uploaded:
    register_user_upload(uploaded.name, uploaded.getvalue(), mime_type=uploaded.type)
    st.success(f"Uploaded {uploaded.name} to your documents.")
    st.experimental_rerun()

if st.button("Back to hub"):
    navigation.switch_page(navigation.HUB_PAGE)

render_ai_launcher()
