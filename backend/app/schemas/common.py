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
    # The exact denominator get_*_coverage() divides achieved_count by
    # (get_{prefix}_count(), always unfiltered - coverage is never
    # period-filtered). Exposed separately from `delivery`/`case_count`
    # because those ARE period-filtered elsewhere on Inborn/Outborn, so
    # reusing them here would silently produce a percentage/fraction
    # mismatch when a Reporting Period is applied.
    total_count: int


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
