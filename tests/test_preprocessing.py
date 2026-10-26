"""Unit tests for feature preprocessing pipelines."""

import numpy as np
import pandas as pd
from src.features.preprocessing import (
    build_crop_preprocessor,
    build_fertilizer_preprocessor,
    build_yield_preprocessor,
)
from src.data.loaders import load_crop_data, load_fertilizer_data, load_yield_data
from src.utils.constants import CROP_FEATURES, FERT_NUM_FEATURES, FERT_CAT_FEATURES, YIELD_CAT_FEATURES, YIELD_NUM_FEATURES


def test_crop_preprocessor():
    df = load_crop_data()
    X = df[CROP_FEATURES]
    prep = build_crop_preprocessor(use_scaler=True)
    transformed = prep.fit_transform(X)
    assert transformed.shape == (2200, 7)
    # Check zero mean, unit variance
    np.testing.assert_almost_equal(transformed.mean(axis=0), np.zeros(7), decimal=1)


def test_fertilizer_preprocessor_with_unknown_categories():
    df = load_fertilizer_data()
    features = FERT_NUM_FEATURES + FERT_CAT_FEATURES
    X = df[features]
    prep = build_fertilizer_preprocessor(use_scaler=True)
    prep.fit(X)

    # Test unknown category in evaluation/inference does not crash
    test_sample = X.iloc[[0]].copy()
    test_sample.loc[0, "Soil_Type"] = "Volcanic_Ash_Unknown"
    test_sample.loc[0, "Region"] = "Outer_Space_Unknown"
    
    transformed = prep.transform(test_sample)
    assert transformed.shape[0] == 1
    assert not np.isnan(transformed).any()


def test_yield_preprocessor_with_unseen_area():
    df = load_yield_data(deduplicate=True)
    features = YIELD_CAT_FEATURES + YIELD_NUM_FEATURES
    X = df[features]
    prep = build_yield_preprocessor(use_scaler=True)
    prep.fit(X)

    # Test an unseen area such as 'Atlantis'
    test_sample = pd.DataFrame([{
        "Area": "Atlantis_Fictional_Country",
        "Item": "Wheat",
        "Year": 2025,
        "average_rain_fall_mm_per_year": 1200.0,
        "pesticides_tonnes": 150.0,
        "avg_temp": 20.5,
    }])
    transformed = prep.transform(test_sample)
    assert transformed.shape[0] == 1
    assert not np.isnan(transformed).any()
