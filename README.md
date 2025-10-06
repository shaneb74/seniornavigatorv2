# Senior Navigator (CCA)
Streamlit app for Guided Care Plan (GCP), Cost Planner v2, and Plan for My Advisor (PFMA).

## Local dev
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

## Deployment notes
Hosted environments such as Streamlit Community Cloud or container-based CI
systems must run the app in headless mode.  Otherwise the CLI can hang while
waiting for the optional onboarding prompt that asks for an email address,
which surfaces as a failed health check even though the app code is fine.  The
`.streamlit/config.toml` committed to this repo enforces headless mode and
disables the analytics prompt so deployments complete successfully without any
changes to `requirements.txt`.

## Structure
- /pages … Streamlit pages (GCP, CP v2, PFMA)
- /cost_planner_v2 … shared CP state & helpers
- /contracts … data contracts (v2)

