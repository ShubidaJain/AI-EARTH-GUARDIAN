import json
from pathlib import Path

import pandas as pd
from xgboost import XGBClassifier


INPUT_FILE = Path(
    "ml/fire/data/processed/"
    "earth_guardian_features.csv"
)

MODEL_DIR = Path(
    "ml/fire/models"
)

MODEL_FILE = MODEL_DIR / "fire_risk_model.json"
FEATURE_FILE = MODEL_DIR / "model_features.json"


# ============================================================
# Features
# ============================================================

FEATURES = [
    "temperature",
    "humidity",
    "wind_speed",
    "rainfall",

    "temperature_3d_mean",
    "temperature_7d_mean",

    "humidity_3d_mean",
    "humidity_7d_mean",

    "wind_3d_mean",
    "wind_7d_mean",

    "rainfall_3d_sum",
    "rainfall_7d_sum",

    "grid_lat",
    "grid_lon",

    "month",
    "day_of_year"
]

TARGET = "fire_occurred"


# ============================================================
# Load
# ============================================================

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE)

df["date"] = pd.to_datetime(df["date"])


history_columns = [
    "temperature_7d_mean",
    "humidity_7d_mean",
    "wind_7d_mean",
    "rainfall_7d_sum"
]

df = df.dropna(
    subset=history_columns
).copy()


# ============================================================
# Training data
# ============================================================

train_mask = (
    df["date"] < "2025-01-01"
)

X_train = df.loc[
    train_mask,
    FEATURES
]

y_train = df.loc[
    train_mask,
    TARGET
]


# ============================================================
# Class imbalance
# ============================================================

negative = (
    y_train == 0
).sum()

positive = (
    y_train == 1
).sum()

scale_pos_weight = (
    negative / positive
)


# ============================================================
# Train final XGBoost model
# ============================================================

print("Training final XGBoost model...")

model = XGBClassifier(
    n_estimators=400,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="binary:logistic",
    eval_metric="logloss",
    scale_pos_weight=scale_pos_weight,
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)


# ============================================================
# Save model
# ============================================================

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

model.save_model(
    MODEL_FILE
)


# ============================================================
# Save feature information
# ============================================================

with open(
    FEATURE_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        {
            "features": FEATURES,
            "target": TARGET,
            "threshold": 0.50
        },
        file,
        indent=4
    )


print()
print("=" * 60)
print("MODEL SAVED")
print("=" * 60)

print(
    f"Model: {MODEL_FILE}"
)

print(
    f"Features: {FEATURE_FILE}"
)

print(
    f"Training rows: {len(X_train)}"
)

print(
    f"Features: {len(FEATURES)}"
)