import pandas as pd
from src.data_loader import load_feature_importance


def get_top_factors(n: int = 5) -> list[dict]:
    fi_df = load_feature_importance()
    if fi_df.empty:
        return []

    top = fi_df.sort_values("importance", ascending=False).head(n)
    factors = []
    for _, row in top.iterrows():
        factors.append({
            "feature": row["feature"],
            "importance": float(row["importance"]),
        })
    return factors


def get_transaction_factors(
    sample_row: pd.Series,
    top_n: int = 5,
) -> list[dict]:
    top_features = get_top_factors(top_n)
    factors = []
    for feat in top_features:
        name = feat["feature"]
        value = sample_row.get(name, None)
        factors.append({
            "feature": name,
            "importance": feat["importance"],
            "value": value,
            "is_local": False,
        })
    return factors
