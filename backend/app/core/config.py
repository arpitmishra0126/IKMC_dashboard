"""
Backend configuration.

This module intentionally does NOT read or hold the upstream IKMC_API_KEY.
That secret stays fully encapsulated inside the existing services/config.py
and services/api_service.py at the repo root (unmodified) - the FastAPI
backend never touches it, so it can never leak into a response body, log
line, or the future React frontend.

This module only configures things specific to running the backend itself:
CORS origins for local frontend development, and the repo-root path
bootstrap needed to import the existing `services` package.
"""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# backend/app/core/config.py -> parents[3] is the repo root (contains services/)
REPO_ROOT = Path(__file__).resolve().parents[3]

if str(REPO_ROOT) not in sys.path:
    # Required so `import services.indicators` / `import services.loader`
    # resolve to the existing, unmodified root-level package rather than
    # anything under backend/. This is the ONLY place the backend reaches
    # outside its own tree.
    sys.path.insert(0, str(REPO_ROOT))

# services/loader.py defines RAW_PATH = Path("data/raw") - a RELATIVE path
# that resolves against the process's current working directory. This is
# existing, unmodified behavior; it works for Streamlit only because
# `streamlit run app.py` is always launched with the repo root as cwd. To
# reuse services/loader.py unchanged, the backend process must satisfy the
# same assumption regardless of where `uvicorn` was invoked from.
if os.getcwd() != str(REPO_ROOT):
    os.chdir(REPO_ROOT)

# Reuse the same .env file the Streamlit app reads (contains IKMC_API_KEY,
# consumed only inside services/config.py, never read here).
load_dotenv(REPO_ROOT / ".env")


def _split_csv_env(name: str, default: str) -> list[str]:
    raw = os.getenv(name, default)
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


class Settings:
    """Plain settings object - no external settings library needed for the
    handful of values the backend itself owns."""

    app_name: str = "IKMC Dashboard API"
    app_env: str = os.getenv("APP_ENV", "development")

    # Vite (5173) and CRA/Next (3000) dev server defaults; override via
    # ALLOWED_ORIGINS="http://a.example.com,http://b.example.com"
    allowed_origins: list[str] = _split_csv_env(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,http://localhost:3000",
    )


settings = Settings()
