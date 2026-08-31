"""
Pytest configuration for the IKMC Dashboard parity/baseline test suite.

WHY THIS SUITE EXISTS
----------------------
Before migrating the dashboard logic into FastAPI, we need a frozen record
of what the CURRENT Streamlit implementation (services/indicators.py)
actually returns. Once the FastAPI port exists, the same assertions in
test_baseline_parity.py can be re-pointed at the new HTTP endpoints to prove

    CURRENT STREAMLIT IMPLEMENTATION  ==  NEW FASTAPI IMPLEMENTATION

No business logic is modified anywhere in this suite. The only thing this
conftest does is force a deterministic, offline DATA SOURCE so results are
reproducible in CI/local runs without network access or a live API key.

DATA SOURCE OVERRIDE
---------------------
services/config.py hardcodes `DATA_SOURCE = "api"` (a Python literal, not
read from the environment). Calling the real API is unsuitable for a
baseline: it requires network access + IKMC_API_KEY, and upstream data
changes over time, which would make the "baseline" a moving target.

Instead we monkeypatch the already-imported `DATA_SOURCE` name inside
`services.loader` (that's the only place the value is actually consulted,
via `load_all_data()`) so it reads from the local fixtures committed at
data/raw/*.json. This does not touch services/config.py or any calculation
code — it only changes which dataset the unmodified functions run against.
"""
import sys
import warnings
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Streamlit prints "missing ScriptRunContext" / "bare mode" warnings when its
# functions run outside `streamlit run`. Harmless here since none of the
# indicator functions render UI - they only compute values.
warnings.filterwarnings("ignore")


@pytest.fixture(scope="session", autouse=True)
def use_local_json_fixtures():
    import services.loader as loader
    loader.DATA_SOURCE = "json"
    yield


@pytest.fixture(scope="session")
def indicators(use_local_json_fixtures):
    import services.indicators as ind
    return ind


@pytest.fixture(scope="session")
def loader_module(use_local_json_fixtures):
    import services.loader as loader
    return loader


@pytest.fixture(scope="session")
def app_source():
    """Raw source text of app.py, used only to detect the hardcoded
    attachment-time literals so a silent edit to them is caught."""
    return (ROOT / "app.py").read_text(encoding="utf-8")
