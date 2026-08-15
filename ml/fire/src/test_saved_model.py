import json
from pathlib import Path

import pandas as pd
from xgboost import XGBClassifier


MODEL_FILE = Path(
    "ml/fire/models/fire_risk_model.json"
)

FEATURE_FILE = Path(
    "ml/fire/models/model_features.json"
)

DATA_FILE = Path(
    "ml/fire/data/processed/"
    "earth_guardian_features.csv"
)


# Load feature configuration

with open(
    FEATURE_FILE,
    "r",
    encoding="utf-8"
) as file:

    config = json.load(file)


features = config["features"]
threshold = config["threshold"]


# Load model

model = XGBClassifier()

model.load_model(
    MODEL_FILE
)


# Load test data

df = pd.read_csv(
    DATA_FILE
)

df["date"] = pd.to_datetime(
    df["date"]
)


df = df.dropna(
    subset=[
        "temperature_7d_mean",
        "humidity_7d_mean",
        "wind_7d_mean",
        "rainfall_7d_sum"
    ]
)


# Pick one 2025 observation

sample = df[
    df["date"] >= "2025-01-01"
].iloc[0]


X = pd.DataFrame(
    [sample[features].values],
    columns=features
)


probability = model.predict_proba(
    X
)[0][1]


prediction = int(
    probability >= threshold
)


print()
print("=" * 60)
print("SAVED MODEL TEST")
print("=" * 60)

print(
    f"Date: {sample['date'].date()}"
)

print(
    f"Location: "
    f"{sample['grid_lat']}, "
    f"{sample['grid_lon']}"
)

print(
    f"Fire probability: "
    f"{probability:.4f}"
)

print(
    f"Threshold: {threshold}"
)

print(
    f"Prediction: {prediction}"
)