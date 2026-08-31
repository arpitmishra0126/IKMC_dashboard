"""
Backend test configuration.

Mirrors the approach used in the repo-root tests/conftest.py (the approved
parity baseline suite): force the existing services.loader.DATA_SOURCE to
"json" so tests run deterministically offline against data/raw/*.json
instead of requiring network access + IKMC_API_KEY. This does not modify
services/config.py or any calculation - it only selects which already-
supported data source the unmodified loader uses.
"""
import json
import warnings
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

warnings.filterwarnings("ignore")

BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent
BASELINE_PATH = REPO_ROOT / "tests" / "baseline" / "baseline_snapshot.json"


@pytest.fixture(scope="session", autouse=True)
def use_local_json_fixtures():
    from app.core.config import settings  # noqa: F401 - triggers repo-root sys.path bootstrap

    import services.loader as loader
    loader.DATA_SOURCE = "json"
    yield


@pytest.fixture(scope="session")
def client(use_local_json_fixtures) -> TestClient:
    from app.main import app
    return TestClient(app)


@pytest.fixture(scope="session")
def baseline() -> dict:
    assert BASELINE_PATH.exists(), (
        f"{BASELINE_PATH} not found. Run `python tests/capture_baseline.py` "
        "from the repo root first."
    )
    return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
