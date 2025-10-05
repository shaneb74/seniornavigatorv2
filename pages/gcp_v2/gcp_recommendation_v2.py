from __future__ import annotations
import streamlit as st
st.set_page_config(layout="wide", page_title="GCP · Recommendation")
from ui.theme import inject_theme
inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)
st.markdown("## Your Care Plan Recommendation")
st.caption("Draft guidance based on your inputs. Refine anytime and share with an advisor.")
st.markdown("""
- **Setting:** In-home support increasing to match supervision needs  
- **Near-term actions:** Fall-prevention (OT eval), medication review, respite  
- **Next step:** Discuss budget & timeline with your advisor
""")
st.divider()
cols = st.columns(2)
with cols[0]:
    if st.button("◀ Back: Context & Preferences", use_container_width=True):
        try: st.switch_page("pages/gcp_v2/gcp_context_prefs_v2.py")
        except Exception:
            st.query_params["next"] = "pages/gcp_v2/gcp_context_prefs_v2.py"; st.rerun()
with cols[1]:
    if st.button("Go to PFMA (Share with Advisor) ▶", use_container_width=True):
        try: st.switch_page("pages/pfma.py")
        except Exception:
            st.query_params["next"] = "pages/pfma.py"; st.rerun()
