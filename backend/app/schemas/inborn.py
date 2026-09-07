from pydantic import BaseModel

from app.schemas.common import AttachmentStatSplit, CoverageSplit, DeliverySplitFloat, DeliverySplitInt


class InbornUnitDetail(BaseModel):
    avg_kmc: float
    total_cases: int
    delivery: DeliverySplitInt
    ssc_under_2h: DeliverySplitInt
    avg_kmc_by_delivery: DeliverySplitFloat
    exclusive_bf: DeliverySplitInt
    attachment: AttachmentStatSplit
    coverage: CoverageSplit
    nvd_definition_note: str


class InbornResponse(BaseModel):
    overall_avg_kmc_hours: float
    msncu: InbornUnitDetail
    pnc: InbornUnitDetail
