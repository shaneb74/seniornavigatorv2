"""Dashboard hub: high-fidelity layout."""
from __future__ import annotations
import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Dashboard", layout="wide")

# ---------- GLOBAL DASHBOARD CSS INJECTION ----------
DASHBOARD_CSS = """
<style>
:root{
  --brand:#0B5CD8;
  --ink:#0f172a;
  --muted:#4b5563;
  --card:#ffffff;
  --bg:#f8fafc;
  --ring:rgba(11,92,216,.14);
  --radius:16px;
  --chip:#eef2ff;
  --chip-ink:#1e3a8a;
}
body, .block-container { background: var(--bg); }
.block-container { max-width: 1160px; padding-top: 8px; }

header[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }

.notice {
  display:flex; align-items:center; gap:.5rem;
  background:#eef6ff; color:#0b3e91; border:1px solid #cfe4ff;
  padding:.625rem .9rem; border-radius:10px; font-size:.92rem; margin: 6px 0 18px;
}
.notice .x { margin-left:auto; opacity:.6; }

.hstack{ display:flex; align-items:center; gap:.5rem; }
.vstack{ display:flex; flex-direction:column; gap:.5rem; }

.page-title {
  letter-spacing:.08em; font-weight:800; font-size:2rem; color:var(--ink);
  margin: 4px 0 14px;
}

.grid {
  display:grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.card {
  background:var(--card);
  border: 1px solid #e5e7eb;
  border-radius: var(--radius);
  padding: 18px;
  box-shadow: 0 1px 0 rgba(16,24,40,.04), 0 1px 2px rgba(16,24,40,.06);
}
.card h3{
  margin: 0 0 8px; font-size:1.15rem; font-weight:750; color:var(--ink);
}
.card p{
  margin: 2px 0 14px; color:var(--muted); font-size:.98rem; line-height:1.45;
}
.badge{
  display:inline-flex; align-items:center; gap:.35rem;
  font-size:.78rem; padding:.28rem .55rem; border-radius:999px;
  background: #eef2ff; color:#1e3a8a; border:1px solid #c7d2fe;
}
.badge .dot{
  width:.45rem; height:.45rem; border-radius:50%; background:#6b8afd;
}
.status{
  display:inline-flex; align-items:center; gap:.4rem; color:#16a34a;
  font-size:.9rem; font-weight:600;
}
.status .tick{ width: .9rem; height: .9rem; border:2px solid #16a34a; border-radius:50%; display:inline-block; position:relative;}
.status .tick:after{ content:""; position:absolute; width:.35rem; height:.2rem; border-left:2px solid #16a34a; border-bottom:2px solid #16a34a; transform: rotate(-45deg); left:.16rem; top:.25rem;}

.btn {
  display:inline-flex; align-items:center; justify-content:center; gap:.45rem;
  font-weight:700; font-size:.95rem;
  padding:.6rem .9rem; border-radius:10px; border:1px solid #d0d7e3; background:#f8fbff; color:#0b3e91;
  transition: all .15s ease;
}
.btn.primary { background:var(--brand); color:white; border-color:transparent; }
.btn:hover { box-shadow:0 0 0 4px var(--ring); transform: translateY(-1px); }

.kicker { color:#79808d; font-size:.88rem; margin-left:.35rem; }

.tile-row {
  display:grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 14px;
}
.tile {
  background:var(--card);
  border:1px solid #e5e7eb; border-radius:14px; padding:14px 16px;
  display:flex; align-items:center; justify-content:space-between;
}
.tile .title { font-weight:700; color:var(--ink); }
.tile .subtitle { color:var(--muted); font-size:.92rem; margin-top:2px; }
.tile .btn { padding:.45rem .75rem; }
.gradient {
  background: radial-gradient(120% 120% at 85% 10%, #ffecec 0%, rgba(255,255,255,0) 40%),
              radial-gradient(120% 120% at 10% 90%, #eef6ff 0%, rgba(255,255,255,0) 42%),
              var(--card);
}
.hr { height: 1px; background:#e5e7eb; margin: 8px 0 10px; border-radius:1px; }
</style>
"""
st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)

