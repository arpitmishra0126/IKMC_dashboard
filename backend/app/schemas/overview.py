from typing import Optional

from pydantic import BaseModel

from app.schemas.common import AttachmentStatSplit, DeliverySplitFloat, DeliverySplitInt


class TotalCasesSummary(BaseModel):
    """Period-aware Total Cases summary (senior feedback), combined across
    Inborn + Outborn, NVD vs. C-Section - backed by the isolated
    services.overview_period_metrics.get_overview_total_cases(), NOT by
    the existing Cohort Summary indicator functions (see
    docs/MIGRATION_DECISIONS.md and that module's docstring for why)."""

    total_cases: int
    delivery: DeliverySplitInt
    ssc_under_2h: DeliverySplitInt
    avg_kmc: DeliverySplitFloat
    exclusive_bf: DeliverySplitInt
    attachment: AttachmentStatSplit


class OverviewResponse(BaseModel):
    pre_screened: int
    screened: int
    eligible_for_enrollment: int
    discharged: int
    referred: int
    lama: int
    death: int
    period_start: Optional[str] = None
    period_end: Optional[str] = None
    total_cases_summary: TotalCasesSummary
