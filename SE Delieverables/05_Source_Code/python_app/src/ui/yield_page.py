"""Crop Yield Prediction UI Page for AgriSmart."""

import streamlit as st
import pandas as pd

from src.ui.styles import render_hero, render_disclaimer
from src.models.predict import YieldPredictor, InputValidationError, ModelArtifactNotFoundError
from src.data.loaders import load_yield_data


@st.cache_data
def get_yield_dataset_options():
    """Retrieve distinct Areas and Items from verified FAO yield data."""
    try:
        df = load_yield_data(deduplicate=True)
        areas = sorted(df["Area"].unique().tolist())
        items = sorted(df["Item"].unique().tolist())
        return areas, items
    except Exception:
        fallback_areas = ["India", "United States of America", "Brazil", "China", "France", "Australia"]
        fallback_items = ["Wheat", "Maize", "Rice, paddy", "Potatoes", "Soybeans"]
        return fallback_areas, fallback_items


def render_yield_page():
    render_hero(
        title="Module C: Crop Yield Prediction",
        subtitle="Continuous machine learning regression forecasting agricultural crop yields across global agro-climatic zones, calibrated on 24 years of historical FAO records.",
        badge="Module C • Temporal Regression",
    )

    areas, items = get_yield_dataset_options()

    st.markdown("### Agricultural Production Parameters")
    st.info("💡 Select the country/region, crop type, and macroeconomic agronomic inputs to project expected harvest yields.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Geographic & Crop Selection")
        default_area_idx = areas.index("India") if "India" in areas else 0
        area = st.selectbox("Country / Area", options=areas, index=default_area_idx, help="National jurisdiction based on FAO statistics.")
        
        default_item_idx = items.index("Wheat") if "Wheat" in items else 0
        item = st.selectbox("Crop Type (Item)", options=items, index=default_item_idx, help="Crop category recorded by FAOSTAT.")

        year = st.slider(
            "Harvest Year",
            min_value=1990,
            max_value=2030,
            value=2013,
            step=1,
            help="Target projection year (training baseline: 1990–2009; held-out test horizon: 2010–2013)."
        )

    with col2:
        st.markdown("#### Climatic & Input Intensification")
        rainfall = st.number_input(
            "Average Annual Rainfall (mm/year)",
            min_value=50.0,
            max_value=3500.0,
            value=1083.0,
            step=50.0,
            help="National mean annual precipitation."
        )

        pesticides = st.number_input(
            "Total National Pesticide Usage (tonnes)",
            min_value=0.0,
            max_value=370000.0,
            value=45000.0,
            step=1000.0,
            help="Cumulative annual pesticide active ingredient application."
        )

        temp = st.number_input(
            "Average Surface Temperature (°C)",
            min_value=1.0,
            max_value=32.0,
            value=24.5,
            step=0.2,
            help="National mean surface air temperature."
        )

    st.markdown("---")

    predict_btn = st.button("📈 Predict Crop Yield", type="primary", use_container_width=True)

    if predict_btn:
        inputs = {
            "Area": area,
            "Item": item,
            "Year": year,
            "average_rain_fall_mm_per_year": rainfall,
            "pesticides_tonnes": pesticides,
            "avg_temp": temp,
        }

        try:
            predictor = YieldPredictor()
            result = predictor.predict(inputs)

            yield_hg = result["predicted_yield_hg_ha"]
            yield_tonnes = result["predicted_yield_tonnes_ha"]

            st.markdown(
                f"""
                <div class="prediction-box">
                    <div class="prediction-label">Projected Agricultural Yield</div>
                    <div class="prediction-value">{yield_tonnes:,.2f} Tonnes / Hectare</div>
                    <div class="prediction-subtext"><strong>Native Verified FAO Unit:</strong> {yield_hg:,.0f} hg/ha (hectograms per hectare)</div>
                    <div style="font-size:0.85rem;color:#475569;margin-top:0.6rem;">
                        Exact Unit Conversion: 1 hg = 0.1 kg &nbsp;•&nbsp; 10,000 hg/ha = 1.000 metric tonne/ha
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Contextual benchmark comparison
            b1, b2, b3 = st.columns(3)
            with b1:
                st.metric("Crop Specimen", item)
            with b2:
                st.metric("Geographic Territory", area)
            with b3:
                st.metric("Projection Horizon", f"Year {year}")

            render_disclaimer(result["disclaimer"])

        except InputValidationError as e:
            st.error(f"Input Validation Error: {e}")
        except ModelArtifactNotFoundError as e:
            st.error(f"Model Artifact Error: {e}")
        except Exception as e:
            st.error(f"Unexpected prediction error: {e}")
