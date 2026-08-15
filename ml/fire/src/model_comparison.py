import pandas as pd


results = [
    {
        "model": "Logistic Regression",
        "roc_auc": None,
        "pr_auc": None,
        "recall": None,
        "f1": None
    },
    {
        "model": "Random Forest",
        "roc_auc": None,
        "pr_auc": None,
        "recall": None,
        "f1": None
    },
    {
        "model": "XGBoost",
        "roc_auc": None,
        "pr_auc": None,
        "recall": None,
        "f1": None
    }
]


df = pd.DataFrame(results)

print(df)