# Senior Navigator (CCA)
Streamlit app for Guided Care Plan (GCP), Cost Planner v2, and Plan for My Advisor (PFMA).

## Local dev
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

## Structure
- /pages … Streamlit pages (GCP, CP v2, PFMA)
- /cost_planner_v2 … shared CP state & helpers
- /contracts … data contracts (v2)

