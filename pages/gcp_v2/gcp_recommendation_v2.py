from __future__ import annotations
import streamlit as st
try:
    from ui.theme import inject_theme
except Exception:
    def inject_theme(): st.markdown("<style>.block-container{max-width:1160px;padding-top:8px}</style>", unsafe_allow_html=True)

def gcp():
    if "gcp" not in st.session_state or not isinstance(st.session_state.gcp, dict):
        st.session_state.gcp = {}
    return st.session_state.gcp

def setv(k, v):
    g = gcp(); g[k] = v; return v

def goto(path: str):
    try:
        st.switch_page(path)
    except Exception:
        st.query_params["next"] = path
        st.rerun()

st.set_page_config(layout="wide", page_title="GCP · Recommendation")
inject_theme()

st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Recommendation")

g = gcp()

payment_context = "medicaid" if g.get("medicaid_status") == "yes" else "private"
setv("payment_context", payment_context)
medicaid_unsure_flag = (g.get("medicaid_status") == "unsure")
setv("medicaid_unsure_flag", medicaid_unsure_flag)

safety_flags = {
    "falls": g.get("falls") in ("one","recurrent"),
    "wandering": ("wandering" in (g.get("behavior_risks") or [])),
    "med_mgmt": g.get("med_mgmt") in ("several","complex"),
}
setv("safety_flags", safety_flags)

recommended_setting = "In-home with supports"
if g.get("home_safety") == "unsafe" or g.get("supervision") in ("rarely","never"):
    recommended_setting = "Assisted Living"
if g.get("cognition") in ("moderate","severe") and "wandering" in (g.get("behavior_risks") or []):
    recommended_setting = "Memory Care"
setv("recommended_setting", recommended_setting)

st.success(f"Recommended setting: **{recommended_setting}**")

if payment_context == "medicaid":
    st.info("Your answers indicate Medicaid. We’ll guide you to the Medicaid path now.")
    if st.button("Open Medicaid off-ramp ▶", use_container_width=True):
        goto("pages/gcp_v2/gcp_medicaid_offramp_v2.py")
else:
    if medicaid_unsure_flag:
        st.warning("Not sure about Medicaid? We’ll double-check coverage during planning.")

st.markdown("### Why this?")
trace = []
trace.append("payment_context = " + str(payment_context))
trace.append("funding_confidence = " + str(g.get("funding_confidence")))
trace.append("cognition = " + str(g.get("cognition")) + ", behavior_risks = " + str(g.get("behavior_risks")))
trace.append("home_safety = " + str(g.get("home_safety")) + ", supervision = " + str(g.get("supervision")))
trace.append("safety_flags = " + str(safety_flags))
st.code("\n".join(trace), language="text")

st.divider()
c1,c2 = st.columns(2)
with c1:
    if st.button("◀ Back: Context & Preferences", use_container_width=True):
        goto("pages/gcp_v2/gcp_context_prefs_v2.py")
with c2:
    if st.button("Go to PFMA (Share with Advisor) ▶", use_container_width=True):
        goto("pages/pfma.py")
