from pathlib import Path

import pandas as pd


DATA_DIR = Path(
    "ml/fire/data/raw/historical"
)

OUTPUT_FILE = Path(
    "ml/fire/data/processed/"
    "historical_fire_dataset.csv"
)


files = sorted(
    DATA_DIR.glob("fires_*.csv")
)


if not files:

    raise FileNotFoundError(
        "No historical fire files found."
    )


print(
    f"Found {len(files)} files."
)


frames = []

for file in files:

    df = pd.read_csv(file)

    frames.append(df)


combined = pd.concat(
    frames,
    ignore_index=True
)


# ------------------------------------------------------------
# Clean dates
# ------------------------------------------------------------

combined["acq_date"] = pd.to_datetime(
    combined["acq_date"]
)

combined = combined[
    (combined["acq_date"] >= "2023-01-01") &
    (combined["acq_date"] <= "2025-12-31")
]


# ------------------------------------------------------------
# Remove duplicates
# ------------------------------------------------------------

before = len(combined)

combined = combined.drop_duplicates()


after = len(combined)


print(
    f"Removed {before - after} duplicates."
)


# ------------------------------------------------------------
# Sort
# ------------------------------------------------------------

combined = combined.sort_values(
    by=["acq_date", "latitude", "longitude"]
)


# ------------------------------------------------------------
# Save
# ------------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


combined.to_csv(
    OUTPUT_FILE,
    index=False
)


print()
print("Historical dataset created.")
print(
    f"Records: {len(combined)}"
)

print(
    f"Date range: "
    f"{combined['acq_date'].min().date()} "
    f"→ "
    f"{combined['acq_date'].max().date()}"
)

print(
    f"Saved: {OUTPUT_FILE}"
)