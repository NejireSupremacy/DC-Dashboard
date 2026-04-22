from __future__ import annotations

import streamlit as st

from utils import apply_theme, render_footer, render_source_table
from utils.data_loader import get_dashboard_stats, get_source_catalog


apply_theme("Mexico Data Center Dashboard", "🏢")

stats = get_dashboard_stats()
catalog = get_source_catalog()

st.title("Mexico Data Center Intelligence Dashboard")
st.caption(
    "UPY final project dashboard built with recent industry data for operations, energy, security, "
    "market intelligence, and emerging technology decisions."
)

left, right = st.columns([1.2, 1])
with left:
    st.markdown(
        """
        This dashboard turns recent industry research into five pages:

        1. **Operations**: uptime tier benchmarks and enterprise MAC processes.
        2. **Energy**: PUE benchmarks, hyperscaler efficiency, and energy mix.
        3. **Security**: TIA-942, ISO 27001, and physical-control baselines.
        4. **Market**: Mexico capacity, operators, and deployment trends.
        5. **Emerging Tech**: AI-era cooling, power, and infrastructure shifts.
        """
    )
with right:
    st.markdown("### Dashboard Coverage")
    k1, k2, k3 = st.columns(3)
    k1.metric("Pages", stats["pages"])
    k2.metric("Sourced items", stats["sourced_items"])
    k3.metric("Unique source links", stats["sources"])
    st.caption(stats["coverage"])

st.markdown("### How To Use It")
info_a, info_b, info_c = st.columns(3)
info_a.markdown("Use the sidebar page menu to move across the five required sections.")
info_b.markdown("Every benchmark table includes the metric year and the source URL used for the research.")
info_c.markdown("The landing page includes a source explorer as the dashboard's extra feature.")

st.markdown("### Source Explorer")
page_filter = st.multiselect(
    "Filter the research catalog by page",
    options=sorted(catalog["Page"].unique()),
    default=sorted(catalog["Page"].unique()),
)
filtered = catalog[catalog["Page"].isin(page_filter)].reset_index(drop=True)
render_source_table(filtered, "Research Catalog")

render_footer(
    "Method note: the dashboard prioritizes 2023-2025 data. Where Mexico-specific public benchmarks were sparse, "
    "the app calls that out instead of inventing a market average."
)
