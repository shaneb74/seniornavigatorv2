import streamlit as st
from pathlib import Path

# Session guard: keep state consistent
if "care_context" not in st.session_state:
    st.session_state.care_context = {}
ctx = st.session_state.care_context

st.set_page_config(layout="wide")
st.title("Welcome")
st.caption("A simple starting point for families and professionals.")

# ============================= CSS =============================
st.markdown(
    """
    <style>
      /* Layout tweaks */
      .block-container { padding-top: 2rem; padding-bottom: 4rem; }

      /* HERO */
      .hero-wrap { display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 4rem; align-items: center; }
      @media (max-width: 1100px) { .hero-wrap { grid-template-columns: 1fr; gap: 2rem; } }

      .hero-h1 {
        font-size: clamp(28px, 5.6vw, 56px);
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: .2px;
        margin: 0 0 .25rem 0;
      }
      .hero-h2 {
        font-size: clamp(20px, 2.2vw, 24px);
        color: rgba(0,0,0,0.7);
        font-weight: 500;
        margin: .5rem 0 1.25rem 0;
      }
      .hero-actions { display: flex; gap: .75rem; flex-wrap: wrap; }
      .hero-photo {
        width: min(520px, 100%);
        margin: 0 auto;
        position: relative;
        transform: rotate(-3.2deg);
        filter: drop-shadow(0 12px 20px rgba(0,0,0,.18));
        border: 10px solid #fff;          /* photo border */
        border-radius: 6px;
        box-sizing: border-box;
      }

      /* Section divider */
      .divider { margin: 2rem 0 1.5rem 0; border: none; border-top: 1px solid rgba(0,0,0,.08); }

      /* Section heading */
      .section-kicker {
        font-size: clamp(22px, 2.8vw, 28px);
        font-weight: 800;
        letter-spacing: .12em;
        text-transform: uppercase;
        color: #2a2a2a;
        margin: .25rem 0 1rem 0;
      }

      /* Cards row */
      .cards {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
      }
      @media (max-width: 1000px) { .cards { grid-template-columns: 1fr; } }

      .card {
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 8px 28px rgba(0,0,0,.08);
        padding: 1rem 1rem 1.25rem 1rem;
        border: 1px solid rgba(0,0,0,.05);
      }
      .card-photo {
        width: 100%;
        border-radius: 16px;
        display: block;
        box-shadow: 0 6px 18px rgba(0,0,0,.12);
        margin-bottom: .75rem;
      }
      .card h4 { margin: .25rem 0 .25rem 0; font-size: 18px; }
      .card .sub { color: rgba(0,0,0,.6); font-size: 14px; margin-bottom: .5rem; }

      /* Button row inside card */
      .card-actions { display: flex; justify-content: flex-end; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================= Small helpers =============================
def html_image(path: str, classes: str = "", style: str = ""):
    """Render image via served /static path for pixel-perfect CSS sizing."""
    p = Path(path)
    if not p.exists():
        st.info(f"Add image at {path}")
        return
    st.markdown(f'<img src="/{p.as_posix()}" class="{classes}" style="{style}">', unsafe_allow_html=True)

def safe_image(path: str, width: int | str = 300):
    """Pure Streamlit helper in case you prefer st.image() semantics."""
    p = Path(path)
    if not p.exists():
        st.info(f"Add image at {path}")
        return
    st.image(str(p), width=width if isinstance(width, int) else width)

# ============================= HERO =============================
with st.container():
    st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)
    # Left column: typographic hero
    st.markdown(
        """
        <div>
          <div class="hero-h1">YOUR COMPASSIONATE<br>GUIDE TO SENIOR<br>CARE DECISIONS</div>
          <div class="hero-h2">
            Every care decision matters. We’re here to guide you — at no cost —
            whether planning for yourself or a loved one.
          </div>
          <div class="hero-actions">
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Right column: tilted “photo”
    st.markdown('<div style="display:flex;justify-content:center;">', unsafe_allow_html=True)
    html_image("static/images/Hero.png", classes="hero-photo")
    st.markdown("</div></div>", unsafe_allow_html=True)

    # Real Streamlit buttons under the hero text (inside the layout flow)
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("Start Now", key="hero_start"):
            st.switch_page("pages/tell_us_about_loved_one.py")
    with c2:
        if st.button("Log in", key="hero_login"):
            st.switch_page("pages/login.py")

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-kicker">How we can help you</div>', unsafe_allow_html=True)

# ============================= CARDS =============================
st.markdown('<div class="cards">', unsafe_allow_html=True)

# Card 1
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    html_image("static/images/Someone-Else.png", classes="card-photo")
    st.markdown("**I would like to support my loved ones**", unsafe_allow_html=True)
    st.markdown('<div class="sub">For someone</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 1])
    with col_b:
        if st.button("For someone", key="tile_someone_btn"):
            st.switch_page("pages/tell_us_about_loved_one.py")
    st.markdown("</div>", unsafe_allow_html=True)

# Card 2
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    html_image("static/images/Myself.png", classes="card-photo")
    st.markdown("**I’m looking for support just for myself**", unsafe_allow_html=True)
    st.markdown('<div class="sub">For myself</div>', unsafe_allow_html=True)
    col_c, col_d = st.columns([1, 1])
    with col_d:
        if st.button("For myself", key="tile_myself_btn"):
            st.switch_page("pages/tell_us_about_you.py")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # end .cards
