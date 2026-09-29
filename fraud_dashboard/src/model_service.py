import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from src.config import MODEL_PATH
from src.data_loader import load_feature_schema


@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        return None
    try:
        import xgboost as xgb
        model = xgb.XGBClassifier()
        model.load_model(str(MODEL_PATH))
        return model
    except Exception:
        return None


def prepare_features(features_df: pd.DataFrame) -> pd.DataFrame:
    schema = load_feature_schema()
    if not schema or "feature_names" not in schema:
        return features_df

    expected = schema["feature_names"]
    current_cols = list(features_df.columns)

    missing = [c for c in expected if c not in current_cols]
    if missing:
        for col in missing:
            features_df[col] = 0

    features_df = features_df[expected]
    return features_df


def predict_fraud_probability(features_df: pd.DataFrame) -> float:
    model = load_model()
    if model is None:
        return -1.0

    prepared = prepare_features(features_df.copy())

    try:
        proba = model.predict_proba(prepared)[:, 1]
        return float(proba[0])
    except Exception:
        return -1.0


def get_precomputed_probability(sample_row: pd.Series) -> float:
    if "fraud_probability" in sample_row.index:
        val = sample_row["fraud_probability"]
        if pd.notna(val):
            return float(val)
    return -1.0
