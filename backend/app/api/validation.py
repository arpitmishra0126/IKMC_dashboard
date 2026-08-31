from fastapi import APIRouter

from app.schemas.validation import ValidationDetailResponse
from app.services import validation_service

router = APIRouter(prefix="/api/validation", tags=["validation"])


@router.get("/{check}", response_model=ValidationDetailResponse)
def get_validation_detail(check: str) -> ValidationDetailResponse:
    # UnknownValidationCheckError is translated to a 404 by the exception
    # handler registered in app.main.
    return ValidationDetailResponse(**validation_service.get_validation_detail(check))
