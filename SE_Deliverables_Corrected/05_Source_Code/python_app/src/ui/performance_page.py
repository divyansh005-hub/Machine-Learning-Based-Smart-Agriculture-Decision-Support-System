"""Model Performance and Empirical Evaluation Page for AgriSmart."""

import json
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff

from src.ui.styles import render_hero
from src.utils.constants import REPORTS_DIR, MODELS_DIR


@st.cache_data
def load_comparison_data():
    csv_path = REPORTS_DIR / "model_comparison.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path)
    return None


@st.cache_data
def load_module_metadata(meta_filename: str):
    path = MODELS_DIR / meta_filename
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def render_performance_page():
    render_hero(
        title="Model Performance & Empirical Benchmarks",
        subtitle="Transparent evaluation tracking held-out test metrics, baseline comparisons, confusion matrices, and regression residual summaries.",
        badge="Rigorous Model Evaluation",
    )

    comp_df = load_comparison_data()
    if comp_df is None:
        st.warning("Model comparison artifact not found. Please train models via 'python src/models/train.py'.")
        return

    st.subheader("1. Master Model Comparison Matrix")
    st.info("📊 Metrics displayed below are strictly computed on unseen held-out test sets. No fabricated or interpolated metrics.")

    st.dataframe(
        comp_df.style.highlight_max(
            subset=["Primary_Metric_Value"],
            color="#dcfce7"
        ),
        use_container_width=True,
    )

    st.markdown("---")

    # Detailed Module Tabs
    tab_a, tab_b, tab_c = st.tabs([
        "🌾 Module A: Crop Recommendation",
        "🧪 Module B: Fertilizer Recommendation",
        "📈 Module C: Crop Yield Prediction"
    ])

    # TAB A: Crop Recommendation
    with tab_a:
        crop_meta = load_module_metadata("crop_recommendation_meta.json")
        if crop_meta:
            st.markdown("#### Crop Recommendation Candidate Evaluation")
            st.markdown(f"**Split Strategy:** {crop_meta.get('all_candidates', {}).get('DummyClassifier (Baseline)', {}).get('split', 'Stratified 80:20 (random_state=42)')}")
            st.markdown(f"**Train Samples:** {crop_meta.get('train_samples')} | **Held-Out Test Samples:** {crop_meta.get('test_samples')}")
            st.markdown(f"**Selected Model:** `{crop_meta.get('selected_model')}`")
            st.caption(crop_meta.get("selection_reason"))

            # Comparison Bar Chart
            crop_cand = crop_meta.get("all_candidates", {})
            chart_data = []
            for name, m in crop_cand.items():
                chart_data.append({"Model": name, "Macro-F1": m["macro_f1"], "Accuracy": m["accuracy"]})
            chart_df = pd.DataFrame(chart_data)

            fig_crop = px.bar(
                chart_df,
                x="Model",
                y=["Macro-F1", "Accuracy"],
                barmode="group",
                title="Held-Out Test Performance: Baseline vs Candidates",
                color_discrete_sequence=["#10b981", "#3b82f6"],
            )
            fig_crop.update_layout(height=350, yaxis_range=[0, 1.05])
            st.plotly_chart(fig_crop, use_container_width=True)

            # Confusion Matrix
            st.markdown("#### Confusion Matrix (Held-Out Test Set)")
            labels = crop_meta["labels"]
            cm = np.array(crop_meta["metrics"]["confusion_matrix"])

            fig_cm = px.imshow(
                cm,
                x=labels,
                y=labels,
                labels=dict(x="Predicted Crop", y="True Crop", color="Samples"),
                color_continuous_scale="Blues",
                title=f"Confusion Matrix: {crop_meta['selected_model']} (22 Balanced Classes, 20 Test Samples Each)",
            )
            fig_cm.update_layout(height=650)
            st.plotly_chart(fig_cm, use_container_width=True)

    # TAB B: Fertilizer Recommendation
    with tab_b:
        fert_meta = load_module_metadata("fertilizer_recommendation_meta.json")
        if fert_meta:
            st.markdown("#### Fertilizer Recommendation Candidate Evaluation")
            st.markdown(f"**Split Strategy:** Stratified 80:20 (`random_state=42`) | Train: {fert_meta.get('train_samples')} | Test: {fert_meta.get('test_samples')}")
            st.markdown(f"**Selected Model:** `{fert_meta.get('selected_model')}`")
            st.caption(fert_meta.get("selection_reason"))

            # Comparison Bar Chart
            fert_cand = fert_meta.get("all_candidates", {})
            f_chart_data = []
            for name, m in fert_cand.items():
                f_chart_data.append({"Model": name, "Macro-F1": m["macro_f1"], "Accuracy": m["accuracy"]})
            f_chart_df = pd.DataFrame(f_chart_data)

            fig_fert = px.bar(
                f_chart_df,
                x="Model",
                y=["Macro-F1", "Accuracy"],
                barmode="group",
                title="Held-Out Test Performance (Imbalance Handled via Class Weights)",
                color_discrete_sequence=["#06b6d4", "#6366f1"],
            )
            fig_fert.update_layout(height=350, yaxis_range=[0, 1.05])
            st.plotly_chart(fig_fert, use_container_width=True)

            # Per Class Metrics Table
            st.markdown("#### Per-Class Classification Report (Attention to Rare Classes)")
            cr = fert_meta["metrics"]["classification_report"]
            rows = []
            for lbl in fert_meta["labels"]:
                if lbl in cr:
                    entry = cr[lbl]
                    rows.append({
                        "Fertilizer Class": lbl,
                        "Precision": round(entry["precision"], 4),
                        "Recall": round(entry["recall"], 4),
                        "F1-Score": round(entry["f1-score"], 4),
                        "Test Support": int(entry["support"]),
                    })
            st.dataframe(pd.DataFrame(rows), use_container_width=True)

            # Confusion Matrix
            labels_f = fert_meta["labels"]
            cm_f = np.array(fert_meta["metrics"]["confusion_matrix"])
            fig_cm_f = px.imshow(
                cm_f,
                x=labels_f,
                y=labels_f,
                labels=dict(x="Predicted Fertilizer", y="True Fertilizer", color="Samples"),
                color_continuous_scale="Teal",
                text_auto=True,
                title=f"Confusion Matrix: {fert_meta['selected_model']}",
            )
            fig_cm_f.update_layout(height=450)
            st.plotly_chart(fig_cm_f, use_container_width=True)

    # TAB C: Crop Yield Prediction
    with tab_c:
        yield_meta = load_module_metadata("yield_prediction_meta.json")
        if yield_meta:
            st.markdown("#### Crop Yield Prediction Candidate Evaluation")
            st.markdown(f"**Split Strategy:** {yield_meta.get('split_strategy')}")
            st.markdown(f"**Train Horizon:** 1990–2009 ({yield_meta.get('train_samples'):,} samples)")
            st.markdown(f"**Held-Out Future Horizon:** 2010–2013 ({yield_meta.get('test_samples'):,} samples)")
            st.markdown(f"**Selected Model:** `{yield_meta.get('selected_model')}`")
            st.caption(yield_meta.get("selection_reason"))

            # Comparison Metrics Table
            yield_cand = yield_meta.get("all_candidates", {})
            y_rows = []
            for name, m in yield_cand.items():
                y_rows.append({
                    "Model Candidate": name,
                    "RMSE (hg/ha)": f"{m['rmse']:,.2f}",
                    "MAE (hg/ha)": f"{m['mae']:,.2f}",
                    "R² Score": f"{m['r2']:.4f}",
                    "RMSE (tonnes/ha)": f"{m.get('rmse_tonnes_per_ha', 0):.2f}" if m.get("rmse_tonnes_per_ha") is not None else "N/A",
                })
            st.dataframe(pd.DataFrame(y_rows), use_container_width=True)

            # RMSE & R2 Comparison Chart
            y_chart_data = []
            for name, m in yield_cand.items():
                y_chart_data.append({"Model": name, "RMSE_hg_ha": m["rmse"], "R2": max(0.0, m["r2"])})
            y_chart_df = pd.DataFrame(y_chart_data)

            yc1, yc2 = st.columns(2)
            with yc1:
                fig_rmse = px.bar(
                    y_chart_df,
                    x="Model",
                    y="RMSE_hg_ha",
                    title="Held-Out Temporal RMSE (Lower is Better)",
                    color="RMSE_hg_ha",
                    color_continuous_scale="Reds_r",
                )
                fig_rmse.update_layout(showlegend=False, height=340)
                st.plotly_chart(fig_rmse, use_container_width=True)
            with yc2:
                fig_r2 = px.bar(
                    y_chart_df,
                    x="Model",
                    y="R2",
                    title="Held-Out Temporal R² Score (Higher is Better)",
                    color="R2",
                    color_continuous_scale="Viridis",
                )
                fig_r2.update_layout(showlegend=False, height=340, yaxis_range=[0, 1.05])
                st.plotly_chart(fig_r2, use_container_width=True)

            # Test Distribution Statistics
            ym = yield_meta["metrics"]
            st.markdown("#### Test Set Error Relative to Yield Distribution")
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("Test Mean Yield", f"{ym['target_mean']/10000:.2f} t/ha", f"{ym['target_mean']:,.0f} hg/ha")
            with m2:
                st.metric("RMSE Error", f"{ym['rmse']/10000:.2f} t/ha", f"{ym['rmse']:,.0f} hg/ha")
            with m3:
                st.metric("RMSE as % of Mean", f"{ym['rmse_pct_of_mean']:.2f}%")
            with m4:
                st.metric("Explained Variance (R²)", f"{ym['r2']:.4f}")
