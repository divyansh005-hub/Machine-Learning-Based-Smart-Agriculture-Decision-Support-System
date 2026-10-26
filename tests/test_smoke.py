"""Smoke tests for artifacts, reports, and modules."""

import json
from pathlib import Path
import pandas as pd

from src.utils.constants import MODELS_DIR, REPORTS_DIR


def test_model_artifacts_exist():
    assert (MODELS_DIR / "crop_recommendation.joblib").exists()
    assert (MODELS_DIR / "crop_recommendation_meta.json").exists()
    assert (MODELS_DIR / "fertilizer_recommendation.joblib").exists()
    assert (MODELS_DIR / "fertilizer_recommendation_meta.json").exists()
    assert (MODELS_DIR / "yield_prediction.joblib").exists()
    assert (MODELS_DIR / "yield_prediction_meta.json").exists()


def test_reports_exist_and_valid():
    csv_path = REPORTS_DIR / "model_comparison.csv"
    assert csv_path.exists()
    df = pd.read_csv(csv_path)
    assert len(df) >= 7
    assert "Module" in df.columns
    assert "Is_Selected" in df.columns
    # Ensure selected model exists for each module
    selected = df[df["Is_Selected"] == True]
    assert len(selected) == 3

    md_path = REPORTS_DIR / "MODEL_EVALUATION.md"
    assert md_path.exists()
    content = md_path.read_text(encoding="utf-8")
    assert "MODEL EVALUATION & BENCHMARK REPORT" in content
    assert "Crop Recommendation" in content
    assert "Fertilizer Recommendation" in content
    assert "Crop Yield Prediction" in content


def test_metadata_json_structure():
    for name in ["crop_recommendation_meta.json", "fertilizer_recommendation_meta.json", "yield_prediction_meta.json"]:
        path = MODELS_DIR / name
        assert path.exists()
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert "module" in data
            assert "selected_model" in data
            assert "metrics" in data
