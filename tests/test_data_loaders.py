"""Unit tests for data loaders and schema validation."""

import pytest
import pandas as pd
from pathlib import Path

from src.data.loaders import (
    load_crop_data,
    load_fertilizer_data,
    load_yield_data,
    get_dataset_summary,
    SchemaValidationError,
)
from src.utils.constants import (
    CROP_FEATURES,
    CROP_TARGET,
    FERT_NUM_FEATURES,
    FERT_CAT_FEATURES,
    FERT_TARGET,
    YIELD_ALL_FEATURES,
    YIELD_TARGET,
)


def test_load_crop_data():
    df = load_crop_data()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2200
    assert df.shape[1] == len(CROP_FEATURES) + 1
    assert CROP_TARGET in df.columns
    assert df.isnull().sum().sum() == 0
    assert df[CROP_TARGET].nunique() == 22


def test_load_fertilizer_data():
    df = load_fertilizer_data()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10000
    assert df.shape[1] == len(FERT_NUM_FEATURES) + len(FERT_CAT_FEATURES) + 1
    assert FERT_TARGET in df.columns
    assert df.isnull().sum().sum() == 0
    assert df[FERT_TARGET].nunique() == 7


def test_load_yield_data_deduplication():
    # Without deduplication vs with deduplication
    df_dedup = load_yield_data(deduplicate=True)
    assert isinstance(df_dedup, pd.DataFrame)
    assert len(df_dedup) == 25932
    assert YIELD_TARGET in df_dedup.columns
    assert "Area" in df_dedup.columns
    assert "Item" in df_dedup.columns


def test_load_yield_data_aggregation():
    df_agg = load_yield_data(deduplicate=True, aggregate_stations=True)
    assert isinstance(df_agg, pd.DataFrame)
    assert len(df_agg) == 13130
    assert df_agg.duplicated(subset=["Area", "Item", "Year"]).sum() == 0


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        load_crop_data(filepath=Path("non_existent_file.csv"))


def test_invalid_schema_raises(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    pd.DataFrame({"invalid_col": [1, 2, 3]}).to_csv(bad_csv, index=False)
    with pytest.raises(SchemaValidationError):
        load_crop_data(filepath=bad_csv)


def test_dataset_summary():
    df = load_crop_data()
    summary = get_dataset_summary(df, "Crop Dataset")
    assert summary["rows"] == 2200
    assert summary["missing_values_total"] == 0
    assert summary["exact_duplicates"] == 0
