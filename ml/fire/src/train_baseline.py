import pandas as pd
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    average_precision_score
)
from sklearn.preprocessing import StandardScaler


INPUT_FILE = Path(
    "ml/fire/data/processed/"
    "earth_guardian_features.csv"
)


# ============================================================
# Load
# ============================================================

print("Loading feature dataset...")

df = pd.read_csv(INPUT_FILE)

df["date"] = pd.to_datetime(df["date"])


# ============================================================
# Remove rows without historical weather
# ============================================================

history_columns = [
    "temperature_7d_mean",
    "humidity_7d_mean",
    "wind_7d_mean",
    "rainfall_7d_sum"
]

before = len(df)

df = df.dropna(
    subset=history_columns
).copy()

print(
    f"Removed {before - len(df)} rows "
    f"without 7-day history."
)


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


X = df[FEATURES]

y = df[TARGET]


# ============================================================
# Chronological split
#
# 2023-2024 → training
# 2025       → testing
# ============================================================

train_mask = (
    df["date"] < "2025-01-01"
)

test_mask = (
    df["date"] >= "2025-01-01"
)


X_train = X[train_mask]
y_train = y[train_mask]

X_test = X[test_mask]
y_test = y[test_mask]


print()
print("=" * 60)
print("DATA SPLIT")
print("=" * 60)

print(
    f"Training rows: {len(X_train)}"
)

print(
    f"Testing rows: {len(X_test)}"
)

print(
    f"Training fire rate: "
    f"{y_train.mean():.3f}"
)

print(
    f"Testing fire rate: "
    f"{y_test.mean():.3f}"
)


# ============================================================
# Scale features
# ============================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(
    X_train
)

X_test_scaled = scaler.transform(
    X_test
)


# ============================================================
# Logistic Regression
# ============================================================

print()
print("=" * 60)
print("TRAINING LOGISTIC REGRESSION")
print("=" * 60)


model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)


model.fit(
    X_train_scaled,
    y_train
)


# ============================================================
# Predictions
# ============================================================

y_pred = model.predict(
    X_test_scaled
)

y_probability = model.predict_proba(
    X_test_scaled
)[:, 1]


# ============================================================
# Evaluation
# ============================================================

print()
print("=" * 60)
print("MODEL RESULTS")
print("=" * 60)

print()

print(
    classification_report(
        y_test,
        y_pred,
        digits=4
    )
)


print("Confusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


roc_auc = roc_auc_score(
    y_test,
    y_probability
)

pr_auc = average_precision_score(
    y_test,
    y_probability
)


print()

print(
    f"ROC-AUC: {roc_auc:.4f}"
)

print(
    f"PR-AUC:  {pr_auc:.4f}"
)