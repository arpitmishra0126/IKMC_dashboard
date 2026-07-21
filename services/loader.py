import json
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st

from services.config import FILES, DATA_SOURCE
from services import api_service

RAW_PATH = Path("data/raw")

# ==========================================================
# JSON LOADER
# ==========================================================

@st.cache_data
def load_json(filename):
    """Load a JSON file from data/raw and return raw data."""
    filepath = RAW_PATH / filename

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


@st.cache_data
def load_json_data():
    """
    Load all datasets from local JSON files.
    """

    data = {}

    for key, filename in FILES.items():

        df = pd.DataFrame(load_json(filename))

        if "deleted" in df.columns:
            df = df[df["deleted"].fillna(0) != 1]

        data[key] = df

    return data

# ==========================================================
# API LOADER 
# ==========================================================

@st.cache_data
def load_api_data():

    print("Loading eligibility...")
    eligibility = api_service.get_eligibility_data()
    print("✓ eligibility loaded")

    print("Loading mother...")
    mother = api_service.get_mother_data()
    print("✓ mother loaded")

    print("Loading daily...")
    daily = api_service.get_daily_data()
    print("✓ daily loaded")

    print("Loading discharge...")
    discharge = api_service.get_discharge_data()
    print("✓ discharge loaded")

    sync_time = datetime.now()

    return {
        "eligibility": eligibility,
        "mother": mother,
        "daily": daily,
        "discharge": discharge,
        "_last_sync": sync_time,
    }
# ==========================================================
# MAIN LOADER
# ==========================================================

@st.cache_data
def load_all_data():
    """
    Load data from the configured source.
    """

    if DATA_SOURCE.lower() == "json":
        return load_json_data()

    elif DATA_SOURCE.lower() == "api":
        return load_api_data()

    else:
        raise ValueError(
            f"Unsupported DATA_SOURCE: {DATA_SOURCE}"
        )

def get_last_sync():
    data = load_all_data()
    latest_date = pd.to_datetime(
        data["eligibility"]["scr_dof"],
        errors="coerce"
    ).max()

    return latest_date

# ==========================================================
# DEBUG
# ==========================================================

def inspect_json(filename):
    """
    Helper function for development and debugging.
    """
    data = load_json(filename)

    print(f"\n{'=' * 60}")
    print(f"FILE: {filename}")
    print(f"TYPE: {type(data)}")

    if isinstance(data, list):
        print(f"RECORDS: {len(data)}")

        if len(data) > 0:
            print("\nFIRST RECORD KEYS:")
            print(list(data[0].keys()))

    elif isinstance(data, dict):
        print(f"TOTAL KEYS: {len(data.keys())}")

        print("\nKEYS:")
        print(list(data.keys())[:50])

    return data


if __name__ == "__main__":

    datasets = load_all_data()

    for name, df in datasets.items():
        print(f"{name}: {len(df)} rows")