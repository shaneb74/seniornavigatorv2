from __future__ import annotations
import contextlib
import streamlit as st

try:
    from ui.cost_planner_template import section_header as _section_header
except Exception:
    _section_header = None

def section_header(title: str, subtitle: str | None = None):
    if _section_header:
        _section_header(title, subtitle or "")
        return
    st.markdown(f"### {title}")
    if subtitle: st.caption(subtitle)

@contextlib.contextmanager
def card():
    with st.container(border=True):
        yield

def nav_buttons(prev: str | None, nxt: str | None):
    cols = st.columns(2)
    with cols[0]:
        if prev and st.button("← Back", width="stretch", type="secondary", key=f"gcp_prev_{prev}"):
            from gcp_v2.nav import goto
            goto(prev)
    with cols[1]:
        if nxt and st.button("Continue →", width="stretch", type="primary", key=f"gcp_next_{nxt}"):
            from gcp_v2.nav import goto
            goto(nxt)
