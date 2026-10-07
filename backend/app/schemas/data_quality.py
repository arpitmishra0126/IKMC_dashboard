from pydantic import BaseModel


class DataQualityResponse(BaseModel):
    missing_baby_ids: int
    duplicate_babies: int
    unmatched_records: int
    missing_daily_care: int
    discharge_duplicates: int
    initiation_before_birth: int
    validation_status: str
