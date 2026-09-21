from typing import Optional

from fastapi import APIRouter, Query

from app.schemas.attachment_cases import AttachmentCasesResponse
from app.schemas.cohorts import CohortsResponse
from app.schemas.data_quality import DataQualityResponse
from app.schemas.discharge import DischargeResponse
from app.schemas.inborn import InbornResponse
from app.schemas.outborn import OutbornResponse
from app.schemas.overview import OverviewResponse
from app.services import (
    attachment_cases_service,
    cohorts_service,
    data_quality_service,
    discharge_service,
    inborn_service,
    outborn_service,
    overview_service,
)

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/overview", response_model=OverviewResponse)
def get_overview(
    period: Optional[str] = Query(default=None, pattern="^(7d|30d|3m|all)$"),
    from_date: Optional[str] = Query(default=None, pattern="^\\d{4}-\\d{2}-\\d{2}$"),
    to_date: Optional[str] = Query(default=None, pattern="^\\d{4}-\\d{2}-\\d{2}$"),
) -> OverviewResponse:
    return OverviewResponse(**overview_service.get_overview(period, from_date, to_date))


@router.get("/cohorts", response_model=CohortsResponse)
def get_cohorts() -> CohortsResponse:
    return CohortsResponse(**cohorts_service.get_cohort_summary())


@router.get("/data-quality", response_model=DataQualityResponse)
def get_data_quality() -> DataQualityResponse:
    return DataQualityResponse(**data_quality_service.get_data_quality())


@router.get("/inborn", response_model=InbornResponse)
def get_inborn(
    period: Optional[str] = Query(default=None, pattern="^(7d|30d|3m|all)$"),
    from_date: Optional[str] = Query(default=None, pattern="^\\d{4}-\\d{2}-\\d{2}$"),
    to_date: Optional[str] = Query(default=None, pattern="^\\d{4}-\\d{2}-\\d{2}$"),
) -> InbornResponse:
    return InbornResponse(**inborn_service.get_inborn_dashboard(period, from_date, to_date))


@router.get("/outborn", response_model=OutbornResponse)
def get_outborn(
    period: Optional[str] = Query(default=None, pattern="^(7d|30d|3m|all)$"),
    from_date: Optional[str] = Query(default=None, pattern="^\\d{4}-\\d{2}-\\d{2}$"),
    to_date: Optional[str] = Query(default=None, pattern="^\\d{4}-\\d{2}-\\d{2}$"),
) -> OutbornResponse:
    return OutbornResponse(**outborn_service.get_outborn_dashboard(period, from_date, to_date))


@router.get("/discharge", response_model=DischargeResponse)
def get_discharge(
    period: Optional[str] = Query(default=None, pattern="^(7d|30d|3m|all)$"),
    from_date: Optional[str] = Query(default=None, pattern="^\\d{4}-\\d{2}-\\d{2}$"),
    to_date: Optional[str] = Query(default=None, pattern="^\\d{4}-\\d{2}-\\d{2}$"),
) -> DischargeResponse:
    return DischargeResponse(**discharge_service.get_discharge_dashboard(period, from_date, to_date))


@router.get("/attachment-cases", response_model=AttachmentCasesResponse)
def get_attachment_cases(
    scope: str,
    period: Optional[str] = Query(default=None, pattern="^(7d|30d|3m|all)$"),
    from_date: Optional[str] = Query(default=None, pattern="^\\d{4}-\\d{2}-\\d{2}$"),
    to_date: Optional[str] = Query(default=None, pattern="^\\d{4}-\\d{2}-\\d{2}$"),
) -> AttachmentCasesResponse:
    # UnknownAttachmentScopeError -> 404, InvalidDateRangeError -> 400,
    # both translated by the exception handlers registered in app.main.
    return AttachmentCasesResponse(
        **attachment_cases_service.get_attachment_cases(scope, period, from_date, to_date)
    )
