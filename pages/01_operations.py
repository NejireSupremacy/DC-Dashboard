from __future__ import annotations

import streamlit as st

from utils import apply_theme, render_footer, render_source_table, section_intro
from utils.charts import tier_availability_chart
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
