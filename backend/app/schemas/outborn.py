from typing import Optional

from pydantic import BaseModel

from app.schemas.common import AttachmentStat, CoverageDetail


class OutbornDeliveryUnit(BaseModel):
    case_count: int
    ssc_under_2h: int
    avg_kmc: float
    exclusive_bf: int
    coverage: CoverageDetail
    attachment: AttachmentStat


class OutbornResponse(BaseModel):
    total_cases: int
    overall_avg_kmc: float
    nvd: OutbornDeliveryUnit
    csection: OutbornDeliveryUnit
    outborn_definition_note: str
    period_start: Optional[str] = None
    period_end: Optional[str] = None
