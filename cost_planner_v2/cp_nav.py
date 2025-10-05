def goto(path: str):
    import streamlit as st
    try:
        st.switch_page(path)
    except Exception:
        st.query_params["next"] = path
        st.rerun()
