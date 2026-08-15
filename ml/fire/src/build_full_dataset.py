import pandas as pd
from pathlib import Path


FIRE_FILE = Path(
    "ml/fire/data/processed/daily_fire_activity.csv"
)

WEATHER_FILE = Path(
    "ml/fire/data/processed/"
    "weather_2023-01-01_2025-12-31.csv"
)

OUTPUT_FILE = Path(
    "ml/fire/data/processed/"
    "earth_guardian_training_data.csv"
)


# ============================================================
# Load
# ============================================================

print("Loading fire data...")
fire = pd.read_csv(FIRE_FILE)

print("Loading weather data...")
weather = pd.read_csv(WEATHER_FILE)


fire["date"] = pd.to_datetime(fire["date"])
weather["date"] = pd.to_datetime(weather["date"])


# ============================================================
# Restrict fire data to training period
# ============================================================

fire = fire[
    (fire["date"] >= "2023-01-01") &
    (fire["date"] <= "2025-12-31")
]


# ============================================================
# Use weather as the master grid
#
# This guarantees that no-fire days exist.
# ============================================================

dataset = weather.merge(
    fire,
    on=[
        "grid_lat",
        "grid_lon",
        "date"
    ],
    how="left"
)


# ============================================================
# Fire columns
# ============================================================

fire_columns = [
    "fire_count",
    "frp_sum",
    "frp_mean",
    "frp_max"
]

for column in fire_columns:

    dataset[column] = (
        dataset[column]
        .fillna(0)
    )


dataset["fire_occurred"] = (
    dataset["fire_occurred"]
    .fillna(0)
    .astype(int)
)


# ============================================================
# Add calendar features
# ============================================================

dataset["month"] = (
    dataset["date"].dt.month
)

dataset["day_of_year"] = (
    dataset["date"].dt.dayofyear
)


def get_season(month):

    if month in [12, 1, 2]:
        return "winter"

    if month in [3, 4, 5]:
        return "spring"

    if month in [6, 7, 8]:
        return "summer"

    return "autumn"


dataset["season"] = (
    dataset["month"]
    .apply(get_season)
)


# ============================================================
# Sort
# ============================================================

dataset = dataset.sort_values(
    [
        "date",
        "grid_lat",
        "grid_lon"
    ]
)


# ============================================================
# Save
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

dataset.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# Summary
# ============================================================

print()
print("=" * 60)
print("EARTH GUARDIAN TRAINING DATASET")
print("=" * 60)

print(
    f"Rows: {len(dataset)}"
)

print(
    f"Columns: {len(dataset.columns)}"
)

print(
    f"Date range: "
    f"{dataset['date'].min().date()} "
    f"→ "
    f"{dataset['date'].max().date()}"
)

print()

print("Class distribution:")

print(
    dataset["fire_occurred"]
    .value_counts()
)

print()

print("Missing values:")

print(
    dataset.isnull().sum()
)

print()

print("Columns:")

print(
    dataset.columns.tolist()
)

print()

print(
    f"Saved to: {OUTPUT_FILE}"
)