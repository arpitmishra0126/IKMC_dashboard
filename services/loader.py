import json
import pandas as pd
import streamlit as st
from pathlib import Path

from services.config import FILES

RAW_PATH = Path("data/raw")


@st.cache_data
def load_json(filename):
    """
    Load a JSON file from data/raw and return raw data.
    """
    filepath = RAW_PATH / filename

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


@st.cache_data
def load_all_data():
    """
    Load all source datasets and return them as DataFrames.
    """

    data = {}

    for key, filename in FILES.items():
        df = pd.DataFrame(load_json(filename))
        if "deleted" in df.columns:
            df = df[df["deleted"].fillna(0) != 1]
            data[key] = df
    return data


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

    for filename in FILES.values():
        inspect_json(filename)