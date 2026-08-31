from pydantic import BaseModel

from app.schemas.common import DischargeBreakdown


class DischargeSummary(BaseModel):
    discharged: int
    referred: int
    lama: int
    death: int
    still_admitted: int


class DischargeResponse(BaseModel):
    summary: DischargeSummary
    inborn: DischargeBreakdown
    outborn: DischargeBreakdown
