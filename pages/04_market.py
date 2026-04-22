from __future__ import annotations

import streamlit as st

from utils import apply_theme, render_footer, render_source_table, section_intro
from utils.charts import deployment_model_chart, market_capacity_chart
from utils.data_loader import get_market_data


apply_theme("Market | Mexico DC Dashboard", "🇲🇽")
data = get_market_data()

overview = data["overview"]
regions = data["regions"]
operators = data["operators"]
models = data["models"]

st.title("Page 4 | Mexico Market Intelligence")
st.caption("Installed capacity, regional concentration, operator landscape, and deployment model direction.")

section_intro(
    "National Market Snapshot",
    "Mexico is one of Latin America's fastest-growing data center markets, with Queretaro acting as the primary hyperscale magnet.",
)

metrics = st.columns(4)
metrics[0].metric("2024 total pipeline", "587.2 MW", "111.5 MW live")
metrics[1].metric("2023 market size", "USD 804M", "Base year")
metrics[2].metric("2029 forecast", "USD 1.319B", "Projected")
metrics[3].metric("Forecast CAGR", "8.60%", "2023-2029")
render_source_table(overview, "Mexico Market Overview")

section_intro(
    "Key Regional Markets",
    "Queretaro dominates capacity, while CDMX and Monterrey remain strategic enterprise and interconnection nodes.",
)
st.plotly_chart(market_capacity_chart(regions), use_container_width=True)
render_source_table(regions, "Regional Capacity Benchmarks")

section_intro(
    "Main Operators In Mexico",
    "These are the operator signals requested in the guide, with current footprint notes and expansion cues.",
)
render_source_table(operators, "Operator Landscape")

section_intro(
    "Deployment Models",
    "Colocation still leads current revenue, but edge growth and hyperscale self-build are reshaping where new MW land.",
)
st.plotly_chart(deployment_model_chart(models), use_container_width=True)
render_source_table(models, "Deployment Model Trends")

render_footer(
    "Market takeaway: Mexico is no longer just a regional enterprise market. It is becoming a hyperscale and edge corridor, with Queretaro carrying the largest power story and Monterrey gaining from nearshoring."
)
