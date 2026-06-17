# services/config.py

FILES = {
    "eligibility": "eligibility-registration.json",
    "mother": "mother-baby-registration.json",
    "daily": "daily-care-tracking.json",
    "discharge": "discharge.json",
}

FIELD_MAP = {
    "place_of_birth": "scr_pob",
    "sncu_type": "scr_sncu_sick",
    "delivery_mode": "scr_del_mode",

    "eligibility_babyid": "scr_babyid",
    "mother_babyid": "enr_babyid",
    "daily_babyid": "dmf_babyid",
    "discharge_babyid": "dis_babyid",
}