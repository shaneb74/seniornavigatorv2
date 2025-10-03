"""Concierge Care Hub — streamlined dashboard layout."""

import streamlit as st


st.set_page_config(page_title="Concierge Care Hub", layout="wide")


# ---------- Session guard ----------
if "care_context" not in st.session_state:
    st.session_state.care_context = {
        "person_name": "Your Loved One",
        "gcp_answers": {},
        "gcp_recommendation": None,  # e.g., 'In-home care' | 'Assisted living' | 'Memory care' | 'None'
        "gcp_cost": None,  # e.g., '$5,200/mo'
    }


ctx = st.session_state.care_context
person_name = ctx.get("person_name", "Your Loved One")


# ---------- Helpers ----------
def reset_guided_plan() -> None:
    """Clear Guided Care Plan state so the user can start over."""

    ctx["gcp_answers"] = {}
    ctx["gcp_recommendation"] = None
    ctx["gcp_cost"] = None


def status_chip(label: str) -> str:
    return f'<span class="hub-chip">{label}</span>'


def render_card(
    *,
    key: str,
    icon: str,
    title: str,
    subtitle: str,
    description: str,
    chips: list[str] | None,
    primary_label: str,
    primary_action,
    secondary_label: str | None = None,
    secondary_action=None,
) -> None:
    """Render a dashboard card with consistent layout and controls."""

    with st.container():
        st.markdown("<div class='hub-card'>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="hub-card-header">
              <div class="hub-card-icon">{icon}</div>
              <div class="hub-card-titles">
                <div class="hub-card-subtitle">{subtitle}</div>
                <div class="hub-card-title">{title}</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if chips:
            chip_html = "".join(status_chip(c) for c in chips)
            st.markdown(f"<div class='hub-chip-row'>{chip_html}</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='hub-card-body'>{description}</div>",
            unsafe_allow_html=True,
        )

        # Buttons row
        button_cols = st.columns(2 if secondary_label else 1, gap="small")
        with button_cols[0]:
            st.markdown("<div class='hub-button hub-button-primary'>", unsafe_allow_html=True)
            if st.button(primary_label, key=f"{key}_primary"):
                primary_action()
            st.markdown("</div>", unsafe_allow_html=True)
        if secondary_label and secondary_action:
            with button_cols[1]:
                st.markdown("<div class='hub-button hub-button-secondary'>", unsafe_allow_html=True)
                if st.button(secondary_label, key=f"{key}_secondary"):
                    secondary_action()
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)


