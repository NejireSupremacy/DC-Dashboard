from __future__ import annotations

import pandas as pd
import streamlit as st

from utils import apply_theme, render_footer, render_source_table, section_intro
from utils.charts import tier_availability_chart, uptime_sla_by_site_gauge
from utils.data_loader import get_operations_data


apply_theme("Operations | Mexico DC Dashboard", "📈")
data = get_operations_data()

tiers = data["tiers"]
notes = data["notes"]
mac = data["mac"]

st.title("Page 1 | Operations")
st.caption("SLA benchmarks by Uptime tier and common enterprise MAC workflows.")

section_intro(
    "Tier Reliability Benchmarks",
    "The percentages below are the widely used legacy availability targets mapped to Uptime tiers in recent industry explainers.",
)

metric_cols = st.columns(4)
for col, row in zip(metric_cols, tiers.to_dict("records")):
    with col:
        st.metric(
            row["Tier"],
            row["Availability benchmark"],
            f"{row['Annual downtime (minutes)']:.1f} min/yr",
        )

st.plotly_chart(tier_availability_chart(tiers), use_container_width=True)
render_source_table(tiers, "Tier Benchmark Table")

section_intro(
    "Uptime SLA by Site",
    "Per-site SLA view for a quick operational health snapshot. Values are simulated where site-level SLA data is not publicly available.",
)
uptime_by_site = pd.DataFrame(
    [
        {"Site": "Queretaro Campus", "Uptime SLA (%)": 99.982},
        {"Site": "Monterrey Hub", "Uptime SLA (%)": 99.964},
        {"Site": "CDMX Edge", "Uptime SLA (%)": 99.951},
    ]
)
st.plotly_chart(uptime_sla_by_site_gauge(uptime_by_site), use_container_width=True)

section_intro(
    "Incident History",
    "Recent outage log used to practice operational review workflows. Values are simulated for coursework and not sourced from operator disclosures.",
)
incident_history = pd.DataFrame(
    [
        {
            "Incident ID": "INC-2026-0418",
            "Outage Date": "2026-04-18",
            "Site": "Queretaro Campus",
            "Service Impact": "Cooling loop B alert",
            "Severity": "High",
            "Resolution Time (minutes)": 84,
        },
        {
            "Incident ID": "INC-2026-0409",
            "Outage Date": "2026-04-09",
            "Site": "Monterrey Hub",
            "Service Impact": "Top-of-rack switch failure",
            "Severity": "Medium",
            "Resolution Time (minutes)": 57,
        },
        {
            "Incident ID": "INC-2026-0327",
            "Outage Date": "2026-03-27",
            "Site": "CDMX Edge",
            "Service Impact": "UPS battery string replacement",
            "Severity": "Medium",
            "Resolution Time (minutes)": 41,
        },
        {
            "Incident ID": "INC-2026-0315",
            "Outage Date": "2026-03-15",
            "Site": "Queretaro Campus",
            "Service Impact": "Planned maintenance overrun",
            "Severity": "Low",
            "Resolution Time (minutes)": 33,
        },
        {
            "Incident ID": "INC-2026-0304",
            "Outage Date": "2026-03-04",
            "Site": "Monterrey Hub",
            "Service Impact": "Generator synchronization issue",
            "Severity": "High",
            "Resolution Time (minutes)": 96,
        },
    ]
)
incident_history["Outage Date"] = pd.to_datetime(incident_history["Outage Date"])
incident_history = incident_history.sort_values("Outage Date", ascending=False)

incident_cols = st.columns(3)
with incident_cols[0]:
    st.metric("Incidents (90 days)", len(incident_history))
with incident_cols[1]:
    st.metric("Avg Resolution", f"{incident_history['Resolution Time (minutes)'].mean():.1f} min")
with incident_cols[2]:
    st.metric("Max Resolution", f"{incident_history['Resolution Time (minutes)'].max():.0f} min")

st.dataframe(
    incident_history,
    use_container_width=True,
    hide_index=True,
)

section_intro(
    "Important Context",
    "Current Uptime documentation is topology-focused, so the dashboard keeps a note beside the legacy uptime target table.",
)
render_source_table(notes, "Tier Interpretation Note")

section_intro(
    "MAC Process Categories",
    "Moves, adds, and changes are the recurring workflow categories used to keep live facilities aligned with business demand.",
)
render_source_table(mac, "Enterprise MAC Categories")

render_footer(
    "Operations takeaway: Tier III remains the practical enterprise sweet spot because it enables maintenance without planned downtime, "
    "while Tier IV is reserved for the most failure-intolerant workloads."
)
