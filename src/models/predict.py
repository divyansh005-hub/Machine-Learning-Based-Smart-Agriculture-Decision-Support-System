"""Production-ready inference engine with input validation, probability ranking, and safety checks."""

from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import joblib
import numpy as np
import pandas as pd

from src.utils.constants import (
    MODELS_DIR,
    CROP_FEATURES,
    CROP_FEATURE_RANGES,
    CROP_DESCRIPTIONS,
    FERT_NUM_FEATURES,
    FERT_CAT_FEATURES,
    FERT_FEATURE_RANGES,
    FERT_CATEGORIES,
    FERT_DESCRIPTIONS,
    YIELD_NUM_FEATURES,
    YIELD_CAT_FEATURES,
    YIELD_FEATURE_RANGES,
    HG_PER_HA_TO_TONNES_PER_HA,
    AGRONOMIC_DISCLAIMER_CROP,
    AGRONOMIC_DISCLAIMER_FERT,
    AGRONOMIC_DISCLAIMER_YIELD,
)


class InputValidationError(ValueError):
    """Raised when user input fails boundary or categorical validation."""
    pass


class ModelArtifactNotFoundError(FileNotFoundError):
    """Raised when a required trained model pipeline is missing."""
    pass


class CropPredictor:
    """Inference handler for Crop Recommendation Module."""

    def __init__(self, model_path: Optional[Path] = None):
        self.model_path = Path(model_path or (MODELS_DIR / "crop_recommendation.joblib"))
        self._pipeline = None

    @property
    def pipeline(self):
        if self._pipeline is None:
            if not self.model_path.exists():
                raise ModelArtifactNotFoundError(
                    f"Crop recommendation model artifact not found at {self.model_path}. "
                    "Please run 'python src/models/train.py' first."
                )
            self._pipeline = joblib.load(self.model_path)
        return self._pipeline

    def validate_inputs(self, inputs: Dict[str, Any]) -> Dict[str, float]:
        """Validate input ranges and types for crop recommendation."""
        cleaned = {}
        for feat in CROP_FEATURES:
            if feat not in inputs:
                raise InputValidationError(f"Missing required crop feature: '{feat}'")
            try:
                val = float(inputs[feat])
            except (ValueError, TypeError):
                raise InputValidationError(f"Feature '{feat}' must be numeric, got: {inputs[feat]}")

            cfg = CROP_FEATURE_RANGES[feat]
            # Generous safety boundaries (+- 50% outside training min/max)
            soft_min = cfg["min"] - 10.0
            soft_max = cfg["max"] + 50.0
            if not (soft_min <= val <= soft_max):
                raise InputValidationError(
                    f"Feature '{cfg['label']}' value {val} is outside acceptable range "
                    f"[{cfg['min']}, {cfg['max']}] {cfg['unit']}."
                )
            cleaned[feat] = val
        return cleaned

    def predict(self, inputs: Dict[str, Any], top_k: int = 3) -> Dict[str, Any]:
        """Run prediction with class probabilities and agronomic descriptions."""
        valid_inputs = self.validate_inputs(inputs)
        df_input = pd.DataFrame([valid_inputs])[CROP_FEATURES]

        pipe = self.pipeline
        pred_label = pipe.predict(df_input)[0]

        top_candidates = []
        confidence = None

        if hasattr(pipe, "predict_proba"):
            probs = pipe.predict_proba(df_input)[0]
            classes = pipe.classes_
            sorted_indices = np.argsort(probs)[::-1]
            confidence = float(probs[sorted_indices[0]])

            for idx in sorted_indices[:top_k]:
                cls_name = str(classes[idx])
                top_candidates.append({
                    "crop": cls_name,
                    "probability": round(float(probs[idx]), 4),
                    "confidence_pct": round(float(probs[idx]) * 100, 1),
                    "description": CROP_DESCRIPTIONS.get(cls_name, "Crop suitable for given agro-ecological conditions."),
                })

        return {
            "recommended_crop": pred_label,
            "confidence": confidence,
            "confidence_pct": round(confidence * 100, 1) if confidence else None,
            "description": CROP_DESCRIPTIONS.get(pred_label, "Crop suitable for provided conditions."),
            "top_candidates": top_candidates,
            "inputs": valid_inputs,
            "disclaimer": AGRONOMIC_DISCLAIMER_CROP,
        }


