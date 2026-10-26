"""Fertilizer Recommendation UI Page for AgriSmart."""

import streamlit as st
import plotly.express as px
import pandas as pd

from src.ui.styles import render_hero, render_disclaimer
from src.models.predict import FertilizerPredictor, InputValidationError, ModelArtifactNotFoundError
from src.utils.constants import FERT_CATEGORIES, FERT_FEATURE_RANGES, FERT_DESCRIPTIONS


def render_fertilizer_page():
    render_hero(
        title="Module B: Fertilizer Recommendation",
        subtitle="Multiclass predictive nutrient management recommending chemical and organic fertilizers tailored to soil chemical deficiencies, crop growth stage, and antecedent field history.",
        badge="Module B • Imbalance-Trained Classifier",
    )

    st.markdown("### Field & Soil Profile Configuration")
    st.info("💡 Enter your soil laboratory analysis, crop type, and management history below. Features are grouped into intuitive categories.")

    tab_soil, tab_crop, tab_history = st.tabs(["🧪 Soil Chemical Properties", "🌱 Crop & Environment", "📜 Field History & Management"])

    with tab_soil:
        c1, c2, c3 = st.columns(3)
        with c1:
            soil_type = st.selectbox("Soil Type", options=FERT_CATEGORIES["Soil_Type"], index=1)
            soil_ph = st.number_input("Soil pH", min_value=4.5, max_value=8.5, value=6.5, step=0.1, help="Acidic (<6.0), Neutral (6.0-7.5), Alkaline (>7.5).")
            soil_moist = st.number_input("Soil Moisture (%)", min_value=10.0, max_value=60.0, value=35.0, step=1.0)
            org_carbon = st.number_input("Organic Carbon (%)", min_value=0.2, max_value=1.5, value=0.85, step=0.05)
        with c2:
            ec = st.number_input("Electrical Conductivity (dS/m)", min_value=0.1, max_value=3.0, value=1.5, step=0.1, help="Salinity indicator.")
            n_level = st.number_input("Nitrogen Level (kg/ha)", min_value=20.0, max_value=160.0, value=108.0, step=2.0)
            p_level = st.number_input("Phosphorus Level (kg/ha)", min_value=10.0, max_value=90.0, value=64.0, step=1.0)
            k_level = st.number_input("Potassium Level (kg/ha)", min_value=10.0, max_value=120.0, value=78.0, step=1.0)
        with c3:
            st.markdown(
                """
                <div style="background:#f8fafc;padding:1rem;border-radius:10px;border:1px solid #e2e8f0;font-size:0.85rem;color:#475569;">
                    <strong>Nutrient Reference Thresholds:</strong><br>
                    • Low Nitrogen (< 50 kg/ha) → Urea deficiency pattern<br>
                    • Low Phosphorus (< 35 kg/ha) → DAP deficiency pattern<br>
                    • Low Potassium (< 40 kg/ha) → MOP deficiency pattern<br>
                    • Acidic Soil (pH < 5.8) → Compost remediation<br>
                    • Alkaline Soil (pH > 7.5) → Zinc Sulphate micronutrient
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab_crop:
        cc1, cc2 = st.columns(2)
        with cc1:
            crop_type = st.selectbox("Current Crop Type", options=FERT_CATEGORIES["Crop_Type"], index=6)
            growth_stage = st.selectbox("Crop Growth Stage", options=FERT_CATEGORIES["Crop_Growth_Stage"], index=1)
            season = st.selectbox("Current Cropping Season", options=FERT_CATEGORIES["Season"], index=1)
            irrigation = st.selectbox("Irrigation System", options=FERT_CATEGORIES["Irrigation_Type"], index=0)
        with cc2:
            temp = st.number_input("Ambient Temperature (°C)", min_value=10.0, max_value=40.0, value=25.0, step=0.5)
            humidity = st.number_input("Relative Humidity (%)", min_value=30.0, max_value=90.0, value=60.0, step=1.0)
            rainfall = st.number_input("Annual Rainfall (mm)", min_value=200.0, max_value=3000.0, value=1580.0, step=20.0)
            region = st.selectbox("Geographic Region", options=FERT_CATEGORIES["Region"], index=2)

    with tab_history:
        h1, h2 = st.columns(2)
        with h1:
            prev_crop = st.selectbox("Previous Season Crop", options=FERT_CATEGORIES["Previous_Crop"], index=3)
            fert_last_season = st.number_input("Fertilizer Applied Last Season (kg/ha)", min_value=50.0, max_value=300.0, value=175.0, step=5.0)
        with h2:
            yield_last_season = st.number_input("Yield Achieved Last Season (tonnes/ha)", min_value=1.0, max_value=8.0, value=4.5, step=0.25)

    st.markdown("---")

    predict_btn = st.button("🧪 Predict Fertilizer Formulation", type="primary", use_container_width=True)

    if predict_btn:
        inputs = {
            "Soil_Type": soil_type,
            "Soil_pH": soil_ph,
            "Soil_Moisture": soil_moist,
            "Organic_Carbon": org_carbon,
            "Electrical_Conductivity": ec,
            "Nitrogen_Level": n_level,
            "Phosphorus_Level": p_level,
            "Potassium_Level": k_level,
            "Temperature": temp,
            "Humidity": humidity,
            "Rainfall": rainfall,
            "Crop_Type": crop_type,
            "Crop_Growth_Stage": growth_stage,
            "Season": season,
            "Irrigation_Type": irrigation,
            "Previous_Crop": prev_crop,
            "Region": region,
            "Fertilizer_Used_Last_Season": fert_last_season,
            "Yield_Last_Season": yield_last_season,
        }

        try:
            predictor = FertilizerPredictor()
            result = predictor.predict(inputs, top_k=3)

            rec_fert = result["recommended_fertilizer"]
            conf = result["confidence_pct"]
            fert_desc = result["description"]

            st.markdown(
                f"""
                <div class="prediction-box">
                    <div class="prediction-label">Recommended Nutrient Formulation</div>
                    <div class="prediction-value">{rec_fert}</div>
                    <div class="prediction-subtext"><strong>Estimated Confidence:</strong> {conf:.1f}%</div>
                    <p style="margin-top: 1rem; color: #1e293b; max-width: 600px; margin-left: auto; margin-right: auto;">
                        {fert_desc}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Top Candidates Visualization
            if result.get("top_candidates"):
                st.subheader("Candidate Fertilizer Formulations & Probability Distribution")
                cand_df = pd.DataFrame(result["top_candidates"])
                fig = px.bar(
                    cand_df,
                    x="probability",
                    y="fertilizer",
                    orientation="h",
                    text=cand_df["confidence_pct"].apply(lambda v: f"{v:.1f}%"),
                    color="probability",
                    color_continuous_scale="Teal",
                    labels={"probability": "Predicted Probability", "fertilizer": "Fertilizer Candidate"},
                )
                fig.update_layout(
                    showlegend=False,
                    coloraxis_showscale=False,
                    margin=dict(l=20, r=20, t=20, b=20),
                    height=240,
                )
                st.plotly_chart(fig, use_container_width=True)

            render_disclaimer(result["disclaimer"])

        except InputValidationError as e:
            st.error(f"Input Validation Error: {e}")
        except ModelArtifactNotFoundError as e:
            st.error(f"Model Artifact Error: {e}")
        except Exception as e:
            st.error(f"Unexpected prediction error: {e}")
