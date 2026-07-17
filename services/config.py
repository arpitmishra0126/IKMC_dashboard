# services/config.py
import os
from dotenv import load_dotenv

load_dotenv()
# ==========================================================
# Data Source
# ==========================================================
# Supported values:
#   - "json" : Load data from local JSON files
#   - "api"  : Load data from backend REST API
# ==========================================================

DATA_SOURCE = "api"


# ==========================================================
# API Configuration
# ==========================================================

API_CONFIG = {
    "base_url": "https://api.cel-one.org/v1",
    "api_key": os.getenv("IKMC_API_KEY"),
    "timeout": 60,
}


# ==========================================================
# API Endpoints
# ==========================================================

ENDPOINTS = {
    "eligibility": "eligibility-registration",
    "mother": "mother-baby-registration",
    "daily": "daily-care-tracking",
    "discharge": "discharge",
}


# ==========================================================
# Local JSON Files
# ==========================================================

FILES = {
    "eligibility": "eligibility-registration.json",
    "mother": "mother-baby-registration.json",
    "daily": "daily-care-tracking.json",
    "discharge": "discharge.json",
}


# ==========================================================
# Field Mapping
# ==========================================================

FIELD_MAP = {
    "place_of_birth": "scr_pob",
    "sncu_type": "scr_sncu_sick",
    "delivery_mode": "scr_del_mode",

    "eligibility_babyid": "scr_babyid",
    "mother_babyid": "enr_babyid",
    "daily_babyid": "dmf_babyid",
    "discharge_babyid": "dis_babyid",
}