class FertilizerPredictor:
    """Inference handler for Fertilizer Recommendation Module."""

    def __init__(self, model_path: Optional[Path] = None):
        self.model_path = Path(model_path or (MODELS_DIR / "fertilizer_recommendation.joblib"))
        self._pipeline = None

    @property
    def pipeline(self):
        if self._pipeline is None:
            if not self.model_path.exists():
                raise ModelArtifactNotFoundError(
                    f"Fertilizer recommendation model artifact not found at {self.model_path}. "
                    "Please run 'python src/models/train.py' first."
                )
            self._pipeline = joblib.load(self.model_path)
        return self._pipeline

    def validate_inputs(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate numeric and categorical inputs for fertilizer recommendation."""
        cleaned = {}

        # Numeric validation
        for feat in FERT_NUM_FEATURES:
            if feat not in inputs:
                raise InputValidationError(f"Missing required numeric fertilizer feature: '{feat}'")
            try:
                val = float(inputs[feat])
            except (ValueError, TypeError):
                raise InputValidationError(f"Feature '{feat}' must be numeric, got: {inputs[feat]}")

            cfg = FERT_FEATURE_RANGES[feat]
            # Safety range boundaries
            if not (cfg["min"] * 0.5 <= val <= cfg["max"] * 1.5):
                raise InputValidationError(
                    f"Feature '{cfg['label']}' value {val} is outside acceptable range "
                    f"[{cfg['min']}, {cfg['max']}] {cfg['unit']}."
                )
            cleaned[feat] = val

        # Categorical validation
        for feat in FERT_CAT_FEATURES:
            if feat not in inputs:
                raise InputValidationError(f"Missing required categorical fertilizer feature: '{feat}'")
            val = str(inputs[feat]).strip()
            # Check against recognized categories
            valid_cats = FERT_CATEGORIES[feat]
            if val not in valid_cats:
                # If unknown category is supplied, raise friendly validation error
                raise InputValidationError(
                    f"Invalid category '{val}' for '{feat}'. Expected one of: {valid_cats}"
                )
            cleaned[feat] = val

        return cleaned

    def predict(self, inputs: Dict[str, Any], top_k: int = 3) -> Dict[str, Any]:
        """Run prediction with class probabilities and fertilizer descriptions."""
        valid_inputs = self.validate_inputs(inputs)
        feature_order = FERT_NUM_FEATURES + FERT_CAT_FEATURES
        df_input = pd.DataFrame([valid_inputs])[feature_order]

        pipe = self.pipeline
        pred_label = pipe.predict(df_input)[0]

        top_candidates = []
        confidence = None

        if hasattr(pipe, "predict_proba"):
            probs = pipe.predict_proba(df_input)[0]
            classes = pipe.classes_
            sorted_indices = np.argsort(probs)[::-1]
            confidence = float(probs[sorted_indices[0]])

            for idx in sorted_indices[:top_k]:
                cls_name = str(classes[idx])
                top_candidates.append({
                    "fertilizer": cls_name,
                    "probability": round(float(probs[idx]), 4),
                    "confidence_pct": round(float(probs[idx]) * 100, 1),
                    "description": FERT_DESCRIPTIONS.get(cls_name, "Agronomic fertilizer formulation."),
                })

        return {
            "recommended_fertilizer": pred_label,
            "confidence": confidence,
            "confidence_pct": round(confidence * 100, 1) if confidence else None,
            "description": FERT_DESCRIPTIONS.get(pred_label, "Agronomic fertilizer formulation."),
            "top_candidates": top_candidates,
            "inputs": valid_inputs,
            "disclaimer": AGRONOMIC_DISCLAIMER_FERT,
        }


class YieldPredictor:
    """Inference handler for Crop Yield Prediction Module."""

    def __init__(self, model_path: Optional[Path] = None):
        self.model_path = Path(model_path or (MODELS_DIR / "yield_prediction.joblib"))
        self._pipeline = None

    @property
    def pipeline(self):
        if self._pipeline is None:
            if not self.model_path.exists():
                raise ModelArtifactNotFoundError(
                    f"Yield prediction model artifact not found at {self.model_path}. "
                    "Please run 'python src/models/train.py' first."
                )
            self._pipeline = joblib.load(self.model_path)
        return self._pipeline

    def validate_inputs(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate inputs for crop yield prediction."""
        cleaned = {}

        # Categorical
        for feat in YIELD_CAT_FEATURES:
            if feat not in inputs:
                raise InputValidationError(f"Missing required categorical yield feature: '{feat}'")
            val = str(inputs[feat]).strip()
            if not val:
                raise InputValidationError(f"Yield feature '{feat}' cannot be empty.")
            cleaned[feat] = val

        # Numeric
        for feat in YIELD_NUM_FEATURES:
            if feat not in inputs:
                raise InputValidationError(f"Missing required numeric yield feature: '{feat}'")
            try:
                val = float(inputs[feat])
            except (ValueError, TypeError):
                raise InputValidationError(f"Feature '{feat}' must be numeric, got: {inputs[feat]}")

            cfg = YIELD_FEATURE_RANGES[feat]
            # Safety range boundaries
            if feat == "Year":
                if not (1960 <= val <= 2050):
                    raise InputValidationError(f"Year {val} is outside realistic range [1960, 2050].")
            else:
                if val < 0 and feat != "avg_temp":
                    raise InputValidationError(f"Feature '{feat}' cannot be negative, got {val}.")
            cleaned[feat] = val

        return cleaned

    def predict(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Predict crop yield in hg/ha and convert to tonnes/ha."""
        valid_inputs = self.validate_inputs(inputs)
        feature_order = YIELD_CAT_FEATURES + YIELD_NUM_FEATURES
        df_input = pd.DataFrame([valid_inputs])[feature_order]

        pipe = self.pipeline
        pred_raw = float(pipe.predict(df_input)[0])

        # Agronomic yield is non-negative
        pred_hg_ha = max(0.0, pred_raw)
        pred_tonnes_ha = pred_hg_ha * HG_PER_HA_TO_TONNES_PER_HA

        return {
            "predicted_yield_hg_ha": round(pred_hg_ha, 2),
            "predicted_yield_tonnes_ha": round(pred_tonnes_ha, 3),
            "target_unit": "hg/ha",
            "inputs": valid_inputs,
            "disclaimer": AGRONOMIC_DISCLAIMER_YIELD,
        }
