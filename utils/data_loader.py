from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Dict

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_FILES = {
    "operations": "operations.json",
    "energy": "energy.json",
    "security": "security.json",
    "market": "market.json",
    "emerging_tech": "emerging_tech.json",
}


@lru_cache(maxsize=None)
def _load_dataset(name: str) -> dict:
    path = DATA_DIR / DATA_FILES[name]
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _frames(name: str) -> Dict[str, pd.DataFrame]:
    payload = _load_dataset(name)
    return {section: pd.DataFrame(rows) for section, rows in payload.items()}


def get_operations_data() -> Dict[str, pd.DataFrame]:
    return _frames("operations")


def get_energy_data() -> Dict[str, pd.DataFrame]:
    return _frames("energy")


def get_security_data() -> Dict[str, pd.DataFrame]:
    return _frames("security")


def get_market_data() -> Dict[str, pd.DataFrame]:
    return _frames("market")


def get_emerging_tech_data() -> Dict[str, pd.DataFrame]:
    return _frames("emerging_tech")


def get_source_catalog() -> pd.DataFrame:
    page_map = {
        "Operations": get_operations_data(),
        "Energy": get_energy_data(),
        "Security": get_security_data(),
        "Market": get_market_data(),
        "Emerging Tech": get_emerging_tech_data(),
    }
    rows = []
    for page, sections in page_map.items():
        for frame in sections.values():
            for _, row in frame.iterrows():
                rows.append({"Page": page, "Year": row["Year"], "Source URL": row["Source URL"]})
    catalog = pd.DataFrame(rows).drop_duplicates().sort_values(["Page", "Year", "Source URL"])
    return catalog.reset_index(drop=True)


def get_dashboard_stats() -> dict:
    source_count = len(get_source_catalog())
    sourced_items = sum(len(frame) for dataset in [
        get_operations_data(),
        get_energy_data(),
        get_security_data(),
        get_market_data(),
        get_emerging_tech_data(),
    ] for frame in dataset.values())
    return {
        "pages": 5,
        "sourced_items": sourced_items,
        "sources": source_count,
        "coverage": "Research centered on 2023-2025, with a few current operator pages used only where public Mexico coverage is sparse.",
    }
