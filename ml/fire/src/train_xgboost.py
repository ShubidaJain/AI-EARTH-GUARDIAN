import pandas as pd
from pathlib import Path

from xgboost import XGBClassifier

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    average_precision_score
)


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
# Remove rows without 7-day history
# ============================================================

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
# 2023–2024 → training
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

print(f"Training rows: {len(X_train)}")
print(f"Testing rows:  {len(X_test)}")

print(
    f"Training fire rate: "
    f"{y_train.mean():.3f}"
)

print(
    f"Testing fire rate: "
    f"{y_test.mean():.3f}"
)


# ============================================================
# Handle class imbalance
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

print(
    f"scale_pos_weight: "
    f"{scale_pos_weight:.3f}"
)


# ============================================================
# XGBoost
# ============================================================

print()
print("=" * 60)
print("TRAINING XGBOOST")
print("=" * 60)


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
# Predictions
# ============================================================

y_probability = model.predict_proba(
    X_test
)[:, 1]

y_pred = (
    y_probability >= 0.5
).astype(int)


# ============================================================
# Evaluation
# ============================================================

print()
print("=" * 60)
print("XGBOOST RESULTS")
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


# ============================================================
# Feature importance
# ============================================================

importance = pd.DataFrame({
    "feature": FEATURES,
    "importance": model.feature_importances_
})


importance = importance.sort_values(
    "importance",
    ascending=False
)


print()
print("=" * 60)
print("FEATURE IMPORTANCE")
print("=" * 60)

print(
    importance.to_string(
        index=False
    )
)