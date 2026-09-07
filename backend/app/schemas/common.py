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


class AttachmentStat(BaseModel):
    """Attachment age in MINUTES (computed directly from the raw datetime
    difference before rounding - not derived from an already-rounded hours
    value): mean (`minutes`), `min_minutes`, `max_minutes`, plus the number
    of cases with a recorded attachment timestamp (enr_bf_bentfed_hw_dt
    non-null - the existing definition, unchanged)."""

    minutes: float
    min_minutes: float
    max_minutes: float
    case_count: int


class AttachmentStatSplit(BaseModel):
    nvd: AttachmentStat
    csection: AttachmentStat
