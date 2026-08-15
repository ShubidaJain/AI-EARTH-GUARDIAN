import pandas as pd
from pathlib import Path

from xgboost import XGBClassifier

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score
)


INPUT_FILE = Path(
    "ml/fire/data/processed/"
    "earth_guardian_features.csv"
)


# ============================================================
# Load dataset
# ============================================================

df = pd.read_csv(INPUT_FILE)

df["date"] = pd.to_datetime(df["date"])


# ============================================================
# Remove insufficient history
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

X = df[FEATURES]
y = df["fire_occurred"]


# ============================================================
# Chronological split
# ============================================================

train_mask = df["date"] < "2025-01-01"
test_mask = df["date"] >= "2025-01-01"

X_train = X[train_mask]
y_train = y[train_mask]

X_test = X[test_mask]
y_test = y[test_mask]


# ============================================================
# Class imbalance
# ============================================================

negative = (y_train == 0).sum()
positive = (y_train == 1).sum()

scale_pos_weight = negative / positive


# ============================================================
# Train XGBoost
# ============================================================

print("Training XGBoost...")

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
# Probabilities
# ============================================================

probabilities = model.predict_proba(
    X_test
)[:, 1]


roc_auc = roc_auc_score(
    y_test,
    probabilities
)

pr_auc = average_precision_score(
    y_test,
    probabilities
)


print()
print("=" * 70)
print("XGBOOST PROBABILITY PERFORMANCE")
print("=" * 70)

print(f"ROC-AUC: {roc_auc:.4f}")
print(f"PR-AUC:  {pr_auc:.4f}")


# ============================================================
# Threshold evaluation
# ============================================================

thresholds = [
    0.20,
    0.25,
    0.30,
    0.35,
    0.40,
    0.45,
    0.50,
    0.55,
    0.60,
    0.65,
    0.70,
    0.75,
    0.80
]


results = []


for threshold in thresholds:

    predictions = (
        probabilities >= threshold
    ).astype(int)

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    results.append({

        "threshold": threshold,

        "precision": precision,

        "recall": recall,

        "f1": f1
    })


results_df = pd.DataFrame(
    results
)


print()
print("=" * 70)
print("THRESHOLD ANALYSIS")
print("=" * 70)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# ============================================================
# Best F1 threshold
# ============================================================

best_f1 = results_df.loc[
    results_df["f1"].idxmax()
]

print()
print("=" * 70)
print("BEST F1 THRESHOLD")
print("=" * 70)

print(
    best_f1.to_string()
)


# ============================================================
# Save threshold results
# ============================================================

output = Path(
    "ml/fire/data/processed/"
    "threshold_results.csv"
)

results_df.to_csv(
    output,
    index=False
)

print()
print(f"Saved: {output}")