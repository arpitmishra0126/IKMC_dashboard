from fastapi import APIRouter

from app.schemas.meta import RefreshResponse, SyncMetadataResponse
from app.services import meta_service

router = APIRouter(prefix="/api/meta", tags=["meta"])


@router.get("/sync", response_model=SyncMetadataResponse)
def get_sync_metadata() -> SyncMetadataResponse:
    return SyncMetadataResponse(**meta_service.get_sync_metadata())


@router.post("/refresh", response_model=RefreshResponse)
def refresh() -> RefreshResponse:
    return RefreshResponse(**meta_service.refresh())
