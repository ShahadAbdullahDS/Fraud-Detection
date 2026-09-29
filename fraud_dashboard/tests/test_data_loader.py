import pytest
import pandas as pd
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch
from src.data_loader import (
    load_json, load_csv, get_display_df,
    get_model_input_for_sample, validate_data_available,
)


def test_load_json_missing_file():
    result = load_json(Path("/nonexistent/path.json"))
    assert result == {}


def test_load_csv_missing_file():
    result = load_csv(Path("/nonexistent/path.csv"))
    assert isinstance(result, pd.DataFrame)
    assert result.empty


def test_load_json_valid(tmp_path):
    data = {"f1": 0.58, "auc": 0.93}
    p = tmp_path / "metrics.json"
    p.write_text(json.dumps(data))
    result = load_json.__wrapped__(p)
    assert result["f1"] == 0.58
    assert result["auc"] == 0.93


def test_get_display_df_filters_columns():
    df = pd.DataFrame({
        "sample_id": [1, 2],
        "TransactionAmt": [100.0, 200.0],
        "hour": [3, 14],
        "V1": [0.5, 0.3],
        "V2": [1.2, 0.8],
        "card4": ["visa", "mastercard"],
    })
    display = get_display_df(df)
    assert "sample_id" in display.columns
    assert "TransactionAmt" in display.columns
    assert "card4" in display.columns
    assert "V1" not in display.columns
    assert "V2" not in display.columns


def test_get_display_df_empty():
    df = pd.DataFrame()
    result = get_display_df(df)
    assert result.empty


def test_get_model_input_matches_sample_id():
    inputs = pd.DataFrame({
        "sample_id": [1, 2, 3],
        "feature_a": [0.1, 0.2, 0.3],
        "feature_b": [1.0, 2.0, 3.0],
    })
    result = get_model_input_for_sample(2, inputs)
    assert not result.empty
    assert "sample_id" not in result.columns
    assert result.iloc[0]["feature_a"] == 0.2


def test_get_model_input_missing_id():
    inputs = pd.DataFrame({
        "sample_id": [1, 2],
        "feature_a": [0.1, 0.2],
    })
    result = get_model_input_for_sample(99, inputs)
    assert result.empty
