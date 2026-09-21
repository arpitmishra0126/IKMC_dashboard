from typing import Optional

from pydantic import BaseModel


class AttachmentCaseRecord(BaseModel):
    """One baby contributing to an Attachment Age stat. Read directly from
    the same per-case rows services.indicators/services.overview_period_metrics
    already merge to compute the displayed min/avg/max/case_count - not a
    separate or approximate dataset."""

    scr_babyid: str
    recordid: Optional[str] = None
    minutes: Optional[float] = None


class AttachmentCasesResponse(BaseModel):
    scope: str
    cases: list[AttachmentCaseRecord]
