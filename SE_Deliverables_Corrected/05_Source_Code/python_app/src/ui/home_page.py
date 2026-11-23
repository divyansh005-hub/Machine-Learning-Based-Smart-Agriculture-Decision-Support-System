"""Home Dashboard page for AgriSmart."""

import json
from pathlib import Path
import streamlit as st
import pandas as pd

from src.ui.styles import render_hero, render_disclaimer
from src.utils.constants import MODELS_DIR, CROP_DATA_PATH, FERT_DATA_PATH, YIELD_DATA_PATH


def render_home_page():
    render_hero(
        title="AgriSmart — Smart Agriculture Decision Support System",
        subtitle="An intelligent pair of predictive machine learning modules assisting agronomists, farmers, and researchers with crop selection, nutrient planning, and regional yield forecasting.",
        badge="Academic Decision Support System",
    )

    # System Status & Artifact Verification
    st.subheader("System Architecture & Model Status")

    modules_status = [
        {
            "name": "Module A: Crop Recommendation",
            "type": "Multiclass Classification (22 Crops)",
            "icon": "🌾",
            "model_file": MODELS_DIR / "crop_recommendation.joblib",
            "meta_file": MODELS_DIR / "crop_recommendation_meta.json",
            "dataset_path": CROP_DATA_PATH,
            "page_target": "Crop Recommendation",
        },
        {
            "name": "Module B: Fertilizer Recommendation",
            "type": "Multiclass Classification (7 Formulations)",
            "icon": "🧪",
            "model_file": MODELS_DIR / "fertilizer_recommendation.joblib",
            "meta_file": MODELS_DIR / "fertilizer_recommendation_meta.json",
            "dataset_path": FERT_DATA_PATH,
            "page_target": "Fertilizer Recommendation",
        },
        {
            "name": "Module C: Crop Yield Prediction",
            "type": "Continuous Regression (hg/ha & tonnes/ha)",
            "icon": "📈",
            "model_file": MODELS_DIR / "yield_prediction.joblib",
            "meta_file": MODELS_DIR / "yield_prediction_meta.json",
            "dataset_path": YIELD_DATA_PATH,
            "page_target": "Crop Yield Prediction",
        },
    ]

    cols = st.columns(3)
    for idx, mod in enumerate(modules_status):
        with cols[idx]:
            is_trained = mod["model_file"].exists() and mod["meta_file"].exists()
            status_badge = '<span class="badge-active">● TRAINED & READY</span>' if is_trained else '<span style="color:#ef4444;font-weight:600;">● RETRAINING REQUIRED</span>'
            
            selected_model = "Not Trained"
            primary_metric = "N/A"
            train_test_info = "N/A"
            
            if is_trained:
                try:
                    with open(mod["meta_file"], "r", encoding="utf-8") as f:
                        meta = json.load(f)
                        selected_model = meta.get("selected_model", "Selected Pipeline")
                        m = meta.get("metrics", {})
                        if "macro_f1" in m:
                            primary_metric = f"Macro-F1: {m['macro_f1']:.4f} (Acc: {m['accuracy']:.4f})"
                        elif "rmse" in m:
                            primary_metric = f"RMSE: {m['rmse']:,.0f} hg/ha (R²: {m['r2']:.4f})"
                        train_test_info = f"Train: {meta.get('train_samples', 0):,} | Test: {meta.get('test_samples', 0):,}"
                except Exception:
                    pass

            st.markdown(
                f"""
                <div class="agrismart-card">
                    <div class="card-icon">{mod['icon']}</div>
                    <div class="card-title">{mod['name']}</div>
                    <div style="margin-bottom: 0.6rem;">{status_badge}</div>
                    <div class="card-desc"><strong>Type:</strong> {mod['type']}</div>
                    <div class="card-desc" style="margin-top:0.3rem;"><strong>Selected Model:</strong> {selected_model}</div>
                    <div class="card-desc" style="margin-top:0.3rem;"><strong>Held-Out Metric:</strong> {primary_metric}</div>
                    <div class="card-desc" style="margin-top:0.3rem;font-size:0.82rem;color:#94a3b8;">{train_test_info}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    
    # Verified Workspace Datasets Inventory
    st.subheader("Audited Workspace Datasets")
    d_col1, d_col2, d_col3, d_col4 = st.columns(4)
    
    with d_col1:
        st.metric(
            label="Crop Recommendation Data",
            value="2,200 Rows",
            help="Balanced 22 classes (100 samples each), 7 soil & climate features. 0 missing values."
        )
    with d_col2:
        st.metric(
            label="Fertilizer Recommendation Data",
            value="10,000 Rows",
            help="7 fertilizer classes (SSP rare: 1.8%), 12 numeric & 7 categorical features. 0 missing values."
        )
    with d_col3:
        st.metric(
            label="FAO Global Yield Data",
            value="25,932 Rows",
            help="Deduplicated FAO agricultural dataset across 101 countries, 10 crops, spanning 1990–2013."
        )
    with d_col4:
        st.metric(
            label="Temporal Horizon Split",
            value="2010–2013",
            help="Chronological held-out testing period (4,627 samples) strictly preserving future horizons."
        )

    # Key Architectural Principles
    st.markdown("### Decision Support Workflow")
    st.markdown(
        """
        1. **Crop Suitability Analysis:** Evaluate soil macronutrients (N-P-K), ambient temperature, humidity, pH, and precipitation to identify the most agronomically viable crop.
        2. **Targeted Nutrient Management:** Input soil chemistry parameters and crop developmental stage to recommend optimal chemical or organic fertilizer formulations with class-imbalance weighting.
        3. **Regional Yield Projection:** Forecast expected harvest productivity in hectograms/hectare and metric tonnes/hectare based on national agro-climatic indicators.
        """
    )

    render_disclaimer(
        "AgriSmart models provide empirical predictions based on historical FAO and agricultural training datasets. "
        "Recommendations are decision aids and should never supersede certified local soil testing or expert agronomic consultation."
    )
