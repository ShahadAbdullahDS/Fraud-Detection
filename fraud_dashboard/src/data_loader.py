import json
import streamlit as st
import pandas as pd
from pathlib import Path
from src.config import (
    METRICS_PATH, FRAUD_STATS_PATH, EDA_SUMMARY_PATH,
    HOURLY_FRAUD_PATH, AMT_DIST_PATH, FEATURE_IMPORTANCE_PATH,
    SAMPLE_TRANSACTIONS_PATH, MODEL_INPUT_PATH,
    FEATURE_SCHEMA_PATH, DISPLAY_COLUMNS,
)


@st.cache_data
def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data
def load_parquet(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_parquet(path)


def load_metrics() -> dict:
    return load_json(METRICS_PATH)


def load_fraud_stats() -> dict:
    return load_json(FRAUD_STATS_PATH)


def load_eda_summary() -> dict:
    return load_json(EDA_SUMMARY_PATH)


def load_hourly_fraud() -> pd.DataFrame:
    return load_csv(HOURLY_FRAUD_PATH)


def load_amount_distribution() -> pd.DataFrame:
    return load_csv(AMT_DIST_PATH)


def load_feature_importance() -> pd.DataFrame:
    df = load_csv(FEATURE_IMPORTANCE_PATH)
    if not df.empty and "importance" in df.columns:
        df = df.sort_values("importance", ascending=True)
    return df


def load_feature_schema() -> dict:
    return load_json(FEATURE_SCHEMA_PATH)


def load_sample_transactions() -> pd.DataFrame:
    df = load_csv(SAMPLE_TRANSACTIONS_PATH)
    if df.empty:
        return df
    df["sample_id"] = range(1, len(df) + 1)
    return df


def load_model_inputs() -> pd.DataFrame:
    df = load_parquet(MODEL_INPUT_PATH)
    return df


def get_display_df(samples: pd.DataFrame) -> pd.DataFrame:
    if samples.empty:
        return samples
    available = [c for c in DISPLAY_COLUMNS if c in samples.columns]
    display = samples[["sample_id"] + available].copy()
    return display


def get_model_input_for_sample(sample_id: int, model_inputs: pd.DataFrame) -> pd.DataFrame:
    if model_inputs.empty or "sample_id" not in model_inputs.columns:
        return pd.DataFrame()
    row = model_inputs[model_inputs["sample_id"] == sample_id]
    if row.empty:
        return pd.DataFrame()
    features = row.drop(columns=["sample_id"], errors="ignore")
    return features


def validate_data_available() -> dict:
    status = {}
    checks = {
        "metrics": METRICS_PATH,
        "fraud_stats": FRAUD_STATS_PATH,
        "hourly_fraud": HOURLY_FRAUD_PATH,
        "amount_dist": AMT_DIST_PATH,
        "feature_importance": FEATURE_IMPORTANCE_PATH,
        "sample_transactions": SAMPLE_TRANSACTIONS_PATH,
        "model_inputs": MODEL_INPUT_PATH,
        "feature_schema": FEATURE_SCHEMA_PATH,
        "eda_summary": EDA_SUMMARY_PATH,
    }
    for name, path in checks.items():
        status[name] = path.exists()
    return status
