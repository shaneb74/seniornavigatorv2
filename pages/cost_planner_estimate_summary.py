"""Summary, runway, and exports for the Cost Planner."""
from __future__ import annotations
from ui.theme import inject_theme

import csv
import io
import json

import streamlit as st

from cost_planner_shared import ensure_core_state, format_currency, recompute_costs

inject_theme()
st.markdown('<div class="sn-scope dashboard">', unsafe_allow_html=True)

ensure_core_state()
cp = st.session_state["cost_planner"]
aud_snapshot = st.session_state.get("audiencing_snapshot") or st.session_state.get("audiencing")
gcp_state = st.session_state.get("gcp", {})

recompute_costs()

st.title("Cost Planner summary & exports")
st.caption("Review totals, runway, and export everything for advisors or CRM.")

summary_cols = st.columns(4)
summary_cols[0].metric("Monthly costs", format_currency(cp["monthly_total"]))
summary_cols[1].metric("Offsets", format_currency(cp["subtotals"]["offsets"]))
summary_cols[2].metric("Net out-of-pocket", format_currency(cp["net_out_of_pocket"]))
if cp.get("runway_months") is not None:
    summary_cols[3].metric("Runway", f"{cp['runway_months']:.1f} months")
else:
    summary_cols[3].metric("Runway", "-")

st.subheader("Category breakdown")
breakdown_rows = []
for key, label in [
    ("housing", "Housing"),
    ("care", "Care"),
    ("medical", "Medical"),
    ("insurance", "Insurance"),
    ("debts", "Debts"),
    ("other", "Other"),
    ("offsets", "Offsets"),
]:
    breakdown_rows.append({"Category": label, "Monthly": cp["subtotals"][key]})
st.dataframe(breakdown_rows, use_container_width=True, hide_index=True)

if cp.get("custom_line_items"):
    st.subheader("Custom line items")
    for item in cp["custom_line_items"]:
        st.write(f"* {item['label']}: {format_currency(item['amount'])}")

if cp.get("notes"):
    st.info(cp["notes"], icon="📝")

snapshot = {
    "audiencing": aud_snapshot,
    "gcp": gcp_state,
    "cost_planner": cp["snapshot_for_crm"],
}

st.subheader("Exports")
json_bytes = json.dumps(snapshot, indent=2).encode("utf-8")

csv_buffer = io.StringIO()
csv_writer = csv.writer(csv_buffer)
csv_writer.writerow(["category", "amount"])
for row in breakdown_rows:
    csv_writer.writerow([row["Category"], row["Monthly"]])
csv_writer.writerow(["Net out-of-pocket", cp["net_out_of_pocket"]])

pdf_lines = [
    "Senior Navigator Cost Planner Summary",
    f"Monthly costs: {cp['monthly_total']:.2f}",
    f"Offsets: {cp['subtotals']['offsets']:.2f}",
    f"Net out-of-pocket: {cp['net_out_of_pocket']:.2f}",
]
if cp.get("runway_months") is not None:
    pdf_lines.append(f"Runway: {cp['runway_months']:.1f} months")
pdf_lines.append("Decision log:")
for entry in cp["decision_log"]:
    pdf_lines.append(f" - {entry}")
pdf_lines.append("Expert flags:")
for flag in cp["expert_flags"]:
    pdf_lines.append(f" - {flag}")
pdf_bytes = "\n".join(pdf_lines).encode("utf-8")

col_pdf, col_csv, col_json = st.columns(3)
col_pdf.download_button("Download PDF", data=pdf_bytes, file_name="cost_planner_summary.pdf", mime="application/pdf")
col_csv.download_button("Download CSV", data=csv_buffer.getvalue(), file_name="cost_planner_summary.csv", mime="text/csv")
col_json.download_button("Download JSON", data=json_bytes, file_name="cost_planner_summary.json", mime="application/json")

with st.expander("Debug snapshot"):
    st.json(snapshot)

st.markdown("---")

col_hub, col_back, col_next = st.columns([1, 1, 1])
with col_hub:
    if st.button("Return to Hub", type="secondary"):
        st.switch_page("pages/hub.py")
with col_back:
    if st.button("Back: Expert Review"):
        st.switch_page("pages/cost_planner_evaluation.py")
with col_next:
    if st.button("Next: Confirm & Share", type="primary"):
        st.switch_page("pages/cost_plan_confirm.py")

st.markdown('</div>', unsafe_allow_html=True)
