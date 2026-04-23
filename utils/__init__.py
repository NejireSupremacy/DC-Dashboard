from __future__ import annotations

import pandas as pd
import streamlit as st


def apply_theme(page_title: str, icon: str) -> None:
    st.set_page_config(page_title=page_title, page_icon=icon, layout="wide")
    st.markdown(
        """
        <style>
            :root {
                --dc-bg-soft: #f8f4ec;
                --dc-bg-card: rgba(255, 255, 255, 0.88);
                --dc-text: #0b1f3a;
                --dc-text-muted: #2f435d;
                --dc-border: rgba(11, 31, 58, 0.14);
                --dc-accent-soft: #d9e8fb;
                --dc-accent-strong: #c4daf8;
            }
            .stApp {
                background:
                    radial-gradient(circle at top right, rgba(45, 212, 191, 0.12), transparent 26%),
                    radial-gradient(circle at bottom left, rgba(245, 158, 11, 0.12), transparent 22%),
                    linear-gradient(180deg, var(--dc-bg-soft) 0%, #ffffff 48%, #f7fbff 100%);
                color: var(--dc-text);
            }
            .block-container {
                padding-top: 2.2rem;
                padding-bottom: 2rem;
            }
            p, span, label, li, div, [data-testid="stMarkdownContainer"] {
                color: var(--dc-text);
            }
            h1, h2, h3 {
                color: var(--dc-text);
                font-family: Georgia, serif;
                letter-spacing: -0.02em;
            }
            [data-testid="stCaptionContainer"] p,
            [data-testid="stCaptionContainer"] {
                color: var(--dc-text-muted) !important;
                opacity: 1 !important;
            }
            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #f5efe4 0%, #f0f8fc 100%);
                border-right: 1px solid var(--dc-border);
            }
            section[data-testid="stSidebar"] * {
                color: var(--dc-text) !important;
            }
            div[data-testid="stMetric"] {
                background: var(--dc-bg-card);
                border: 1px solid var(--dc-border);
                border-radius: 18px;
                padding: 0.8rem;
                box-shadow: 0 12px 30px rgba(11, 31, 58, 0.06);
            }
            [data-testid="stMetricLabel"],
            [data-testid="stMetricValue"],
            [data-testid="stMetricDelta"] {
                color: var(--dc-text) !important;
            }
            div[data-testid="stDataFrame"] {
                border-radius: 18px;
                overflow: hidden;
                border: 1px solid var(--dc-border);
                background: #ffffff;
            }
            div[data-testid="stDataFrame"] [role="columnheader"] {
                background: #eaf1fa;
                color: var(--dc-text);
                font-weight: 600;
            }
            div[data-testid="stDataFrame"] [role="gridcell"] {
                color: var(--dc-text);
                background: #ffffff;
            }
            .stAlert {
                border-radius: 14px;
                border: 1px solid var(--dc-border);
            }
            div[data-testid="stDownloadButton"] button {
                background: #94a3b8 !important;
                color: #ffffff !important;
                border: 1px solid #7c8aa0 !important;
            }
            div[data-testid="stDownloadButton"] button:hover {
                background: #7c8aa0 !important;
                color: #ffffff !important;
                border: 1px solid #64748b !important;
            }
            .stCheckbox label,
            .stRadio label,
            .stSelectbox label,
            .stMultiSelect label,
            .stNumberInput label {
                color: var(--dc-text) !important;
                font-weight: 600;
            }
            div[data-baseweb="select"] > div {
                background: #ffffff !important;
                border: 1px solid var(--dc-border) !important;
            }
            div[data-baseweb="select"] input,
            div[data-baseweb="select"] span,
            div[data-baseweb="select"] svg,
            div[data-baseweb="select"] div {
                color: var(--dc-text) !important;
                fill: var(--dc-text) !important;
                -webkit-text-fill-color: var(--dc-text) !important;
            }
            div[data-baseweb="tag"] {
                background: var(--dc-accent-soft) !important;
                color: var(--dc-text) !important;
                border: 1px solid #9db8df;
                font-weight: 600;
            }
            div[data-baseweb="tag"] span,
            div[data-baseweb="tag"] svg {
                color: var(--dc-text) !important;
                fill: var(--dc-text) !important;
            }
            [role="listbox"] [role="option"] {
                background: #ffffff !important;
                color: var(--dc-text) !important;
                font-weight: 500;
            }
            [role="listbox"] [role="option"]:hover,
            [role="listbox"] [role="option"][aria-selected="false"]:hover {
                background: #eef5ff !important;
                color: var(--dc-text) !important;
            }
            [role="listbox"] [role="option"][aria-selected="true"] {
                background: var(--dc-accent-strong) !important;
                color: var(--dc-text) !important;
                font-weight: 700;
            }
            [role="listbox"] [role="option"][aria-disabled="false"]:focus,
            [role="listbox"] [role="option"][data-highlighted="true"] {
                background: #e3efff !important;
                color: var(--dc-text) !important;
            }
            div[data-baseweb="popover"],
            div[data-baseweb="menu"],
            ul[role="listbox"] {
                background: #ffffff !important;
                color: var(--dc-text) !important;
                border: 1px solid var(--dc-border) !important;
            }
            div[data-baseweb="popover"] * {
                color: #FFFFFF !important;
                fill: #FFFFFF !important;
            }
            div[data-baseweb="select"] input::placeholder {
                color: var(--dc-text-muted) !important;
                -webkit-text-fill-color: var(--dc-text-muted) !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_intro(title: str, subtitle: str) -> None:
    st.markdown(f"## {title}")
    st.caption(subtitle)


def _download_filename(title: str) -> str:
    normalized = "".join(char.lower() if char.isalnum() else "_" for char in title)
    cleaned = "_".join(part for part in normalized.split("_") if part)
    return f"{cleaned or 'table'}.csv"


def render_source_table(df: pd.DataFrame, title: str = "Sources") -> None:
    st.markdown(f"### {title}")
    st.download_button(
        label="Descargar CSV",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name=_download_filename(title),
        mime="text/csv",
        key=f"download_{title}",
    )
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_footer(note: str) -> None:
    st.info(note)
