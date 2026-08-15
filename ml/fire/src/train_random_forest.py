import pandas as pd
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
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
    f"Training fire rate: {y_train.mean():.3f}"
)

print(
    f"Testing fire rate: {y_test.mean():.3f}"
)


# ============================================================
# Random Forest
# ============================================================

print()
print("=" * 60)
print("TRAINING RANDOM FOREST")
print("=" * 60)


model = RandomForestClassifier(
    n_estimators=300,
    max_depth=15,
    min_samples_leaf=5,
    class_weight="balanced",
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

y_pred = model.predict(
    X_test
)

y_probability = model.predict_proba(
    X_test
)[:, 1]


# ============================================================
# Evaluation
# ============================================================

print()
print("=" * 60)
print("RANDOM FOREST RESULTS")
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