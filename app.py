
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="CCA Senior Navigator", layout="centered")

def inject_css(path: str):
    p = Path(path)
    if p.exists():
        mtime = int(p.stat().st_mtime)
        st.markdown(f"<style>{p.read_text()}</style><!-- v:{mtime} -->", unsafe_allow_html=True)

inject_css("static/style.css")

def ensure_page(path: str, title: str, icon: str, default: bool=False):
    p = Path(path)
    if not p.exists():
        return None, path
    page = st.Page(path, title=title, icon=icon, default=bool(default)) if default else st.Page(path, title=title, icon=icon)
    return page, None

# NOTE: This is only the registration delta; keep your existing INTENDED list.
INTENDED = [
    ("pages/welcome.py", "Welcome", "👋", True),
    ("pages/hub.py", "Hub", "🏠", False),
    ("pages/login.py", "Login / Sign up", "🔐", False),
]

# In a real app.py this list merges with the rest of your pages.
pages = []
missing = []
for args in INTENDED:
    page, miss = ensure_page(*args)
    if page:
        pages.append(page)
    if miss:
        missing.append(miss)

# If you paste this into your main app.py, merge 'pages' with your full set before calling st.navigation
if missing:
    st.sidebar.warning("Missing pages detected:\n" + "\n".join(f"- {m}" for m in missing))

if pages:
    pg = st.navigation(pages)
    pg.run()
