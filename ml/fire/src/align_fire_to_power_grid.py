import pandas as pd
from pathlib import Path


FIRE_FILE = Path(
    "ml/fire/data/processed/"
    "historical_fire_dataset.csv"
)

WEATHER_FILE = Path(
    "ml/fire/data/processed/weather/"
    "weather_2023-01-01_2023-01-31.csv"
)

OUTPUT_FILE = Path(
    "ml/fire/data/processed/"
    "fire_power_grid_dataset.csv"
)


# --------------------------------------------------
# Load data
# --------------------------------------------------

fires = pd.read_csv(
    FIRE_FILE
)

weather = pd.read_csv(
    WEATHER_FILE
)


fires["acq_date"] = pd.to_datetime(
    fires["acq_date"]
)

weather["date"] = pd.to_datetime(
    weather["date"]
)


# --------------------------------------------------
# Get actual POWER grid coordinates
# --------------------------------------------------

power_lats = sorted(
    weather["grid_lat"].unique()
)

power_lons = sorted(
    weather["grid_lon"].unique()
)


print(
    f"POWER latitude points: {len(power_lats)}"
)

print(
    f"POWER longitude points: {len(power_lons)}"
)


# --------------------------------------------------
# Find nearest grid coordinate
# --------------------------------------------------

def nearest(value, values):

    return min(
        values,
        key=lambda x: abs(x - value)
    )


fires["power_lat"] = fires[
    "latitude"
].apply(
    lambda x: nearest(x, power_lats)
)

fires["power_lon"] = fires[
    "longitude"
].apply(
    lambda x: nearest(x, power_lons)
)


# --------------------------------------------------
# Save
# --------------------------------------------------

fires.to_csv(
    OUTPUT_FILE,
    index=False
)


print()
print("=" * 60)
print("FIRE → POWER GRID ALIGNMENT COMPLETE")
print("=" * 60)

print(
    f"Fire observations: {len(fires)}"
)

print(
    "Unique POWER grid cells:",
    fires[
        ["power_lat", "power_lon"]
    ].drop_duplicates().shape[0]
)

print(
    f"Saved: {OUTPUT_FILE}"
)