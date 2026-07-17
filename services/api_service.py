# services/api_service.py

"""
API Service

This module is responsible for communicating with the
backend REST API.

It fetches data from the API and returns Pandas DataFrames.
"""

import time

import pandas as pd
import requests

from services.config import API_CONFIG, ENDPOINTS


# ==========================================================
# API CONFIGURATION
# ==========================================================

HEADERS = {
    "Authorization": f"Bearer {API_CONFIG['api_key']}"
}


# ==========================================================
# GENERIC FETCHER
# ==========================================================

def fetch_all(endpoint: str, limit: int = 5000) -> pd.DataFrame:
    """
    Fetch all records from a paginated API endpoint.

    Parameters
    ----------
    endpoint : str
        API endpoint name.

    limit : int, default=5000
        Number of records requested per API call.

    Returns
    -------
    pd.DataFrame
        DataFrame containing all records from the endpoint.
    """

    rows = []
    offset = 0

    while True:

        response = requests.get(
            f"{API_CONFIG['base_url']}/{endpoint}",
            params={
                "limit": limit,
                "offset": offset,
            },
            headers=HEADERS,
            timeout=API_CONFIG["timeout"],
        )

        response.raise_for_status()

        page = response.json()

        rows.extend(page["data"])

        if page["next_offset"] is None:
            break

        offset = page["next_offset"]

        time.sleep(1)

    return pd.DataFrame(rows)


# ==========================================================
# DATASET FUNCTIONS
# ==========================================================

def get_eligibility_data() -> pd.DataFrame:
    """
    Fetch Eligibility Registration dataset.
    """
    return fetch_all(ENDPOINTS["eligibility"])


def get_mother_data() -> pd.DataFrame:
    """
    Fetch Mother-Baby Registration dataset.
    """
    return fetch_all(ENDPOINTS["mother"])


def get_daily_data() -> pd.DataFrame:
    """
    Fetch Daily Care Tracking dataset.
    """
    return fetch_all(ENDPOINTS["daily"])


def get_discharge_data() -> pd.DataFrame:
    """
    Fetch Discharge dataset.
    """
    return fetch_all(ENDPOINTS["discharge"])

if __name__ == "__main__":

    datasets = {
        "Eligibility": get_eligibility_data(),
        "Mother": get_mother_data(),
        "Daily": get_daily_data(),
        "Discharge": get_discharge_data(),
    }

    for name, df in datasets.items():
        print(f"{name}: {df.shape}")


