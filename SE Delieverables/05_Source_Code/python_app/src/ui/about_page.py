"""About and Project Limitations Page for AgriSmart."""

import streamlit as st
from src.ui.styles import render_hero, render_disclaimer


def render_about_page():
    render_hero(
        title="About AgriSmart & Project Limitations",
        subtitle="Academic architecture, machine learning engineering methodology, dataset provenance, and responsible agronomic deployment guidelines.",
        badge="Documentation & Governance",
    )

    st.markdown("### 1. Project Objectives & Academic Scope")
    st.markdown(
        """
        The **Machine Learning Based Smart Agriculture Decision Support System (AgriSmart)** is designed as an integrated 
        computational suite bridging predictive machine learning algorithms with agricultural management challenges.
        The project addresses three fundamental agricultural decisions:
        
        - **Module A (Crop Recommendation):** Multi-class botanical classification predicting the most physiologically compatible crop for a given parcel's soil macronutrients (N-P-K), pH, and climate regime.
        - **Module B (Fertilizer Recommendation):** Multi-class agronomic classification proposing chemical and organic nutrient interventions to alleviate detected nutrient deficits during critical growth stages.
        - **Module C (Crop Yield Prediction):** Non-linear temporal regression estimating harvest yields per unit area to assist national food security planning and farm economic risk analysis.
        """
    )

    st.markdown("---")

    st.markdown("### 2. Machine Learning Methodology")
    st.markdown(
        """
        - **Strict Train/Test Isolation:** All data scaling, one-hot category encoding, and frequency transformations are fitted exclusively on training splits. No test or validation information leaks into transformer states.
        - **Appropriate Partitioning Strategies:**
          - *Module A:* Stratified 80:20 split (`random_state=42`) ensuring balanced 20-sample representation per crop in the held-out test set.
          - *Module B:* Stratified 80:20 split (`random_state=42`) paired with cost-sensitive class weighting (`class_weight='balanced'`) to protect rare classes (SSP: 1.8%).
          - *Module C:* Chronological split (Training: 1990–2009; Held-out Test: 2010–2013) preventing future temporal leakage and reflecting real-world forward forecasting conditions.
        - **Empirical Baseline Anchors:**
          - DummyClassifier (most frequent strategy) establishes the minimal zero-information benchmark for classification tasks.
          - Mean-yield DummyRegressor anchored on historical training data establishes the regression baseline.
        - **Model Selection Protocol:** Selections are determined strictly by measured held-out generalization metrics (Macro-F1 for classification, RMSE for regression), never by heuristic assumptions.
        """
    )

    st.markdown("---")

    st.markdown("### 3. Data Provenance & Metadata")
    st.markdown(
        """
        - **Crop Recommendation:** Benchmark precision agriculture dataset compiled by the Indian Council of Agricultural Research (ICAR) & Kaggle open data initiatives, documenting empirical physiological growth bounds across 22 crops.
        - **Fertilizer Recommendation:** Agronomic nutrient decision dataset modeling soil chemical indices (pH, EC, Organic Carbon), macronutrients, and crop phenological stages.
        - **Global Crop Yield:** Food and Agriculture Organization of the United Nations (FAOSTAT) agricultural production database merged with World Meteorological Organization surface temperature and precipitation records (1990–2013).
        """
    )

    st.markdown("---")

    st.markdown("### 4. Known Limitations & Responsible Use Statement")
    st.markdown(
        """
        1. **Regional vs Parcel Scale:** Module C yield predictions are calibrated on country-level FAO aggregates. They do not capture micro-topography, pest infestations, frost pockets, or farm-specific management variations.
        2. **Synthetic Boundary Semantics:** Module B dataset targets reflect algorithmic decision boundaries rather than certified multi-year agronomic trial results.
        3. **Advisory Role:** AgriSmart is intended exclusively as a computerized decision support system. It must never replace official agricultural extension services, soil testing laboratory analyses, or certified agronomist recommendations.
        """
    )

    render_disclaimer(
        "AgriSmart models provide predictive approximations based on historical data. "
        "The software is provided for research and academic decision-support purposes without warranty of any kind."
    )
