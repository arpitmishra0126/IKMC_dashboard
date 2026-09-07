from pydantic import BaseModel


class OverviewResponse(BaseModel):
    pre_screened: int
    screened: int
    eligible_for_enrollment: int
    discharged: int
    referred: int
    lama: int
    death: int
