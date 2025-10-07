import streamlit as st
from contextlib import contextmanager

@contextmanager
def card_panel(padding="1rem", gap="1rem", **kwargs):
    """
    Context-managed card wrapper used as:
        with card_panel(padding="..."):
            ...children...
    """
    st.markdown(
        f"""
        <div class="sn-card-panel" style="
            padding:{padding};
            display:flex; flex-direction:column; gap:{gap};
            background:var(--surface, #f6f8fa);
            border:1px solid rgba(0,0,0,.08);
            border-radius:16px;
        ">
        """,
        unsafe_allow_html=True,
    )
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)

# Generic fallbacks for any other component names referenced in legacy code.
def __getattr__(name: str):
    # Non-context-manager placeholder: prints a small notice, returns None.
    def _fallback(*args, **kwargs):
        st.caption(f"ui.components.{name}() placeholder")
    return _fallback
