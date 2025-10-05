from __future__ import annotations
import streamlit as st

def goto(path: str) -> None:
    try:
        st.switch_page(path)  # type: ignore[attr-defined]
    except Exception:
        st.query_params["next"] = path
        st.rerun()
