"""Crop Recommendation UI Page for AgriSmart."""

import streamlit as st
import plotly.express as px
import pandas as pd

from src.ui.styles import render_hero, render_disclaimer
from src.models.predict import CropPredictor, InputValidationError, ModelArtifactNotFoundError
from src.utils.constants import CROP_FEATURE_RANGES, CROP_DESCRIPTIONS


def render_crop_page():
    render_hero(
        title="Module A: Crop Recommendation",
        subtitle="Multiclass predictive classification recommending optimal crops based on N-P-K soil nutrients, climatic conditions, and soil acidity.",
        badge="Module A • Multiclass Classifier",
    )

    st.markdown("### Agricultural Input Parameters")
    st.info("💡 Adjust the sliders or numeric fields below to reflect your field's soil test values and prevailing weather conditions.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Soil Chemistry (Macronutrients & pH)")
        n_cfg = CROP_FEATURE_RANGES["N"]
        n_val = st.number_input(
            f"{n_cfg['label']} ({n_cfg['unit']})",
            min_value=float(n_cfg["min"]),
            max_value=float(n_cfg["max"]),
            value=float(n_cfg["default"]),
            step=1.0,
            help="Available Nitrogen in topsoil (0 - 140 kg/ha)."
        )

        p_cfg = CROP_FEATURE_RANGES["P"]
        p_val = st.number_input(
            f"{p_cfg['label']} ({p_cfg['unit']})",
            min_value=float(p_cfg["min"]),
            max_value=float(p_cfg["max"]),
            value=float(p_cfg["default"]),
            step=1.0,
            help="Available Phosphorus in topsoil (5 - 145 kg/ha)."
        )

        k_cfg = CROP_FEATURE_RANGES["K"]
        k_val = st.number_input(
            f"{k_cfg['label']} ({k_cfg['unit']})",
            min_value=float(k_cfg["min"]),
            max_value=float(k_cfg["max"]),
            value=float(k_cfg["default"]),
            step=1.0,
            help="Available Potassium in topsoil (5 - 205 kg/ha)."
        )

        ph_cfg = CROP_FEATURE_RANGES["ph"]
        ph_val = st.slider(
            f"{ph_cfg['label']} (Acidity/Alkalinity)",
            min_value=float(ph_cfg["min"]),
            max_value=float(ph_cfg["max"]),
            value=float(ph_cfg["default"]),
            step=0.1,
            help="Soil pH: < 6.0 (acidic), 6.0-7.5 (neutral/optimal), > 7.5 (alkaline)."
        )

    with col2:
        st.markdown("#### Environmental & Climate Conditions")
        t_cfg = CROP_FEATURE_RANGES["temperature"]
        temp_val = st.number_input(
            f"{t_cfg['label']} ({t_cfg['unit']})",
            min_value=float(t_cfg["min"]),
            max_value=float(t_cfg["max"]),
            value=float(t_cfg["default"]),
            step=0.5,
            help="Average ambient temperature during the growing season (8°C - 45°C)."
        )

        h_cfg = CROP_FEATURE_RANGES["humidity"]
        hum_val = st.slider(
            f"{h_cfg['label']} ({h_cfg['unit']})",
            min_value=float(h_cfg["min"]),
            max_value=float(h_cfg["max"]),
            value=float(h_cfg["default"]),
            step=1.0,
            help="Mean relative atmospheric humidity (14% - 100%)."
        )

        r_cfg = CROP_FEATURE_RANGES["rainfall"]
        rain_val = st.number_input(
            f"{r_cfg['label']} ({r_cfg['unit']})",
            min_value=float(r_cfg["min"]),
            max_value=float(r_cfg["max"]),
            value=float(r_cfg["default"]),
            step=5.0,
            help="Total cumulative seasonal precipitation (20 mm - 300 mm)."
        )

    st.markdown("---")
    
    predict_btn = st.button("🌱 Predict Recommended Crop", type="primary", use_container_width=True)

    if predict_btn:
        inputs = {
            "N": n_val,
            "P": p_val,
            "K": k_val,
            "temperature": temp_val,
            "humidity": hum_val,
            "ph": ph_val,
            "rainfall": rain_val,
        }

        try:
            predictor = CropPredictor()
            result = predictor.predict(inputs, top_k=3)

            rec_crop = result["recommended_crop"]
            conf = result["confidence_pct"]
            crop_desc = result["description"]

            st.markdown(
                f"""
                <div class="prediction-box">
                    <div class="prediction-label">Optimal Agricultural Recommendation</div>
                    <div class="prediction-value">{rec_crop.upper()}</div>
                    <div class="prediction-subtext"><strong>Model Confidence:</strong> {conf:.1f}%</div>
                    <p style="margin-top: 1rem; color: #1e293b; max-width: 600px; margin-left: auto; margin-right: auto;">
                        {crop_desc}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Top Candidates Visualization
            if result.get("top_candidates"):
                st.subheader("Top-Ranked Crop Candidates & Class Probabilities")
                candidates_df = pd.DataFrame(result["top_candidates"])
                candidates_df["crop_clean"] = candidates_df["crop"].str.capitalize()

                fig = px.bar(
                    candidates_df,
                    x="probability",
                    y="crop_clean",
                    orientation="h",
                    text=candidates_df["confidence_pct"].apply(lambda v: f"{v:.1f}%"),
                    color="probability",
                    color_continuous_scale="Greens",
                    labels={"probability": "Predicted Probability", "crop_clean": "Crop Candidate"},
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
