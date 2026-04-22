from __future__ import annotations

import streamlit as st

from utils import apply_theme, render_footer, render_source_table, section_intro
from utils.charts import pue_comparison_chart, stacked_energy_chart
from utils.data_loader import get_energy_data


apply_theme("Energy | Mexico DC Dashboard", "⚡")
data = get_energy_data()

pue = data["pue"]
mexico_notes = data["mexico_notes"]
breakdown = data["breakdown"]
cooling_note = data["cooling_note"]

st.title("Page 2 | Energy")
st.caption("PUE benchmarks, hyperscaler efficiency, and the energy overhead structure of a modern data center.")

section_intro(
    "PUE Benchmarks",
    "The global average remains far above the best hyperscaler fleets, which is why Mexico projects increasingly target lower-overhead designs.",
)

topline = st.columns(3)
topline[0].metric("Global average PUE", "1.56", "Uptime 2024")
topline[1].metric("Google fleet PUE", "1.09", "2024")
topline[2].metric("AWS global PUE", "1.15", "2024")

st.plotly_chart(pue_comparison_chart(pue), use_container_width=True)
render_source_table(pue, "PUE Source Table")

section_intro(
    "Mexico / LatAm Readiness",
    "Public Mexico-wide average PUE data is sparse, so this page separates confirmed public notes from representative market planning signals.",
)
render_source_table(mexico_notes, "Mexico-Specific PUE Notes")

section_intro(
    "Facility Energy Breakdown",
    "Typical facilities still spend a large share of non-IT energy on cooling and electrical overhead.",
)
st.plotly_chart(stacked_energy_chart(breakdown), use_container_width=True)
render_source_table(breakdown, "Energy Breakdown Table")
render_source_table(cooling_note, "Cooling Efficiency Note")

section_intro(
    "Interactive PUE Calculator",
    "Extra feature: estimate your own facility PUE from total facility power and IT load.",
)
calc_a, calc_b = st.columns(2)
with calc_a:
    total_power = st.number_input("Total facility power (kW)", min_value=1.0, value=1500.0, step=50.0)
with calc_b:
    it_power = st.number_input("IT equipment power (kW)", min_value=1.0, value=1000.0, step=50.0)

if it_power > 0:
    pue_value = total_power / it_power
    st.metric("Calculated PUE", f"{pue_value:.5f}")
    if pue_value <= 1.2:
        st.success("This sits in a very efficient range for a modern facility.")
    elif pue_value <= 1.5:
        st.warning("This is a respectable enterprise range, but not hyperscale-leading.")
    else:
        st.error("This indicates substantial overhead relative to the IT load.")

render_footer(
    "Energy takeaway: the Mexico market is growing into hyperscale-style efficiency expectations, but public Mexico-wide PUE disclosure still lags behind the operator narratives."
)
