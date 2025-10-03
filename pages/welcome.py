import streamlit as st
from pathlib import Path

# ---------- Config ----------
HERO_IMG = Path("assets/Hero.png")
CARD_SOMEONE_IMG = Path("assets/Someone Else.png")
CARD_MYSELF_IMG = Path("assets/Myself.png")

st.title("Welcome")
st.caption("A simple starting point for families and professionals.")

# ---------- Hero ----------
c1, c2 = st.columns([1.1, 1])
with c1:
    st.markdown(
        """
        <div style="margin-top: 12px">
          <div style="color:#6b7280;font-weight:600">Concierge Care • Senior Navigator</div>
          <h1 style="margin: 8px 0 12px; font-size:40px; line-height:1.1;">
            Your compassionate<br/>guide to senior care decisions
          </h1>
          <p style="max-width:520px; color:#374151;">
            Every care decision matters. We’re here to guide you — at no cost —
            whether planning for yourself or a loved one.
          </p>
          <div style="display:flex; gap:10px; margin-top:14px;">
            <form action="#" method="post">
              <button class="stButton" style="background:#0B5CD8;color:#fff;border:none;border-radius:12px;padding:10px 14px;font-weight:600;" onclick="return false;">Start Now</button>
            </form>
            <form action="#" method="post">
              <button class="stButton" style="background:#111827;color:#fff;border:none;border-radius:12px;padding:10px 14px;font-weight:600;" onclick="return false;">Log in</button>
            </form>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    if HERO_IMG.exists():
        st.image(str(HERO_IMG), use_container_width=True, caption=None)
    else:
        st.info("Add hero image at assets/Hero.png")

st.markdown("---")

# ---------- “How we can help you” ----------
st.markdown('<h2 style="margin-top:8px;">How we can help you</h2>', unsafe_allow_html=True)

colL, colR = st.columns(2)

def tile(img_path: Path, title: str, subtitle_right: str, primary_key: str, primary_to: str):
    with st.container(border=True):
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
        else:
            st.info(f"Add image at {img_path}")
        st.markdown(f"<p style='font-size:18px;margin:6px 0 12px;'>{title}</p>", unsafe_allow_html=True)
        row = st.columns([1,1,1])
        with row[0]:
            if st.button("Continue", key=primary_key, use_container_width=True):
                st.switch_page(primary_to)
        with row[-1]:
            st.markdown(
                f"<div style='text-align:right;'><span class='button-link'>{subtitle_right}</span></div>",
                unsafe_allow_html=True,
            )

with colL:
    tile(
        CARD_SOMEONE_IMG,
        "I would like to support my loved ones",
        "For someone",
        "welcome_for_someone",
        "pages/tell_us_about_loved_one.py",
    )

with colR:
    tile(
        CARD_MYSELF_IMG,
        "I’m looking for support just for myself",
        "For myself",
        "welcome_for_myself",
        "pages/tell_us_about_you.py",
    )

# ---------- For professionals (secondary) ----------
st.markdown(
    """
    <div style="display:flex; justify-content:center; margin-top:8px;">
      <a href="#" id="for-pro" style="display:inline-flex;align-items:center;gap:8px;
         background:#f8fafc;color:#111827;border:1px solid #e5e7eb;border-radius:10px;
         padding:10px 14px;text-decoration:none;font-weight:600;">For professionals</a>
    </div>
    <script>
      const link = document.getElementById("for-pro");
      if (link) link.addEventListener("click", (e) => { e.preventDefault(); window.parent.postMessage({type:"NAV", page:"pages/professional_mode.py"}, "*"); });
    </script>
    """,
    unsafe_allow_html=True,
)

# Minimal JS → Streamlit navigation bridge
nav_target = st.experimental_get_query_params().get("nav", [None])[0]
if nav_target == "pro":
    st.switch_page("pages/professional_mode.py")
