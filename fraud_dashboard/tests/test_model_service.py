import pytest
import pandas as pd
from unittest.mock import patch
from src.model_service import prepare_features, get_precomputed_probability


def test_prepare_features_reorders():
    schema = {
        "feature_names": ["b", "a", "c"],
        "n_features": 3,
    }
    df = pd.DataFrame({"a": [1], "b": [2], "c": [3]})

    with patch("src.model_service.load_feature_schema", return_value=schema):
        result = prepare_features(df)
        assert list(result.columns) == ["b", "a", "c"]


def test_prepare_features_adds_missing():
    schema = {
        "feature_names": ["a", "b", "c", "d"],
        "n_features": 4,
    }
    df = pd.DataFrame({"a": [1], "c": [3]})

    with patch("src.model_service.load_feature_schema", return_value=schema):
        result = prepare_features(df)
        assert list(result.columns) == ["a", "b", "c", "d"]
        assert result.iloc[0]["b"] == 0
        assert result.iloc[0]["d"] == 0


def test_prepare_features_no_schema():
    df = pd.DataFrame({"x": [1], "y": [2]})
    with patch("src.model_service.load_feature_schema", return_value={}):
        result = prepare_features(df)
        assert list(result.columns) == ["x", "y"]


def test_get_precomputed_probability():
    row = pd.Series({"fraud_probability": 0.85, "other": 123})
    assert get_precomputed_probability(row) == 0.85


def test_get_precomputed_probability_missing():
    row = pd.Series({"other": 123})
    assert get_precomputed_probability(row) == -1.0
