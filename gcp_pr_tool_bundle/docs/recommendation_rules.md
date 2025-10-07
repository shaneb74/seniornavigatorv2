# GCP — Data-driven Engine & Deterministic Blurbs
Date: 2025-10-06

This doc summarizes how engine.py consumes `questions.csv` and `scoring_model.json` and emits stable outputs
while selecting empathetic blurbs from `context_blurbs.json`. DecisionTrace order is stable:
1) primary recommendation rule (gcp.rec.*)
2) medicaid_path (if applicable)
3) financial_confidence nudge (if private & low confidence)
