import json
import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw")


def load_json(filename):
    filepath = RAW_PATH / filename

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def inspect_json(filename):
    data = load_json(filename)

    print(f"\n{'='*60}")
    print(f"FILE: {filename}")
    print(f"TYPE: {type(data)}")

    if isinstance(data, list):
        print(f"RECORDS: {len(data)}")
        if len(data) > 0:
            print("\nFIRST RECORD KEYS:")
            print(list(data[0].keys()))

    elif isinstance(data, dict):
        print(f"TOTAL KEYS: {len(data.keys())}")
        print("\nKEYS:")
        print(list(data.keys())[:50])

    return data

def load_all_data():
    files = {
        "eligibility": "eligibility-registration.json",
        "mother": "mother-baby-registration.json",
        "daily": "daily-care-tracking.json",
        "discharge": "discharge.json",
    }

    data = {}

    for key, filename in files.items():
        data[key] = pd.DataFrame(load_json(filename))

    return data

if __name__ == "__main__":
    files = [
        "mother-baby-registration.json",
        "eligibility-registration.json",
        "daily-care-tracking.json",
        "discharge.json",
    ]

    for file in files:
        inspect_json(file)