# ---------- Page-level styling ----------
st.markdown(
    f"""
    <style>
      body {{
        background: #f6f8fc;
      }}
      .block-container {{
        max-width: 1120px;
        margin: 0 auto;
        padding-top: 2.6rem;
        padding-bottom: 3.2rem;
      }}
      .concierge-shell {{
        display: flex;
        flex-direction: column;
        gap: 1.75rem;
      }}
      .hub-banner {{
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(180deg, rgba(79, 70, 229, 0.12), rgba(79, 70, 229, 0.06));
        border: 1px solid rgba(79, 70, 229, 0.22);
        border-radius: 18px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 18px 36px -28px rgba(30, 41, 59, 0.45);
      }}
      .hub-banner p {{
        margin: 0;
        font-size: 0.95rem;
        color: #23324c;
      }}
      .hub-banner strong {{
        color: #1e1b4b;
      }}
      .hub-banner-actions {{
        display: flex;
        gap: 0.6rem;
      }}
      .hub-banner-actions .stButton>button {{
        border-radius: 999px;
        padding: 0.45rem 1.1rem;
        font-weight: 600;
        border: 1px solid rgba(79, 70, 229, 0.4);
        background: #ffffff;
        color: #1e1b4b;
        box-shadow: 0 14px 28px -24px rgba(30, 41, 59, 0.6);
      }}
      .hub-banner-actions .stButton>button:hover {{
        background: rgba(255, 255, 255, 0.85);
      }}
      .hub-header {{
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
      }}
      .hub-header h1 {{
        font-family: "Plus Jakarta Sans", var(--font-base, "Inter", sans-serif);
        font-weight: 700;
        font-size: clamp(1.9rem, 4vw, 2.4rem);
        color: #1e1b4b;
        margin: 0;
      }}
      .hub-context {{
        display: inline-flex;
        align-items: center;
        gap: 0.65rem;
        background: #ffffff;
        border: 1px solid rgba(148, 163, 184, 0.35);
        border-radius: 999px;
        padding: 0.45rem 0.9rem;
        font-size: 0.9rem;
        color: #334155;
        box-shadow: 0 12px 30px -24px rgba(15, 23, 42, 0.55);
      }}
      .hub-card-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 1.25rem;
      }}
      .hub-card {{
        background: #ffffff;
        border-radius: 22px;
        border: 1px solid rgba(148, 163, 184, 0.28);
        padding: 1.35rem 1.45rem 1.5rem;
        box-shadow: 0 24px 44px -32px rgba(15, 23, 42, 0.45);
        display: flex;
        flex-direction: column;
        min-height: 260px;
        gap: 0.6rem;
      }}
      .hub-card-header {{
        display: flex;
        gap: 0.9rem;
        align-items: center;
      }}
      .hub-card-icon {{
        width: 48px;
        height: 48px;
        border-radius: 16px;
        background: linear-gradient(140deg, rgba(79, 70, 229, 0.18), rgba(37, 99, 235, 0.1));
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.45rem;
        color: #3730a3;
      }}
      .hub-card-titles {{
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
      }}
      .hub-card-subtitle {{
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        color: rgba(55, 48, 163, 0.7);
        font-size: 0.75rem;
      }}
      .hub-card-title {{
        font-weight: 700;
        font-size: 1.05rem;
        color: #1f2937;
      }}
      .hub-card-body {{
        font-size: 0.94rem;
        color: #42556b;
        line-height: 1.55;
        flex: 1;
      }}
      .hub-chip-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
      }}
      .hub-chip {{
        background: #eef2ff;
        color: #3730a3;
        border-radius: 999px;
        padding: 0.2rem 0.75rem;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
      }}
      .hub-button .stButton>button {{
        width: 100%;
        border-radius: 12px;
        padding: 0.7rem 1rem;
        font-weight: 600;
        letter-spacing: 0.01em;
        border: 1px solid transparent;
      }}
      .hub-button-primary .stButton>button {{
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        color: #ffffff;
        box-shadow: 0 18px 30px -20px rgba(79, 70, 229, 0.8);
      }}
      .hub-button-primary .stButton>button:hover {{
        background: linear-gradient(135deg, #4338ca, #4f46e5);
        border-color: rgba(79, 70, 229, 0.45);
      }}
      .hub-button-secondary .stButton>button {{
        background: rgba(79, 70, 229, 0.08);
        border-color: rgba(79, 70, 229, 0.28);
        color: #3730a3;
        box-shadow: none;
      }}
      .hub-button-secondary .stButton>button:hover {{
        background: rgba(79, 70, 229, 0.18);
      }}
      .hub-additional {{
        background: #ffffff;
        border-radius: 18px;
        border: 1px solid rgba(148, 163, 184, 0.28);
        padding: 1.2rem 1.5rem;
        box-shadow: 0 18px 34px -30px rgba(15, 23, 42, 0.42);
      }}
      .hub-additional h3 {{
        margin: 0 0 0.8rem 0;
        font-size: 1rem;
        font-weight: 700;
        color: #1f2937;
      }}
      .hub-additional .stButton>button {{
        width: 100%;
        border-radius: 999px;
        padding: 0.55rem 0.85rem;
        font-size: 0.85rem;
        font-weight: 600;
        background: #f5f7ff;
        border: 1px solid rgba(148, 163, 184, 0.45);
        color: #1f2a4c;
        box-shadow: none;
      }}
      .hub-additional .stButton>button:hover {{
        background: #eef2ff;
      }}
      @media (max-width: 640px) {{
        .hub-card-grid {{
          grid-template-columns: 1fr;
        }}
      }}
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown("<div class='concierge-shell'>", unsafe_allow_html=True)

# ---------- Banner ----------
with st.container():
    st.markdown("<div class='hub-banner'>", unsafe_allow_html=True)
    banner_cols = st.columns([3.5, 2], gap="large")
    with banner_cols[0]:
        st.markdown(
            """
            <p><strong>Log in for a better experience</strong> &mdash; continue where you left off, with your information kept secure and consistent following HIPAA guidelines.</p>
            """,
            unsafe_allow_html=True,
        )
    with banner_cols[1]:
        st.markdown("<div class='hub-banner-actions'>", unsafe_allow_html=True)
        actions = st.columns(2, gap="small")
        with actions[0]:
            if st.button("Log in", key="hub_login"):
                st.switch_page("pages/login.py")
        with actions[1]:
            if st.button("Start over", key="hub_reset"):
                reset_guided_plan()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ---------- Header ----------
st.markdown(
    f"""
    <div class="hub-header">
      <h1>Dashboard</h1>
      <span class="hub-context">For someone {person_name}</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------- Cards ----------
gcp_completed = bool(ctx.get("gcp_recommendation")) or bool(ctx.get("gcp_answers"))
gcp_recommendation = ctx.get("gcp_recommendation") or "Recommendation"
gcp_chips: list[str] = []
if gcp_completed:
    gcp_chips.append(gcp_recommendation)
    if ctx.get("gcp_cost"):
        gcp_chips.append(ctx["gcp_cost"])
else:
    gcp_chips.append("Guided plan")
gcp_chips.append("Completed" if gcp_completed else "In progress")

st.markdown("<div class='hub-card-grid'>", unsafe_allow_html=True)

render_card(
    key="gcp",
    icon="🧭",
    title="Understand the situation",
    subtitle="Guided Care Plan",
    description=f"See what we learned from your answers and refine the recommendation for {person_name}.",
    chips=gcp_chips,
    primary_label="See responses" if gcp_completed else "Start guided plan",
    primary_action=lambda: st.switch_page("pages/gcp.py"),
    secondary_label="Start over" if gcp_completed else None,
    secondary_action=reset_guided_plan if gcp_completed else None,
)

render_card(
    key="costs",
    icon="💰",
    title="Understand the costs",
    subtitle="Cost Estimator",
    description=f"Assess the total cost scenarios across options for {person_name}. The cost estimate will automatically update based on your guided plan.",
    chips=["Cost planner"],
    primary_label="Open estimator",
    primary_action=lambda: st.switch_page("pages/cost_planner.py"),
)

render_card(
    key="advisor",
    icon="🤝",
    title="Connect with an advisor to plan the care",
    subtitle="Care Team",
    description=f"Talk with a concierge advisor, share important details about {person_name}, and map next steps together.",
    chips=["Get connected"],
    primary_label="Get connected",
    primary_action=lambda: st.switch_page("pages/pfma.py"),
)

render_card(
    key="faqs",
    icon="💬",
    title="FAQs &amp; Answers",
    subtitle="AI Assistant",
    description="Receive instant, tailored guidance about benefits, housing, safety, and more.",
    chips=["AI agent"],
    primary_label="Open",
    primary_action=lambda: st.switch_page("pages/ai_advisor.py"),
)

st.markdown("</div>", unsafe_allow_html=True)


# ---------- Additional services ----------
with st.container():
    st.markdown("<div class='hub-additional'>", unsafe_allow_html=True)
    st.markdown("<h3>Additional services</h3>", unsafe_allow_html=True)
    pill_data = [
        ("🛡️ Risk Navigator", "pages/risk_navigator.py", "hub_risk_pill"),
        ("💊 Medication Check", "pages/medication_management.py", "hub_meds_pill"),
        ("📄 Save or export plans", "pages/export_results.py", "hub_export_pill"),
        ("🎓 Learning Center", "pages/trusted_partners.py", "hub_learning_pill"),
    ]
    for idx in range(0, len(pill_data), 2):
        row = pill_data[idx : idx + 2]
        cols = st.columns(len(row), gap="small")
        for col, (label, target, key) in zip(cols, row):
            with col:
                if st.button(label, key=key):
                    st.switch_page(target)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
