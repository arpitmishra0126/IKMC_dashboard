from pydantic import BaseModel

from app.schemas.common import AttachmentStatSplit, DeliverySplitFloat, DeliverySplitInt


class CohortCard(BaseModel):
    total_cases: int
    delivery: DeliverySplitInt
    ssc_under_2h: DeliverySplitInt
    avg_kmc: DeliverySplitFloat
    exclusive_bf: DeliverySplitInt
    attachment: AttachmentStatSplit


class CohortsResponse(BaseModel):
    inborn: CohortCard
    outborn: CohortCard
