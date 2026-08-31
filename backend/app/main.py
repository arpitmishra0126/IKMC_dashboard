"""
FastAPI backend for the IKMC Dashboard.

This is a SEPARATE application from the existing Streamlit app (app.py at
the repo root). It does not modify, import into, or run alongside the
Streamlit process - it independently imports the same underlying
services/indicators.py, services/loader.py, services/api_service.py, and
services/config.py to compute identical values via a REST API, per
docs/API_MIGRATION_PLAN.md.

Run with:
    cd backend
    uvicorn app.main:app --reload --port 8000
"""
import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import dashboard, meta, validation
from app.core.config import settings
from app.core.exceptions import UnknownValidationCheckError, UpstreamDataError

app = FastAPI(
    title=settings.app_name,
    description=(
        "Read-only REST API over the existing IKMC Dashboard business "
        "logic (services/indicators.py). See docs/MIGRATION_DECISIONS.md "
        "for known business-logic ambiguities preserved as-is, and "
        "docs/API_MIGRATION_PLAN.md for the endpoint design rationale."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.exception_handler(UnknownValidationCheckError)
async def handle_unknown_validation_check(
    request: Request, exc: UnknownValidationCheckError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc),
            "known_checks": exc.known_checks,
        },
    )


@app.exception_handler(UpstreamDataError)
async def handle_upstream_data_error(
    request: Request, exc: UpstreamDataError
) -> JSONResponse:
    return JSONResponse(status_code=502, content={"detail": exc.detail})


@app.exception_handler(requests.exceptions.RequestException)
async def handle_requests_exception(
    request: Request, exc: requests.exceptions.RequestException
) -> JSONResponse:
    # Deliberately generic - never echo the exception's request/response
    # objects back to the client, since services/api_service.py attaches
    # the Authorization header (containing IKMC_API_KEY) to outgoing
    # requests, and that header can be reachable via exc.request.headers.
    return JSONResponse(
        status_code=502,
        content={"detail": "Upstream data source is unavailable. Please try again later."},
    )


@app.get("/api/health", tags=["meta"])
def health_check() -> dict:
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}


app.include_router(meta.router)
app.include_router(dashboard.router)
app.include_router(validation.router)
