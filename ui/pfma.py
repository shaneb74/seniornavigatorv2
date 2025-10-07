import time
from types import SimpleNamespace
from typing import Any, Dict, Iterable, Optional, Callable

import streamlit as st


# -----------------------------
# Theme
# -----------------------------
def apply_pfma_theme(
    primary: str = "#0B5CD8",
    surface: str = "var(--surface, #f6f8fa)",
    ink: str = "var(--ink, #111418)",
    ink_muted: str = "var(--ink-muted, #6b7280)",
) -> None:
    st.markdown(
        f"""
        <style>
          :root {{
            --brand: {primary};
            --ink: {ink};
            --ink-muted: {ink_muted};
          }}
          .pfma-header h1 {{
            margin: 0 0 .25rem 0;
            font-size: clamp(1.6rem, 3.2vw, 2.2rem);
          }}
          .pfma-header p {{
            margin: 0;
            color: var(--ink-muted);
          }}
          .pfma-card {{
            background: {surface};
            border: 1px solid rgba(0,0,0,.08);
            border-radius: 16px;
            padding: clamp(1rem, 2vw, 1.5rem);
          }}
          .pfma-note {{
            font-size:.9rem;color:var(--ink-muted);
            margin:.25rem 0 0 0;
          }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# State (defaults)
# -----------------------------
DEFAULT_PFMA: Dict[str, Any] = {
    "personal_info": {},
    "household_legal": {},
    "benefits": {},
    "care_needs": {},
    "care_prefs": {},
    "cost_plan": {},
    "care_plan": {},
    "booking": {},
    # pages from older builds expect a sections bucket
    "sections": {},    # <- IMPORTANT for render_drawer/update_section
}

# Default step order used by progress widget and go_to_step
PFMA_STEPS = [
    "personal_info",
    "household_legal",
    "benefits",
    "care_needs",
    "care_prefs",
    "cost_plan",
    "care_plan",
    "booking",
]

def ensure_pfma_state() -> Dict[str, Any]:
    """Ensure st.session_state['pfma'] exists and return it."""
    if "pfma" not in st.session_state or not isinstance(st.session_state.pfma, dict):
        st.session_state.pfma = dict(DEFAULT_PFMA)
    else:
        # guarantee required keys exist
        for k, v in DEFAULT_PFMA.items():
            st.session_state.pfma.setdefault(k, v if not isinstance(v, dict) else dict(v))
    return st.session_state.pfma

def get_state() -> Dict[str, Any]:
    """Alias some pages might use."""
    return ensure_pfma_state()

# -----------------------------
# Header / Progress
# -----------------------------
def render_header(
    title: Optional[str] = None,
    subtitle: str = "",
    kicker: Optional[str] = None,
    right: Optional[str] = None,
) -> None:
    # Render even if title is None (acts as no-op chrome)
    left, right_col = st.columns([1, 1], gap="large")
    with left:
        st.markdown('<div class="pfma-header">', unsafe_allow_html=True)
        if kicker:
            st.caption(kicker)
        if title:
            st.markdown(f"<h1>{title}</h1>", unsafe_allow_html=True)
        if subtitle:
            st.markdown(f"<p>{subtitle}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right_col:
        if right:
            st.markdown(right, unsafe_allow_html=True)

def render_progress(
    current=0,
    total: Optional[int] = None,
    steps: Optional[Iterable[str]] = None,
) -> None:
    """
    Accepts either an int step index or a string step key (e.g., "booking").
    If 'steps' not provided, uses PFMA_STEPS.
    """
    labels = list(steps) if steps is not None else list(PFMA_STEPS)

    # map current -> index
    if isinstance(current, str):
        try:
            idx = labels.index(current)
        except ValueError:
            labels.append(current)
            idx = len(labels) - 1
    else:
        try:
            idx = int(current)
        except Exception:
            idx = 0

    # total defaults to number of labels
    if total is None:
        total = len(labels)

    idx_clamped = max(0, min(idx, max(0, total)))
    ratio = idx_clamped / max(1, total)
    st.progress(ratio)

    # label rail under the bar (bold up to idx)
    try:
        st.caption(" · ".join(
            [f"**{lbl}**" if i <= idx_clamped else str(lbl)
             for i, lbl in enumerate(labels[:total])]
        ))
    except Exception:
        pass

# -----------------------------
# Controls used by older pages
# -----------------------------
def segmented_control(
    label: str,
    options: Iterable[str],
    *,
    key: str,
    default: Optional[str] = None,
) -> None:
    """
    Writes the chosen value to st.session_state['pfma_segment_{key}'].
    Uses st.segmented_control when available; falls back to selectbox.
    """
    ss_key = f"pfma_segment_{key}"
    if ss_key not in st.session_state and default is not None:
        st.session_state[ss_key] = default

    try:
        # Streamlit >= 1.32
        st.segmented_control(
            label,
            options=list(options),
            key=ss_key,
            default=st.session_state.get(ss_key, default),
        )
    except Exception:
        st.selectbox(label, list(options), key=ss_key, index=(
            list(options).index(default) if (default in options) else 0
        ))

def update_section(step_key: str, payload: Dict[str, Any]) -> None:
    """
    Persist drawer payload under pfma['sections'][step_key] = { data, ts }.
    """
    pfma = ensure_pfma_state()
    pfma.setdefault("sections", {})
    pfma["sections"][step_key] = {
        "data": dict(payload or {}),
        "ts": int(time.time()),
    }

def go_to_step(step_key: str) -> None:
    """
    Stash a 'next step' hint for callers and rerun. Pages can decide how to use it.
    """
    st.session_state["pfma_next_step"] = step_key
    # Some pages rely on rerun to jump flows
    try:
        st.rerun()
    except Exception:
        pass

# -----------------------------
# Drawer pattern used by PFMA pages
# -----------------------------
def render_drawer(
    *,
    step_key: str,
    title: str,
    badge: Optional[str] = None,
    description: str = "",
    body: Callable[[Dict[str, Any]], Dict[str, Any]],
    footer_note: Optional[str] = None,
) -> SimpleNamespace:
    """
    Renders a card-like drawer:
      - Calls body(pfma_state) -> payload dict
      - Shows Save / Save & Continue buttons
      - Returns SimpleNamespace(saved: bool, payload: dict, next_step: Optional[str])
    """
    pfma = ensure_pfma_state()
    with st.container(border=True):
        # header
        header_cols = st.columns([1, 1])
        with header_cols[0]:
            st.subheader(title)
            if description:
                st.caption(description)
            if badge:
                st.markdown(f"<div class='pfma-note'>{badge}</div>", unsafe_allow_html=True)
        with header_cols[1]:
            pass  # reserved for future right-side content

        st.markdown("---")
        payload = body(pfma) or {}

        st.markdown("---")
        left, right = st.columns([1, 1])
        with left:
            if footer_note:
                st.markdown(f"<div class='pfma-note'>{footer_note}</div>", unsafe_allow_html=True)
        with right:
            col1, col2 = st.columns([1, 1])
            with col1:
                save = st.button("Save", key=f"{step_key}_save")
            with col2:
                next_clicked = st.button("Save & Continue", key=f"{step_key}_save_next")

    saved = bool(save or next_clicked)
    next_step = st.session_state.get("pfma_next_step") if next_clicked else None

    return SimpleNamespace(
        saved=saved,
        payload=payload,
        next_step=next_step,
        ok=saved,
        message=None,
    )

# -----------------------------
# Safe fallback for unknown PFMA helpers
# -----------------------------
def __getattr__(name: str):
    """
    Unknown helper -> return a callable that yields a SimpleNamespace with
    .saved/.ok defaults so old pages don't crash.
    """
    def _fn(*args, **kwargs):
        return SimpleNamespace(saved=False, ok=False, value=None, data=None, message=None)
    return _fn
