from fastapi import APIRouter

from app.schemas.cohorts import CohortsResponse
from app.schemas.data_quality import DataQualityResponse
from app.schemas.discharge import DischargeResponse
from app.schemas.inborn import InbornResponse
from app.schemas.outborn import OutbornResponse
from app.schemas.overview import OverviewResponse
from app.services import (
    cohorts_service,
    data_quality_service,
    discharge_service,
    inborn_service,
    outborn_service,
    overview_service,
)

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/overview", response_model=OverviewResponse)
def get_overview() -> OverviewResponse:
    return OverviewResponse(**overview_service.get_overview())


@router.get("/cohorts", response_model=CohortsResponse)
def get_cohorts() -> CohortsResponse:
    return CohortsResponse(**cohorts_service.get_cohort_summary())


@router.get("/data-quality", response_model=DataQualityResponse)
def get_data_quality() -> DataQualityResponse:
    return DataQualityResponse(**data_quality_service.get_data_quality())


@router.get("/inborn", response_model=InbornResponse)
def get_inborn() -> InbornResponse:
    return InbornResponse(**inborn_service.get_inborn_dashboard())


@router.get("/outborn", response_model=OutbornResponse)
def get_outborn() -> OutbornResponse:
    return OutbornResponse(**outborn_service.get_outborn_dashboard())


@router.get("/discharge", response_model=DischargeResponse)
def get_discharge() -> DischargeResponse:
    return DischargeResponse(**discharge_service.get_discharge_dashboard())
