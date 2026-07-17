import json
from pathlib import Path

import pandas as pd
import streamlit as st

from services.config import FILES, DATA_SOURCE

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
# MYSQL LOADER (Placeholder)
# ==========================================================

@st.cache_data
def load_mysql_data():
    """
    Load all datasets from MySQL.

    This will be implemented after database
    connection details are available.
    """

    raise NotImplementedError(
        "MySQL loader has not been implemented yet."
    )


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

    elif DATA_SOURCE.lower() == "mysql":
        return load_mysql_data()

    else:
        raise ValueError(
            f"Unsupported DATA_SOURCE: {DATA_SOURCE}"
        )


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

    if DATA_SOURCE == "json":

        for filename in FILES.values():
            inspect_json(filename)

    else:

        datasets = load_all_data()

        for name, df in datasets.items():
            print(f"{name}: {len(df)} rows")