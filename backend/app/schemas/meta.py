from typing import Optional

from pydantic import BaseModel, Field


class SyncMetadataResponse(BaseModel):
    latest_screening_date: Optional[str] = Field(
        None,
        description=(
            "max(eligibility['scr_dof']) from services.loader.get_last_sync(). "
            "A data-content fact (latest screening date present in the "
            "loaded dataset), NOT a record of when data was fetched."
        ),
    )
    api_fetch_timestamp: Optional[str] = Field(
        None,
        description=(
            "Timestamp captured by services.loader.load_api_data() when "
            "DATA_SOURCE == 'api'. Null when the configured data source is "
            "'json' or when no fetch has occurred yet in this process - "
            "never fabricated."
        ),
    )
    data_source: str = Field(
        description="The DATA_SOURCE currently configured in services/loader.py."
    )


class RefreshResponse(BaseModel):
    status: str
    detail: str
