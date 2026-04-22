from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


PALETTE = {
    "navy": "#0B1F3A",
    "teal": "#0E7490",
    "mint": "#2DD4BF",
    "amber": "#F59E0B",
    "coral": "#FB7185",
    "slate": "#475569",
    "sand": "#F8F4EC",
}


def base_layout(fig: go.Figure, title: str | None = None) -> go.Figure:
    fig.update_layout(
        title=title,
        title_font={"color": PALETTE["navy"], "size": 22},
        paper_bgcolor="rgba(255,255,255,0.65)",
        plot_bgcolor="rgba(255,255,255,0.85)",
        font={"family": "Georgia, serif", "color": PALETTE["navy"]},
        margin={"l": 24, "r": 24, "t": 60, "b": 24},
        bargap=0.25,
        legend={"orientation": "h", "y": 1.08, "x": 0, "font": {"color": PALETTE["navy"]}},
    )
    fig.update_xaxes(showgrid=False, zeroline=False, tickfont={"color": PALETTE["navy"]}, title_font={"color": PALETTE["navy"]})
    fig.update_yaxes(
        gridcolor="rgba(71,85,105,0.22)",
        zeroline=False,
        tickfont={"color": PALETTE["navy"]},
        title_font={"color": PALETTE["navy"]},
    )
    return fig


def tier_availability_chart(df: pd.DataFrame) -> go.Figure:
    colors = [PALETTE["coral"], PALETTE["amber"], PALETTE["teal"], PALETTE["navy"]]
    chart = go.Figure(
        go.Bar(
            x=df["Annual downtime (minutes)"],
            y=df["Tier"],
            orientation="h",
            text=df["Availability benchmark"],
            marker={"color": [colors[i % len(colors)] for i in range(len(df))]},
            textposition="outside",
            textfont={"color": PALETTE["navy"], "size": 13},
            cliponaxis=False,
        )
    )

    chart.update_xaxes(title="Downtime minutes per year")
    chart.update_yaxes(categoryorder="array", categoryarray=df["Tier"].tolist(), automargin=True)

    return base_layout(chart, "Legacy Uptime Targets by Tier")


def pue_comparison_chart(df: pd.DataFrame) -> go.Figure:
    colors = [PALETTE["slate"], PALETTE["teal"], PALETTE["navy"], PALETTE["mint"], PALETTE["amber"], PALETTE["coral"]]
    chart = go.Figure(
        go.Bar(
            x=df["Scope"],
            y=df["PUE"],
            text=df["PUE"],
            texttemplate="%{text:.2f}",
            textposition="outside",
            marker={"color": [colors[i % len(colors)] for i in range(len(df))]},
            textfont={"color": PALETTE["navy"], "size": 13},
            cliponaxis=False,
        )
    )
    chart.update_xaxes(categoryorder="array", categoryarray=df["Scope"].tolist(), automargin=True)
    chart.update_yaxes(title="Lower is better", range=[0.0, max(df["PUE"]) + 0.15])
    return base_layout(chart, "PUE Benchmarks: Industry vs. Hyperscalers")


def stacked_energy_chart(df: pd.DataFrame) -> go.Figure:
    chart = go.Figure(
        data=[
            go.Bar(
                x=["Typical benchmark mix"],
                y=[row["Share (%)"]],
                name=row["Category"],
            )
            for _, row in df.iterrows()
        ]
    )
    chart.update_layout(barmode="stack")
    chart.update_yaxes(title="Share of facility energy (%)")
    return base_layout(chart, "Typical Data Center Energy Breakdown")


def market_capacity_chart(df: pd.DataFrame) -> go.Figure:
    colors = [PALETTE["navy"], PALETTE["teal"], PALETTE["amber"]]
    chart = go.Figure(
        go.Bar(
            x=df["Market"],
            y=df["Capacity (MW)"],
            text=df["Capacity (MW)"],
            texttemplate="%{text:.1f}",
            textposition="outside",
            marker={"color": [colors[i % len(colors)] for i in range(len(df))]},
            textfont={"color": PALETTE["navy"], "size": 13},
            cliponaxis=False,
        )
    )
    chart.update_xaxes(categoryorder="array", categoryarray=df["Market"].tolist(), automargin=True)
    chart.update_yaxes(title="MW")
    return base_layout(chart, "Mexico Hotspots by Installed Capacity")


def deployment_model_chart(df: pd.DataFrame) -> go.Figure:
    numeric = []
    for _, row in df.iterrows():
        label = row["Share / trend"]
        value = None
        if "%" in label and "CAGR" not in label:
            value = float(label.replace("%", "").split()[0])
        elif "20.05%" in label:
            value = 20.05
        else:
            value = 10.0
        numeric.append(value)
    chart_df = df.copy()
    chart_df["Reference value"] = numeric
    colors = [PALETTE["teal"], PALETTE["navy"], PALETTE["amber"]]
    chart = go.Figure(
        go.Bar(
            x=chart_df["Model"],
            y=chart_df["Reference value"],
            text=chart_df["Share / trend"],
            textposition="outside",
            marker={"color": [colors[i % len(colors)] for i in range(len(chart_df))]},
            textfont={"color": PALETTE["navy"], "size": 13},
            cliponaxis=False,
        )
    )
    chart.update_xaxes(categoryorder="array", categoryarray=chart_df["Model"].tolist(), automargin=True)
    chart.update_yaxes(title="Share or directional trend")
    return base_layout(chart, "Mexico Deployment Model Signals")


def emerging_timeline_chart(df: pd.DataFrame) -> go.Figure:
    start_year = []
    end_year = []
    for _, row in df.iterrows():
        start, end = row["Timeline"].split("-")
        start_year.append(pd.Timestamp(f"{int(start)}-01-01"))
        end_year.append(pd.Timestamp(f"{int(end)}-12-31"))
    chart_df = df.copy()
    chart_df["Start"] = start_year
    chart_df["Finish"] = end_year
    chart = px.timeline(
        chart_df,
        x_start="Start",
        x_end="Finish",
        y="Technology",
        color="Maturity stage",
        color_discrete_sequence=[PALETTE["amber"], PALETTE["teal"], PALETTE["navy"], PALETTE["mint"]],
        hover_data=["Why it matters"],
    )
    chart.update_yaxes(autorange="reversed")
    chart.update_xaxes(dtick="M12", tickformat="%Y")
    chart = base_layout(chart, "Emerging Technology Adoption Window")
    chart.update_layout(
        legend={"orientation": "h", "x": 0, "y": -0.28, "xanchor": "left", "yanchor": "top"},
        margin={"l": 24, "r": 24, "t": 60, "b": 110},
    )
    return chart
