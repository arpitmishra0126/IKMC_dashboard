# services/repository.py

"""
Repository layer.

This module contains all database queries.
The rest of the application should never execute SQL directly.
"""

import pandas as pd

from services.db import get_connection
from services.config import TABLES


def get_eligibility_data() -> pd.DataFrame:
    """
    Fetch Eligibility dataset from MySQL.
    """
    raise NotImplementedError(
        "Eligibility table has not been configured yet."
    )


def get_mother_data() -> pd.DataFrame:
    """
    Fetch Mother-Baby Registration dataset from MySQL.
    """
    raise NotImplementedError(
        "Mother table has not been configured yet."
    )


def get_daily_data() -> pd.DataFrame:
    """
    Fetch Daily Care Tracking dataset from MySQL.
    """
    raise NotImplementedError(
        "Daily Care table has not been configured yet."
    )


def get_discharge_data() -> pd.DataFrame:
    """
    Fetch Discharge dataset from MySQL.
    """
    raise NotImplementedError(
        "Discharge table has not been configured yet."
    )