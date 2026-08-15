import pandas as pd
from pathlib import Path


FIRE_FILE = Path(
    "ml/fire/data/processed/daily_fire_activity.csv"
)

WEATHER_FILE = Path(
    "ml/fire/data/processed/weather/"
    "weather_2023-01-01_2023-01-31.csv"
)

OUTPUT_FILE = Path(
    "ml/fire/data/processed/"
    "training_dataset_january_2023.csv"
)


# ============================================================
# Load data
# ============================================================

fire = pd.read_csv(FIRE_FILE)

weather = pd.read_csv(WEATHER_FILE)


fire["date"] = pd.to_datetime(
    fire["date"]
)

weather["date"] = pd.to_datetime(
    weather["date"]
)


# ============================================================
# Restrict fire data to January 2023
# ============================================================

fire = fire[
    (fire["date"] >= "2023-01-01") &
    (fire["date"] <= "2023-01-31")
]


# ============================================================
# Get actual POWER grid
# ============================================================

grid = weather[
    ["grid_lat", "grid_lon"]
].drop_duplicates()


print(
    f"POWER grid cells: {len(grid)}"
)


# ============================================================
# Create every grid × every day
# ============================================================

dates = pd.DataFrame({
    "date": pd.date_range(
        "2023-01-01",
        "2023-01-31",
        freq="D"
    )
})


grid["key"] = 1
dates["key"] = 1


grid_days = grid.merge(
    dates,
    on="key"
).drop(
    columns="key"
)


print(
    f"Possible grid-days: {len(grid_days)}"
)


# ============================================================
# Join weather
# ============================================================

dataset = grid_days.merge(
    weather,
    on=[
        "grid_lat",
        "grid_lon",
        "date"
    ],
    how="left"
)


# ============================================================
# Join fire activity
# ============================================================

dataset = dataset.merge(
    fire,
    on=[
        "grid_lat",
        "grid_lon",
        "date"
    ],
    how="left"
)


# ============================================================
# Fill no-fire observations
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
# Select final columns
# ============================================================

dataset = dataset[
    [
        "grid_lat",
        "grid_lon",
        "date",

        "temperature",
        "humidity",
        "wind_speed",
        "rainfall",

        "fire_count",
        "frp_sum",
        "frp_mean",
        "frp_max",

        "fire_occurred"
    ]
]


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
print("TRAINING DATASET CREATED")
print("=" * 60)

print(
    f"Rows: {len(dataset)}"
)

print(
    f"Columns: {len(dataset.columns)}"
)

print(
    f"Fire days: "
    f"{dataset['fire_occurred'].sum()}"
)

print(
    f"No-fire days: "
    f"{(dataset['fire_occurred'] == 0).sum()}"
)

print()

print(
    dataset.head(10).to_string(
        index=False
    )
)

print()

print(
    "Missing values:"
)

print(
    dataset.isnull().sum()
)

print()

print(
    f"Saved: {OUTPUT_FILE}"
)