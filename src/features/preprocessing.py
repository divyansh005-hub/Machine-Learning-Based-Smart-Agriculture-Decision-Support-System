"""Preprocessing pipelines and transformer builders for AgriSmart."""

from typing import List, Optional
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline

from src.utils.constants import (
    CROP_FEATURES,
    FERT_NUM_FEATURES,
    FERT_CAT_FEATURES,
    YIELD_NUM_FEATURES,
    YIELD_CAT_FEATURES,
)


def build_crop_preprocessor(use_scaler: bool = True) -> ColumnTransformer:
    """Build preprocessing transformer for crop recommendation features.
    
    Args:
        use_scaler: If True, applies StandardScaler to all numeric features.
        
    Returns:
        ColumnTransformer: Fitted or unfitted transformer.
    """
    if use_scaler:
        num_trans = StandardScaler()
    else:
        num_trans = "passthrough"
        
    return ColumnTransformer(
        transformers=[
            ("num", num_trans, CROP_FEATURES),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )


def build_fertilizer_preprocessor(use_scaler: bool = True) -> ColumnTransformer:
    """Build preprocessing transformer for fertilizer recommendation features.
    
    Handles both numeric scaling and one-hot encoding of categorical features
    with unknown category handling for production safety.
    
    Args:
        use_scaler: If True, scales numeric columns with StandardScaler.
        
    Returns:
        ColumnTransformer: Preprocessor for fertilizer inputs.
    """
    num_trans = StandardScaler() if use_scaler else "passthrough"
    cat_trans = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    
    return ColumnTransformer(
        transformers=[
            ("num", num_trans, FERT_NUM_FEATURES),
            ("cat", cat_trans, FERT_CAT_FEATURES),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )


def build_yield_preprocessor(use_scaler: bool = True) -> ColumnTransformer:
    """Build preprocessing transformer for crop yield prediction features.
    
    Encodes 'Area' (Country) and 'Item' (Crop) via OneHotEncoder with handle_unknown='ignore',
    safely handling unseen regions such as 'Sudan' in post-2009 periods or in inference.
    
    Args:
        use_scaler: If True, scales numeric features (rainfall, pesticides, temperature, year).
        
    Returns:
        ColumnTransformer: Preprocessor for yield inputs.
    """
    num_trans = StandardScaler() if use_scaler else "passthrough"
    cat_trans = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    
    return ColumnTransformer(
        transformers=[
            ("num", num_trans, YIELD_NUM_FEATURES),
            ("cat", cat_trans, YIELD_CAT_FEATURES),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )
