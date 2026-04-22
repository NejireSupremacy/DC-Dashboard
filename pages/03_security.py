from __future__ import annotations

import streamlit as st

from utils import apply_theme, render_footer, render_source_table, section_intro
from utils.data_loader import get_security_data


apply_theme("Security | Mexico DC Dashboard", "🛡️")
data = get_security_data()

tia = data["tia942"]
iso = data["iso27001"]
controls = data["controls"]

st.title("Page 3 | Security & Compliance")
st.caption("TIA-942 security posture, ISO 27001 control domains, and common physical controls for resilient facilities.")

section_intro(
    "TIA-942 Physical Security Summary",
    "TIA-942 ratings escalate from limited protection in Rated-1 to full physical-event protection in Rated-4.",
)
render_source_table(tia, "TIA-942 Security Summary")

section_intro(
    "ISO 27001 Domains Relevant To Data Centers",
    "The 2022 structure groups Annex A controls into four themes, which map cleanly to data center governance and operations.",
)
render_source_table(iso, "ISO 27001 Control Domains")

section_intro(
    "Common Tier III / IV Physical Controls",
    "These controls show up repeatedly across colocation and mission-critical site security programs.",
)
render_source_table(controls, "Physical Security Control Set")

st.markdown("### Quick Readiness Checklist")
for item in [
    "Layered perimeter plus monitored gates",
    "24x7 staffing and visitor escort rules",
    "Multi-factor entry with anti-tailgating controls",
    "Video coverage of perimeter, entries, and halls",
    "Cage or cabinet segmentation for customer separation",
]:
    st.checkbox(item, value=True)

render_footer(
    "Security takeaway: physical compliance is not just about perimeter hardening. The strongest facilities blend topology resilience, auditable access, staffing, and cabinet-level segmentation."
)
