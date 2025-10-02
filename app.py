import streamlit as st
from pathlib import Path

st.set_page_config(page_title="CCA Senior Navigator", layout="centered")

# ---------- CSS ----------
def inject_css(path: str):
    p = Path(path)
    if p.exists():
        mtime = int(p.stat().st_mtime)
        st.markdown(f"<style>{p.read_text()}</style><!-- v:{mtime} -->", unsafe_allow_html=True)

inject_css("static/style.css")

# ---------- Session flags ----------
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

# ---------- Page registration helpers ----------
def ensure_page(path: str, title: str, icon: str, default: bool=False):
    p = Path(path)
    if not p.exists():
        return None, path
    page = st.Page(path, title=title, icon=icon, default=bool(default)) if default else st.Page(path, title=title, icon=icon)
    return page, None

INTENDED = [
    # Entry & Hub
    ("pages/welcome.py", "Welcome", "👋", True),
    ("pages/hub.py", "Your Concierge Care Hub", "🏠", False),

    # Tell-us flows
    ("pages/tell_us_about_you.py", "Tell Us About You", "ℹ️", False),
    ("pages/tell_us_about_loved_one.py", "Tell Us About Loved One", "ℹ️", False),
    ("pages/professional_mode.py", "Professional Mode", "🧑‍⚕️", False),

    # Guided Care Plan (all subpages explicitly registered)
    ("pages/gcp.py", "Guided Care Plan", "🗺️", False),
    ("pages/gcp_daily_life.py", "GCP — Daily Life & Support", "🗺️", False),
    ("pages/gcp_health_safety.py", "GCP — Health & Safety", "🗺️", False),
    ("pages/gcp_context_prefs.py", "GCP — Context & Preferences", "🗺️", False),
    ("pages/gcp_recommendation.py", "GCP Recommendation", "🗺️", False),

    # Core planner stubs (make sure these exist in your repo or they'll be listed as missing)
    ("pages/cost_planner.py", "Cost Planner: Mode", "💰", False),
    ("pages/cost_planner_modules.py", "Cost Planner: Modules", "📊", False),
    ("pages/login.py", "Login", "🔐", False),
]

pages, missing = [], []
for args in INTENDED:
    page, miss = ensure_page(*args)
    if page: pages.append(page)
    if miss: missing.append(miss)

if missing:
    st.sidebar.warning("Missing pages detected:\n" + "\n".join(f"- " + m for m in missing))

if pages:
    pg = st.navigation(pages)
    pg.run()
else:
    st.error("No pages available. Check file paths in app.py.")

# ---------- Sidebar auth toggle ----------
with st.sidebar:
    st.markdown("---")
    if st.session_state.is_authenticated:
        st.success("Signed in")
        if st.button("Log out", key="logout_btn"):
            st.session_state.is_authenticated = False
            st.rerun()
    else:
        st.info("Not signed in")
        if st.button("Log in", key="login_btn"):
            if Path("pages/login.py").exists():
                st.switch_page("pages/login.py")
