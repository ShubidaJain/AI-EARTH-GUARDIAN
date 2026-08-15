import pandas as pd
from pathlib import Path


INPUT_FILE = Path(
    "ml/fire/data/processed/"
    "earth_guardian_training_data.csv"
)

OUTPUT_FILE = Path(
    "ml/fire/data/processed/"
    "earth_guardian_features.csv"
)


# ============================================================
# Load dataset
# ============================================================

print("Loading dataset...")

df = pd.read_csv(
    INPUT_FILE
)

df["date"] = pd.to_datetime(
    df["date"]
)


# ============================================================
# Sort by grid and date
# ============================================================

df = df.sort_values(
    [
        "grid_lat",
        "grid_lon",
        "date"
    ]
)


# ============================================================
# Group by geographic cell
# ============================================================

group = df.groupby(
    [
        "grid_lat",
        "grid_lon"
    ]
)


# ============================================================
# Temperature rolling features
# ============================================================

df["temperature_3d_mean"] = (
    group["temperature"]
    .transform(
        lambda x:
        x.shift(1)
        .rolling(3)
        .mean()
    )
)


df["temperature_7d_mean"] = (
    group["temperature"]
    .transform(
        lambda x:
        x.shift(1)
        .rolling(7)
        .mean()
    )
)


# ============================================================
# Humidity rolling features
# ============================================================

df["humidity_3d_mean"] = (
    group["humidity"]
    .transform(
        lambda x:
        x.shift(1)
        .rolling(3)
        .mean()
    )
)


df["humidity_7d_mean"] = (
    group["humidity"]
    .transform(
        lambda x:
        x.shift(1)
        .rolling(7)
        .mean()
    )
)


# ============================================================
# Wind rolling features
# ============================================================

df["wind_3d_mean"] = (
    group["wind_speed"]
    .transform(
        lambda x:
        x.shift(1)
        .rolling(3)
        .mean()
    )
)


df["wind_7d_mean"] = (
    group["wind_speed"]
    .transform(
        lambda x:
        x.shift(1)
        .rolling(7)
        .mean()
    )
)


# ============================================================
# Rainfall rolling features
# ============================================================

df["rainfall_3d_sum"] = (
    group["rainfall"]
    .transform(
        lambda x:
        x.shift(1)
        .rolling(3)
        .sum()
    )
)


df["rainfall_7d_sum"] = (
    group["rainfall"]
    .transform(
        lambda x:
        x.shift(1)
        .rolling(7)
        .sum()
    )
)


# ============================================================
# Save
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# Summary
# ============================================================

print()
print("=" * 60)
print("FEATURE ENGINEERING COMPLETE")
print("=" * 60)

print(
    f"Rows: {len(df)}"
)

print(
    f"Columns: {len(df.columns)}"
)

print()

print(
    "New features:"
)

print(
    [
        "temperature_3d_mean",
        "temperature_7d_mean",
        "humidity_3d_mean",
        "humidity_7d_mean",
        "wind_3d_mean",
        "wind_7d_mean",
        "rainfall_3d_sum",
        "rainfall_7d_sum"
    ]
)

print()

print(
    "Missing values:"
)

print(
    df.isnull().sum()
)

print()

print(
    f"Saved: {OUTPUT_FILE}"
)