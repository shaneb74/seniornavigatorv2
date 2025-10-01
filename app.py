import streamlit as st
from pathlib import Path

# Set page config for centered layout
st.set_page_config(page_title="Senior Care Navigator Demo", layout="centered")

# CSS Injection for Streamlit Cloud
def inject_css(path: str):
    css_path = Path(path)
    if css_path.exists():
        mtime = int(css_path.stat().st_mtime)
        st.markdown(f"<style>{css_path.read_text()}</style><!-- v:{mtime} -->", unsafe_allow_html=True)
    else:
        st.warning(f"Missing CSS: {path}")

# Load CSS (ensure static/style.css in repo root)
inject_css("static/style.css")

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1
if "care_option" not in st.session_state:
    st.session_state.care_option = None

# Sidebar for page navigation
with st.sidebar:
    page = st.radio("Navigate", ["Home", "Details"], key="nav_radio")

# Progress rail (for both pages)
total_steps = 5
step = st.session_state.step
segs = ''.join(
    f'<div class="seg{" active" if i < step else ""}"></div>'
    for i in range(total_steps)
)
rail = f'<div class="progress-rail">{segs}</div>'
st.markdown(rail, unsafe_allow_html=True)

# Page: Home
if page == "Home":
    st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
    st.title("Senior Care Navigator Demo")
    st.markdown("<h2>Welcome</h2>", unsafe_allow_html=True)
    st.markdown("<p>Select a care option to begin planning.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Radio buttons styled as pills
    care_option = st.radio(
        "Choose a care option",
        ["In-Home Care", "Assisted Living", "Memory Care"],
        key="care_option"
    )

    # Navigation buttons
    st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Reset", key="reset", type="secondary"):
            st.session_state.step = 1
            st.session_state.care_option = None
            st.rerun()
    with col2:
        if st.button("Next", key="next", type="primary"):
            if care_option:
                st.session_state.step = 2
                st.session_state.care_option = care_option
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Page: Details
elif page == "Details":
    st.markdown('<div class="scn-hero">', unsafe_allow_html=True)
    st.title("Care Details")
    st.markdown("<h2>Your Plan</h2>", unsafe_allow_html=True)
    st.markdown(f"<p>Selected: {st.session_state.get('care_option', 'None')}</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Display sample radio group
    st.write("Care Type")
    care_type = st.radio(
        "Refine care type",
        ["Basic", "Advanced", "Specialized"],
        key="care_type"
    )

    # Navigation buttons
    st.markdown('<div class="scn-nav-row">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back", key="back", type="secondary"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Finish", key="finish", type="primary"):
            st.session_state.step = 3
            st.success("Plan completed!")
    st.markdown('</div>', unsafe_allow_html=True)
