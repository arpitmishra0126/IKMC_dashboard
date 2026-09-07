# IKMC Dashboard

## Overview

The IKMC Dashboard is a facility-wide monitoring dashboard for the IKMC
program: SSC, KMC, breastfeeding compliance, cohort performance, and
discharge outcomes.

The application was originally a Streamlit app. It has since been
migrated to a **React frontend** talking to a **FastAPI backend**, which
serves the existing Python indicator/business logic:

```
React (frontend/)  ->  FastAPI (backend/)  ->  services/ (indicator logic + data loading)
```

The `services/` business logic itself is unchanged by the migration.

## Tech stack

- **Frontend:** React, TypeScript, Vite, Tailwind CSS
- **Backend:** FastAPI, Pydantic, Uvicorn
- **Shared business logic:** Python (`services/`), Pandas
- **Data source:** upstream IKMC REST API (`services/api_service.py`);
  local JSON fixtures under `data/raw/` are used for tests and offline
  development

## Project structure

```
backend/          FastAPI application (app/, tests/, requirements.txt)
frontend/         React application (src/, package.json)
services/         Shared indicator/business logic and data loading, used by backend/
data/raw/         Local JSON fixtures (used for tests / offline development)
tests/            Root-level parity/baseline test suite for services/indicators.py
docs/             Migration decisions, API design notes, deployment audits, handoff notes
```

## Local development

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The backend reads `IKMC_API_KEY` from the environment (a `.env` file at
the repository root, or real environment variables) and, for local
development, allows requests from `http://localhost:5173` and
`http://localhost:3000` by default — override with `ALLOWED_ORIGINS` (a
comma-separated list; see `backend/app/core/config.py`).

### Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

Copy `frontend/.env.example` to `frontend/.env.local` and set
`VITE_API_BASE_URL` to point at the backend (defaults to
`http://localhost:8000`).

### Tests

```bash
# Root parity/baseline suite (services/indicators.py)
pytest

# Backend API test suite
cd backend
pytest
```

### Frontend production build

```bash
cd frontend
npm run build
```

## Configuration

| Variable | Used by | Purpose |
|---|---|---|
| `IKMC_API_KEY` | backend (`services/config.py`) | Upstream IKMC API bearer token |
| `ALLOWED_ORIGINS` | backend | Comma-separated list of allowed frontend origins (CORS) |
| `VITE_API_BASE_URL` | frontend (build-time) | Public URL of the FastAPI backend |

## Deployment

The backend and frontend are deployed as two separate services from this
repository's `react-migration` branch — a Python/FastAPI service built
from `backend/`, and a static site built from `frontend/` via
`npm run build`. See `docs/CLAUDE_HANDOFF.md` for current production URLs
and deployment status, and `docs/` generally for migration decisions and
API design notes.

## Notes

- API credentials are loaded from environment variables
  (`python-dotenv` reads a local `.env` file when present).
- This project is intended for internal use.
