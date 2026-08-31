"""Small reusable response building blocks shared across dashboard schemas."""
from pydantic import BaseModel


class DeliverySplitInt(BaseModel):
    nvd: int
    csection: int


class DeliverySplitFloat(BaseModel):
    nvd: float
    csection: float


class CoverageDetail(BaseModel):
    percentage: float
    achieved_count: int


class CoverageSplit(BaseModel):
    nvd: CoverageDetail
    csection: CoverageDetail


class DischargeOutcome(BaseModel):
    discharged: int
    referred: int
    lama: int
    death: int


class DischargeBreakdown(BaseModel):
    nvd: DischargeOutcome
    csection: DischargeOutcome
