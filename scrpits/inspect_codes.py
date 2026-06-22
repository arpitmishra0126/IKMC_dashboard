import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1])
)

from services.indicators import get_master_df

df = get_master_df()

print("=" * 60)
print("enr_ssc_rec DISTRIBUTION")
print("=" * 60)

print(
    df["enr_ssc_rec"]
    .value_counts(dropna=False)
)

df = get_master_df()

print(
    df.groupby("dmf_babyid")["enr_ssc_rec"]
    .first()
    .value_counts(dropna=False)
)