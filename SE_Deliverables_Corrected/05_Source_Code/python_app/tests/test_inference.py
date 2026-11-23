"""Unit tests for inference classes, validation, and error handling."""

import pytest
from pathlib import Path

from src.models.predict import (
    CropPredictor,
    FertilizerPredictor,
    YieldPredictor,
    InputValidationError,
    ModelArtifactNotFoundError,
)


def test_crop_predictor_valid():
    predictor = CropPredictor()
    inputs = {
        "N": 90.0,
        "P": 42.0,
        "K": 43.0,
        "temperature": 20.8,
        "humidity": 82.0,
        "ph": 6.5,
        "rainfall": 202.9,
    }
    result = predictor.predict(inputs)
    assert "recommended_crop" in result
    assert result["recommended_crop"] == "rice"
    assert "top_candidates" in result
    assert len(result["top_candidates"]) == 3
    assert result["confidence"] is not None
    assert result["confidence"] > 0.5
    assert "disclaimer" in result


def test_crop_predictor_missing_feature():
    predictor = CropPredictor()
    inputs = {
        "N": 90.0,
        "P": 42.0,
        # missing K
        "temperature": 20.8,
        "humidity": 82.0,
        "ph": 6.5,
        "rainfall": 202.9,
    }
    with pytest.raises(InputValidationError, match="Missing required crop feature"):
        predictor.predict(inputs)


def test_crop_predictor_out_of_range():
    predictor = CropPredictor()
    inputs = {
        "N": 9999.0,  # Invalid extreme
        "P": 42.0,
        "K": 43.0,
        "temperature": 20.8,
        "humidity": 82.0,
        "ph": 6.5,
        "rainfall": 202.9,
    }
    with pytest.raises(InputValidationError, match="outside acceptable range"):
        predictor.predict(inputs)


def test_fertilizer_predictor_valid():
    predictor = FertilizerPredictor()
    inputs = {
        "Soil_pH": 6.07,
        "Soil_Moisture": 35.0,
        "Organic_Carbon": 0.85,
        "Electrical_Conductivity": 1.5,
        "Nitrogen_Level": 35,  # Deficient nitrogen -> expect Urea
        "Phosphorus_Level": 65,
        "Potassium_Level": 78,
        "Temperature": 25.0,
        "Humidity": 60.0,
        "Rainfall": 1500.0,
        "Fertilizer_Used_Last_Season": 175.0,
        "Yield_Last_Season": 4.5,
        "Soil_Type": "Clay",
        "Crop_Type": "Wheat",
        "Crop_Growth_Stage": "Vegetative",
        "Season": "Rabi",
        "Irrigation_Type": "Canal",
        "Previous_Crop": "Rice",
        "Region": "North",
    }
    result = predictor.predict(inputs)
    assert "recommended_fertilizer" in result
    assert result["recommended_fertilizer"] in ["Urea", "DAP", "MOP", "NPK", "Compost", "Zinc Sulphate", "SSP"]
    assert len(result["top_candidates"]) == 3
    assert result["confidence"] is not None
    assert "disclaimer" in result


def test_fertilizer_predictor_invalid_category():
    predictor = FertilizerPredictor()
    inputs = {
        "Soil_pH": 6.5,
        "Soil_Moisture": 35.0,
        "Organic_Carbon": 0.85,
        "Electrical_Conductivity": 1.5,
        "Nitrogen_Level": 100,
        "Phosphorus_Level": 50,
        "Potassium_Level": 60,
        "Temperature": 25.0,
        "Humidity": 60.0,
        "Rainfall": 1500.0,
        "Fertilizer_Used_Last_Season": 175.0,
        "Yield_Last_Season": 4.5,
        "Soil_Type": "Martian_Regolith",  # Invalid category
        "Crop_Type": "Wheat",
        "Crop_Growth_Stage": "Vegetative",
        "Season": "Rabi",
        "Irrigation_Type": "Canal",
        "Previous_Crop": "Rice",
        "Region": "North",
    }
    with pytest.raises(InputValidationError, match="Invalid category"):
        predictor.predict(inputs)


def test_yield_predictor_valid():
    predictor = YieldPredictor()
    inputs = {
        "Area": "India",
        "Item": "Wheat",
        "Year": 2013,
        "average_rain_fall_mm_per_year": 1083.0,
        "pesticides_tonnes": 50000.0,
        "avg_temp": 24.5,
    }
    result = predictor.predict(inputs)
    assert "predicted_yield_hg_ha" in result
    assert "predicted_yield_tonnes_ha" in result
    assert result["predicted_yield_hg_ha"] > 0
    assert result["predicted_yield_tonnes_ha"] > 0
    # Verified conversion check: tonnes/ha should equal hg/ha / 10000.0 rounded to 3 decimal places
    expected_tonnes = round(result["predicted_yield_hg_ha"] / 10000.0, 3)
    assert result["predicted_yield_tonnes_ha"] == expected_tonnes


def test_yield_predictor_unseen_area():
    predictor = YieldPredictor()
    # Test Sudan (which appears only in post-2009 data)
    inputs = {
        "Area": "Sudan",
        "Item": "Sorghum",
        "Year": 2013,
        "average_rain_fall_mm_per_year": 400.0,
        "pesticides_tonnes": 120.0,
        "avg_temp": 28.5,
    }
    result = predictor.predict(inputs)
    assert result["predicted_yield_hg_ha"] > 0


def test_missing_model_artifact_raises():
    fake_path = Path("models/non_existent_model.joblib")
    predictor = CropPredictor(model_path=fake_path)
    with pytest.raises(ModelArtifactNotFoundError):
        predictor.predict({
            "N": 50.0, "P": 50.0, "K": 50.0,
            "temperature": 25.0, "humidity": 70.0,
            "ph": 6.5, "rainfall": 100.0,
        })
