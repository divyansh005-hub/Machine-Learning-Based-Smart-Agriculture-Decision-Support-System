"""Data loading and schema validation routines for AgriSmart."""

from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd
import numpy as np

from src.utils.constants import (
    CROP_DATA_PATH,
    FERT_DATA_PATH,
    YIELD_DATA_PATH,
    CROP_FEATURES,
    CROP_TARGET,
    FERT_NUM_FEATURES,
    FERT_CAT_FEATURES,
    FERT_TARGET,
    YIELD_ALL_FEATURES,
    YIELD_TARGET,
)


class SchemaValidationError(ValueError):
    """Raised when dataset does not match expected schema."""
    pass


def load_crop_data(filepath: Optional[Path] = None) -> pd.DataFrame:
    """Load and validate the crop recommendation dataset.
    
    Args:
        filepath: Optional path to crop recommendation CSV. Defaults to CROP_DATA_PATH.
        
    Returns:
        pd.DataFrame: Clean validated DataFrame.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        SchemaValidationError: If required columns are missing.
    """
    path = Path(filepath or CROP_DATA_PATH)
    if not path.exists():
        raise FileNotFoundError(f"Crop dataset not found at {path}")
    
    df = pd.read_csv(path)
    expected_cols = set(CROP_FEATURES + [CROP_TARGET])
    actual_cols = set(df.columns)
    missing = expected_cols - actual_cols
    if missing:
        raise SchemaValidationError(f"Crop dataset is missing columns: {missing}")
    
    # Verify non-empty
    if len(df) == 0:
        raise SchemaValidationError("Crop dataset is empty.")
    
    # Validate types of features
    for col in CROP_FEATURES:
        if not np.issubdtype(df[col].dtype, np.number):
            raise SchemaValidationError(f"Expected numeric column for {col}, got {df[col].dtype}")
            
    return df[CROP_FEATURES + [CROP_TARGET]].copy()


def load_fertilizer_data(filepath: Optional[Path] = None) -> pd.DataFrame:
    """Load and validate the fertilizer recommendation dataset.
    
    Args:
        filepath: Optional path to fertilizer CSV. Defaults to FERT_DATA_PATH.
        
    Returns:
        pd.DataFrame: Clean validated DataFrame.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        SchemaValidationError: If required columns are missing.
    """
    path = Path(filepath or FERT_DATA_PATH)
    if not path.exists():
        raise FileNotFoundError(f"Fertilizer dataset not found at {path}")
        
    df = pd.read_csv(path)
    expected_cols = set(FERT_NUM_FEATURES + FERT_CAT_FEATURES + [FERT_TARGET])
    actual_cols = set(df.columns)
    missing = expected_cols - actual_cols
    if missing:
        raise SchemaValidationError(f"Fertilizer dataset is missing columns: {missing}")
        
    if len(df) == 0:
        raise SchemaValidationError("Fertilizer dataset is empty.")
        
    for col in FERT_NUM_FEATURES:
        if not np.issubdtype(df[col].dtype, np.number):
            raise SchemaValidationError(f"Expected numeric column for {col}, got {df[col].dtype}")
            
    return df[FERT_NUM_FEATURES + FERT_CAT_FEATURES + [FERT_TARGET]].copy()


def load_yield_data(
    filepath: Optional[Path] = None,
    deduplicate: bool = True,
    aggregate_stations: bool = False,
) -> pd.DataFrame:
    """Load and validate the FAO crop yield dataset.
    
    Args:
        filepath: Optional path to yield_df.csv. Defaults to YIELD_DATA_PATH.
        deduplicate: Whether to drop exact row duplicates (removes 2,310 duplicated rows).
        aggregate_stations: If True, aggregates multi-station temperature entries by
                            grouping on (Area, Item, Year) and taking the mean of avg_temp.
                            
    Returns:
        pd.DataFrame: Clean validated DataFrame.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        SchemaValidationError: If required columns are missing.
    """
    path = Path(filepath or YIELD_DATA_PATH)
    if not path.exists():
        raise FileNotFoundError(f"Yield dataset not found at {path}")
        
    df = pd.read_csv(path)
    
    # Drop serial index column if present
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])
        
    expected_cols = set(YIELD_ALL_FEATURES + [YIELD_TARGET])
    actual_cols = set(df.columns)
    missing = expected_cols - actual_cols
    if missing:
        raise SchemaValidationError(f"Yield dataset is missing columns: {missing}")
        
    if deduplicate:
        df = df.drop_duplicates().copy()
        
    if aggregate_stations:
        # Group by Area, Item, Year, hg/ha_yield, average_rain_fall_mm_per_year, pesticides_tonnes
        # and average avg_temp across weather stations
        df = (
            df.groupby(
                ["Area", "Item", "Year", "hg/ha_yield", "average_rain_fall_mm_per_year", "pesticides_tonnes"],
                as_index=False
            )["avg_temp"]
            .mean()
        )
        
    # Reorder columns consistently
    cols = ["Area", "Item", "Year", "average_rain_fall_mm_per_year", "pesticides_tonnes", "avg_temp", "hg/ha_yield"]
    return df[cols].copy()


def get_dataset_summary(df: pd.DataFrame, name: str) -> Dict[str, Any]:
    """Compute summary statistics and metadata for a DataFrame.
    
    Args:
        df: The pandas DataFrame.
        name: Name of the dataset.
        
    Returns:
        Dict[str, Any]: Dictionary containing shape, null count, duplicates, columns, and types.
    """
    return {
        "dataset_name": name,
        "rows": int(len(df)),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "missing_values_total": int(df.isnull().sum().sum()),
        "missing_by_column": {k: int(v) for k, v in df.isnull().sum().items()},
        "exact_duplicates": int(df.duplicated().sum()),
        "memory_mb": round(float(df.memory_usage(deep=True).sum() / (1024 * 1024)), 2),
    }