# ---------- TOP NOTICE ----------
st.markdown(
    """
    <div class="notice">
      <span>Log in for a better experience — continue where you left off, with your information kept secure and confidential following HIPAA guidelines.</span>
      <span class="x">✕</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- ASSESSMENT CONTEXT BAR ----------
col_a, col_b = st.columns([0.8, 0.2])
with col_a:
    st.markdown('<div class="page-title">DASHBOARD</div>', unsafe_allow_html=True)
with col_b:
    # right-side tiny context chips
    st.markdown(
        """
        <div style="display:flex; gap:.4rem; justify-content:flex-end; margin-top:6px;">
          <span class="kicker">Assessment</span>
          <span class="badge"><span class="dot"></span> For someone</span>
          <span class="badge">John</span>
          <span class="badge">Add +</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")  # small spacer

# ---------- CARD GRID ----------
st.markdown('<div class="grid">', unsafe_allow_html=True)

# Card 1: Understand the situation (Guided Care Plan)
st.markdown(
    """
    <div class="card">
      <div class="hstack" style="justify-content:space-between;">
        <h3>Understand the situation</h3>
        <span class="badge">🧭 Guided Care Plan</span>
      </div>
      <p>
        <span class="hstack" style="gap:.5rem;">
          <span style="opacity:.9;">Recommendation</span>
          <strong>In-Home Care</strong>
        </span>
      </p>
      <div class="hstack" style="gap:.6rem;">
        <a class="btn" href="?view=see_responses">See responses</a>
        <a class="btn" href="?view=start_over">Start over</a>
        <span class="status"><span class="tick"></span> Completed</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Card 2: Understand the costs (Cost Estimator)
st.markdown(
    """
    <div class="card">
      <div class="hstack" style="justify-content:space-between;">
        <h3>Understand the costs</h3>
        <span class="badge">🧮 Cost Estimator</span>
      </div>
      <p>Assess the cost structure for various care options for John. The cost estimate will automatically update based on your selected choices.</p>
      <div class="hstack" style="gap:.6rem;">
        <a class="btn primary" href="?view=start_costs">Start</a>
        <span class="kicker">Next step ✺</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Card 3: Connect with an advisor
st.markdown(
    """
    <div class="card">
      <div class="hstack" style="justify-content:space-between;">
        <h3>Connect with an advisor to plan the care</h3>
        <span class="badge">🎧 Get Connected</span>
      </div>
      <p>Whenever you’re ready to meet with an advisor.</p>
      <a class="btn primary" href="?view=get_connected">Get connected</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Card 4: FAQs & Answers (AI Agent) with soft gradient
st.markdown(
    """
    <div class="card gradient">
      <div class="hstack" style="justify-content:space-between;">
        <h3>FAQs &amp; Answers</h3>
        <span class="badge">✨ AI Agent</span>
      </div>
      <p>Receive instant, tailored assistance from our advanced AI chat.</p>
      <a class="btn" href="?view=ai_open">Open</a>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('</div>', unsafe_allow_html=True)  # end grid

# ---------- START FROM SCRATCH ----------
st.markdown(
    """
    <div class="hstack" style="gap:.5rem; margin-top:14px;">
      <span class="badge">↻ Start from scratch</span>
      <span class="kicker">Chose this option if you would like remove saved progress for John and start fresh.</span>
    </div>
    <div class="hr"></div>
    """,
    unsafe_allow_html=True,
)

# ---------- ADDITIONAL SERVICES ROW ----------
st.markdown(
    """
    <div style="font-weight:800; margin: 2px 0 8px; color:var(--ink);">Additional services</div>
    <div class="tile-row">
      <div class="tile">
        <div class="vstack">
          <div class="title">AI Health Check</div>
          <div class="subtitle">Get insights about John overall body health</div>
        </div>
        <a class="btn" href="?view=health_open">Open</a>
      </div>
      <div class="tile">
        <div class="vstack">
          <div class="title">Learning Center</div>
          <div class="subtitle">Media Center</div>
        </div>
        <a class="btn" href="?view=media_open">Open</a>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- NAVIGATION FALLBACKS ----------
# If your app uses st.switch_page, wire query params to it here.
view = st.query_params.get("view")
if view:
    # Replace these with your actual page routes if available.
    try:
        if view == "start_costs":
            st.switch_page("pages/02_Cost_Estimator.py")
        elif view == "get_connected":
            st.switch_page("pages/05_Get_Connected.py")
        elif view == "ai_open":
            st.switch_page("pages/06_AI_Agent.py")
        elif view == "see_responses":
            st.switch_page("pages/01_Guided_Care_Plan.py")
        elif view == "start_over":
            # placeholder for reset logic
            st.experimental_rerun()
        elif view == "health_open":
            st.switch_page("pages/07_AI_Health_Check.py")
        elif view == "media_open":
            st.switch_page("pages/08_Learning_Center.py")
    except Exception:
        # If switch_page is not available, we simply render the hub.
        pass
