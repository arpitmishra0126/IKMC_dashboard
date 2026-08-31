"""
Sync/refresh metadata assembly.

Deliberately keeps two distinct concepts separate, per
docs/MIGRATION_DECISIONS.md #2 ("Sync metadata conflates two different
concepts") - this module does not repeat that mislabeling:

- `latest_screening_date`: services.loader.get_last_sync() - the latest
  `scr_dof` value present in the loaded eligibility data. This is a data
  content fact, not a fetch timestamp.
- `api_fetch_timestamp`: only available when services.config.DATA_SOURCE is
  "api" - services.loader.load_api_data() stashes `datetime.now()` (captured
  at the moment the upstream API calls completed) into
  `data["_last_sync"]`. When DATA_SOURCE is "json" (e.g. local/offline
  development), no such value exists, and this module returns None rather
  than fabricating one.

get_last_sync() itself is not modified or reimplemented.
"""
from __future__ import annotations

from typing import Any

import pandas as pd

from app.services.indicators_bridge import clear_cache, loader


def get_sync_metadata() -> dict[str, Any]:
    latest_screening_date = loader.get_last_sync()

    data = loader.load_all_data()
    api_fetch_timestamp = data.get("_last_sync")  # only present for DATA_SOURCE == "api"

    return {
        "latest_screening_date": (
            latest_screening_date.isoformat()
            if pd.notna(latest_screening_date)
            else None
        ),
        "api_fetch_timestamp": (
            api_fetch_timestamp.isoformat() if api_fetch_timestamp is not None else None
        ),
        "data_source": loader.DATA_SOURCE,
    }


def refresh() -> dict[str, Any]:
    clear_cache()
    return {
        "status": "ok",
        "detail": (
            "Cache cleared. The next request will re-run load_all_data() "
            "against the configured DATA_SOURCE."
        ),
    }
