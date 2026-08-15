import pandas as pd

INPUT_FILE = (
    "ml/fire/data/processed/"
    "historical_fire_dataset.csv"
)

OUTPUT_FILE = (
    "ml/fire/data/processed/"
    "fire_grid_dataset.csv"
)


df = pd.read_csv(INPUT_FILE)

df["acq_date"] = pd.to_datetime(
    df["acq_date"]
)


# --------------------------------------------------
# Map every fire to a 0.5° grid cell
# --------------------------------------------------

df["grid_lat"] = (
    (df["latitude"] * 2).round() / 2
)

df["grid_lon"] = (
    (df["longitude"] * 2).round() / 2
)


# --------------------------------------------------
# Save
# --------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("Grid mapping complete.")

print(
    "Fire observations:",
    len(df)
)

print(
    "Unique grid cells:",
    df[
        ["grid_lat", "grid_lon"]
    ].drop_duplicates().shape[0]
)

print(
    "Unique grid/date combinations:",
    df[
        ["grid_lat", "grid_lon", "acq_date"]
    ].drop_duplicates().shape[0]
)

print(
    f"Saved to: {OUTPUT_FILE}"
)