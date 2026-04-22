from __future__ import annotations

import streamlit as st

from utils import apply_theme, render_footer, render_source_table, section_intro
from utils.charts import emerging_timeline_chart
from utils.data_loader import get_emerging_tech_data


apply_theme("Emerging Tech | Mexico DC Dashboard", "🚀")
data = get_emerging_tech_data()

technologies = data["technologies"]
signals = data["signals"]

st.title("Page 5 | Emerging Technologies")
st.caption("Technology radar for 2024-2030 with analyst and operator signals tied to AI-era infrastructure demand.")

section_intro(
    "Technology Radar",
    "The maturity stages shown below are planning labels inferred from the cited 2024-2025 operator and analyst signals.",
)
render_source_table(technologies, "Emerging Technology Matrix")

section_intro(
    "Adoption Timeline 2024-2030",
    "Cooling, power procurement, and AI hardware are moving faster than traditional enterprise refresh cycles.",
)
st.plotly_chart(emerging_timeline_chart(technologies), use_container_width=True)

section_intro(
    "Analyst Signals",
    "These shorter signals anchor the roadmap with named analyst viewpoints from Gartner and JLL.",
)
render_source_table(signals, "Analyst Projections")

priority = st.selectbox(
    "Strategic priority for a Mexico facility in 2026",
    options=[
        "Reduce energy overhead",
        "Support AI rack density",
        "Secure long-term power capacity",
        "Expand low-latency edge coverage",
    ],
)

if priority == "Reduce energy overhead":
    st.success("Best near-term bets: direct liquid cooling retrofits, AI-aware controls, and better rack-level airflow management.")
elif priority == "Support AI rack density":
    st.success("Best near-term bets: direct liquid cooling now, immersion pilots next, and hardware/power-path co-design.")
elif priority == "Secure long-term power capacity":
    st.success("Best near-term bets: renewable PPAs now, substation planning immediately, and nuclear partnerships as a medium-term hedge.")
else:
    st.success("Best near-term bets: modular edge nodes, carrier-neutral interconnection, and selective metro expansion beyond Queretaro.")

render_footer(
    "Emerging-tech takeaway: the next competitive edge will come from power access and thermal architecture at least as much as from raw real estate."
)
