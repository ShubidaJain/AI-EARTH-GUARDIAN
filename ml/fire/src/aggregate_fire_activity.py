import pandas as pd
from pathlib import Path


INPUT_FILE = Path(
    "ml/fire/data/processed/"
    "fire_power_grid_dataset.csv"
)

OUTPUT_FILE = Path(
    "ml/fire/data/processed/"
    "daily_fire_activity.csv"
)


fires = pd.read_csv(
    INPUT_FILE
)

fires["acq_date"] = pd.to_datetime(
    fires["acq_date"]
)


# --------------------------------------------------
# Aggregate by POWER grid + date
# --------------------------------------------------

daily = (
    fires
    .groupby(
        [
            "power_lat",
            "power_lon",
            "acq_date"
        ]
    )
    .agg(
        fire_count=(
            "latitude",
            "count"
        ),
        frp_sum=(
            "frp",
            "sum"
        ),
        frp_mean=(
            "frp",
            "mean"
        ),
        frp_max=(
            "frp",
            "max"
        )
    )
    .reset_index()
)


# --------------------------------------------------
# Fire label
# --------------------------------------------------

daily["fire_occurred"] = (
    daily["fire_count"] > 0
).astype(int)


# --------------------------------------------------
# Rename date
# --------------------------------------------------

daily = daily.rename(
    columns={
        "power_lat": "grid_lat",
        "power_lon": "grid_lon",
        "acq_date": "date"
    }
)


# --------------------------------------------------
# Save
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

daily.to_csv(
    OUTPUT_FILE,
    index=False
)


print()
print("=" * 60)
print("DAILY FIRE AGGREGATION COMPLETE")
print("=" * 60)

print(
    f"Rows: {len(daily)}"
)

print(
    f"Grid cells: "
    f"{daily[['grid_lat','grid_lon']].drop_duplicates().shape[0]}"
)

print(
    f"Fire days: "
    f"{daily['fire_occurred'].sum()}"
)

print()
print(
    daily.head(10).to_string(
        index=False
    )
)

print(
    f"\nSaved: {OUTPUT_FILE}"
)