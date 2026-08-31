from pydantic import BaseModel

from app.schemas.common import DeliverySplitFloat, DeliverySplitInt


class AttachmentDisplay(BaseModel):
    """Both the value currently displayed on the dashboard (hardcoded) and
    the real computed value are exposed - see
    docs/MIGRATION_DECISIONS.md #3. Neither is treated as "correct" here."""

    displayed_nvd: str
    displayed_csection: str
    is_hardcoded: bool
    computed_nvd_hours: float
    computed_csection_hours: float


class CohortCard(BaseModel):
    total_cases: int
    delivery: DeliverySplitInt
    ssc_under_2h: DeliverySplitInt
    avg_kmc: DeliverySplitFloat
    exclusive_bf: DeliverySplitInt
    attachment: AttachmentDisplay


class CohortsResponse(BaseModel):
    inborn: CohortCard
    outborn: CohortCard
