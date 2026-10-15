import json
from contextvars import ContextVar
from pathlib import Path
from datetime import datetime
from typing import Optional

import pandas as pd
import streamlit as st

from services.config import FILES, DATA_SOURCE
from services import api_service

RAW_PATH = Path("data/raw")

# A single dashboard request (e.g. GET /api/dashboard/overview) ends up
# calling load_all_data() a dozen-plus times - once per indicator function
# it touches. st.cache_data already avoids re-fetching/re-parsing on a
# cache hit, but it still returns a fresh deep copy of the whole 4-dataset
# dict on EVERY call, by design, so accidental mutation by one caller can't
# leak into another's cached result. Repeating that copy a dozen times per
# request is pure overhead - none of the existing callers mutate the
# DataFrames they get back, they only filter/read them.
#
# _REQUEST_DATA holds that one deep copy for the lifetime of a single
# request so every indicator call within it reuses the same object instead
# of paying for a fresh copy each time. It is request-scoped, not
# process-wide: ContextVar state doesn't cross asyncio Tasks (FastAPI gives
# each request its own Task), so concurrent requests never see each
# other's value, and nothing here changes what "Refresh Dashboard" does -
# clearing st.cache_data still forces the next request's first call to
# re-run load_all_data() against the configured DATA_SOURCE.
_REQUEST_DATA: ContextVar[Optional[dict]] = ContextVar("_REQUEST_DATA", default=None)

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
    # The 4 datasets are independent REST calls to the same upstream API -
    # fetching them one after another serialized their network latency
    # (and any inter-page rate-limit sleep in services/api_service.py) into
    # one long wait on every cold cache load. They don't depend on each
    # other, so fetch them concurrently and let the slowest one set the
    # total time instead of the sum of all four.
    from concurrent.futures import ThreadPoolExecutor

    fetchers = {
        "eligibility": api_service.get_eligibility_data,
        "mother": api_service.get_mother_data,
        "daily": api_service.get_daily_data,
        "discharge": api_service.get_discharge_data,
    }

    with ThreadPoolExecutor(max_workers=len(fetchers)) as pool:
        futures = {key: pool.submit(fn) for key, fn in fetchers.items()}
        results = {key: future.result() for key, future in futures.items()}

    eligibility = results["eligibility"]
    mother = results["mother"]
    daily = results["daily"]
    discharge = results["discharge"]

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
def _load_all_data_cached():
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


def load_all_data():
    """
    Load data from the configured source. Reuses the same already-loaded
    (and already copied out of st.cache_data) dict for every call made
    within the current request, instead of paying for a fresh deep copy on
    each of the many indicator calls a single request makes. See
    _REQUEST_DATA above.
    """
    data = _REQUEST_DATA.get()
    if data is None:
        data = _load_all_data_cached()
        _REQUEST_DATA.set(data)
    return data

def get_last_sync():
    data = load_all_data()
    latest_date = pd.to_datetime(
        data["eligibility"]["scr_dof"],
        errors="coerce"
    ).max()

    return latest_date


def get_last_enrollment_date():
    """Latest STUDY ENROLLMENT DATE (mother.enr_dof) present in the data -
    NOT the same as get_last_sync()'s scr_dof-based "Latest screening
    date" (a distinct, already-displayed concept, left untouched). Added
    to anchor the Overview Reporting Period filter's relative periods
    (Last 7/30 Days, Last 3 Months) to real enrollment-date data instead
    of the browser's wall-clock date."""
    data = load_all_data()
    latest_date = pd.to_datetime(
        data["mother"]["enr_dof"],
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